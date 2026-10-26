#!/usr/bin/env python3
"""Wave-5 cascade level-2 tight crops for slide_057 (recursion: parse-gap + gt-gap driven)."""
import json, os
from PIL import Image

RUN = "/home/ahmed/Projects/ai_llm_slides/doc-parse-test/run_20261025-024314"
BASE = f"{RUN}/11_cascade/slide_057"
SRC = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_057.jpg"
FRAME_W, FRAME_H = 960, 540
SCALE = 3

# (id, parent, driver, region description, x0, y0, x1, y1)
REGIONS = [
    ("crop08_ychips_tight", "crop01_enc_top_ychips_bars", "gt-gap", "Y-chip serif-italic row Y_0..Y_{N-1}", 100, 98, 445, 135),
    ("crop09_kv_column", "crop04_central_kv", "gt-gap", "central striped column + K/V badges + tiny Q badges", 450, 100, 615, 420),
    ("crop10_xchips_tight", "crop02_enc_bottom_emb", "gt-gap", "X-chip serif-italic row X_0..X_{N-1}", 100, 450, 445, 495),
    ("crop11_wordrow_tight", "crop02_enc_bottom_emb", "parse-block+gt-gap", "word row Word 0..Word N-1 (parse chart block garbled N-1)", 100, 492, 445, 518),
    ("crop12_softmax_bar", "crop05_dec_top_bars_attn", "gt-gap", "Softmax maroon bar", 590, 60, 795, 85),
    ("crop13_bottom_tokens", "crop06_dec_bottom_tokens", "gt-gap", "decoder bottom token row SOS Je ne suis faisait", 592, 490, 800, 520),
    ("crop14_big_q", "crop06_dec_bottom_tokens", "gt-gap", "big Q badge bottom-right of decoder", 740, 400, 900, 480),
]

def clamp(v, lo, hi):
    return max(lo, min(hi, v))

frame = Image.open(SRC).convert("RGB")
assert frame.size == (FRAME_W, FRAME_H)

with open(f"{BASE}/manifest.json") as f:
    man = json.load(f)

for cid, parent, driver, desc, x0, y0, x1, y1 in REGIONS:
    mw = round((x1 - x0) * 0.04)
    mh = round((y1 - y0) * 0.04)
    bx0, by0 = clamp(x0 - mw, 0, FRAME_W), clamp(y0 - mh, 0, FRAME_H)
    bx1, by1 = clamp(x1 + mw, 0, FRAME_W), clamp(y1 + mh, 0, FRAME_H)
    region = frame.crop((bx0, by0, bx1, by1))
    w, h = region.size
    crop = region.resize((w * SCALE, h * SCALE), Image.LANCZOS)
    out_dir = f"{BASE}/crops/{cid}"
    os.makedirs(out_dir, exist_ok=True)
    crop.save(f"{out_dir}/crop.png", "PNG")
    g = crop.convert("L")
    px = list(g.getdata())
    mean = sum(px) / len(px)
    ok = crop.size[0] >= 480 and crop.size[0] <= 1664 and crop.size[1] <= 2048 and mean > 0
    man["nodes"].append({
        "id": cid,
        "level": 2,
        "parent": parent,
        "driver": driver,
        "provenance": "judge-supplement",
        "source_region": desc,
        "region_frame_px": [x0, y0, x1, y1],
        "box_frame_px": [bx0, by0, bx1, by1],
        "scale": SCALE,
        "crop_px": list(crop.size),
        "transform": "frame_x = crop_x/scale + box.x0; frame_y = crop_y/scale + box.y0",
        "precheck": {"dims_ok": ok, "mean_lum": round(mean, 2)},
        "parse_call_dir": None,
        "judge_files": [],
        "novel_strings": 0,
        "stop_reason": None,
    })
    print(f"{cid}: box=({bx0},{by0})-({bx1},{by1}) crop={crop.size[0]}x{crop.size[1]} mean={mean:.1f} ok={ok}")

with open(f"{BASE}/manifest.json", "w") as f:
    json.dump(man, f, indent=2)
print("manifest updated; nodes:", len(man["nodes"]))
