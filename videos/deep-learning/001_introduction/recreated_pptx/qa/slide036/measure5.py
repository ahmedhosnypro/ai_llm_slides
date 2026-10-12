#!/usr/bin/env python3
# measure5.py — final pre-build measurements for slide 036 (960x540, 1px=1pt).
# Focus: content-box border, =/+ signs, neuron, arrow-to-neuron, question/equation
# color-separated rows, black strip, and crop-edge safety for planned asset crops.
from PIL import Image
import numpy as np

FR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_036.jpg"
im = np.array(Image.open(FR).convert("RGB")).astype(int)
H, W = im.shape[:2]
print(f"frame {W}x{H}")

def runs(mask_row):
    idx = np.where(mask_row)[0]
    return (idx.min(), idx.max(), len(idx)) if len(idx) else None

# ---- 1. content box red border ----
red = (im[:, :, 0] > 130) & (im[:, :, 1] < 80) & (im[:, :, 2] < 80)
print("\n== content-box border: rows with >300 red px in x 100..900, y 130..520 ==")
for y in range(130, 521):
    r = runs(red[y, 100:900])
    if r and r[2] > 300:
        print(f"  row y={y}: x {r[0]+100}..{r[1]+100} n={r[2]}")
print("== cols with >150 red px in y 140..520 ==")
for x in range(100, 901):
    c = runs(red[140:520, x])
    if c and c[2] > 150:
        print(f"  col x={x}: y {c[0]+140}..{c[1]+140} n={c[2]}")

# ---- 2. '=' sign (cyan-ish, region x 495..550 y 270..320) ----
print("\n== '=' sign region 495..550 x 270..320: non-white px ==")
reg = im[270:320, 495:550]
nw = (np.abs(reg - reg.mean(axis=2, keepdims=True)).max(axis=2) > 30) | (reg.mean(axis=2) < 215)
for yy in range(nw.shape[0]):
    r = runs(nw[yy])
    if r and r[2] > 3:
        px = im[270 + yy, 495 + r[0]:495 + r[1] + 1]
        print(f"  y={270+yy}: x {r[0]+495}..{r[1]+495} n={r[2]} modal={px.reshape(-1,3)[np.argsort(-((px[:,0].astype(int)+px[:,1]+px[:,2]))%7)][:1]}")
# modal core of bars
bars = im[288:305, 505:540].reshape(-1, 3)
bars = bars[(bars[:, 2] > bars[:, 0] + 40)]  # blue-dominant
if len(bars):
    from collections import Counter
    print("  = bar modal:", Counter(map(tuple, bars)).most_common(4))

# ---- 3. '+' sign (gray, region x 540..585 y 285..330) ----
print("\n== '+' gray (140<lum<215, low chroma) x 540..585 y 285..330 ==")
reg = im[285:330, 540:585]
lum = reg.mean(axis=2)
chroma = reg.max(axis=2) - reg.min(axis=2)
g = (lum > 140) & (lum < 218) & (chroma < 25)
for yy in range(g.shape[0]):
    r = runs(g[yy])
    if r and r[2] > 1:
        print(f"  y={285+yy}: x {r[0]+540}..{r[1]+540} n={r[2]}")
gr = reg[g]
if len(gr):
    from collections import Counter
    print("  + modal:", Counter(map(tuple, gr)).most_common(3))

# ---- 4. neuron ----
print("\n== neuron: orange ring x 560..625 y 270..320 ==")
reg = im[270:320, 560:625]
o = (reg[:, :, 0] > 170) & (reg[:, :, 1] > 90) & (reg[:, :, 1] < 180) & (reg[:, :, 2] < 90)
ys, xs = np.where(o)
if len(ys):
    print(f"  ring bbox: x {xs.min()+560}..{xs.max()+560} y {ys.min()+270}..{ys.max()+270}")
cy = (reg[:, :, 2] > 180) & (reg[:, :, 0] < 120) & (reg[:, :, 1] > 140)
ys2, xs2 = np.where(cy)
if len(ys2):
    print(f"  cyan-center bbox: x {xs2.min()+560}..{xs2.max()+560} y {ys2.min()+270}..{ys2.max()+270}")
from collections import Counter
print("  center modal:", Counter(map(tuple, reg[cy])).most_common(3))
print("  ring modal:", Counter(map(tuple, reg[o])).most_common(3))

# ---- 5. arrow-to-neuron (dark ink x 595..700, y 312..408) ----
print("\n== arrow-to-neuron dark px (lum<120) x 595..700 y 312..408, per-row ==")
reg = im[312:409, 595:700]
d = reg.mean(axis=2) < 120
for yy in range(d.shape[0]):
    r = runs(d[yy])
    if r:
        print(f"  y={312+yy}: x {r[0]+595}..{r[1]+595} n={r[2]}")

