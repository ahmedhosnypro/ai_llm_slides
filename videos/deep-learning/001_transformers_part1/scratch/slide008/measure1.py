#!/usr/bin/env python3
"""Measure slide_008.jpg delta geometry: blue callout, wait boxes, leaders, title line 2.
Frame: 960x540, 1px = 1pt, inches = px/72. Chrome + base diagram = parent slide 6 component.
"""
from PIL import Image
import json, collections

im = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_008.jpg").convert("RGB")
W, H = im.size
print("frame size:", W, H)
pxl = im.load()

def mode_of(region, mask_fn):
    c = collections.Counter()
    for y in range(region[1], region[3]):
        for x in range(region[0], region[2]):
            p = pxl[x, y]
            if mask_fn(p):
                c[(p[0]//8*8, p[1]//8*8, p[2]//8*8)] += 1
    return c.most_common(8)

def bbox_of(pred, x0, y0, x1, y1):
    minx, miny, maxx, maxy, n = 10**9, 10**9, -1, -1, 0
    for y in range(y0, y1):
        for x in range(x0, x1):
            if pred(pxl[x, y]):
                n += 1
                if x < minx: minx = x
                if x > maxx: maxx = x
                if y < miny: miny = y
                if y > maxy: maxy = y
    return (minx, miny, maxx, maxy, n) if n else None

# --- 1. light-blue fill mask: high blue, mid-high all channels, b >= r ---
def lightblue(p):
    r, g, b = p
    return b > 200 and b - r > 12 and g > 190 and r > 170

# scan left-middle band where callout+wait boxes live (x<480, y 150..320)
lb = bbox_of(lightblue, 0, 150, 480, 330)
print("lightblue all bbox (x<480, y150..330):", lb)

# row profile of light-blue ink to separate the 3 boxes
rows = []
for y in range(150, 330):
    cnt = sum(1 for x in range(0, 480) if lightblue(pxl[x, y]))
    rows.append((y, cnt))
# print transitions
prev = 0
for y, cnt in rows:
    if (prev < 5) != (cnt < 5):
        print(f"  y={y}: lightblue row count {prev} -> {cnt}")
    prev = cnt

# --- 2. per-box bboxes: find connected columns per row band ---
def col_profile(y0, y1):
    cols = []
    for x in range(0, 480):
        cnt = sum(1 for y in range(y0, y1) if lightblue(pxl[x, y]))
        cols.append((x, cnt))
    return cols

# --- 3. blue text mask (callout text + leaders): dark blue ---
def blueink(p):
    r, g, b = p
    return b > 110 and b - r > 40 and g < 140

# --- 4. title area: check for "(Challenges)" line under the red title ---
# parent title: y 54.5..84.5 pt. Look for blue ink in y 60..140, x 200..760
tb = bbox_of(blueink, 150, 60, 800, 150)
print("blue ink bbox in title band (x150..800, y60..150):", tb)
if tb:
    print("  title-band blue ink mode:", mode_of((tb[0], tb[1], tb[2]+1, tb[3]+1), blueink)[:4])

# red title ink bbox for reference
def redink(p):
    r, g, b = p
    return r > 120 and r - g > 60 and r - b > 60
tr = bbox_of(redink, 150, 40, 800, 100)
print("red title ink bbox (y40..100):", tr)

# --- 5. full-blue-ink inventory on the left half (leaders + callout text) ---
bb = bbox_of(blueink, 0, 140, 500, 330)
print("blue ink bbox left half (y140..330):", bb)

out = {"W": W, "H": H}
print(json.dumps(out))
