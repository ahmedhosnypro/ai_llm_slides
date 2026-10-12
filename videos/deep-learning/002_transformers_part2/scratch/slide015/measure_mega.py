#!/usr/bin/env python3
"""Mega-measurement on the slide-coords resample (960x540, 1px=1pt).
Targeted scans for: cards, pills, ovals, chips, containers, climbing boxes,
ellipses, flow boxes, swoosh, plane, title. Reports color runs per scanline.
"""
from PIL import Image
import json

img = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide015/frame_in_slide_coords.png").convert("RGB")
W, H = img.size
px = img.load()

def runs_h(y, x0=45, x1=915, q=18, minlen=3):
    prev = None; out = []
    for x in range(x0, x1):
        p = px[x, y]
        key = (p[0] // q, p[1] // q, p[2] // q)
        if key != prev:
            out.append([x, x, p]); prev = key
        else:
            out[-1][1] = x
    return [(a, b, tuple(c)) for a, b, c in out if b - a + 1 >= minlen]

def runs_v(x, y0=48, y1=516, q=18, minlen=3):
    prev = None; out = []
    for y in range(y0, y1):
        p = px[x, y]
        key = (p[0] // q, p[1] // q, p[2] // q)
        if key != prev:
            out.append([y, y, p]); prev = key
        else:
            out[-1][1] = y
    return [(a, b, tuple(c)) for a, b, c in out if b - a + 1 >= minlen]

out = {}
# --- cards: tops via vertical scans at several x; right edges via horizontal scans
for x in (150, 250, 350, 450, 550, 650, 700, 750, 800, 830):
    out[f"v_x{x}"] = runs_v(x)
for y in (110, 130, 150, 170, 190, 210, 300, 380, 430):
    out[f"h_y{y}"] = runs_h(y)

# --- front card bottom edge: vertical scans near bottom
for x in (120, 300, 500, 620):
    out[f"vbot_x{x}"] = runs_v(x, 380, 516)

# --- pills/ovals bands: rows through each band
for y in (196, 176, 156, 136, 116):
    out[f"band_y{y}"] = runs_h(y, 100, 860, q=14, minlen=2)

# --- title band
for y in (484, 492, 500):
    out[f"title_y{y}"] = runs_h(y, 45, 915, q=14, minlen=2)

# --- swoosh band rows
for y in (250, 270, 290, 310, 330, 350, 370):
    out[f"swoosh_y{y}"] = runs_h(y, 550, 915, q=16, minlen=2)

print(json.dumps(out, indent=0, default=str))
