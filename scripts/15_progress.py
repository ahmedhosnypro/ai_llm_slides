#!/usr/bin/env python3
"""Progress DB helper for the slide-recreation batch.

Usage:
  15_progress.py init                          create slides_progress.db + schema
  15_progress.py register                      seed rows from unique_slides/slides_index.json
                                               (+ edges/pattern_groups from slide_dependencies.json;
                                               placeholder entries get analysis_status='n/a-placeholder',
                                               validation_status='ready')
  15_progress.py sync                          refresh analysis/validation fields from analysis/
  15_progress.py set <slide_id> <field> <val>  update one field (whitelisted)
                                               [--worker <id>] [--force]  (ownership guard)
  15_progress.py get <slide_id>                print one row as JSON
  15_progress.py report                       print the full status table
  15_progress.py ready                         print slide_ids with validation_status='ready'
  15_progress.py deps                          dependency graph: root/blocked/unblocked per slide
                                               (a dependent slide may BUILD only when every
                                               dependency is certified: gen_status='passed'
                                               AND visual_check='PASS')
  15_progress.py buildable                    ids passing content gate + dep gate + pattern gate
                                               that are not built yet (the dispatch list)
  15_progress.py claim <slide_id> <worker_id> [--force]
                                               take ownership of a build lane: refuses if a
                                               DIFFERENT worker holds a FRESH claim (heartbeat
                                               < 40 min) — that is a live peer, stand down;
                                               stale claims are taken over automatically.
  15_progress.py heartbeat <slide_id> <worker_id>
                                               ONLY liveness writer: stamps worker_heartbeat_at
                                               (never touched by set/sync). The truth signal that
                                               a 'building' row has a live owner.
  15_progress.py release <slide_id> <worker_id>
                                               clear the claim when the worker finishes.
  15_progress.py sweep [--stale-min N]         the DB-vs-reality check: every gen_status='building'
                                               row classified live / ZOMBIE (heartbeat stale or
                                               missing) / unclaimed. Zombies are the re-dispatch
                                               list. (lesson 2026-10-12: file-mtime inference
                                               over-counted live workers 6 vs actual 4 — the DB
                                               must carry worker liveness itself.)

WORKER LIVENESS CONTRACT (founder directive 2026-10-12, after mtime-guessing
miscounted the fleet): a builder subagent (1) `claim`s its slide with a
self-generated unique id at start, (2) calls `heartbeat` after every completed
step (and at least every ~10 min during long phases), (3) `release`s at the end.
'building' + fresh heartbeat = live; 'building' + stale/missing heartbeat =
zombie (safe to reclaim via claim's takeover path). updated_at records CONTENT
writes (any writer, incl. bulk syncs) and must never be read as liveness.

Dependency token grammar (depends_on CSV, v2 — founder directive 2026-10-11):
  bare int                  same-video parent        e.g.  26
  <namespace>:<slide_id>    cross-video parent       e.g.  deep-learning/001_transformers_part1:15
Cross-video certification is resolved in the PARENT video's own slides_progress.db
(SELECT-only; this script never writes outside VIDEO's namespace).

Pattern groups (slide_dependencies.json v2 "pattern_groups"): members build STRICTLY
sequentially in listed order — member k is gated on member k-1 being certified.
Builds only; analysis (12) and validation (13) are NEVER gated.
"""
import datetime
import glob
import json
import os
import sqlite3
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Multi-video layout: each video gets its own namespace under videos/<VIDEO>/.
# VIDEO selects the namespace (env var, so parallel videos never collide).
VIDEO = os.environ.get("VIDEO", "ml-intro")
VROOT = os.path.join(ROOT, "videos", VIDEO)
DB = os.path.join(VROOT, "slides_progress.db")
IDX = os.path.join(VROOT, "unique_slides", "slides_index.json")
ANALYSIS = os.path.join(VROOT, "analysis")
DEPS = os.path.join(VROOT, "slide_dependencies.json")

TEXT_FIELDS = {"title", "analysis_status", "validation_status", "validation_verdict",
               "gen_status", "pptx_path", "build_script", "visual_check",
               "visual_transcript", "last_error", "depends_on", "pattern_group"}
