#!/usr/bin/env python3
"""Measure slide_039 CONTENT: line segmentation of all ink between chrome borders,
color classification per line, box border detection. Mapping (from m1):
frame_x = 18.63 + 0.96123*slide_x ; frame_y = 0.95556*slide_y
slide_x = (frame_x-18.63)/0.96123 ; slide_y = frame_y/0.95556"""
from PIL import Image
import json

SRC = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_039.jpg"
img = Image.open(SRC).convert("RGB")
W, H = img.size
px = img.load()

SH, DH = 0.96123, 18.63
SV, DV = 0.95556, 0.0
def to_slide(fx, fy):
    return ((fx - DH) / SH, (fy - DV) / SV)

def ink(p):
    r, g, b = p
    return sum(p) < 640  # anything clearly darker than bg

def classify(p):
    r, g, b = p
    if r > 120 and r - g > 50 and r - b > 50: return "red"
    if b > 110 and b - r > 60 and b - g > 40: return "blue"
    if sum(p) < 260: return "black"
    return "?"

# content area inside chrome border: x 62..899, y 47..513
X0, X1, Y0, Y1 = 62, 899, 47, 513

# per-row ink profile
rowprof = {}
for y in range(Y0, Y1 + 1):
    xs = [x for x in range(X0, X1 + 1) if ink(px[x, y])]
    if xs:
        rowprof[y] = (min(xs), max(xs), len(xs))

# segment rows into bands separated by >=2 empty rows
bands = []
cur = None
for y in sorted(rowprof):
    if cur and y <= cur[1] + 2:
        cur[1] = y
        cur[2].append(y)
    else:
        if cur: bands.append(cur)
        cur = [y, y, [y]]
if cur: bands.append(cur)

# split wide bands into text lines when a nearly-empty row row exists inside
# (nearly-empty = <3 ink px); then report each line's bbox + dominant colors
lines = []
for y0, y1, ys in bands:
    # find sub-splits within band on <3-ink rows
    seg = []
    run = [ys[0], ys[0]]
    for y in ys[1:]:
        if y <= run[1] + 1:
            run[1] = y
        else:
            seg.append(tuple(run)); run = [y, y]
    seg.append(tuple(run))
    # merge segments separated by tiny gaps (<2 rows) that have overlapping x
    merged = []
    for s in seg:
        if merged and s[0] - merged[-1][1] <= 1:
            merged[-1] = (merged[-1][0], s[1])
        else:
            merged.append(list(s))
    for y0s, y1s in merged:
        xs = [x for y in range(y0s, y1s + 1) for x in range(X0, X1 + 1) if ink(px[x, y])]
        if not xs: continue
        x0, x1 = min(xs), max(xs)
        colors = {}
        for y in range(y0s, y1s + 1):
            for x in range(x0, x1 + 1):
                p = px[x, y]
                if ink(p):
                    c = classify(p)
                    if c != "?": colors[c] = colors.get(c, 0) + 1
        tot = sum(colors.values()) or 1
        colstr = ",".join(f"{c}:{round(100*v/tot)}%" for c, v in sorted(colors.items(), key=lambda kv: -kv[1]))
        sx0, sy0 = to_slide(x0, y0s); sx1, sy1 = to_slide(x1, y1s)
        lines.append({
            "frame": [x0, y0s, x1, y1s], "h": y1s - y0s + 1,
            "slide": [round(sx0, 1), round(sy0, 1), round(sx1, 1), round(sy1, 1)],
            "slide_h": round(sy1 - sy0, 1),
            "colors": colstr,
        })

out = {"lines": lines}
print(json.dumps(out, indent=1))
