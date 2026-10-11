#!/usr/bin/env python3
"""Phase 3: scanline profiles — find color bands precisely."""
from PIL import Image
import json

img = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_020.jpg").convert("RGB")
W, H = img.size
px = img.load()

def near(p, c, tol):
    return all(abs(p[i] - c[i]) <= tol for i in range(3))

def bands(color, tol, xmin, xmax, ymin=0, ymax=540, min_count=6, gap=2):
    """contiguous y bands where count of color px in [xmin,xmax] >= min_count"""
    counts = []
    for y in range(ymin, ymax):
        n = sum(1 for x in range(xmin, xmax) if near(px[x, y], color, tol))
        counts.append((y, n))
    out = []
    cur = None
    for y, n in counts:
        if n >= min_count:
            if cur and y <= cur[1] + gap:
                cur[1] = y; cur[2] = max(cur[2], n)
            else:
                if cur: out.append(cur)
                cur = [y, y, n]
    if cur: out.append(cur)
    return out

def colbands(color, tol, ymin, ymax, xmin=40, xmax=920, min_count=4, gap=2):
    counts = []
    for x in range(xmin, xmax):
        n = sum(1 for y in range(ymin, ymax) if near(px[x, y], color, tol))
        counts.append((x, n))
    out = []
    cur = None
    for x, n in counts:
        if n >= min_count:
            if cur and x <= cur[1] + gap:
                cur[1] = x; cur[2] = max(cur[2], n)
            else:
                if cur: out.append(cur)
                cur = [x, x, n]
    if cur: out.append(cur)
    return out

RED = (192, 0, 0)
DRED = (153, 0, 0)
GREEN = (0, 165, 80)
BLUE = (51, 51, 204)
ORANGE = (255, 165, 0)
GRAY = (140, 140, 140)

res = {}
res["red_bands"] = bands(RED, 60, 60, 900, 40, 500, 8)
res["darkred_bands"] = bands(DRED, 25, 60, 900, 260, 350, 60)
res["green_bands"] = bands(GREEN, 60, 60, 900, 120, 300, 8)
res["blue_bands"] = bands(BLUE, 60, 60, 900, 180, 500, 8)
res["orange_bands"] = bands(ORANGE, 55, 60, 900, 180, 300, 3)
res["green_inset"] = bands((0, 128, 0), 55, 30, 230, 380, 540, 3)

# for each red band print x-extent
for b in res["red_bands"]:
    y0, y1, _ = b
    bb = colbands(RED, 60, y0, y1 + 1, 40, 920, 2, 3)
    b.append(bb[:20] if len(bb) <= 20 else [bb[0], bb[1], f"...{len(bb)} cols", bb[-2], bb[-1]])

print(json.dumps(res, indent=1))
