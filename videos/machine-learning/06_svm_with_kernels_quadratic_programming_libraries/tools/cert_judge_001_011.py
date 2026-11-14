#!/usr/bin/env python3
import base64, hashlib, json, os, re, sys, time, urllib.error, urllib.request
from pathlib import Path

NS = Path("/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries")
OUT = NS / "qa/rejudge2"
PROMPT = (OUT / "judge_prompt_frozen.txt").read_text().strip()
KEY = os.environ.get("IR_API_KEY") or Path("/home/codespace/nvidia/.keys/ironrouter.key").read_text().strip()


def data_url(path):
    mime = "image/png" if path.suffix == ".png" else "image/jpeg"
    return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode()


def md5(path):
    return hashlib.md5(path.read_bytes()).hexdigest()


def bank(row):
    with (OUT / "ledger.jsonl").open("a") as fh:
        fh.write(json.dumps(row) + "\n")


def next_attempt(slide):
    best = 0
    for line in (OUT / "ledger.jsonl").read_text().splitlines():
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        if str(row.get("slide")).zfill(3) == slide:
            try:
                best = max(best, int(row.get("attempt", 0)))
            except (TypeError, ValueError):
                pass
    return best + 1


def call(slide, attempt, pptx, orig, render):
    prompt = PROMPT + f"\n\nSlide number printed on the original: {int(slide)}. Compare image 1 (ORIGINAL) with image 2 (RECREATION)."
    payload = {"model": "images", "stream": True, "max_tokens": 32000, "messages": [{"role": "user", "content": [
        {"type": "text", "text": prompt},
        {"type": "image_url", "image_url": {"url": data_url(orig)}},
        {"type": "image_url", "image_url": {"url": data_url(render)}},
    ]}]}
    req = urllib.request.Request("http://localhost:17844/v1/chat/completions", data=json.dumps(payload).encode(),
        headers={"Authorization": "Bearer " + KEY, "Content-Type": "application/json"})
    transcript = OUT / f"slide_{slide}_cert_a{attempt}.txt"
    raw = OUT / f"slide_{slide}_cert_a{attempt}.stream.jsonl"
    chunks = []
    with urllib.request.urlopen(req, timeout=900) as response, raw.open("w") as out:
        for line in response:
            text = line.decode("utf-8", "replace").strip()
            if not text:
                continue
            out.write(text + "\n")
            out.flush()
            if not text.startswith("data:") or text == "data: [DONE]":
                continue
            event = json.loads(text[5:].strip())
            for choice in event.get("choices", []):
                token = (choice.get("delta") or {}).get("content") or ""
                if token:
                    chunks.append(token)
    body = "".join(chunks)
    transcript.write_text(body + "\n")
    match = None
    for match in re.finditer(r"FINAL VERDICT:\s*(PASS|FAIL)", body, re.I):
        pass
    return body, (match.group(1).upper() if match else "NO_VERDICT"), transcript, raw


def main():
    slide = sys.argv[1].zfill(3)
    pptx = NS / f"recreated_pptx/slide_{slide}_recreated.pptx"
    orig = OUT / f"orig_png/slide_{slide}.png"
    render = OUT / f"cert_renders/slide_{slide}.png"
    attempt = next_attempt(slide)
    for retry in range(1, 5):
        before = md5(pptx)
        try:
            body, verdict, transcript, raw = call(slide, attempt, pptx, orig, render)
            error = None
        except Exception as exc:
            body, verdict, transcript, raw, error = "", "NO_TRANSCRIPT", None, None, f"{type(exc).__name__}: {exc}"
        after = md5(pptx)
        row = {"slide": slide, "attempt": attempt, "ts": time.strftime("%F %T"), "pptx_md5": before,
               "verdict": verdict, "model": "images", "driver": "direct_stream", "transport_retry": retry,
               "stable_md5": before == after}
        if transcript:
            row["transcript"] = str(transcript)
            row["raw_stream"] = str(raw)
            row["chars"] = len(body)
        if error:
            row["error"] = error
        bank(row)
        print(json.dumps({k: row[k] for k in ("slide", "attempt", "verdict", "pptx_md5", "transport_retry")}))
        if verdict != "NO_TRANSCRIPT":
            return
    print(json.dumps({"slide": slide, "attempt": attempt, "verdict": "NO_TRANSCRIPT", "retries": 4}))


if __name__ == "__main__":
    main()
