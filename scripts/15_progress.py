#!/usr/bin/env python3
"""Progress DB helper for the slide-recreation batch.

Usage:
  15_progress.py init                          create slides_progress.db + schema
  15_progress.py register                      seed rows from unique_slides/slides_index.json
  15_progress.py sync                          refresh analysis/validation fields from analysis/
  15_progress.py set <slide_id> <field> <val>  update one field (whitelisted)
  15_progress.py get <slide_id>                print one row as JSON
  15_progress.py report                       print the full status table
  15_progress.py ready                         print slide_ids with validation_status='ready'
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

TEXT_FIELDS = {"title", "analysis_status", "validation_status", "validation_verdict",
               "gen_status", "pptx_path", "build_script", "visual_check",
               "visual_transcript", "last_error"}
INT_FIELDS = {"analysis_attempts", "validation_attempts", "visual_attempts",
              "recreatability_score"}
COLS = ["slide_id", "image_path", "title", "analysis_status", "analysis_attempts",
        "validation_status", "validation_verdict", "recreatability_score",
        "validation_attempts", "gen_status", "pptx_path", "build_script",
        "visual_check", "visual_attempts", "visual_transcript", "last_error", "updated_at"]


def now():
    return datetime.datetime.now().isoformat(timespec="seconds")


def conn():
    c = sqlite3.connect(DB, timeout=30)
    c.execute("PRAGMA busy_timeout=30000")
    return c


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
    print(f"registered {len(entries)} slides from slides_index.json")


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
        print(json.dumps(dict(zip(COLS, row)), indent=1))


def report():
    cols = ["id", "title", "analysis", "verdict", "score", "gen", "visual", "vatt", "pptx", "err"]
    sel = """SELECT slide_id,title,analysis_status,validation_verdict,recreatability_score,
             gen_status,visual_check,visual_attempts,pptx_path,last_error
             FROM slides ORDER BY slide_id"""
    with conn() as c:
        rows = c.fetchall() if False else c.execute(sel).fetchall()
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
    else:
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
