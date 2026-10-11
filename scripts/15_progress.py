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
  15_progress.py get <slide_id>                print one row as JSON
  15_progress.py report                       print the full status table
  15_progress.py ready                         print slide_ids with validation_status='ready'
  15_progress.py deps                          dependency graph: root/blocked/unblocked per slide
                                               (a dependent slide may BUILD only when every
                                               dependency is certified: gen_status='passed'
                                               AND visual_check='PASS')
  15_progress.py buildable                    ids passing content gate + dep gate + pattern gate
                                               that are not built yet (the dispatch list)

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
        "depends_on", "pattern_group", "pattern_seq"]


def now():
    return datetime.datetime.now().isoformat(timespec="seconds")


def conn():
    c = sqlite3.connect(DB, timeout=30)
    c.execute("PRAGMA busy_timeout=30000")
    # dependency-gated decks (founder directive 2026-10-11): depends_on holds a csv of
    # direct-parent tokens — bare ints (same video) or qualified '<namespace>:<id>'
    # (cross-video). pattern_group/pattern_seq encode sequential-build pattern groups.
    # Guarded adds keep old DBs compatible (and no-op before init creates the table).
    cols = [r[1] for r in c.execute("PRAGMA table_info(slides)")]
    if cols:
        for col, typ in (("depends_on", "TEXT"), ("pattern_group", "TEXT"),
                         ("pattern_seq", "INTEGER")):
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
            last_error TEXT, updated_at TEXT)""")


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


def set_field(sid, field, value):
    if field not in TEXT_FIELDS and field not in INT_FIELDS:
        sys.exit(f"bad field {field!r}; allowed: {sorted(TEXT_FIELDS | INT_FIELDS)}")
    if field in INT_FIELDS:
        value = int(value)
    with conn() as c:
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
            "deps", "pat", "pptx", "err"]
    sel = """SELECT slide_id,title,analysis_status,validation_verdict,recreatability_score,
             gen_status,visual_check,visual_attempts,depends_on,
             COALESCE(pattern_group || '#' || pattern_seq, ''), pptx_path,last_error
             FROM slides ORDER BY slide_id"""
    with conn() as c:
        rows = c.execute(sel).fetchall()
    data = [[("" if v is None else str(v)) for v in r] for r in rows]
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
    if cmd == "init":
        init()
    elif cmd == "register":
        register()
    elif cmd == "sync":
        sync()
    elif cmd == "set" and len(sys.argv) == 5:
        set_field(int(sys.argv[2]), sys.argv[3], sys.argv[4])
    elif cmd == "get" and len(sys.argv) == 3:
        get(int(sys.argv[2]))
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