INT_FIELDS = {"analysis_attempts", "validation_attempts", "visual_attempts",
              "recreatability_score", "pattern_seq"}
# NOTE: legacy docs said depends_on must stay the LAST column; that held for the
# 17-column era. Column order is now irrelevant — get() derives names from
# PRAGMA table_info — and guarded ALTERs append pattern_group/pattern_seq AFTER
# depends_on in migrated DBs. Never rely on positional column order anywhere.
COLS = ["slide_id", "image_path", "title", "analysis_status", "analysis_attempts",
        "validation_status", "validation_verdict", "recreatability_score",
        "validation_attempts", "gen_status", "pptx_path", "build_script",
        "visual_check", "visual_attempts", "visual_transcript", "last_error", "updated_at",
        "depends_on", "pattern_group", "pattern_seq",
        "worker_id", "worker_heartbeat_at"]

# Worker-claim staleness (minutes): a 'building' row whose heartbeat is older
# than this has a dead owner (the banked dual-condition death-test threshold).
STALE_MIN = 40


def now():
    return datetime.datetime.now().isoformat(timespec="seconds")


def conn():
    c = sqlite3.connect(DB, timeout=30)
    c.execute("PRAGMA busy_timeout=30000")
    # dependency-gated decks (founder directive 2026-10-11): depends_on holds a csv of
    # direct-parent tokens — bare ints (same video) or qualified '<namespace>:<id>'
    # (cross-video). pattern_group/pattern_seq encode sequential-build pattern groups.
    # worker_id/worker_heartbeat_at are the worker-liveness contract (founder
    # directive 2026-10-12): claim/heartbeat/release manage them; set/sync never do.
    # Guarded adds keep old DBs compatible (and no-op before init creates the table).
    cols = [r[1] for r in c.execute("PRAGMA table_info(slides)")]
    if cols:
        for col, typ in (("depends_on", "TEXT"), ("pattern_group", "TEXT"),
                         ("pattern_seq", "INTEGER"),
                         ("worker_id", "TEXT"), ("worker_heartbeat_at", "TEXT")):
            if col not in cols:
                c.execute(f"ALTER TABLE slides ADD COLUMN {col} {typ}")
        c.commit()
    return c


def table_cols(c):
    """Actual column names in on-disk order — never trust the COLS constant."""
    return [r[1] for r in c.execute("PRAGMA table_info(slides)")]


def init():
    with conn() as c:
        c.execute("PRAGMA journal_mode=WAL")
        c.execute("""CREATE TABLE IF NOT EXISTS slides(
            slide_id INTEGER PRIMARY KEY,
            image_path TEXT, title TEXT,
            analysis_status TEXT DEFAULT 'pending', analysis_attempts INTEGER DEFAULT 0,
            validation_status TEXT DEFAULT 'pending', validation_verdict TEXT,
            recreatability_score INTEGER, validation_attempts INTEGER DEFAULT 0,
            gen_status TEXT DEFAULT 'pending', pptx_path TEXT, build_script TEXT,
            visual_check TEXT, visual_attempts INTEGER DEFAULT 0, visual_transcript TEXT,
            last_error TEXT, updated_at TEXT,
            worker_id TEXT DEFAULT '', worker_heartbeat_at TEXT)""")


def register():
    entries = json.load(open(IDX))
    with conn() as c:
        for e in entries:
            c.execute("INSERT OR IGNORE INTO slides(slide_id,image_path,updated_at) VALUES(?,?,?)",
                      (e["slide"], os.path.join("unique_slides", e["image"]), now()))
            if e.get("placeholder"):
                # placeholder cover (missing frame): no 12/13 possible — hand-spec path
                c.execute("""UPDATE slides SET title=?, analysis_status='n/a-placeholder',
                    validation_status='ready', updated_at=? WHERE slide_id=?""",
                          (e.get("title"), now(), e["slide"]))
    print(f"registered {len(entries)} slides from slides_index.json")
    if os.path.exists(DEPS):
        d = json.load(open(DEPS))
        edges = d.get("edges", {})
        with conn() as c:
            for child, parents in edges.items():
                c.execute("UPDATE slides SET depends_on=?, updated_at=? WHERE slide_id=?",
                          (",".join(str(p) for p in parents), now(), int(child)))
        print(f"applied {len(edges)} dependency edges from slide_dependencies.json")
        groups = d.get("pattern_groups", {})
        if groups:
            n = 0
            with conn() as c:
                for gname, members in groups.items():
                    for seq, sid in enumerate(members, 1):
                        c.execute("UPDATE slides SET pattern_group=?, pattern_seq=?, updated_at=? "
                                  "WHERE slide_id=?", (gname, seq, now(), int(sid)))
                        n += 1
            print(f"applied {len(groups)} pattern groups ({n} members)")


