#!/usr/bin/env python3
"""Slide 045 — content geometry: bands, boxes, colors (frame px -> slide pts)."""
import numpy as np
from PIL import Image

F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_045.jpg"
img = np.asarray(Image.open(F).convert("RGB")).astype(int)
H, W, _ = img.shape
R, G, B = img[:, :, 0], img[:, :, 1], img[:, :, 2]

SX, OX = 0.962329, 17.582
SY, OY = 0.957576, -0.0909
def sx_(fx): return (fx - OX) / SX
def sy_(fy): return (fy - OY) / SY
def band(name, x0, x1, y0, y1):
    print(f"{name}: frame x {x0}..{x1} y {y0}..{y1} -> slide x {sx_(x0):.1f}..{sx_(x1):.1f} y {sy_(y0):.1f}..{sy_(y1):.1f}")

# 1) title red ink rows 50..85, x 200..760
red = (R > 140) & (G < 80) & (B < 80)
seg = red[50:85, 150:800]
rows = np.where(seg.any(axis=1))[0]; cols = np.where(seg.any(axis=0))[0]
band("title ink", cols.min()+150, cols.max()+150, rows.min()+50, rows.max()+50)

# 2) annotation box: yellow fill FFFFCC-ish + blue border
yel2 = (R > 230) & (G > 230) & (B > 170) & (B < 225)  # FFFFCC fill
seg = yel2[60:160, 60:900]
rows = np.where(seg.sum(axis=1) > 200)[0]; cols = np.where(seg.sum(axis=0) > 30)[0]
band("annot box yellow fill", cols.min()+60, cols.max()+60, rows.min()+60, rows.max()+60)
blue = (B > 120) & (R < 110) & (G < 110)
seg2 = blue[60:160, 60:900]
rows2 = np.where(seg2.any(axis=1))[0]; cols2 = np.where(seg2.any(axis=0))[0]
print("annot blue ink bbox:", cols2.min()+60, cols2.max()+60, rows2.min()+60, rows2.max()+60)

# 3) diagram panel blue border: long blue horizontal lines below y=150
for y in range(150, 200):
    row = blue[y, 70:890]
    if row.mean() > 0.7:
        print("panel top long blue row:", y, f"frac={row.mean():.2f}", tuple(img[y, 400])); break
for y in range(516, 460, -1):
    row = blue[y, 70:890]
    if row.mean() > 0.7:
        print("panel bottom long blue row:", y, f"frac={row.mean():.2f}", tuple(img[y, 400])); break
# panel left/right long blue verticals
for x in range(58, 90):
    col = blue[160:500, x]
    if col.mean() > 0.7:
        print("panel left long blue col:", x, f"frac={col.mean():.2f}", tuple(img[300, x])); break
for x in range(901, 870, -1):
    col = blue[160:500, x]
    if col.mean() > 0.7:
        print("panel right long blue col:", x, f"frac={col.mean():.2f}", tuple(img[300, x])); break

# 4) vector stack rows: pink F4B8C4-ish cells
pink = (np.abs(R-244)<35)&(np.abs(G-184)<40)&(np.abs(B-196)<40)
seg = pink[150:520, 60:900]
rowsum = seg.sum(axis=1)
ys = np.where(rowsum > 30)[0]
if len(ys):
    # split into bands
    bands = []
    start = ys[0]
    for i in range(1, len(ys)):
        if ys[i] != ys[i-1]+1:
            bands.append((start+150, ys[i-1]+150)); start = ys[i]
    bands.append((start+150, ys[-1]+150))
    print("pink-cell row bands (frame y):", bands)
    for b in bands:
        if b[1]-b[0] > 5:
            seg2 = pink[b[0]:b[1]+1, 60:900]
            cs = np.where(seg2.any(axis=0))[0]
            print(f"  band y{b}: x {cs.min()+60}..{cs.max()+60} -> slide x {sx_(cs.min()+60):.1f}..{sx_(cs.max()+60):.1f} y {sy_(b[0]):.1f}..{sy_(b[1]):.1f}")

