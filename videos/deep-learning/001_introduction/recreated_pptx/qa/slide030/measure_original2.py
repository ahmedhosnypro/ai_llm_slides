#!/usr/bin/env python3
"""Pass 2: precise structure of slide 030 original."""
import numpy as np
from PIL import Image

im = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_030.jpg").convert("RGB")
a = np.asarray(im).astype(int)
H, W = a.shape[:2]
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]
lum = 0.299 * R + 0.587 * G + 0.114 * B
red = (R > 130) & (G < 90) & (B < 90)
dark = lum < 90

def runs(mask_1d, min_len=3):
    """contiguous True runs in 1d mask"""
    idx = np.where(mask_1d)[0]
    if len(idx) == 0:
        return []
    out = []
    s = p = idx[0]
    for i in idx[1:]:
        if i - p > 1:
            if p - s + 1 >= min_len: out.append((int(s), int(p)))
            s = i
        p = i
    if p - s + 1 >= min_len: out.append((int(s), int(p)))
    return out

print("=== title glyph rows (red, y<130) ===")
t = red.copy(); t[130:, :] = False
print("  row runs:", runs(t.sum(axis=1) > 0))
print("  col extent:", runs(t.sum(axis=0) > 0, 1)[:3], "...", runs(t.sum(axis=0) > 0, 1)[-3:])
# cap height: use column of letter 'A' (first glyph ~x117)
sub = t[:, 117:180]
print("  'Ap' region row runs:", runs(sub.sum(axis=1) > 0))

print("\n=== left panel red border ===")
# vertical strip x84-88: extent
strip = red[:, 84:89]
print("  rows with red in x84-88:", runs(strip.sum(axis=1) > 0))
# find horizontal red runs in y470..485 (bottom border?)
for y in range(470, 486):
    r = runs(red[y, :], 20)
    if r: print(f"  y={y} red col runs:", r)

print("\n=== right panel red border ===")
strip = red[:, 477:482]
print("  rows red x477-481:", runs(strip.sum(axis=1) > 0))
strip = red[:, 883:887]
print("  rows red x883-886:", runs(strip.sum(axis=1) > 0))
for y in list(range(95, 112)) + list(range(440, 452)):
    r = runs(red[y, 400:], 20)
    if r: print(f"  y={y} red col runs (x>400):", r)

print("\n=== panel top borders: horizontal red runs y in 95..250 (left half x80..475) ===")
for y in range(95, 255):
    r = runs(red[y, 80:475], 40)
    if r: print(f"  y={y}:", r)

print("\n=== arrow region: red x455..545, y300..430 ===")
ar = red.copy(); ar[:, :455] = False; ar[:, 545:] = False; ar[:300, :] = False; ar[430:, :] = False
ys, xs = np.where(ar)
if len(xs):
    print(f"  arrow red bbox x[{xs.min()}..{xs.max()}] y[{ys.min()}..{ys.max()}]")
    for y in range(ys.min(), ys.max() + 1, 3):
        r = runs(ar[y, :], 3)
        if r: print(f"    y={y}:", r)
# arrow white fill
aw = (R > 230) & (G > 230) & (B > 230)
awr = aw.copy(); awr[:, :455] = False; awr[:, 545:] = False; awr[:300, :] = False; awr[430:, :] = False
ys2, xs2 = np.where(awr)
if len(xs2):
    print(f"  arrow white-fill bbox x[{xs2.min()}..{xs2.max()}] y[{ys2.min()}..{ys2.max()}] px={len(xs2)}")

print("\n=== matrix (brackets + digits) ===")
# bracket columns 140-147, 392-399: row extents
for (x0, x1, lbl) in [(139, 149, "left bracket"), (391, 401, "right bracket")]:
    sub = red[:, x0:x1]
    print(f"  {lbl} row runs:", runs(sub.sum(axis=1) > 0))
