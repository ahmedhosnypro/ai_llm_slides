#!/usr/bin/env python3
"""Wave-5 cascade level-1 crops for slide_057 from judge-supplement defect regions."""
import json, os
from PIL import Image

RUN = "/home/ahmed/Projects/ai_llm_slides/doc-parse-test/run_20261025-024314"
BASE = f"{RUN}/11_cascade/slide_057"
SRC = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_057.jpg"
FRAME_W, FRAME_H = 960, 540
SCALE = 3

# (id, region description, x0, y0, x1, y1) frame px, pre-margin; all provenance judge-supplement
REGIONS = [
    ("crop01_enc_top_ychips_bars", "Y-chip row (Y_0..Y_{N-1}) + Encoder Block M/2 bars", 100, 95, 448, 235),
    ("crop02_enc_bottom_emb", "Word Embedding + Positional Encoding box + X-chip row + word row", 100, 410, 448, 518),
    ("crop03_enc_mid_bars_vlabel", "Encoder Block 1/0 bars + vertical 'Encoder' label", 60, 250, 448, 395),
    ("crop04_central_kv", "K/V badges + central striped column + tiny Q badges", 430, 90, 590, 440),
    ("crop05_dec_top_bars_attn", "Softmax + Residual/FFN bar labels + attention-box 3-line text + vertical 'Decoder' label", 580, 60, 860, 345),
    ("crop06_dec_bottom_tokens", "Multi-Head/Self-Attention lavender boxes + purple bar + bottom token row + big Q", 580, 400, 860, 520),
    ("crop07_legend", "legend lines: Encoder / Decoder / Attention", 425, 405, 585, 505),
]

def clamp(v, lo, hi):
    return max(lo, min(hi, v))

frame = Image.open(SRC).convert("RGB")
assert frame.size == (FRAME_W, FRAME_H), frame.size

nodes = []
for cid, desc, x0, y0, x1, y1 in REGIONS:
    mw = round((x1 - x0) * 0.04)
    mh = round((y1 - y0) * 0.04)
    bx0, by0 = clamp(x0 - mw, 0, FRAME_W), clamp(y0 - mh, 0, FRAME_H)
    bx1, by1 = clamp(x1 + mw, 0, FRAME_W), clamp(y1 + mh, 0, FRAME_H)
    region = frame.crop((bx0, by0, bx1, by1))
    w, h = region.size
    crop = region.resize((w * SCALE, h * SCALE), Image.LANCZOS)
    out_dir = f"{BASE}/crops/{cid}"
    os.makedirs(out_dir, exist_ok=True)
    out = f"{out_dir}/crop.png"
    crop.save(out, "PNG")
    g = crop.convert("L")
    mean = sum(g.getdata()) / (crop.size[0] * crop.size[1])
    ok = crop.size[0] >= 480 and crop.size[0] <= 1664 and crop.size[1] <= 2048 and mean > 0
    node = {
        "id": cid,
        "level": 1,
        "provenance": "judge-supplement",
        "source_region": desc,
        "region_frame_px": [x0, y0, x1, y1],
        "box_frame_px": [bx0, by0, bx1, by1],
        "scale": SCALE,
        "crop_px": list(crop.size),
        "transform": "frame_x = crop_x/scale + box.x0; frame_y = crop_y/scale + box.y0",
        "precheck": {"dims_ok": ok and crop.size[1] <= 2048, "mean_lum": round(mean, 2)},
        "parse_call_dir": None,
        "judge_files": [],
        "novel_strings": 0,
        "stop_reason": None,
    }
    nodes.append(node)
    print(f"{cid}: box=({bx0},{by0})-({bx1},{by1}) crop={crop.size[0]}x{crop.size[1]} mean={mean:.1f} ok={ok}")

with open(f"{BASE}/manifest.json", "w") as f:
    json.dump({"slide": "057", "frame_px": [FRAME_W, FRAME_H], "source_jpg": SRC, "nodes": nodes}, f, indent=2)
print("manifest written:", f"{BASE}/manifest.json")
