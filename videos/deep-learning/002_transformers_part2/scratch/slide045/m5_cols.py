#!/usr/bin/env python3
"""Slide 045 — numeric detection: bar boxes, label clusters, plus circles, dots, arrows."""
import numpy as np
from PIL import Image

F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_045.jpg"
img = np.asarray(Image.open(F).convert("RGB")).astype(int)
R, G, B = img[:, :, 0], img[:, :, 1], img[:, :, 2]
SX, OX = 0.962329, 17.582
SY, OY = 0.957576, -0.0909
def sx_(fx): return (fx - OX) / SX
def sy_(fy): return (fy - OY) / SY

def clusters(cols, gap=6):
    out = []
    if len(cols) == 0: return out
    s = p = cols[0]
    for c in cols[1:]:
        if c > p + gap: out.append((s, p)); s = c
        p = c
    out.append((s, p))
    return out

def rowbars(y0, y1, name):
    """bars = non-white, non-pale regions in band; label = dark-red text pixels."""
    band = img[y0:y1, 60:900]
    nonwhite = ~((R[y0:y1, 60:900] > 235) & (G[y0:y1, 60:900] > 235) & (B[y0:y1, 60:900] > 235))
    colsum = nonwhite.sum(axis=0)
    cols = np.where(colsum > (y1 - y0) * 0.5)[0]  # columns mostly covered = bar bodies
    cl = clusters(cols, gap=4)
    print(f"-- {name} band y{y0}..{y1}: {len(cl)} bar clusters")
    for a, b in cl:
        cx = (a + b) / 2 + 60
        print(f"   bar fx {a+60}..{b+60} w={b-a+1} cx={cx:.1f} -> slide cx {sx_(cx):.1f} w{(b-a+1)/SX:.1f}")
    # label text: dark red
    dred = (R[y0:y1, 60:900] > 100) & (R[y0:y1, 60:900] < 200) & (G[y0:y1, 60:900] < 60) & (B[y0:y1, 60:900] < 60)
    cols2 = np.where(dred.sum(axis=0) > 1)[0]
    cl2 = clusters(cols2, gap=5)
    print(f"   label clusters: {[round((a+b)/2+60,1) for a,b in cl2]}")

rowbars(478, 500, "X row")
rowbars(373, 398, "Y row C (container)")
rowbars(270, 294, "Y row B (mid)")
rowbars(163, 188, "Y row A (top)")

# plus circles: red ring ~990000 around white, band y 340..368
band_y = (340, 368)
ring = (R[band_y[0]:band_y[1], 60:900] > 120) & (R[band_y[0]:band_y[1], 60:900] < 190) & \
       (G[band_y[0]:band_y[1], 60:900] < 50) & (B[band_y[0]:band_y[1], 60:900] < 50)
colsum = ring.sum(axis=0)
cols = np.where(colsum >= 6)[0]
cl = clusters(cols, gap=8)
print("-- plus circles:", len(cl))
for a, b in cl:
    cx = (a + b) / 2 + 60
    seg = ring[:, a:b+1]
    ys = np.where(seg.any(axis=1))[0]
    print(f"   plus fx {a+60}..{b+60} cx={cx:.1f} y {ys.min()+band_y[0]}..{ys.max()+band_y[0]} -> slide cx {sx_(cx):.1f} cy {sy_((ys.min()+ys.max())/2+band_y[0]):.1f} d={(ys.max()-ys.min()+1)/SY:.1f}")

# dots rows: blue dots (row C right side), green dots (row D)
blue = (B > 130) & (R < 90) & (G < 90)
seg = blue[380:396, 480:660]
cols = np.where(seg.sum(axis=0) > 2)[0]
cl = clusters(cols, gap=4)
print("-- row C blue dots fx:", [round((a+b)/2+480,1) for a,b in cl], "-> slide", [round(sx_((a+b)/2+480),1) for a,b in cl])
ys = np.where(seg.any(axis=1))[0]
if len(ys): print("   dots y", ys.min()+380, ys.max()+380, "-> slide", round(sy_(ys.min()+380),1), round(sy_(ys.max()+380),1))
green = (G > 150) & (R < 120) & (B < 120)
seg = green[482:498, 480:660]
cols = np.where(seg.sum(axis=0) > 2)[0]
cl = clusters(cols, gap=4)
print("-- row D green dots fx:", [round((a+b)/2+480,1) for a,b in cl], "-> slide", [round(sx_((a+b)/2+480),1) for a,b in cl])
ys = np.where(seg.any(axis=1))[0]
if len(ys): print("   dots y", ys.min()+482, ys.max()+482, "-> slide", round(sy_(ys.min()+482),1), round(sy_(ys.max()+482),1))
# row A/B blue dots
for nm, (ya, yb) in [("A", (168, 184)), ("B", (274, 290))]:
    seg = blue[ya:yb, 480:660]
    cols = np.where(seg.sum(axis=0) > 2)[0]
    cl = clusters(cols, gap=4)
    ys = np.where(seg.any(axis=1))[0]
    print(f"-- row {nm} blue dots fx:", [round((a+b)/2+480,1) for a,b in cl], "y", (ys.min()+ya, ys.max()+ya) if len(ys) else None)