# digit region between brackets
dig = red.copy(); dig[:, :150] = False; dig[:, 390:] = False; dig[:280, :] = False; dig[460:, :] = False
print("  digits row runs:", runs(dig.sum(axis=1) > 2))
ys, xs = np.where(dig)
print(f"  digits bbox x[{xs.min()}..{xs.max()}] y[{ys.min()}..{ys.max()}]")
# per-digit-row col runs
for (y0, y1) in runs(dig.sum(axis=1) > 2):
    sub = dig[y0:y1+1]
    cols = runs(sub.sum(axis=0) > 0, 2)
    print(f"    digit row y[{y0}..{y1}] col runs:", cols)

print("\n=== cursor hunt: near-black px in matrix neighborhood x330..430 y400..470 ===")
cur = dark.copy(); cur[:, :330] = False; cur[:, 430:] = False; cur[:400, :] = False; cur[470:, :] = False
ys, xs = np.where(cur)
print(f"  near-black px={len(xs)}", f"bbox x[{xs.min()}..{xs.max()}] y[{ys.min()}..{ys.max()}]" if len(xs) else "")
if len(xs):
    for y in range(ys.min(), ys.max() + 1, 2):
        r = runs(cur[y, :], 1)
        if r: print(f"    y={y}:", r)

print("\n=== left photo bbox ===")
# photo: below caption (y>280), inside panel (x 88..470): non-white non-red content
nw = (R < 235) | (G < 235) | (B < 235)
ph = nw.copy(); ph[:, :88] = False; ph[:, 471:] = False; ph[:281, :] = False; ph[477:, :] = False
ph = ph & ~red
colsum = ph.sum(axis=0); rowsum = ph.sum(axis=1)
print("  photo col runs (x, >5):", runs(colsum > 5, 5))
print("  photo row runs (y, >5):", runs(rowsum > 5, 5))

print("\n=== caption ink precise ===")
cap = (lum < 120)
cap = cap & (np.arange(H)[:, None] >= 200) & (np.arange(H)[:, None] <= 280)
cap[:, :80] = False; cap[:, 480:] = False
ys, xs = np.where(cap)
print(f"  caption dark ink bbox x[{xs.min()}..{xs.max()}] y[{ys.min()}..{ys.max()}] px={len(xs)}")
print("  row runs:", runs(cap.sum(axis=1) > 0))
print("  col runs:", runs(cap.sum(axis=0) > 0, 3))

print("\n=== right image precise ===")
# dark image bbox refined with lum<130 in right half
d2 = (lum < 130); d2[:, :480] = False; d2[:130, :] = False
ys, xs = np.where(d2)
print(f"  right img bbox x[{xs.min()}..{xs.max()}] y[{ys.min()}..{ys.max()}] px={len(xs)}")
print("  row runs (y, >100px):", runs(d2.sum(axis=1) > 100, 2))
print("  col runs (x, >100px):", runs(d2.sum(axis=0) > 100, 2))

print("\n=== background check: gray band behind title? ===")
for y in [30, 50, 70, 90, 110, 125, 135, 145, 160, 200]:
    row = a[y, :, :]
    print(f"  y={y}: x20=#{row[20,0]:02X}{row[20,1]:02X}{row[20,2]:02X} x250=#{row[250,0]:02X}{row[250,1]:02X}{row[250,2]:02X} x480=#{row[480,0]:02X}{row[480,1]:02X}{row[480,2]:02X} x700=#{row[700,0]:02X}{row[700,1]:02X}{row[700,2]:02X} x930=#{row[930,0]:02X}{row[930,1]:02X}{row[930,2]:02X}")

print("\n=== watermark bottom-left of right image ===")
wm = (lum > 110)
wm2 = wm.copy(); wm2[:, :500] = False; wm2[:, 660:] = False; wm2[:425, :] = False
ys, xs = np.where(wm2)
print(f"  lighter px in bottom-left strip of right img: px={len(xs)}", f"bbox x[{xs.min()}..{xs.max()}] y[{ys.min()}..{ys.max()}]" if len(xs) else "")
