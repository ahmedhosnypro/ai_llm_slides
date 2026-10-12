#!/usr/bin/env python3
"""Fine scans: left inset vertical strip, header red rows, center inset frame, right panel frame."""
from PIL import Image
from collections import Counter
import json

img = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_037.jpg").convert("RGB")
px = img.load()
AX, SX = 17.101, 0.962329
BY, SY = -0.224, 0.96053
def mx(fx): return round((fx-AX)/SX, 1)
def my(fy): return round((fy-BY)/SY, 1)
out = {}

# 1. vertical strip x=130 (mid left inset), y 200..525: print color changes
def scan_col(x, y0, y1, label):
    runs = []
    prev = None; start = y0
    for y in range(y0, y1):
        p = px[x, y]
        key = (p[0]//16*16, p[1]//16*16, p[2]//16*16)
        if key != prev:
            if prev is not None:
                runs.append((start, y-1, prev))
            prev = key; start = y
    runs.append((start, y1-1, prev))
    out[label] = [(a, b, list(c)) for a, b, c in runs if b-a >= 1]
scan_col(130, 200, 525, "left_strip_x130")

# 2. header red rows profile x40..215, y190..280
def is_red(p): r,g,b=p; return r>120 and (r-g)>60 and (r-b)>60
rows = {}
for y in range(190, 285):
    c = sum(1 for x in range(40, 215) if is_red(px[x, y]))
    if c: rows[y] = c
out["left_header_red_rows"] = rows

# 3. center inset green frame bbox
def is_green(p): r,g,b=p; return g>90 and (g-r)>40 and (g-b)>40
xs=[];ys=[]
for y in range(200,540):
    for x in range(285,530):
        if is_green(px[x,y]): xs.append(x);ys.append(y)
out["center_green_frame_bbox_frame"] = (min(xs),min(ys),max(xs),max(ys))
out["center_green_frame_bbox_slide"] = (mx(min(xs)),my(min(ys)),mx(max(xs)),my(max(ys)))
gcols = Counter(xs); grows = Counter(ys)
out["center_green_tall_cols"] = sorted([x for x,c in gcols.items() if c>150])
out["center_green_wide_rows"] = sorted([y for y,c in grows.items() if c>90])

# 4. right panel green frame bbox (x>540)
xs=[];ys=[]
for y in range(80,540):
    for x in range(530,960):
        if is_green(px[x,y]): xs.append(x);ys.append(y)
out["right_green_bbox_frame"] = (min(xs),min(ys),max(xs),max(ys))
out["right_green_bbox_slide"] = (mx(min(xs)),my(min(ys)),mx(max(xs)),my(max(ys)))
gcols = Counter(xs); grows = Counter(ys)
out["right_green_tall_cols"] = sorted([x for x,c in gcols.items() if c>250])
out["right_green_wide_rows"] = sorted([y for y,c in grows.items() if c>200])

# 5. center header red rows x285..530 y195..250
rows = {}
for y in range(195, 255):
    c = sum(1 for x in range(285, 530) if is_red(px[x, y]))
    if c: rows[y] = c
out["center_header_red_rows"] = rows

print(json.dumps(out, indent=0, default=str))
