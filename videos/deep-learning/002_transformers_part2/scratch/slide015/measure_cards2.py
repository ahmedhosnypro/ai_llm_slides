#!/usr/bin/env python3
"""Round 2: precise card masks + key structure bboxes in frame coords.
Fills calibrated from probes: salmon (241,139,150), lavender (199,192,244),
peach (245,222,200), mint/green-card (229,253,230), sage (189,227,197),
yellow-dimmed target around (205,205,140) bright (237,232,127),
orange ellipse (243,129,75), green ellipse (130,214,139).
Reports per-color row/col extents -> card quads; plus targeted bboxes.
"""
from PIL import Image
import json

img = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_015.jpg").convert("RGB")
W, H = img.size
px = img.load()

def near(p, c, tol):
    return abs(p[0]-c[0]) <= tol and abs(p[1]-c[1]) <= tol and abs(p[2]-c[2]) <= tol

FILLS = {
    "salmon": ((241, 139, 150), 22),
    "lavender": ((199, 192, 244), 20),
    "peach": ((245, 222, 200), 18),
    "mintcard": ((231, 254, 230), 14),
    "sage": ((189, 227, 197), 16),
    "yellow": ((236, 231, 130), 30),
    "orange": ((243, 129, 75), 26),
    "greenell": ((130, 214, 139), 30),
}

out = {}
for name, (c, tol) in FILLS.items():
    pts = [(x, y) for y in range(45, 516) for x in range(60, 900) if near(px[x, y], c, tol)]
    if not pts:
        out[name] = None
        continue
    bb = (min(p[0] for p in pts), min(p[1] for p in pts), max(p[0] for p in pts), max(p[1] for p in pts))
    # row extents at a few rows to see shape (left/right edges per y)
    rows = {}
    for (x, y) in pts:
        r = rows.setdefault(y, [x, x])
        r[0] = min(r[0], x); r[1] = max(r[1], x)
    ys = sorted(rows)
    prof = {str(y): rows[y] for y in ys[:: max(1, len(ys) // 14)]}
    out[name] = {"bbox": bb, "count": len(pts), "row_profile": prof}

print(json.dumps(out, indent=1))
