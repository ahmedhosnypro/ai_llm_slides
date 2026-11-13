#!/usr/bin/env python3
import base64, hashlib, json, os, re, sys, time, urllib.request
from pathlib import Path

NS = Path("/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries")
OUT = NS / "qa/rejudge2"
MODEL = os.environ.get("JUDGE_MODEL", "images")
PROMPT = (OUT / "judge_prompt_frozen.txt").read_text().strip()


def data_url(path):
    return "data:image/png;base64," + base64.b64encode(path.read_bytes()).decode()


def md5(path):
    return hashlib.md5(path.read_bytes()).hexdigest()


def bank(row):
    with (OUT / "ledger.jsonl").open("a") as f:
        f.write(json.dumps(row) + "\n")


def judge(num):
    ss = f"{num:03d}"
    pptx = NS / f"recreated_pptx/slide_{ss}_recreated.pptx"
    orig = OUT / f"orig_png/slide_{ss}.png"
    render = NS / f"recreated_pptx/renders/slide_{ss}_recreated-1.png"
    prompt = PROMPT + f"\n\nSlide number printed on the original: {num}. Compare image 1 (ORIGINAL) with image 2 (RECREATION)."
    payload = {
        "model": MODEL, "stream": True, "max_tokens": 8192,
        "messages": [{"role": "user", "content": [
            {"type": "text", "text": prompt},
            {"type": "image_url", "image_url": {"url": data_url(orig)}},
            {"type": "image_url", "image_url": {"url": data_url(render)}},
        ]}],
    }
    req = urllib.request.Request(
        "http://localhost:17844/v1/chat/completions", data=json.dumps(payload).encode(),
        headers={"Authorization": "Bearer " + os.environ["IR_API_KEY"], "Content-Type": "application/json"})
    attempts = []
    for line in (OUT / "ledger.jsonl").read_text().splitlines():
        try:
            row = json.loads(line)
            if str(row.get("slide")).zfill(3) == ss:
                attempts.append(int(row.get("attempt", 0)))
        except (ValueError, TypeError, json.JSONDecodeError):
            pass
    attempt = max(attempts, default=0) + 1
    chunks = []
    try:
        with urllib.request.urlopen(req, timeout=600) as response:
            for raw in response:
                line = raw.decode("utf-8", "replace").strip()
                if not line.startswith("data:") or line == "data: [DONE]":
                    continue
                event = json.loads(line[5:].strip())
                choices = event.get("choices") or []
                if not choices:
                    continue
                delta = choices[0].get("delta", {})
                if delta.get("content"):
                    chunks.append(delta["content"])
    except Exception as exc:
        bank({"slide": ss, "attempt": attempt, "ts": time.strftime("%F %T"),
              "pptx_md5": md5(pptx), "verdict": "NO_TRANSCRIPT", "model": MODEL,
              "driver": "direct_stream", "error": f"{type(exc).__name__}: {exc}"})
        print(f"[{ss}] NO_TRANSCRIPT attempt {attempt}: {type(exc).__name__}: {exc}")
        return
    text = "".join(chunks)
    transcript = OUT / f"slide_{ss}_direct_a{attempt}.txt"
    transcript.write_text(text)
    match = re.search(r"FINAL VERDICT:\s*(PASS|FAIL)", text, re.I)
    verdict = match.group(1).upper() if match else "NO_VERDICT"
    bank({"slide": ss, "attempt": attempt, "ts": time.strftime("%F %T"),
          "pptx_md5": md5(pptx), "verdict": verdict, "model": MODEL,
          "transcript": str(transcript), "driver": "direct_stream"})
    print(f"[{ss}] {verdict} attempt {attempt}; transcript {transcript}")


if __name__ == "__main__":
    judge(int(sys.argv[1]))
