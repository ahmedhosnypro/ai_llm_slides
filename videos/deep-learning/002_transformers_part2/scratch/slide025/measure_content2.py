#!/usr/bin/env python3
"""Content measurement v2: per-line bands, direct pixel samples, ring trace scan."""
from PIL import Image
import numpy as np

F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_025.jpg"
im = Image.open(F).convert("RGB")
a = np.asarray(im).astype(int)
H, W = a.shape[:2]
r, g, b = a[..., 0], a[..., 1], a[..., 2]

GRAY = np.array([234, 234, 234])

def bands_and_x(y0, y1, x0, x1, inkfn, minpix=2):
    """Find horizontal text-line bands in window; per band return x extent."""
    sub_ink = inkfn(y0, y1, x0, x1)
    rowc = sub_ink.sum(axis=1)
    bands = []
    inb = False
    for i, c in enumerate(rowc):
        if c >= minpix and not inb:
            s = i; inb = True
        elif c < minpix and inb:
            bands.append((y0 + s, y0 + i - 1)); inb = False
    if inb:
        bands.append((y0 + s, y0 + len(rowc) - 1))
    out = []
    for (bs, be) in bands:
        cols = sub_ink[bs - y0:be - y0 + 1].sum(axis=0)
        xs = np.nonzero(cols >= 1)[0]
        out.append((bs, be, x0 + int(xs.min()), x0 + int(xs.max())))
    return out

def ink_dark(y0, y1, x0, x1):
    sub = a[y0:y1, x0:x1]
    return (np.abs(sub - GRAY).max(axis=2) > 60)

def ink_red(y0, y1, x0, x1):
    sub = a[y0:y1, x0:x1]
    return (sub[...,0] - sub[...,1] > 60) & (sub[...,0] - sub[...,2] > 50) & (sub[...,0] > 110)

def ink_green(y0, y1, x0, x1):
    sub = a[y0:y1, x0:x1]
    return (sub[...,1] - sub[...,0] > 30) & (sub[...,1] - sub[...,2] > 20) & (sub[...,1] > 70)

def ink_blue(y0, y1, x0, x1):
    sub = a[y0:y1, x0:x1]
    return (sub[...,2] - sub[...,0] > 40) & (sub[...,2] - sub[...,1] > 30) & (sub[...,2] > 90)

print("== direct samples ==")
print("subtitle px @ (300,104):", tuple(a[104, 300]), " @ (500,104):", tuple(a[104, 500]))
print("title px @ (400,80):", tuple(a[80, 400]))
print("panel border row 171 x200:", tuple(a[171, 200]), " row 172:", tuple(a[172, 200]), " row 170:", tuple(a[170,200]))
print("right panel border row 141 x600:", tuple(a[141, 600]), "row 142:", tuple(a[142,600]), "row 143:", tuple(a[143,600]))
# scan left panel border rows at x=200
for row in range(166, 180):
    print(f"  Lborder row {row}: {tuple(a[row,200])}")

print("\n== title red bands ==")
print(bands_and_x(60, 95, 150, 800, ink_red))
print("== subtitle blue bands ==")
print(bands_and_x(90, 122, 150, 800, ink_blue))
print("== summary dark bands ==")
print(bands_and_x(395, 460, 120, 850, ink_dark))
print("== footer blue bands ==")
print(bands_and_x(460, 512, 60, 650, ink_blue))
print("== arrow red bbox ==")
ys, xs = np.nonzero(ink_red(205, 260, 320, 470))
print("arrow red:", (320+xs.min(), 205+ys.min(), 320+xs.max(), 205+ys.max()) if len(xs) else None)
print("== arrow label red bands ==")
print(bands_and_x(255, 320, 300, 470, ink_red))

print("\n== ring: red/green ink bbox in right panel ==")
ys, xs = np.nonzero(ink_red(150, 395, 450, 845))
print("red bbox:", (450+xs.min(), 150+ys.min(), 450+xs.max(), 150+ys.max()) if len(xs) else None)
ys, xs = np.nonzero(ink_green(150, 395, 450, 845))
print("green bbox:", (450+xs.min(), 150+ys.min(), 450+xs.max(), 150+ys.max()) if len(xs) else None)

# panel rects (green border): green ink bbox in left/right regions
print("\n== left panel green border ==")
ys, xs = np.nonzero(ink_green(150, 390, 80, 330))
print("left panel green bbox:", (80+xs.min(), 150+ys.min(), 80+xs.max(), 150+ys.max()) if len(xs) else None)
print("== right panel green border ==")
ys, xs = np.nonzero(ink_green(125, 400, 435, 855))
print("right panel green bbox:", (435+xs.min(), 125+ys.min(), 435+xs.max(), 125+ys.max()) if len(xs) else None)