# 5) navy MHSA block: dark navy fill 00008B
navy = (R < 60) & (G < 60) & (B > 100)
seg = navy[380:470, 60:900]
rows = np.where(seg.sum(axis=1) > 200)[0]
if len(rows):
    y0, y1 = rows.min()+380, rows.max()+380
    cols = np.where(seg[(rows[len(rows)//2])].any(axis=0))[0] if False else np.where(seg.sum(axis=0) > 10)[0]
    band("navy block", cols.min()+60, cols.max()+60, y0, y1)

# 6) plus circles: dark red filled circles (990000)
dred = (R > 110) & (R < 190) & (G < 40) & (B < 40)
seg = dred[330:380, 100:880]
rows = np.where(seg.sum(axis=1) > 8)[0]
if len(rows):
    y0, y1 = rows.min()+330, rows.max()+330
    cols = np.where(seg.sum(axis=0) > 2)[0]
    # cluster cols
    cl = []
    s = cols[0]; p = cols[0]
    for c in cols[1:]:
        if c > p + 5: cl.append((s, p)); s = c
        p = c
    cl.append((s, p))
    print("plus row y", y0, y1, "centers frame:", [round((a+b)/2,1) for a,b in cl])
    print("plus row -> slide y", round(sy_(y0),1), round(sy_(y1),1), "centers:", [round(sx_((a+b)/2),1) for a,b in cl])

# 7) gray LayerNorm bar D9D9D9
gray = (np.abs(R-217)<18)&(np.abs(G-217)<18)&(np.abs(B-217)<18)
seg = gray[290:340, 100:880]
rows = np.where(seg.sum(axis=1) > 300)[0]
if len(rows):
    y0, y1 = rows.min()+290, rows.max()+290
    cols = np.where(seg[(rows[len(rows)//2])])[0]
    band("gray bar", cols.min()+100, cols.max()+100, y0, y1)

# 8) green dashed container: light green fill E2EFDA + dashed border 00B050
grnfill = (np.abs(R-226)<14)&(np.abs(G-239)<12)&(np.abs(B-218)<14)
seg = grnfill[280:380, 60:900]
rows = np.where(seg.sum(axis=1) > 150)[0]
if len(rows):
    band("container green fill", 0, 0, rows.min()+280, rows.max()+280)
grnline = (G > 130) & (R < 110) & (B < 130) & (G-R > 40)
seg = grnline[280:390, 60:900]
rows = np.where(seg.any(axis=1))[0]; cols = np.where(seg.any(axis=0))[0]
if len(rows): print("green line ink bbox:", cols.min()+60, cols.max()+60, rows.min()+280, rows.max()+280)

# 9) orange curves
orange = (R > 200) & (G > 120) & (G < 200) & (B < 110)
seg = orange[330:510, 60:900]
rows = np.where(seg.sum(axis=1) > 3)[0]
if len(rows): print("orange ink rows frame:", rows.min()+330, rows.max()+330, "-> slide", round(sy_(rows.min()+330),1), round(sy_(rows.max()+330),1))

# 10) caption yellow FFFF00 highlight at bottom
yel3 = (R > 230) & (G > 230) & (B < 90)
seg = yel3[480:516, 60:900]
rows = np.where(seg.sum(axis=1) > 50)[0]; cols = np.where(seg.sum(axis=0) > 10)[0]
if len(rows): band("caption highlight", cols.min()+60, cols.max()+60, rows.min()+480, rows.max()+480)

# 11) FFN box: blue border around 170..250
seg = blue[160:260, 60:900]
rows = np.where(seg.sum(axis=1) > 400)[0]
print("FFN box long blue rows:", [r+160 for r in rows])
for x in range(60, 900):
    col = blue[170:250, x]
    if col.mean() > 0.7:
        print("FFN left long blue col:", x); break
for x in range(900, 60, -1):
    col = blue[170:250, x]
    if col.mean() > 0.7:
        print("FFN right long blue col:", x); break
