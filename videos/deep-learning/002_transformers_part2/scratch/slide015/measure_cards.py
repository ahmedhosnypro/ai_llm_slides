#!/usr/bin/env python3
"""Measure 002 slide_015 frame: card staircase bboxes + key block zones.
Frame coords measured directly; converted to slide coords via
slide_x = (frame_x - 17.628)/0.961232, slide_y = frame_y/0.955556.
"""
from PIL import Image
import json, math

img = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_015.jpg").convert("RGB")
W, H = img.size
px = img.load()
AX, SX, SY = 17.628, 0.961232, 0.955556
to_slide = lambda fx_, fy_: ((fx_ - AX) / SX, fy_ / SY)

def bbox_of(pred, x0, y0, x1, y1, step=1):
    pts = [(x, y) for y in range(y0, y1, step) for x in range(x0, x1, step) if pred(px[x, y])]
    if not pts:
        return None, 0
    return (min(p[0] for p in pts), min(p[1] for p in pts),
            max(p[0] for p in pts), max(p[1] for p in pts)), len(pts)

# color probes at sample points (frame coords) to calibrate fills
samples = {
    "front_card@ (320,380)": (320, 380),
    "front_card@ (250,300)": (250, 300),
    "lavender@ (700,260)": (700, 260),
    "yellow@ (760,200)": (760, 200),
    "green@ (800,160)": (800, 160),
    "peach@ (830,120)": (830, 120),
    "orange_ellipse@ (170,300)": (170, 300),
    "green_ellipse@ (215,300)": (215, 300),
    "dotprod@ (250,320)": (250, 320),
    "scaling_pill@ (300,350)": (300, 350),
    "softmax_pill@ (350,350)": (350, 350),
    "sigma@ (400,320)": (400, 320),
    "plane@ (250,140)": (250, 140),
    "plane@ (350,180)": (350, 180),
}
probes = {k: px[v] for k, v in samples.items()}

out = {"probes": probes}

# ---- card color masks (loose windows around measured cores) ----
# sample first, then define families from actual cores
def fam(c, tol=26):
    r, g, b = c
    return lambda p: abs(p[0] - r) < tol and abs(p[1] - g) < tol and abs(p[2] - b) < tol

fams = {}
for name, (x, y) in samples.items():
    c = px[x, y]
    fams[name] = fam(c)

# card staircase: scan column x=600 (frame) top->bottom, print color runs
def col_runs(x, y0=45, y1=516, q=14):
    prev = None; out = []
    for y in range(y0, y1):
        p = px[x, y]
        key = (p[0] // q, p[1] // q, p[2] // q)
        if key != prev:
            out.append((y, p)); prev = key
    return out

def compress(runs, minlen=5):
    rr = []
    for i, (y, p) in enumerate(runs):
        y2 = runs[i + 1][0] if i + 1 < len(runs) else 516
        if y2 - y >= minlen:
            rr.append((y, y2, p))
    return rr

out["col_x600_runs"] = compress(col_runs(600))
out["col_x760_runs"] = compress(col_runs(760))
out["col_x300_runs"] = compress(col_runs(300))
out["col_x200_runs"] = compress(col_runs(200))
out["col_x500_runs"] = compress(col_runs(500))

print(json.dumps(out, indent=1, default=str))
