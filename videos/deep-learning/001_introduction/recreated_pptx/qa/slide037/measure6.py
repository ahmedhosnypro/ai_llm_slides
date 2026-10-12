#!/usr/bin/env python3
"""Measure slide_037.jpg pass 6 — precise zones: labels, dashes, stack, cube, arrows."""
from PIL import Image
import numpy as np
from collections import Counter

VID = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction'
im = Image.open(VID + '/unique_slides/slide_037.jpg').convert('RGB')
a = np.asarray(im).astype(int)
im2 = Image.fromarray(np.uint8(np.clip(a, 0, 255)))

def runs(mask, min_gap=2):
    idx = np.where(mask)[0]
    if len(idx) == 0:
        return []
    out = []
    s = p = idx[0]
    for v in idx[1:]:
        if v - p > min_gap:
            out.append((s, p)); s = v
        p = v
    out.append((s, p))
    return out

def inkbox(y0, y1, x0, x1, thr=330, exclude_red=False, label=""):
    z = a[y0:y1, x0:x1]
    m = z.sum(axis=-1) < thr
    if exclude_red:
        m &= ~((z[:, :, 0] - z[:, :, 1] > 50) & (z[:, :, 0] - z[:, :, 2] > 50))
    ys, xs = np.where(m)
    if len(ys) == 0:
        print(f"{label}: empty"); return None
    print(f"{label}: x{x0+xs.min()}..{x0+xs.max()} y{y0+ys.min()}..{y0+ys.max()} n={len(ys)}")
    return (x0 + xs.min(), x0 + xs.max(), y0 + ys.min(), y0 + ys.max())

print("== small glyphs ==")
inkbox(320, 345, 318, 348, label="glyph A (7#3 or 5?) above cyan filter")
inkbox(355, 382, 295, 320, label="glyph B (7#4?) left of cyan filter")
inkbox(360, 392, 148, 180, label="glyph C (7#1) at slab lower-left", exclude_red=False)
inkbox(360, 400, 195, 225, label="glyph D (7#2) right of C", exclude_red=False)
inkbox(310, 340, 120, 195, label="'3 dims' text (excl border)", exclude_red=False)
inkbox(325, 345, 195, 232, label="'3 dims' arrow")
inkbox(385, 420, 308, 340, label="'3' below stack")
inkbox(385, 455, 290, 480, thr=330, label="fan arrows zone")

print("\n== dash rows: per-row x-extent (dark px in x255..380) ==")
dash = a.sum(axis=-1) < 300
for y in range(292, 392):
    xs = np.where(dash[y, 255:382])[0]
    if len(xs) >= 4:
        # find dash segments
        segs = runs(xs > -1, min_gap=3)
        print(f"y={y}: n={len(xs)} segs={[(255+s, 255+e) for s, e in segs][:8]}")

print("\n== scribble+X bbox (blue+black, x225..320 y315..390) ==")
z = a[315:390, 225:320]
m = (z.sum(axis=-1) < 480) | ((z[:, :, 2] - z[:, :, 0] > 30) & (z[:, :, 2] > 90))
ys, xs = np.where(m)
print(f"scribble: x{225+xs.min()}..{225+xs.max()} y{315+ys.min()}..{315+ys.max()} n={len(ys)}")

print("\n== stack: saturated color bbox, x295..520 y280..400 ==")
z = a[280:400, 295:520]
sat = (z.max(axis=-1) - z.min(axis=-1) > 50) & (z.sum(axis=-1) > 180) & (z.sum(axis=-1) < 720)
ys, xs = np.where(sat)
print(f"stack sat bbox: x{295+xs.min()}..{295+xs.max()} y{280+ys.min()}..{280+ys.max()} n={len(ys)}")
rp = sat.sum(axis=1); cp = sat.sum(axis=0)
print("rows:", [(280+s, 280+e) for s, e in runs(rp > 2, min_gap=4)])
print("cols:", [(295+s, 295+e) for s, e in runs(cp > 2, min_gap=3)])

print("\n== front slab x-boundaries at y=365 (color runs) ==")
row = a[365, 300:480]
for x in range(0, 179):
    r, g, b = row[x]
    print(f"x={300+x}: ({r},{g},{b})", end="  " if (x % 4) < 3 else "\n")

