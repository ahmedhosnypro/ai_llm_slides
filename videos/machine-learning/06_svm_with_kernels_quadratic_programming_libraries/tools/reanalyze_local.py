#!/usr/bin/env python3
# Namespace-local re-analysis runner. Identical contract to tools/reanalyze_all.py
# (same prompt, same out dir, same done() gate) but sends a payload the Nvidia
# upstream lane accepts: the published skill's disable block adds
# reasoning_effort:"none", which the nva candidate 400s; thinking-only works.
import argparse, base64, json, os, subprocess, sys, time, urllib.request

BASE = "/home/codespace/ai_llm_slides"
NS = BASE + "/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries"
GATE = BASE + "/scripts/16_vision_gate.sh"
OUT = NS + "/qa/reanalysis2"
PROMPT = NS + "/analysis_prompt_v2.txt"
KEY_FILE = BASE + "/.agents/skills/image-analysis/scripts/.analyze-image-key"
ENDPOINT = "http://localhost:17844/v1/chat/completions"

p = argparse.ArgumentParser()
p.add_argument("--start", type=int, required=True)
p.add_argument("--end", type=int, required=True)
p.add_argument("--concurrency", type=int, default=4)
p.add_argument("--timeout", type=int, default=420)
p.add_argument("--max-tokens", type=int, default=24000)
a = p.parse_args()

os.makedirs(OUT, exist_ok=True)
RULES = open(PROMPT).read().strip()
KEY = open(KEY_FILE).read().strip()

WORKER = r'''
import base64, json, sys, urllib.request
img, prompt, out, mt = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4])
key = open(sys.argv[5]).read().strip()
with open(img, "rb") as f:
    url = "data:image/png;base64," + base64.b64encode(f.read()).decode()
payload = {"model": "images", "max_tokens": mt, "stream": True,
           "thinking": {"type": "disabled"},
           "messages": [{"role": "user", "content": [
               {"type": "text", "text": prompt},
               {"type": "image_url", "image_url": {"url": url}}]}]}
req = urllib.request.Request("http://localhost:17844/v1/chat/completions",
    data=json.dumps(payload).encode(),
    headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"})
total = 0
with open(out, "w") as f, urllib.request.urlopen(req, timeout=int(sys.argv[6])) as r:
    for line in r:
        line = line.decode("utf-8", "replace").strip()
        if not line.startswith("data:"):
            continue
        d = line[5:].strip()
        if d == "[DONE]":
            break
        try:
            c = json.loads(d)["choices"][0]["delta"].get("content")
        except Exception:
            c = None
        if c:
            f.write(c)
            f.flush()
            total += len(c)
print("banked", total)
'''

with open(NS + "/tools/_rean_worker.py", "w") as f:
    f.write(WORKER)

def done(n):
    d = OUT + f"/slide_{n:03d}_analysis.txt"
    if not os.path.exists(d) or os.path.getsize(d) < 4000:
        return False
    body = open(d, errors="replace").read()
    return all(f"{i}." in body for i in range(1, 12))

nums = [n for n in range(a.start, a.end + 1) if not done(n)]
print(f"todo={len(nums)} of range {a.start}-{a.end} (concurrency={a.concurrency})", flush=True)
alive, i = {}, 0
while i < len(nums) or alive:
    while len(alive) < a.concurrency and i < len(nums):
        n = nums[i]
        ss = f"{n:03d}"
        view = f"original lecture slide {n} of 55 (SVM/kernels/QP math lecture)"
        prompt = RULES + f"\n\nVIEW: {view}\nCAPTURE: 960x540 CSS px, scale 1, app=lecture-video-frame"
        alive[n] = subprocess.Popen(
            ["timeout", "780", GATE, "python3", NS + "/tools/_rean_worker.py",
             NS + f"/qa/rejudge2/orig_png/slide_{ss}.png", prompt,
             OUT + f"/slide_{ss}_analysis.txt", str(a.max_tokens), KEY_FILE,
             str(a.timeout)],
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        print(f"[{ss}] launched {time.strftime('%F %T')}", flush=True)
        i += 1
        time.sleep(3)
    for n in [n for n, q in alive.items() if q.poll() is not None]:
        q = alive.pop(n)
        tail = q.communicate()[0] or ""
        with open(OUT + f"/slide_{n:03d}_driver.log", "w") as f:
            f.write(tail)
        sz = os.path.getsize(OUT + f"/slide_{n:03d}_analysis.txt") \
            if os.path.exists(OUT + f"/slide_{n:03d}_analysis.txt") else 0
        print(f"[{n:03d}] rc={q.returncode} banked_bytes={sz} {time.strftime('%F %T')}", flush=True)
    if not alive:
        break
    time.sleep(4)
print("DONE", flush=True)
