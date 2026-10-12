#!/usr/bin/env python3
"""Batch 1 measurements on ORIGINAL slide_037.jpg (frame space), mapped to slide space.
Mapping: slide_x=(fx-17.101)/0.962329 ; slide_y=(fy+0.224)/0.96053"""
from PIL import Image
from collections import Counter
import json

img = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_037.jpg").convert("RGB")
W,H = img.size
px = img.load()
AX, SX = 17.101, 0.962329
BY, SY = -0.224, 0.96053
def mx(fx): return round((fx-AX)/SX, 1)
def my(fy): return round((fy-BY)/SY, 1)

out = {}

# ---- TITLE: red ink bbox in band y50..100, x60..900
def is_red(p): r,g,b=p; return r>120 and (r-g)>60 and (r-b)>60
xs=[];ys=[]
for y in range(50,100):
    for x in range(60,900):
        if is_red(px[x,y]): xs.append(x); ys.append(y)
out["title_ink_frame_bbox"] = (min(xs),min(ys),max(xs),max(ys))
out["title_ink_slide_bbox"] = (mx(min(xs)),my(min(ys)),mx(max(xs)),my(max(ys)))
# row profile of red ink (to see line structure / cap heights)
rows = {}
for y in range(50,100):
    c = sum(1 for x in range(60,900) if is_red(px[x,y]))
    if c>0: rows[y]=c
out["title_red_rows"] = rows

# ---- LEGENDS absent? probe fills
def near(p,c,tol=25): return all(abs(p[i]-c[i])<=tol for i in range(3))
probes = {
 "legend1_fill(200,252,252)": ((150,110),(330,125)),
 "legend2_fill(156,160,160)": ((320,150),(500,165)),
 "legend3_fill(220,252,192)": ((275,188),(450,203)),
}
for name,((x0,y0),(x1,y1)) in probes.items():
    cnt=0; tot=0
    target = tuple(int(n) for n in name.split("(")[1][:-1].split(","))
    for y in range(y0,y1):
        for x in range(x0,x1):
            tot+=1
            if near(px[x,y],target): cnt+=1
    out[name] = f"{cnt}/{tot}"

# ---- LEFT INSET: green frame border
def is_green(p): r,g,b=p; return g>90 and (g-r)>40 and (g-b)>40
xs=[];ys=[]
for y in range(200,530):
    for x in range(40,215):
        if is_green(px[x,y]): xs.append(x);ys.append(y)
out["left_green_frame_bbox_frame"] = (min(xs),min(ys),max(xs),max(ys))
out["left_green_frame_bbox_slide"] = (mx(min(xs)),my(min(ys)),mx(max(xs)),my(max(ys)))
# green column profile: verticals
gcols = Counter(x for x,y in zip(xs,ys))
grows = Counter(y for x,y in zip(xs,ys))
out["left_green_tall_cols"] = sorted([x for x,c in gcols.items() if c>150])
out["left_green_wide_rows"] = sorted([y for y,c in grows.items() if c>80])

# ---- WHITE fill inside left inset: find white region extent
def is_white(p): r,g,b=p; return r>245 and g>245 and b>242
xs=[];ys=[]
for y in range(210,530):
    for x in range(45,215):
        if is_white(px[x,y]): xs.append(x);ys.append(y)
out["left_white_bbox_frame"] = (min(xs),min(ys),max(xs),max(ys))
out["left_white_bbox_slide"] = (mx(min(xs)),my(min(ys)),mx(max(xs)),my(max(ys)))

# ---- LEFT header red ink (above the frame, y200..270 frame)
xs=[];ys=[]
for y in range(195,275):
    for x in range(40,215):
        if is_red(px[x,y]): xs.append(x);ys.append(y)
if xs:
    out["left_header_ink_frame"] = (min(xs),min(ys),max(xs),max(ys))
    out["left_header_ink_slide"] = (mx(min(xs)),my(min(ys)),mx(max(xs)),my(max(ys)))

# ---- LEFT interior boxes: census of non-white colors inside inset
c = Counter()
for y in range(270,470):
    for x in range(60,190):
        p = px[x,y]
        if not is_white(p) and not is_green(p):
            c[(p[0]//8*8, p[1]//8*8, p[2]//8*8)] += 1
out["left_interior_top_colors"] = [[list(k),v] for k,v in c.most_common(14)]

print(json.dumps(out, indent=1, default=str))
