#!/usr/bin/env python3
# debug3.py — row profiles in arrow bands, softmax text histogram, outline color,
# box border scan, green circle profile, cursor region.
from PIL import Image
import numpy as np

im = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_056.jpg").convert("RGB")
a = np.asarray(im).astype(int)
H, W = a.shape[:2]

def nonbg(band, tol=18):
    return (np.abs(band[..., 0] - 233) > tol) | (np.abs(band[..., 1] - 233) > tol) | (np.abs(band[..., 2] - 231) > tol)

def rowprofile(y0, y1, x0=150, x1=850, label=""):
    print(f"--- rows {y0}..{y1} {label}")
    for y in range(y0, y1):
        band = a[y:y+1, x0:x1]
        m = nonbg(band)
        n = int(m.sum())
        if n > 0:
            cols = band[0][m[0]]
            xs = np.nonzero(m[0])[0] + x0
            print(f"  y={y} n={n} x[{xs.min()}..{xs.max()}] mean={cols.mean(axis=0).round(0)}")

# blue arrows band (between pale row and softmax)
rowprofile(180, 226, label="blue-arrows")
# red arrows band (between softmax and green box)
rowprofile(262, 298, label="red-arrows")
# green arrows band (between green box and blue bar)
rowprofile(433, 463, 250, 700, label="green-arrows")

# softmax white text: column histogram of white-ish inside bar
bar = a[228:268, 170:826]
wm = (bar[..., 0] > 190) & (bar[..., 1] > 190) & (bar[..., 2] > 190)
colhit = wm.sum(axis=0)
xs = np.nonzero(colhit)[0]
print("softmax white cols:", xs.min() + 170, xs.max() + 170, "total", int(wm.sum()))
rows_hit = np.nonzero(wm.sum(axis=1))[0]
print("softmax white rows:", rows_hit.min() + 228, rows_hit.max() + 228)

# pale circle outline: darkest pixels in ring band around first circle (center 197? d~33 -> ring x 180..214)
reg = a[138:182, 178:218]
lum = reg.sum(axis=2)
yy, xx = np.unravel_index(np.argsort(lum, axis=None)[:30], lum.shape)
print("darkest ring colors:", [tuple(reg[y, x]) for y, x in yy[:8]])

# box border: scan with relaxed green (g-r>22) rows 292..302 and 428..438, cols 160..172 and 826..838
greenish = (a[..., 1] - a[..., 0] > 22) & (a[..., 1] - a[..., 2] > 15) & (a[..., 1] > 110)
for y in range(292, 303):
    n = int(greenish[y, 170:830].sum())
    if n: print(f"top border row y={y} n={n}", tuple(a[y, 400]))
for y in range(428, 439):
    n = int(greenish[y, 170:830].sum())
    if n: print(f"bottom border row y={y} n={n}", tuple(a[y, 400]))
for x in range(158, 172):
    n = int(greenish[305:430, x].sum())
    if n: print(f"left border col x={x} n={n}", tuple(a[370, x]))
for x in range(826, 840):
    n = int(greenish[305:430, x].sum())
    if n: print(f"right border col x={x} n={n}", tuple(a[370, x]))

# green circle col values at x=398
col = a[388:436, 398]
print("col x=398:", [(388 + i, tuple(col[i])) for i in range(0, 48, 2)])

# cursor region right of 'Block' (text ends x=609)
reg = a[460:500, 605:665]
m = nonbg(reg, 25)
ys, xs = np.nonzero(m)
print("cursor-region nonbg:", len(xs), "x", (xs.min() + 605, xs.max() + 605) if len(xs) else "-", "y", (ys.min() + 460, ys.max() + 460) if len(ys) else "-")
if len(xs):
    print("  mean color:", reg[ys, xs].mean(axis=0).round(0))