def _parse_dep(tok):
    """'26' -> (None, 26); 'deep-learning/001_transformers_part1:15' -> (ns, 15)."""
    tok = tok.strip()
    if ":" in tok:
        ns, sid = tok.rsplit(":", 1)
        return ns, int(sid)
    return None, int(tok)


def _cross_certified(ns, sid, cache):
    """Certification of a cross-video parent, read from the PARENT's own DB (SELECT only)."""
    if ns not in cache:
        pdb = os.path.join(ROOT, "videos", ns, "slides_progress.db")
        rows = {}
        if os.path.exists(pdb):
            pc = None
            try:
                try:
                    pc = sqlite3.connect(f"file:{pdb}?mode=ro", uri=True, timeout=30)
                except sqlite3.OperationalError:
                    # read-only open can fail on WAL without a live -shm; plain connect
                    pc = sqlite3.connect(pdb, timeout=30)
                pc.execute("PRAGMA busy_timeout=30000")
                rows = {r[0]: (r[1], r[2]) for r in pc.execute(
                    "SELECT slide_id, gen_status, visual_check FROM slides")}
            except sqlite3.Error as ex:
                rows = {}  # unresolvable -> treated as not certified
            finally:
                if pc is not None:
                    pc.close()
        cache[ns] = rows
    gen, vis = cache[ns].get(sid, (None, None))
    return gen == "passed" and vis == "PASS"


def _dep_states(c):
    """Return {slide_id: {deps, pattern, status, blocked_by}}.
    status: root | blocked | unblocked. Certified == gen_status='passed' AND
    visual_check='PASS' (cross-video parents certified in their OWN video's DB).
    Pattern groups add a sequential gate: member k waits for member k-1."""
    rows = c.execute("SELECT slide_id, gen_status, visual_check, depends_on, "
                     "pattern_group, pattern_seq FROM slides").fetchall()
    certified = {r[0] for r in rows if r[1] == "passed" and r[2] == "PASS"}
    by_group = {}
    for r in rows:
        if r[4]:
            by_group.setdefault(r[4], {})[r[5]] = r[0]
    cross_cache = {}
    out = {}
    for sid, _gen, _vis, dep, pgroup, pseq in rows:
        parents = [p for p in str(dep or "").split(",") if p.strip()]
        missing = []
        for tok in parents:
            ns, pid = _parse_dep(tok)
            if ns is None:
                if pid not in certified:
                    missing.append(str(pid))
            elif not _cross_certified(ns, pid, cross_cache):
                missing.append(tok)
        pred = None
        if pgroup and pseq and pseq > 1:
            pred = by_group.get(pgroup, {}).get(pseq - 1)
            if pred is not None and pred not in certified:
                missing.append(f"pattern {pgroup}#{pseq - 1} (slide {pred})")
        if not parents and pred is None:
            status = "root"
        elif not missing:
            status = "unblocked"
        else:
            status = "blocked"
        out[sid] = {"deps": dep or "", "pattern": (f"{pgroup}#{pseq}" if pgroup else ""),
                    "status": status, "blocked_by": missing}
    return out


