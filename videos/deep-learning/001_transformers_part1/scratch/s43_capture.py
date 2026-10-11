#!/usr/bin/env python3
"""One-off: slide 43 vision analysis via the fallback model, response banked to the
project scratch (no /tmp — the user's /tmp quota is hard-blocked). Mimics script 12
exactly (same prompt/params) but saves the raw text even when JSON parsing fails."""
import base64, json, sys, time
import openai

S = "videos/deep-learning/001_transformers_part1/scratch"
KEY = open(".analyze-image-key").read().strip()
client = openai.OpenAI(base_url="http://localhost:17844/v1", api_key=KEY)
sys.path.insert(0, "scripts")
import importlib.util
spec = importlib.util.spec_from_file_location("a12", "scripts/12_analyze_slides.py")
a12 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(a12)

b64 = base64.b64encode(
    open("videos/deep-learning/001_transformers_part1/unique_slides/slide_043.jpg", "rb").read()
).decode()
t0 = time.time()
resp = client.chat.completions.create(
    model="glm-5.3-flash",
    messages=[{"role": "user", "content": [
        {"type": "text", "text": a12.ANALYSIS_PROMPT},
        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}},
    ]}],
    max_tokens=65536, temperature=0.1, stream=True)
parts, finish = [], None
for chunk in resp:
    if chunk.choices and chunk.choices[0].delta and chunk.choices[0].delta.content:
        parts.append(chunk.choices[0].delta.content)
    if chunk.choices and chunk.choices[0].finish_reason:
        finish = chunk.choices[0].finish_reason
text = "".join(parts)
open(f"{S}/s43_raw_response.txt", "w").write(text)
print(f"captured {len(text)} chars, finish={finish}, {time.time()-t0:.0f}s")
try:
    a12.extract_json(text)
    print("PARSE: OK")
except Exception as e:
    print(f"PARSE FAIL: {e}")
