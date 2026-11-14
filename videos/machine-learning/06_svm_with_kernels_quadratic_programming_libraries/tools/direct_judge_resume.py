#!/usr/bin/env python3
import base64, hashlib, json, os, re, sys, time, urllib.error, urllib.request
from pathlib import Path

NS = Path("/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries")
OUT = NS / "qa/rejudge2"
PROMPT = (OUT / "judge_prompt_frozen.txt").read_text().strip()
LEDGER = OUT / "ledger.jsonl"


def md5(path):
    return hashlib.md5(path.read_bytes()).hexdigest()


def bank(row):
    with LEDGER.open("a") as f:
        f.write(json.dumps(row) + "\n")


def attempt_num(ss):
    n = 0
    for line in LEDGER.read_text().splitlines():
        try:
            if str(json.loads(line).get("slide")).zfill(3) == ss:
                n = max(n, int(json.loads(line).get("attempt", 0)))
        except Exception:
            pass
    return n + 1


def call(ss, num, attempt):
    pptx = NS / f"recreated_pptx/slide_{ss}_recreated.pptx"
    orig = OUT / f"orig_png/slide_{ss}.png"
    render = NS / f"recreated_pptx/renders/slide_{ss}_recreated-1.png"
    prompt = PROMPT + f"\n\nSlide number printed on the original: {num}. Compare image 1 (ORIGINAL) with image 2 (RECREATION)."
    payload = {"model": "images", "stream": True, "max_tokens": 32000, "messages": [{"role": "user", "content": [
        {"type": "text", "text": prompt},
        {"type": "image_url", "image_url": {"url": "data:image/png;base64," + base64.b64encode(orig.read_bytes()).decode()}},
        {"type": "image_url", "image_url": {"url": "data:image/png;base64," + base64.b64encode(render.read_bytes()).decode()}},
    ]}]}
    req = urllib.request.Request("http://localhost:17844/v1/chat/completions", data=json.dumps(payload).encode(), headers={
        "Authorization": "Bearer " + os.environ["IR_API_KEY"], "Content-Type": "application/json"})
    chunks = []
    try:
        with urllib.request.urlopen(req, timeout=900) as response:
            for raw in response:
                line = raw.decode("utf-8", "replace").strip()
                if not line.startswith("data:") or line == "data: [DONE]":
                    continue
                event = json.loads(line[5:].strip())
                delta = (event.get("choices") or [{}])[0].get("delta", {})
                if delta.get("content"):
                    chunks.append(delta["content"])
        text = "".join(chunks)
        if not text.strip():
            return "EMPTY_STREAM", ""
        return text, None
    except urllib.error.HTTPError as e:
        return f"HTTP_{e.code}", e.read().decode("utf-8", "replace")[:500]
    except Exception as e:
        return type(e).__name__, str(e)[:500]


def judge(num):
    ss = f"{num:03d}"
    for attempt in range(1, 5):
        text, error = call(ss, num, attempt)
        transcript = OUT / f"slide_{ss}_resume_a{attempt}.txt"
        transcript.write_text(text if text else (error or ""))
        match = re.search(r"FINAL VERDICT:\s*(PASS|FAIL)", text, re.I)
        verdict = match.group(1).upper() if match else ("TRANSPORT_RETRY" if error else "NO_VERDICT")
        bank({"slide": ss, "attempt": attempt, "ts": time.strftime("%F %T"), "pptx_md5": md5(NS / f"recreated_pptx/slide_{ss}_recreated.pptx"), "verdict": verdict, "transcript": str(transcript), "driver": "direct_stream_resume", "error": error})
        print(f"[{ss}] {verdict} attempt {attempt}", flush=True)
        if verdict in ("PASS", "FAIL"):
            return verdict
    return "UNRESOLVED"


if __name__ == "__main__":
    for value in sys.argv[1:]:
        judge(int(value))