def deps():
    with conn() as c:
        states = _dep_states(c)
        rows = c.execute("SELECT slide_id, title, gen_status, visual_check FROM slides "
                         "ORDER BY slide_id").fetchall()
    print(f"{'id':>3}  {'deps':<38}  {'pat':<7}  {'status':<9}  {'gen':<8}  {'vis':<5}  blocked_by / title")
    n_root = n_blk = n_unblk = 0
    for sid, title, gen, vis in rows:
        st = states[sid]
        n_root += st["status"] == "root"; n_blk += st["status"] == "blocked"
        n_unblk += st["status"] == "unblocked"
        extra = ", ".join(st["blocked_by"]) + " not certified" if st["blocked_by"] else (title or "")
        print(f"{sid:>3}  {(st['deps'] or '—'):<38}  {st['pattern'] or '—':<7}  "
              f"{st['status']:<9}  {gen or '':<8}  {vis or '':<5}  {extra}")
    print(f"\n{len(rows)} slides: {n_root} roots, {n_unblk} unblocked (may build), {n_blk} blocked")
    print("build gate: every dependency certified (cross-video parents in their own DB) "
          "+ pattern predecessor certified")


def buildable():
    """Content gate + dep gate + pattern gate + not built yet — the dispatch list."""
    with conn() as c:
        states = _dep_states(c)
        rows = c.execute("SELECT slide_id FROM slides WHERE validation_status='ready' "
                         "AND gen_status='pending' ORDER BY slide_id").fetchall()
    ids = [r[0] for r in rows if states[r[0]]["status"] != "blocked"]
    print(" ".join(map(str, ids)))


def sync():
    with conn() as c:
        for p in sorted(glob.glob(os.path.join(ANALYSIS, "slide_*_raw.json"))):
            sid = int(os.path.basename(p).split("_")[1])
            c.execute("INSERT OR IGNORE INTO slides(slide_id,image_path,updated_at) VALUES(?,?,?)",
                      (sid, f"unique_slides/slide_{sid:03d}.jpg", now()))
            c.execute("UPDATE slides SET analysis_status='ok', updated_at=? WHERE slide_id=?",
                      (now(), sid))
        for p in sorted(glob.glob(os.path.join(ANALYSIS, "slide_*_final.json"))):
            sid = int(os.path.basename(p).split("_")[1])
            try:
                d = json.load(open(p))
                v = d.get("validation") or {}
                verdict = v.get("verdict")
                score = v.get("recreatability_score_1_to_10")
                score = int(score) if score is not None else None
                status = ("ready" if verdict in ("PASS", "PASS_WITH_FIXES")
                          and score is not None and score >= 8 else "failed")
                c.execute("""UPDATE slides SET title=?, validation_status=?,
                    validation_verdict=?, recreatability_score=?, updated_at=?
                    WHERE slide_id=?""",
                    (d.get("slide_title"), status, verdict, score, now(), sid))
            except Exception as ex:
                c.execute("""UPDATE slides SET validation_status='failed', last_error=?,
                    updated_at=? WHERE slide_id=?""", (f"sync: {ex}", now(), sid))
    print("synced analysis/ -> db")


def _hb_age_minutes(hb):
    """Minutes since a worker_heartbeat_at timestamp; None if never stamped/unparseable."""
    if not hb:
        return None
    try:
        dt = datetime.datetime.fromisoformat(hb)
    except ValueError:
        return None
    return (datetime.datetime.now() - dt).total_seconds() / 60.0


def claim(sid, wid, force=False):
    """Take ownership of a build lane. Refuses a DIFFERENT worker's FRESH claim
    (that is a live peer — stand down); stale claims are taken over."""
    with conn() as c:
        row = c.execute("SELECT worker_id, worker_heartbeat_at FROM slides WHERE slide_id=?",
                        (sid,)).fetchone()
        if not row:
            sys.exit(f"no row for slide {sid} (run register first)")
        owner, hb = row
        age = _hb_age_minutes(hb)
        if owner and owner != wid and not force:
            if age is None or age >= STALE_MIN:
                pass  # stale/unparseable claim -> takeover
            else:
                sys.exit(f"REFUSED: slide {sid} claimed by live worker {owner!r} "
                         f"(heartbeat {age:.0f}m ago, fresh < {STALE_MIN}m) — "
                         f"that is a live peer; stand down (or --force to override)")
        took = ""
        if owner and owner != wid:
            took = f" (took over from {owner!r}, heartbeat " + (
                f"{age:.0f}m stale)" if age is not None else "none)")
        c.execute("UPDATE slides SET worker_id=?, worker_heartbeat_at=?, "
                  "gen_status='building', updated_at=? WHERE slide_id=?",
                  (wid, now(), now(), sid))
    print(f"claimed slide {sid} by {wid}{took}")