# ---- 6. equation RED rows (r>150, g<95) x 300..620 y 435..505 ----
print("\n== equation red rows x 300..620 y 435..505 ==")
reg = im[435:505, 300:620]
er = (reg[:, :, 0] > 140) & (reg[:, :, 1] < 95) & (reg[:, :, 2] < 95)
for yy in range(er.shape[0]):
    r = runs(er[yy])
    if r and r[2] > 2:
        print(f"  y={435+yy}: x {r[0]+300}..{r[1]+300} n={r[2]}")
ys3, xs3 = np.where(er)
if len(ys3):
    print(f"  eq red bbox: x {xs3.min()+300}..{xs3.max()+300} y {ys3.min()+435}..{ys3.max()+435}")
    print("  eq core modal:", Counter(map(tuple, reg[er])).most_common(4))

# ---- 7. question BLACK rows x 140..810 y 400..460 ----
print("\n== question black rows (lum<90) x 140..810 y 400..462 ==")
reg = im[400:462, 140:810]
qb = reg.mean(axis=2) < 90
ys4, xs4 = np.where(qb)
if len(ys4):
    print(f"  question bbox: x {xs4.min()+140}..{xs4.max()+140} y {ys4.min()+400}..{ys4.max()+400}")

# ---- 8. black strip bottom ----
print("\n== bottom strip rows (lum<60, full width) y 505..540 ==")
for y in range(505, 540):
    r = runs(im[y].mean(axis=1) < 60)
    if r and r[2] > 700:
        print(f"  y={y}: n={r[2]}")

# ---- 9. crop-edge safety ----
def edge_report(name, x1, y1, x2, y2):
    print(f"\n== crop {name}: box x {x1}..{x2} y {y1}..{y2} (w={x2-x1+1}, h={y2-y1+1}) ==")
    bg = lambda p: abs(p[0]-p[1]) < 26 and abs(p[1]-p[2]) < 26 and p.mean() > 205
    for label, coords in [
        ("top edge y-1", [(x, y1-1) for x in range(x1, x2+1)]),
        ("bottom edge y+1", [(x, y2+1) for x in range(x1, x2+1)]),
        ("left edge x-1", [(x1-1, y) for y in range(y1, y2+1)]),
        ("right edge x+1", [(x2+1, y) for y in range(y1, y2+1)]),
    ]:
        ink = [(x, y, tuple(im[y, x])) for x, y in coords if not bg(im[y, x])]
        print(f"  {label}: {len(ink)} non-bg px" + (f" e.g. {ink[:6]}" if ink else ""))

edge_report("A slabtop", 158, 153, 402, 219)
edge_report("B slabbody", 158, 219, 380, 394)
edge_report("C filterunit", 378, 240, 499, 409)

# ---- 10. title lines precise ----
print("\n== title red ink rows (r>120, g<70) y 50..140 x 100..860 ==")
reg = im[50:140, 100:860]
tr = (reg[:, :, 0] > 120) & (reg[:, :, 1] < 70) & (reg[:, :, 2] < 70)
rowsum = tr.sum(axis=1)
lines = []
inl = False
for i, n in enumerate(rowsum):
    if n > 2 and not inl:
        start = i; inl = True
    elif n <= 2 and inl:
        lines.append((50 + start, 50 + i - 1)); inl = False
if inl:
    lines.append((50 + start, 50 + len(rowsum) - 1))
for (a, b) in lines:
    band = tr[a-50:b-50+1]
    xs = np.where(band.any(axis=0))[0]
    print(f"  line y {a}..{b}: x {xs.min()+100}..{xs.max()+100}")
print("  title core modal:", Counter(map(tuple, reg[tr])).most_common(3))

# ---- 11. chrome edges ----
print("\n== chrome: sample colors ==")
print("  (10,10) canvas:", tuple(im[10, 10]), " (30,480) above panel:", tuple(im[30, 480]))
print("  (300,60) panel:", tuple(im[300, 60]), " (300,900) panel:", tuple(im[300, 900]))
print("  (480,50) col50:", tuple(im[480, 50]), " (480,919):", tuple(im[480, 919]))

# ---- 12. dash bands reference ----
print("\n== dash band y-centers in gap x 390..410 (cyan-dominant) ==")
reg = im[240:340, 390:410]
cy2 = (reg[:, :, 2] > reg[:, :, 0] + 30) & (reg[:, :, 2] > 150)
rowsum = cy2.sum(axis=1)
bands = []
inb = False
for i, n in enumerate(rowsum):
    if n > 2 and not inb:
        s = i; inb = True
    elif n <= 2 and inb:
        bands.append((240 + s, 240 + i - 1)); inb = False
if inb:
    bands.append((240 + s, 240 + len(rowsum) - 1))
print("  bands:", bands)
print("  dash modal:", Counter(map(tuple, reg[cy2])).most_common(3))
