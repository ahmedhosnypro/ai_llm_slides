#!/usr/bin/env python3
"""Read-only watcher for 002:33 peer (verification-only dispatch).
Polls peer artifacts + DB row. Exits with verdict:
  CERTIFIED   - gen_status=passed AND visual_check=PASS AND transcript banked
  DEAD        - >=40 min no peer artifact writes AND row mid-state
  ALIVE <age> - still active, re-run watcher
  (mine = measure_full.py/measure_p2.py/measure_p3.py excluded from peer clock)
"""
import glob, json, os, subprocess, sys, time

ROOT = "/home/ahmed/Projects/ai_llm_slides"
D = f"{ROOT}/videos/deep-learning/002_transformers_part2"
MINE = {"measure_full.py", "measure_p2.py", "measure_p3.py"}
GRACE = 40 * 60  # seconds of peer silence = death

def peer_files():
    pats = [f"{D}/scratch/slide033/*", f"{D}/recreated_pptx/qa/slide033/*",
            f"{D}/recreated_pptx/build/slide_033*", f"{D}/recreated_pptx/slide_033*",
            f"{D}/recreated_pptx/build/assets/*033*"]
    out = []
    for p in pats:
        for f in glob.glob(p):
            if os.path.isfile(f) and os.path.basename(f) not in MINE:
                out.append(f)
    return out

def dbrow():
    env = dict(os.environ, VIDEO="deep-learning/002_transformers_part2")
    r = subprocess.run(["python3", f"{ROOT}/scripts/15_progress.py", "get", "33"],
                       capture_output=True, text=True, env=env, cwd=ROOT)
    try:
        return json.loads(r.stdout)
    except Exception:
        return {}

now = time.time()
files = peer_files()
if files:
    newest = max(os.path.getmtime(f) for f in files)
    newest_f = max(files, key=os.path.getmtime)
else:
    newest = 0; newest_f = "-"
row = dbrow()
silence = now - newest if newest else float("inf")
cert = (row.get("gen_status") == "passed" and row.get("visual_check") == "PASS"
        and row.get("visual_transcript") and os.path.isfile(os.path.join(ROOT, row["visual_transcript"])))
print(f"now={time.strftime('%H:%M:%S')} newest_peer={time.strftime('%H:%M:%S', time.localtime(newest))} ({newest_f}) silence={silence/60:.1f}min row=gen:{row.get('gen_status')} vis:{row.get('visual_check')} vcatt:{row.get('visual_attempts')}")
if cert:
    print("CERTIFIED", row.get("visual_transcript")); sys.exit(0)
if newest and silence >= GRACE and row.get("gen_status") not in ("passed", "failed"):
    print("DEAD"); sys.exit(0)
if row.get("gen_status") == "failed":
    print("ROW_FAILED"); sys.exit(0)
print(f"ALIVE {silence/60:.1f}"); sys.exit(3)
