#!/usr/bin/env python3
"""m20_crops.py — dense-region crops for attempt-2 self-check §6 (crop-pair vision).
Regions fixed per judge attempt-1: dec-top (Output/Decoder overprint) and enc stack
(two-sub-block structure). Original = 960x540 frame; render = 2000x1125 @150dpi.
Both cropped at the SAME frame-px window, upscaled x2."""
from PIL import Image
import os

BASE = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1"
ORIG = f"{BASE}/unique_slides/slide_016.jpg"
REND = f"{BASE}/recreated_pptx/qa/slide016/render_2.png"
OUT = f"{BASE}/scratch/slide016/crops"
os.makedirs(OUT, exist_ok=True)

SCALE = 150 / 72.0
o = Image.open(ORIG).convert("RGB")   # 960x540, 1px = 1pt
rr = Image.open(REND).convert("RGB")  # 2000x1125

REGIONS = {
    "dectop":   (722, 98, 900, 205),   # Output Probabilities / Decoder / red arrow / Softmax / Linear
    "encstack": (578, 253, 748, 420),  # enc container + sub-blocks + VKQ
}
for name, (x0, y0, x1, y1) in REGIONS.items():
    oc = o.crop((x0, y0, x1, y1))
    rc = rr.crop((int(x0 * SCALE), int(y0 * SCALE), int(x1 * SCALE), int(y1 * SCALE)))
    # upscale so the smaller dimension is >= ~400px
    w, h = oc.size
    f = max(1, int(np.ceil(400 / min(w, h)))) if (np := __import__("numpy")) else 2
    f = max(f, 2)
    oc2 = oc.resize((w * f, h * f), Image.LANCZOS)
    rw, rh = rc.size
    rc2 = rc.resize((int(rw * (w * f) / rw / (h * f) * rh) if False else rw * f // 1, rh * f), Image.LANCZOS) if False else rc.resize((rw * f, rh * f), Image.LANCZOS)
    oc2.save(f"{OUT}/{name}_orig.png")
    rc2.save(f"{OUT}/{name}_render.png")
    print(name, "orig", oc.size, "->", oc2.size, "| render", rc.size, "->", rc2.size)