def heartbeat(sid, wid):
    """The ONLY liveness writer. Refuses a foreign live claim; implicitly claims
    an unclaimed row. Never touches updated_at — content writes and liveness
    are separate signals."""
    with conn() as c:
        row = c.execute("SELECT worker_id FROM slides WHERE slide_id=?", (sid,)).fetchone()
        if not row:
            sys.exit(f"no row for slide {sid} (run register first)")
        owner = row[0]
        if owner and owner != wid:
            age = _hb_age_minutes(
                c.execute("SELECT worker_heartbeat_at FROM slides WHERE slide_id=?",
                          (sid,)).fetchone()[0])
            if age is not None and age < STALE_MIN:
                sys.exit(f"REFUSED: slide {sid} claimed by live worker {owner!r} "
                         f"({age:.0f}m) — heartbeat from {wid!r} rejected")
        c.execute("UPDATE slides SET worker_id=CASE WHEN worker_id IS NULL OR worker_id='' "
                  "THEN ? ELSE worker_id END, worker_heartbeat_at=? WHERE slide_id=?",
                  (wid, now(), sid))
    print("ok")


def release(sid, wid):
    """Clear the claim when the worker finishes (pass or fail)."""
    with conn() as c:
        n = c.execute("UPDATE slides SET worker_id='', worker_heartbeat_at=NULL "
                      "WHERE slide_id=? AND worker_id=?", (sid, wid)).rowcount
        if not n:
            sys.exit(f"slide {sid} is not claimed by {wid!r} — nothing released")
    print(f"released slide {sid} ({wid})")


def sweep(stale_min):
    """The DB-vs-reality check: every 'building'/'judging' row classified by claim
    freshness. Zombies (stale/missing heartbeat) are the re-dispatch list; fresh
    claims are live workers. This is what 'is anything actually running?' is
    answered FROM. Judging rows are included — a judge attempt through the gate can
    outlive the 40-min threshold while the worker is mid-call, so a zombie verdict
    here means VERIFY via fresh writes before re-dispatching, never auto-kill."""
    with conn() as c:
        rows = c.execute("SELECT slide_id, worker_id, worker_heartbeat_at FROM slides "
                         "WHERE gen_status IN ('building','judging') "
                         "ORDER BY slide_id").fetchall()
    live, zombie, unclaimed = [], [], []
    for sid, wid, hb in rows:
        age = _hb_age_minutes(hb)
        if not wid or age is None:
            unclaimed.append((sid, wid or ""))
        elif age <= stale_min:
            live.append((sid, wid, age))
        else:
            zombie.append((sid, wid, age))
    print(f"sweep @ {now()} (stale threshold {stale_min}m): "
          f"{len(live)} live, {len(zombie)} ZOMBIE, {len(unclaimed)} unclaimed-building")
    for sid, wid, age in live:
        print(f"  LIVE      {sid:>3}  {wid}  heartbeat {age:.0f}m ago")
    for sid, wid, age in zombie:
        print(f"  ZOMBIE    {sid:>3}  {wid}  heartbeat {age:.0f}m ago (STALE > {stale_min}m) — reclaimable")
    for sid, wid in unclaimed:
        print(f"  UNCLAIMED {sid:>3}  worker_id={wid!r} heartbeat none — legacy row, claim it")
    if zombie or unclaimed:
        print("re-dispatch list: " + " ".join(str(s) for s, *_ in zombie + unclaimed))


def set_field(sid, field, value, worker=None, force=False):
    if field not in TEXT_FIELDS and field not in INT_FIELDS:
        sys.exit(f"bad field {field!r}; allowed: {sorted(TEXT_FIELDS | INT_FIELDS)}")
    if field in INT_FIELDS:
        value = int(value)
    with conn() as c:
        row = c.execute("SELECT worker_id, worker_heartbeat_at FROM slides WHERE slide_id=?",
                        (sid,)).fetchone()
        if not row:
            sys.exit(f"no row for slide {sid} (run register first)")
        owner, hb = row
        # Ownership guard (worker-liveness contract): a row claimed by a live worker
        # is that worker's to write. Stale claims pass through (dead owner); the
        # row's own owner passes --worker <id>; coordinator repairs pass --force.
        if owner and owner != worker and not force:
            age = _hb_age_minutes(hb)
            if age is not None and age < STALE_MIN:
                sys.exit(f"REFUSED: slide {sid} claimed by live worker {owner!r} "
                         f"({age:.0f}m) — writers pass --worker {owner}; coordinator "
                         f"repairs pass --force")
        n = c.execute(f"UPDATE slides SET {field}=?, updated_at=? WHERE slide_id=?",
                      (value, now(), sid)).rowcount
        if not n:
            sys.exit(f"no row for slide {sid} (run register first)")
    print("ok")


