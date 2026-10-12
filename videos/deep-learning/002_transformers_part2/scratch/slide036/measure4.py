#!/usr/bin/env python3
"""Stage 4: focused profiles — box structure, arrows, dots, title, gutter, label rows."""
import numpy as np
from PIL import Image

FRAME = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_036.jpg"
im = np.asarray(Image.open(FRAME).convert("RGB")).astype(int)
H, W = im.shape[:2]

def colprof(x, y0, y1, step=1):
    print(f"--- col {x}, y {y0}..{y1}:")
    print(" ".join(f"{y}:{tuple(im[y,x])}" for y in range(y0, y1, step)))

# box 1 center col (Y box1 x 176..213 -> center 194)
colprof(194, 340, 396)
# box 1 center col X row
colprof(194, 455, 510)
# gap col between Y boxes 1 and 2 (x 300) — arrows?
colprof(300, 340, 396)
# arrow column test below banner (x 275 per earlier hit) rows 440..475
colprof(275, 440, 475)
# arrow column above banner? find dark-blue in rows 350..393 across x 150..860
db = (im[:,:,2] > 110) & (im[:,:,2] < 200) & (im[:,:,0] < 80) & (im[:,:,1] < 80)
sub = db[345:393, 150:860]
rows = sub.sum(axis=1)
print("\ndark-blue rows 345..392 (x150..860):", [(y+345, int(rows[y])) for y in range(len(rows)) if rows[y] > 10])
sub2 = db[445:500, 150:860]
rows2 = sub2.sum(axis=1)
print("dark-blue rows 445..499:", [(y+445, int(rows2[y])) for y in range(len(rows2)) if rows2[y] > 10])
# arrow columns in row 455 (below banner) and row 460
for yy in (450, 455, 460, 465):
    cols = np.where(db[yy, 150:860])[0] + 150
    if len(cols):
        runs, s, p = [], cols[0], cols[0]
        for x in cols[1:]:
            if x == p+1: p = x
            else: runs.append((s,p)); s=p=x
        runs.append((s,p))
        print(f"dark-blue col runs row {yy}:", runs)

# green dots: find them anywhere in diagram
grn = (im[:,:,1] > 140) & (im[:,:,0] < 130) & (im[:,:,2] < 130)
ys, xs = np.where(grn[440:520, :])
if len(ys):
    print("\ngreen px bbox: x", xs.min(), "..", xs.max(), " y", ys.min()+440, "..", ys.max()+440, "n=", len(ys))
    print("green sample:", [tuple(im[ys[i]+440, xs[i]]) for i in range(0, min(len(ys), 200), 40)])
else:
    print("\nNO green pixels in rows 440..520")

# blue dots (Y row) exact positions: dark blue in row band 360..372, x 580..720
dbd = (im[:,:,2] > 100) & (im[:,:,0] < 90) & (im[:,:,1] < 90)
ys, xs = np.where(dbd[355:375, 580:730])
if len(ys):
    print("Y dots bbox: x", xs.min()+580, "..", xs.max()+580, " y", ys.min()+355, "..", ys.max()+355)
    cols = sorted(set(xs))
    runs, s, p = [], cols[0], cols[0]
    for x in cols[1:]:
        if x <= p+2: p = x
        else: runs.append((s+580,p+580)); s=p=x
    runs.append((s+580,p+580))
    print("Y dot col runs:", runs)

# token labels: red ink rows within box1 x-range (176..213), rows 335..395
red = (im[:,:,0] > 110) & (im[:,:,1] < 110) & (im[:,:,2] < 110)
sub = red[330:396, 176:214]
rows = sub.sum(axis=1)
print("\nred rows in box1 x-range (y 330..395):", [(y+330, int(rows[y])) for y in range(len(rows)) if rows[y] > 0])
sub = red[440:510, 176:214]
rows = sub.sum(axis=1)
print("red rows in box1 x-range (y 440..510):", [(y+440, int(rows[y])) for y in range(len(rows)) if rows[y] > 0])

# title bbox excluding chrome: y 45..110, x 100..860
tsub = red[45:112, 100:860]
ys, xs = np.where(tsub)
print("\ntitle red bbox (excl chrome): x", xs.min()+100, "..", xs.max()+100, " y", ys.min()+45, "..", ys.max()+45)

# gutter labels precise: red in x 60..175, y 335..395 and y 440..500
for (y0,y1,tag) in ((335,395,"upper gutter"), (440,500,"lower gutter")):
    sub = red[y0:y1, 60:175]
    ys, xs = np.where(sub)
    if len(ys):
        print(f"{tag} red bbox: x {xs.min()+60}..{xs.max()+60}  y {ys.min()+y0}..{ys.max()+y0}")
        rows = sub.sum(axis=1)
        bands, inline = [], False
        for y in range(len(rows)):
            if rows[y] > 0 and not inline: st=y; inline=True
            elif rows[y] == 0 and inline: bands.append((st+y0, y-1+y0)); inline=False
        if inline: bands.append((st+y0, y1-1))
        print(f"   line bands: {bands}")

# info panel border cols/rows precise (blue border): dark blue rows 105..340, cols 95..865
db2 = (im[:,:,2] > 90) & (im[:,:,0] < 110) & (im[:,:,1] < 110)
sub = db2[105:340, :]
rows = sub.sum(axis=1)
print("\npanel border heavy rows (>300):", [(y+105, int(rows[y])) for y in range(len(rows)) if rows[y] > 300])
band = db2[112:332, :]
cols = band.sum(axis=0)
cc = [x for x in range(W) if cols[x] > 150]
print("panel border heavy cols (>150):", cc[:6], cc[-6:] if len(cc)>6 else cc)
# panel text line left/right extents per band
lines = [(119,129),(137,152),(156,167),(196,207),(215,228),(256,266),(274,289),(293,304),(312,327)]
for (a,bb) in lines:
    sub = db2[a:bb+1, 100:865]
    ys, xs = np.where(sub)
    if len(ys):
        print(f"line {a}..{bb}: x {xs.min()+100}..{xs.max()+100}")
# cream fill bounds precise
cream = (im[:,:,0] > 245) & (im[:,:,1] > 245) & (im[:,:,2] > 195) & (im[:,:,2] < 238)
fr = [y for y in range(H) if cream[y, 200:700].mean() > 0.5]
fc = [x for x in range(W) if cream[120:330, x].mean() > 0.5]
print("cream fill rows:", fr[0], "..", fr[-1], " cols:", fc[0], "..", fc[-1])
