#!/usr/bin/env python3
"""monitor_peer.py — READ-ONLY peer-activity monitor for slide 008 (worker: main dispatch).

Watches (without touching) the shared slide-008 namespaces for the live peer's activity.
Exits:
  JUDGED   — a judge/zoom transcript containing a FINAL VERDICT appeared (certify-from-peer path)
  SILENT   — >= silence_min minutes with zero peer artifact movement AND DB row unchanged (takeover path)
  TIMEOUT  — monitor budget exhausted while peer still active (keep waiting)
Peers' files = anything in the watched dirs whose mtime is newer than monitor start and
whose name is NOT in MY_FILES (my known artifacts).
"""
import os, time, glob, json, subprocess, sys

BASE = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2"
WATCH = [
    f"{BASE}/scratch/slide008",
    f"{BASE}/recreated_pptx/qa/slide008",
    f"{BASE}/recreated_pptx/build",
    f"{BASE}/recreated_pptx",
]
MY_FILES = {
    "landmarks.py", "delta.py", "probe.py", "measure2.py", "measure3.py", "measure4.py",
    "measure5.py", "measure6.py", "selfcheck_attempt_1.py", "monitor_peer.py",
    "frame8_remapped_960x540.png",
}
MY_PREFIXES = ("selfcheck_attempt_1",)

START = time.time()
SILENCE_MIN = 40
BUDGET_MIN = 150
last_peer_activity = START
last_db = None

def db_row():
    env = dict(os.environ, VIDEO="deep-learning/002_transformers_part2")
    try:
        out = subprocess.run(["python3", "/home/ahmed/Projects/ai_llm_slides/scripts/15_progress.py", "get", "8"],
                             capture_output=True, text=True, env=env, timeout=30).stdout
        d = json.loads(out[out.index("{"):])
        return (d.get("gen_status"), d.get("visual_check"), d.get("visual_attempts"), d.get("updated_at"),
                d.get("visual_transcript"))
    except Exception as e:
        return ("err", str(e), None, None, None)

def peer_files():
    hits = []
    for d in WATCH:
        for p in glob.glob(d + "/*"):
            b = os.path.basename(p)
            if b in MY_FILES or any(b.startswith(pf) for pf in MY_PREFIXES):
                continue
            if b == "slide_008.js" or b == "slide_008_recreated.pptx" or b.startswith("render_"):
                # shared deliverable chain: track mtimes (peer overwriting counts as movement)
                pass
            try:
                m = os.path.getmtime(p)
            except OSError:
                continue
            if m > START - 5:
                hits.append((p, m))
    return hits

def judge_verdict_present():
    for p in sorted(glob.glob(f"{BASE}/recreated_pptx/qa/slide008/*.txt"), key=os.path.getmtime, reverse=True):
        b = os.path.basename(p)
        if os.path.getmtime(p) < START - 5:
            continue  # only transcripts written during the collision window
            try:
                body = open(p, errors="ignore").read()
            except OSError:
                continue
            if "FINAL VERDICT" in body:
                return p
    return None

while True:
    now = time.time()
    hits = peer_files()
    if hits:
        last_peer_activity = max(last_peer_activity, max(m for _, m in hits))
    cur_db = db_row()
    db_moved = last_db is not None and cur_db != last_db
    last_db = cur_db
    if db_moved:
        last_peer_activity = now
    jp = judge_verdict_present()
    silent_min = (now - last_peer_activity) / 60
    print(f"[{time.strftime('%H:%M:%S')}] peer_files_now={len(hits)} last_activity={time.strftime('%H:%M', time.localtime(last_peer_activity))} silent={silent_min:.1f}min db={cur_db} verdict_file={jp}", flush=True)
    if jp:
        print(json.dumps({"exit": "JUDGED", "verdict_file": jp, "db": cur_db}), flush=True)
        sys.exit(0)
    if silent_min >= SILENCE_MIN:
        print(json.dumps({"exit": "SILENT", "silent_min": silent_min, "db": cur_db}), flush=True)
        sys.exit(0)
    if (now - START) / 60 > BUDGET_MIN:
        print(json.dumps({"exit": "TIMEOUT", "silent_min": silent_min, "db": cur_db}), flush=True)
        sys.exit(0)
    time.sleep(90)