def get(sid):
    with conn() as c:
        row = c.execute("SELECT * FROM slides WHERE slide_id=?", (sid,)).fetchone()
        if not row:
            sys.exit(f"no row for slide {sid}")
        print(json.dumps(dict(zip(table_cols(c), row)), indent=1))


def report():
    cols = ["id", "title", "analysis", "verdict", "score", "gen", "visual", "vatt",
            "deps", "pat", "pptx", "wkr", "hb", "err"]
    sel = """SELECT slide_id,title,analysis_status,validation_verdict,recreatability_score,
             gen_status,visual_check,visual_attempts,depends_on,
             COALESCE(pattern_group || '#' || pattern_seq, ''), pptx_path,
             COALESCE(worker_id,''), worker_heartbeat_at, last_error
             FROM slides ORDER BY slide_id"""
    with conn() as c:
        rows = c.execute(sel).fetchall()
    # hb column: minutes since the owning worker's last heartbeat (liveness),
    # NOT updated_at — content writes and worker liveness are separate signals.
    data = []
    for r in rows:
        r = list(r)
        age = _hb_age_minutes(r[12])
        r[12] = f"{age:.0f}m" if age is not None else ""
        data.append([("" if v is None else str(v)) for v in r])
    widths = [max([len(cols[i])] + [len(r[i]) for r in data] or [0]) for i in range(len(cols))]
    print("  ".join(cols[i].ljust(widths[i]) for i in range(len(cols))))
    for r in data:
        print("  ".join(r[i].ljust(widths[i]) for i in range(len(cols))))
    done = sum(1 for r in data if r[6] == "PASS")
    print(f"\n{len(rows)} slides, {done} visually certified PASS")


def ready():
    with conn() as c:
        ids = [r[0] for r in c.execute(
            "SELECT slide_id FROM slides WHERE validation_status='ready' ORDER BY slide_id")]
    print(" ".join(map(str, ids)))


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    cmd = sys.argv[1]
    rest = sys.argv[2:]
    FLAGS_WITH_VALUES = ("--worker", "--stale-min")  # any other --flag is boolean
    def optval(name, default=None):
        return rest[rest.index(name) + 1] if name in rest else default
    # Positionals = tokens that are neither a flag nor a flag's VALUE (else
    # '--worker w-A' puts w-A in the positional list and the command falls
    # through to the usage error — hit in the first live test).
    pos, skip = [], False
    for a in rest:
        if skip:
            skip = False
            continue
        if a.startswith("--"):
            skip = a in FLAGS_WITH_VALUES
            continue
        pos.append(a)
    if cmd == "init":
        init()
    elif cmd == "register":
        register()
    elif cmd == "sync":
        sync()
    elif cmd == "set" and len(pos) == 3:
        set_field(int(pos[0]), pos[1], pos[2],
                  worker=optval("--worker"), force="--force" in rest)
    elif cmd == "claim" and len(pos) == 2:
        claim(int(pos[0]), pos[1], force="--force" in rest)
    elif cmd == "heartbeat" and len(pos) == 2:
        heartbeat(int(pos[0]), pos[1])
    elif cmd == "release" and len(pos) == 2:
        release(int(pos[0]), pos[1])
    elif cmd == "sweep":
        stale = int(optval("--stale-min", STALE_MIN))
        sweep(stale)
    elif cmd == "get" and len(pos) == 1:
        get(int(pos[0]))
    elif cmd == "report":
        report()
    elif cmd == "ready":
        ready()
    elif cmd == "deps":
        deps()
    elif cmd == "buildable":
        buildable()
    else:
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
