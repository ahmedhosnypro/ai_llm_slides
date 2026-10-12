#!/usr/bin/env python3
"""Remaining element measurements for slide_025.jpg."""
from PIL import Image
import numpy as np

F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_025.jpg"
im = Image.open(F).convert("RGB")
a = np.asarray(im).astype(int)
r, g, b = a[..., 0], a[..., 1], a[..., 2]

GRAY = np.array([234, 234, 234])
WHITE = np.array([255, 255, 255])

def ink(y0, y1, x0, x1, bg=GRAY, tol=50):
    sub = a[y0:y1, x0:x1]
    return (np.abs(sub - np.array(bg)).max(axis=2) > tol)

def redm(y0, y1, x0, x1):
    sub = a[y0:y1, x0:x1]
    return (sub[...,0] - sub[...,1] > 60) & (sub[...,0] - sub[...,2] > 50) & (sub[...,0] > 110)

def greenm(y0, y1, x0, x1):
    sub = a[y0:y1, x0:x1]
    return (sub[...,1] - sub[...,0] > 30) & (sub[...,1] - sub[...,2] > 20) & (sub[...,1] > 70)

def tanm(y0, y1, x0, x1):
    sub = a[y0:y1, x0:x1]
    return (sub[...,0] > 200) & (sub[...,1] > 165) & (sub[...,1] < 225) & (sub[...,2] > 120) & (sub[...,2] < 200) & (sub[...,0] - sub[...,2] > 40)

def bands(y0, y1, x0, x1, maskfn, minpix=2, gap=1):
    m = maskfn(y0, y1, x0, x1)
    rowc = m.sum(axis=1)
    out, inb, s = [], False, 0
    for i, c in enumerate(rowc):
        if c >= minpix and not inb: s, inb = i, True
        elif c <= gap - 1 and inb:
            out.append((y0 + s, y0 + i - 1)); inb = False
    if inb: out.append((y0 + s, y0 + len(rowc) - 1))
    res = []
    for (bs, be) in out:
        cols = m[bs - y0:be - y0 + 1].sum(axis=0)
        xs = np.nonzero(cols >= 1)[0]
        res.append((bs, be, x0 + int(xs.min()), x0 + int(xs.max())))
    return res

print("== Rotation direction + CCW/CW (dark ink, window top of right panel) ==")
print(bands(180, 245, 480, 700, lambda y0,y1,x0,x1: ink(y0,y1,x0,x1,GRAY,60)))
print("== curved arrow above Rotation direction (dark ink) ==")
print(bands(165, 195, 500, 690, lambda y0,y1,x0,x1: ink(y0,y1,x0,x1,GRAY,60)))
print("== cos red label ==")
print(bands(190, 225, 700, 800, redm))
print("== sin green label ==")
print(bands(215, 250, 700, 800, greenm))
print("== Line count + parenthetical (dark) ==")
print(bands(275, 340, 540, 720, lambda y0,y1,x0,x1: ink(y0,y1,x0,x1,GRAY,60)))
print("== Sin/Cos signal period label (dark) ==")
print(bands(255, 295, 715, 830, lambda y0,y1,x0,x1: ink(y0,y1,x0,x1,GRAY,60)))
print("== period double-arrow (dark, right edge) ==")
print(bands(230, 300, 800, 832, lambda y0,y1,x0,x1: ink(y0,y1,x0,x1,GRAY,60)))

print("== tan callout bbox ==")
ys, xs = np.nonzero(tanm(290, 380, 100, 320))
print("tan bbox:", (100+xs.min(), 290+ys.min(), 100+xs.max(), 290+ys.max()) if len(xs) else None)
print("== callout dark-red text bands (window = tan bbox) ==")
print(bands(300, 370, 110, 250, lambda y0,y1,x0,x1: redm(y0,y1,x0,x1)))
print("== AC Motor label (dark ink, right of motor) ==")
print(bands(195, 240, 205, 310, lambda y0,y1,x0,x1: ink(y0,y1,x0,x1,WHITE,60)))

# motor art: non-white, non-tan ink inside left panel excluding callout and label
print("== motor art bbox (ink on white, excluding tan+label window) ==")
m = ink(160, 380, 95, 315, WHITE, 50)
# zero out callout region and label region and panel border rows/cols
m[300-160:380-160, 100-95:250-95] = False   # callout area (rough)
m[190-160:245-160, 205-95:315-95] = False   # label area (rough)
m[:14, :] = False; m[-6:, :] = False; m[:, :10] = False; m[:, -14:] = False
ys, xs = np.nonzero(m)
print("motor art bbox:", (95+xs.min(), 160+ys.min(), 95+xs.max(), 160+ys.max()) if len(xs) else None)

print("== hub circle: white disk near (600,266) ==")
wm = (r > 243) & (g > 243) & (b > 243)
# search white blob 30px around (605,266): white pixels bounded by gray ring
ys, xs = np.nonzero(wm[250:285, 585:625])
if len(xs):
    print("hub white bbox:", (585+xs.min(), 250+ys.min(), 585+xs.max(), 250+ys.max()), "count", len(xs))

print("== gray hub ring: gray stroke pixels around hub ==")
gm = (np.abs(r-g)<25) & (np.abs(g-b)<25) & (r>110) & (r<215)
ys, xs = np.nonzero(gm[248:290, 580:630])
if len(xs):
    print("hub ring gray bbox:", (580+xs.min(), 248+ys.min(), 580+xs.max(), 248+ys.max()), "count", len(xs))

print("== right panel border bbox (green long runs) ==")
gm2 = greenm(130, 400, 440, 845)
# horizontal border rows: rows where green count > 200
rowc = gm2.sum(axis=1)
for i, c in enumerate(rowc):
    if c > 150: print("  green-heavy row:", 130+i, c)
colc = gm2.sum(axis=0)
for j, c in enumerate(colc):
    if c > 80: print("  green-heavy col:", 440+j, c)