print("\n== cube: exact faces ==")
tan = (a[:, :, 0] > 195) & (a[:, :, 1] > 140) & (a[:, :, 1] < 225) & (a[:, :, 2] > 95) & (a[:, :, 2] < 195)
z = tan[275:460, 505:800]
ys, xs = np.where(z)
print(f"cube tan bbox: x{505+xs.min()}..{505+xs.max()} y{275+ys.min()}..{275+ys.max()}")
# top face vs front face: tan at each row's x-extent
for y in [285, 295, 305, 315, 325, 335, 345, 355, 365, 375, 385, 400, 420, 440, 448]:
    xs2 = np.where(tan[y, 505:800])[0]
    if len(xs2):
        print(f"y={y}: x{505+xs2.min()}..{505+xs2.max()} n={len(xs2)}")

print("\n== cube circles: top face row y~310, front face row y~360 ==")
for yy in [305, 310, 355, 360]:
    row = a[yy, 520:790]
    satm = (row.max(axis=-1) - row.min(axis=-1) > 60)
    xs3 = np.where(satm)[0]
    if len(xs3):
        segs = runs(xs3 > -1, min_gap=4)
        print(f"y={yy}: circle segs: {[(520+s, 520+e) for s, e in segs]}")

print("\n== Depth label + arrow into cube ==")
inkbox(283, 310, 525, 620, label="arrow into cube zone", exclude_red=False)
inkbox(283, 312, 725, 900, label="Depth=5 dims text")

print("\n== question & equation precise ==")
inkbox(448, 480, 55, 640, thr=350, label="question line", exclude_red=True)
inkbox(475, 502, 150, 470, thr=430, label="equation (red)")
r = (a[:, :, 0] > 150) & (a[:, :, 0] - a[:, :, 1] > 70) & (a[:, :, 0] - a[:, :, 2] > 70)
z = r[475:502, 150:470]
ys, xs = np.where(z)
print("modal eq red:", Counter(map(tuple, a[475:502, 150:470][z])).most_common(3))

print("\n== yellow box precise (B<238, R>244,G>244) ==")
yb = (a[:, :, 0] > 244) & (a[:, :, 1] > 244) & (a[:, :, 2] < 238)
z = yb[130:250, :]
rp = z.sum(axis=1)
rr = [(y, int(c)) for y, c in enumerate(rp) if c > 200]
print("yellow rows:", rr[0], "..", rr[-1], f"({len(rr)})")
y0, y1 = rr[0][0], rr[-1][0]
cp = yb[y0:y1 + 1].sum(axis=0)
xs4 = np.where(cp > (y1 - y0) * 0.5)[0]
print(f"yellow box x{xs4[0]}..{xs4[-1]} y{y0}..{y1}")

# body lines within
sub = a[y0:y1 + 1]
ink = sub.sum(axis=-1) < 430
rp2 = ink.sum(axis=1)
print("body lines:")
for s, e in runs(rp2 > 2, min_gap=4):
    xs5 = np.where(ink[s:e + 1].sum(axis=0) > 0)[0]
    print(f"  y{y0+s}..{y0+e} h={e-s+1} x{xs5[0]}..{xs5[-1]}")

print("\n== title precise (red core) ==")
rc = (a[:, :, 0] > 150) & (a[:, :, 1] < 80) & (a[:, :, 2] < 80)
z = rc[70:125, 40:920]
rp3 = z.sum(axis=1)
ys6 = np.where(rp3 > 2)[0]
cp3 = z.sum(axis=0)
xs6 = np.where(cp3 > 0)[0]
print(f"title ink x{40+xs6[0]}..{40+xs6[-1]} y{70+ys6[0]}..{70+ys6[-1]}")
print("modal title core:", Counter(map(tuple, a[70:125, 40:920][z])).most_common(2))

print("\n== panel border precise (loose red, per-row/col) ==")
red = (a[:, :, 0] - a[:, :, 1] > 45) & (a[:, :, 0] - a[:, :, 2] > 45) & (a[:, :, 0] > 120)
rr2 = [(y, int(c)) for y, c in enumerate(red[255:520, 60:900].sum(axis=1)) if c > 300]
print("border rows:", rr2)
cc2 = [(x, int(c)) for x, c in enumerate(red[268:505, :].sum(axis=0)) if c > 120]
print("border cols:", cc2)
