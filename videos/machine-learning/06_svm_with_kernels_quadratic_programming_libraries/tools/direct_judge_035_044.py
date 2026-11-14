#!/usr/bin/env python3
import base64, hashlib, json, re, sys, time, urllib.request
from pathlib import Path

NS = Path("/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries")
OUT = NS / "qa/rejudge2"
PROMPT = (OUT / "judge_prompt_frozen.txt").read_text().strip()
KEY = Path("/home/codespace/nvidia/.keys/ironrouter.key").read_text().strip()


def md5(path):
    return hashlib.md5(path.read_bytes()).hexdigest()


def bank(row):
    with (OUT / "ledger.jsonl").open("a") as f:
        f.write(json.dumps(row) + "\n")


def next_attempt(ss):
    attempts = []
    for line in (OUT / "ledger.jsonl").read_text().splitlines():
        try:
            row = json.loads(line)
            if str(row.get("slide")).zfill(3) == ss:
                attempts.append(int(row.get("attempt", 0)))
        except (ValueError, TypeError, json.JSONDecodeError):
            pass
    return max(attempts, default=0) + 1


def image(path):
    return "data:image/png;base64," + base64.b64encode(path.read_bytes()).decode()


def request(payload):
    req = urllib.request.Request(
        "http://localhost:17844/v1/chat/completions", data=json.dumps(payload).encode(),
        headers={"Authorization": "Bearer " + KEY, "Content-Type": "application/json"})
    chunks, raw = [], []
    with urllib.request.urlopen(req, timeout=600) as response:
        for line in response:
            text = line.decode("utf-8", "replace").strip()
            if not text:
                continue
            raw.append(text)
            if not text.startswith("data:") or text == "data: [DONE]":
                continue
            event = json.loads(text[5:].strip())
            choices = event.get("choices") or []
            if choices and choices[0].get("delta", {}).get("content"):
                chunks.append(choices[0]["delta"]["content"])
    return "".join(chunks), raw


def judge(num):
    ss = f"{num:03d}"
    pptx = NS / f"recreated_pptx/slide_{ss}_recreated.pptx"
    orig = OUT / f"orig_png/slide_{ss}.png"
    render = NS / f"recreated_pptx/renders/slide_{ss}_recreated-1.png"
    before = md5(pptx)
    prompt = PROMPT + f"\n\nSlide number printed on the original: {num}. Compare image 1 (ORIGINAL) with image 2 (RECREATION)."
    payload = {"model": "images", "stream": True, "max_tokens": 16384,
               "messages": [{"role": "user", "content": [
                   {"type": "text", "text": prompt},
                   {"type": "image_url", "image_url": {"url": image(orig)}},
                   {"type": "image_url", "image_url": {"url": image(render)}}]}]}
    for retry in range(4):
        attempt = next_attempt(ss)
        transcript = OUT / f"slide_{ss}_direct_a{attempt}.txt"
        stream = OUT / f"slide_{ss}_direct_a{attempt}.stream.jsonl"
        try:
            text, raw = request(payload)
            stream.write_text("\n".join(raw) + "\n")
            transcript.write_text(text)
            lines = [x.strip() for x in text.splitlines() if x.strip()]
            match = re.fullmatch(r"FINAL VERDICT:\s*(PASS|FAIL)", lines[-1], re.I) if lines else None
            coherent = len(text) >= 150 and "Ground rules acknowledged:" in text
            verdict = match.group(1).upper() if match and coherent else "NO_TRANSCRIPT"
            error = None
        except Exception as exc:
            verdict = "NO_TRANSCRIPT"
            error = f"{type(exc).__name__}: {exc}"
            transcript.write_text(error + "\n")
        row = {"slide": ss, "attempt": attempt, "ts": time.strftime("%F %T"),
               "pptx_md5": before, "render_md5": md5(render), "verdict": verdict,
               "model": "images", "driver": "direct_stream", "transcript": str(transcript),
               "raw_stream": str(stream) if stream.exists() else None, "transport_retry": retry + 1}
        if error:
            row["error"] = error
        bank(row)
        print(f"[{ss}] {verdict} attempt {attempt} transport {retry + 1}", flush=True)
        if verdict != "NO_TRANSCRIPT":
            if md5(pptx) != before:
                raise RuntimeError("pptx changed during judge")
            return verdict
        time.sleep(20)
    return "NO_TRANSCRIPT"


if __name__ == "__main__":
    judge(int(sys.argv[1]))
