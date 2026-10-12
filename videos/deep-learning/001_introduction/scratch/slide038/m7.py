#!/usr/bin/env python3
"""Slide 038 forensics pass 7: precise geometry fits + annotation maps + color extremes."""
from PIL import Image
import numpy as np

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_038.jpg').convert('RGB')
a = np.asarray(im).astype(int)
r, g, b = a[..., 0], a[..., 1], a[..., 2]

brown = (r > 120) & (g > 60) & (g < 175) & (b < 120) & ((r - b) > 55) & ((r - g) > 25)

print("=== image slab: per-row brown extent (y288..445) ===")
for y in range(288, 446, 4):
    xs = np.nonzero(brown[y, 200:400])[0] + 200
    if len(xs):
        print(f"y={y}: x {xs.min()}..{xs.max()}  n={len(xs)}")

print()
print("=== filter slabs: per-row extent per color (y330..405) ===")
cyan = (g > 120) & (b > 120) & (r < 140) & ((b - r) > 40)
green = (g > 110) & (r < 120) & (b < 120) & ((g - r) > 40)
bred = (r > 170) & (g < 100) & (b < 100)
yel = (r > 190) & (g > 170) & (b < 150)
pur = (r > 70) & (r < 200) & (b > 100) & (g < 100) & ((b - g) > 40)
for name, m in [("cyan", cyan), ("green", green), ("red", bred), ("yellow", yel), ("purple", pur)]:
    rows = []
    for y in range(330, 406, 5):
        xs = np.nonzero(m[y, 380:570])[0] + 380
        if len(xs):
            rows.append(f"y={y}: x {xs.min()}..{xs.max()}")
    print(f"-- {name}: " + " | ".join(rows))

print()
print("=== circles: per-color disc bboxes (y350..390) ===")
for name, m in [("cyan", cyan), ("green", green), ("red", bred), ("yellow", yel), ("purple", pur)]:
    reg = m[345:395, 595:810]
    ys, xs = np.where(reg)
    if len(ys):
        print(f"{name}: x {xs.min()+595}..{xs.max()+595} y {ys.min()+345}..{ys.max()+345}")

print()
print("=== circle 1 zoom x605..648 y350..386 (2px cells) ===")
def cls(p):
    rr, gg, bb = p
    if rr > 235 and gg > 235 and bb > 235: return '.'
    if rr < 110 and gg < 110 and bb < 110: return '#'
    if rr > 170 and gg < 100 and bb < 100: return 'R'
    if rr > 150 and gg > 95 and gg < 180 and bb < 110 and (rr - bb) > 40: return 'o'
    if gg > 120 and (gg - rr) > 30 and (gg - bb) > 15: return 'G'
    if bb > 130 and gg > 120 and rr < 140: return 'c'
    if rr > 190 and gg > 170 and bb < 150: return 'y'
    if rr > 80 and bb > 110 and gg < 100: return 'P'
    if bb > 190 and rr < 160: return 'l'
    return '+'
for cy in range(350, 386, 2):
    row = ''
    for cx in range(605, 649, 2):
        row += cls(a[cy, cx])
    print(f"{cy:3d} {row}")

print()
print("=== '=' hunt: non-white ink in x548..615 y320..420 ===")
ink = (r < 200) & (g < 200) & (b < 210)
for y in range(320, 421, 2):
    xs = np.nonzero(ink[y, 548:616])[0] + 548
    if len(xs) > 1:
        print(f"y={y}: n={len(xs)} x {xs.min()}..{xs.max()} sample {a[y, xs[len(xs)//2]]}")

print()
print("=== formula box border darkest pixels ===")
print("top border rows 116..120, cols 300..700 min per channel:", a[116:121, 300:700].reshape(-1, 3).min(axis=0))
print("left border cols 89..94, rows 130..220 min:", a[130:220, 89:95].reshape(-1, 3).min(axis=0))
print("right border cols 877..880, rows 130..220 min:", a[130:220, 877:881].reshape(-1, 3).min(axis=0))
print("bottom border rows 231..235 min:", a[231:236, 300:700].reshape(-1, 3).min(axis=0))
print()
print("=== title/formula text colors ===")
print("title modal (sampled):", np.median(a[70:96, 340:630][(r[70:96, 340:630] < 190)], axis=0))
f1 = a[139:158, 149:866]; f1m = (r[139:158, 149:866] < 150)
print("formula line1 text modal:", np.median(f1[f1m], axis=0))
# line2 colored runs: red/blue/green x-extents
band = slice(174, 192)
redm = (r[band] > 140) & (g[band] < 90) & (b[band] < 90)
blum = (b[band] > 120) & ((b - r) > 40) & ((b - g) > 30)
grnm = (g[band] > 110) & ((g - r) > 40) & ((g - b) > 30)
for nm, m in [("red", redm), ("blue", blum), ("green", grnm)]:
    xs = np.nonzero(m.sum(axis=0) > 0)[0]
    if len(xs):
        # find contiguous groups
        groups = []
        s = p = xs[0]
        for v in xs[1:]:
            if v <= p + 6: p = v
            else: groups.append((s, p)); s = p = v
        groups.append((s, p))
        print(f"line2 {nm} groups: {[(g0+0, g1+0) for g0, g1 in groups]}")
band3 = slice(209, 225)
redm3 = (r[band3] > 140) & (g[band3] < 90) & (b[band3] < 90)
blum3 = (b[band3] > 120) & ((b - r) > 40) & ((b - g) > 30)
grnm3 = (g[band3] > 110) & ((g - r) > 40) & ((g - b) > 30)
for nm, m in [("red", redm3), ("blue", blum3), ("green", grnm3)]:
    xs = np.nonzero(m.sum(axis=0) > 0)[0]
    if len(xs):
        print(f"line3 {nm} x {xs.min()}..{xs.max()}")
