#!/usr/bin/env python3
"""Judge slides 027/028: comparison orig vs render via frozen prompt + vision gate."""
import hashlib, json, os, re, subprocess, sys, time

BASE = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries"
ROOT = "/home/codespace/ai_llm_slides"
ANALYZE = os.path.join(ROOT, ".agents/skills/image-analysis/scripts/analyze_image.py")
GATE = os.path.join(ROOT, "scripts/16_vision_gate.sh")
OUTDIR = os.path.join(BASE, "qa", "rejudge2")
RULES = open(os.path.join(OUTDIR, "judge_prompt_frozen.txt")).read().strip()

CONTEXT = """VIEW: Slide {ss} — original lecture frame vs its PowerPoint recreation (SVM/kernels/QP lecture)
FACTS: the printed slide number is {num}. House chrome is MANDATORY in image 2 and never a discrepancy.
Images are attached in this order: image 1 = ORIGINAL, image 2 = RECREATION.
"""


def md5(p):
    h = hashlib.md5()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 16), b""):
            h.update(c)
    return h.hexdigest()


def verdict_of(p):
    if not os.path.exists(p):
        return "NO_TRANSCRIPT"
    for line in reversed(open(p, errors="replace").read().splitlines()):
        m = re.search(r"FINAL VERDICT:\s*(PASS|FAIL)", line, re.I)
        if m:
            return m.group(1).upper()
    return "INVALID_NO_VERDICT_LINE"


def judge(ss):
    orig = os.path.join(BASE, "unique_slides", f"slide_{ss}.jpg")
    render = os.path.join(BASE, "recreated_pptx", "qa", f"slide{ss}", "render_1.png")
    pptx = os.path.join(BASE, "recreated_pptx", f"slide_{ss}_recreated.pptx")
    m = md5(pptx)
    prompt = CONTEXT.format(ss=ss, num=int(ss)) + "\n" + RULES
    tpath = os.path.join(OUTDIR, f"slide_{ss}_judge_a1.txt")
    cmd = ["timeout", "2400", GATE, "python3", ANALYZE, "comparison",
           orig, render, "-p", prompt,
           "--timeout", "420", "--rounds", "1", "--tries", "1",
           "--max-tokens", "32000", "--transcript", tpath]
    t0 = time.time()
    r = subprocess.run(cmd, capture_output=True, text=True)
    v = verdict_of(tpath)
    row = {"slide": ss, "attempt": 1, "ts": time.strftime("%F %T"),
           "pptx_md5": m, "verdict": v, "transcript": tpath,
           "secs": round(time.time() - t0)}
    with open(os.path.join(OUTDIR, "ledger.jsonl"), "a") as f:
        f.write(json.dumps(row) + "\n")
    print(ss, v, f"{time.time()-t0:.0f}s", m, flush=True)
    return v


if __name__ == "__main__":
    for ss in sys.argv[1:]:
        judge(ss)
