#!/usr/bin/env python3
# Serial rejudge of slides 045-055: frozen prompt, orig_png vs rejudge2 renders, model images.
# Banks every attempt to qa/rejudge2/ledger.jsonl. Up to 4 attempts per slide.
import hashlib, json, os, re, subprocess, sys, time

BASE = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries"
ANALYZE = "/home/codespace/ai_llm_slides/.agents/skills/image-analysis/scripts/analyze_image.py"
GATE = "/home/codespace/ai_llm_slides/scripts/16_vision_gate.sh"
OUT = os.path.join(BASE, "qa", "rejudge2")
LEDGER = os.path.join(OUT, "ledger.jsonl")
PROMPT = open(os.path.join(OUT, "judge_prompt_frozen.txt")).read().strip()
MODEL = os.environ.get("JUDGE_MODEL", "images")
ATTEMPTS = int(os.environ.get("JUDGE_ATTEMPTS", "4"))
WALL = int(os.environ.get("JUDGE_WALL", "2400"))
HTTP_TIMEOUT = int(os.environ.get("JUDGE_HTTP_TIMEOUT", "420"))


def md5(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for c in iter(lambda: f.read(1 << 16), b""):
            h.update(c)
    return h.hexdigest()


def bank(row):
    with open(LEDGER, "a") as f:
        f.write(json.dumps(row) + "\n")


def verdict_of(path):
    if not os.path.exists(path):
        return "NO_TRANSCRIPT"
    for line in reversed(open(path, errors="replace").read().splitlines()):
        m = re.search(r"FINAL VERDICT:\s*(PASS|FAIL)", line, re.I)
        if m:
            return m.group(1).upper()
    return "NO_VERDICT"


def judge(num):
    ss = f"{num:03d}"
    pptx = os.path.join(BASE, "recreated_pptx", f"slide_{ss}_recreated.pptx")
    orig = os.path.join(OUT, "orig_png", f"slide_{ss}.png")
    render = os.path.join(OUT, "renders", f"slide_{ss}-1.png")
    for tag, p in (("pptx", pptx), ("orig", orig), ("render", render)):
        if not os.path.exists(p):
            print(f"[{ss}] MISSING {tag}: {p}", flush=True)
            return "MISSING"
    m = md5(pptx)
    prior_attempts = []
    if os.path.exists(LEDGER):
        for line in open(LEDGER):
            try:
                row = json.loads(line)
                if str(row.get("slide")).zfill(3) == ss:
                    prior_attempts.append(int(row.get("attempt", 0)))
            except (ValueError, TypeError, json.JSONDecodeError):
                pass
    first_attempt = max(prior_attempts, default=0) + 1
    prompt = PROMPT + f"\n\nSlide number printed on the original: {num}. Compare image 1 (ORIGINAL) with image 2 (RECREATION)."
    for attempt in range(first_attempt, first_attempt + ATTEMPTS):
        out_k = os.path.join(OUT, f"slide_{ss}_rj_a{attempt}.txt")
        log_k = os.path.join(OUT, f"slide_{ss}_rj_a{attempt}.log")
        cmd = ["timeout", str(WALL), "bash", GATE, "python3", ANALYZE, "comparison",
               orig, render, "-p", prompt, "--models", MODEL,
               "--timeout", str(HTTP_TIMEOUT), "--rounds", "1", "--tries", "1",
               "--max-tokens", "32000", "--transcript", out_k]
        t0 = time.time()
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=WALL + 120)
        tail = (proc.stdout or "") + (proc.stderr or "")
        with open(log_k, "w") as f:
            f.write(tail)
        rc = proc.returncode
        v = verdict_of(out_k)
        row = {"slide": ss, "attempt": attempt, "ts": time.strftime("%F %T"),
               "pptx_md5": m, "verdict": v, "rc": rc, "transcript": out_k,
               "secs": round(time.time() - t0, 1)}
        bank(row)
        print(f"[{ss}] {v} rc={rc} (attempt {attempt}, {row['secs']}s)", flush=True)
        if v in ("PASS", "FAIL"):
            return v
        if rc not in (124, 1) and v not in ("NO_VERDICT", "NO_TRANSCRIPT"):
            return v
    bank({"slide": ss, "verdict": "UNRESOLVED", "ts": time.strftime("%F %T"), "pptx_md5": m})
    return "UNRESOLVED"


if __name__ == "__main__":
    for a in sys.argv[1:]:
        print(f"=== slide {a} ===", flush=True)
        judge(int(a))
