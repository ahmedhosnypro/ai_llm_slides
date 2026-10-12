#!/usr/bin/env python3
"""Pass 3: element-exact measurement for slide_034.jpg (960x540, 1px=1pt)."""
import numpy as np
from PIL import Image

im = np.asarray(Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_034.jpg").convert("RGB")).astype(int)
H, W = im.shape[:2]
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]

def runs(idx):
    out, s, p = [], None, None
    for i in idx:
        if s is None: s = p = i
        elif i == p + 1: p = i
        else: out.append((s, p)); s = p = i
    if s is not None: out.append((s, p))
    return out

print("== 1. red matrix clean bbox (x 70..340, y 175..475) ==")
red = (r > 120) & (g < 110) & (b < 110)
ys, xs = np.where(red[175:475, 70:340])
print(f"  matrix red x {70+xs.min()}..{70+xs.max()}, y {175+ys.min()}..{175+ys.max()}, n={len(xs)}")
rowr = red[175:475, 70:340].sum(axis=1)
print("  row runs>3:", runs([int(175+y) for y in np.where(rowr > 3)[0]])[:20])
colr = red[175:475, 70:340].sum(axis=0)
print("  col runs>3:", runs([int(70+x) for x in np.where(colr > 3)[0]])[:20])

print("== 2. header text (dark, x 70..380, y 195..255; stroke cols excluded) ==")
dark = (r < 130) & (g < 130) & (b < 130)
ys, xs = np.where(dark[195:255, 70:380])
print(f"  ink x {70+xs.min()}..{70+xs.max()}, y {195+ys.min()}..{195+ys.max()}, n={len(xs)}")
cold = dark[195:255, 70:380].sum(axis=0)
print("  col runs>0:", runs([int(70+x) for x in np.where(cold > 0)[0]])[:24])
rowd = dark[195:255, 70:380].sum(axis=1)
print("  row runs>0:", runs([int(195+y) for y in np.where(rowd > 0)[0]])[:12])

print("== 3. meme photo edges: scan transitions from white ==")
nonwhite = (r < 249) | (g < 249) | (b < 249)
# horizontal scan at several rows: first/last nonwhite col in x 66..380 (skip stroke cols 63-67)
for y in [260, 300, 340, 380, 420, 440]:
    xs = [x for x in range(70, 380) if nonwhite[y, x]]
    if xs:
        rr = runs(xs)
        print(f"  row {y}: first {rr[0]}, last {rr[-1]}, nruns={len(rr)}")
# vertical scan at several cols
for x in [100, 150, 200, 250, 300, 330]:
    ys = [y for y in range(200, 500) if nonwhite[y, x] and not red[y, x]]
    if ys:
        rr = runs(ys)
        print(f"  col {x}: first {rr[0]}, last {rr[-1]}, nruns={len(rr)}")

print("== 4. RGB copies per channel ==")
redt = (r - g > 40) & (r - b > 40) & (r > 110)
grnt = (g - r > 25) & (g - b > 25)
blut = (b - r > 40) & (b - g > 40)
for name, m in [("RED copy", redt), ("GREEN copy", grnt), ("BLUE copy", blut)]:
    ys, xs = np.where(m[180:500, 380:880])
    if len(xs):
        print(f"  {name}: x {380+xs.min()}..{380+xs.max()}, y {180+ys.min()}..{180+ys.max()}, n={len(xs)}")
        rowm = m[180:500, 380:880].sum(axis=1)
        rrun = runs([int(180+y) for y in np.where(rowm > 30)[0]])
        colm = m[180:500, 380:880].sum(axis=0)
        crun = runs([int(380+x) for x in np.where(colm > 30)[0]])
        print(f"      dense rows {rrun[:6]}  dense cols {crun[:6]}")

print("== 5. label '3-D Filter' background check ==")
for (x, y) in [(745, 240), (760, 242), (800, 242), (830, 242), (855, 242), (770, 230), (770, 255), (860, 240)]:
    print(f"  ({x},{y}): {tuple(im[y, x])}")
print("  red-text bbox precise (x 745..870, y 225..260):")
ys, xs = np.where(red[225:260, 745:870])
print(f"    x {745+xs.min()}..{745+xs.max()}, y {225+ys.min()}..{225+ys.max()}, n={len(xs)}")

print("== 6. cube + arrow extents ==")
# cube black lines incl grid; wide window
ys, xs = np.where(dark[200:500, 600:940])
print(f"  all dark x {600+xs.min()}..{600+xs.max()}, y {200+ys.min()}..{200+ys.max()}, n={len(xs)}")
rowb = dark[200:500, 600:940].sum(axis=1)
print("  row runs>6:", runs([int(200+y) for y in np.where(rowb > 6)[0]])[:16])
colb = dark[200:500, 600:940].sum(axis=0)
print("  col runs>6:", runs([int(600+x) for x in np.where(colb > 6)[0]])[:16])
# cube faces: light gray fill vs white bg — sample
for (x, y, tag) in [(800, 300, "cube top face?"), (840, 330, "cube right face?"), (760, 350, "cube left face?"),
                    (880, 300, "right of cube?"), (700, 260, "left of cube?"), (820, 430, "cube bottom?")]:
    print(f"  ({x},{y}) {tag}: {tuple(im[y, x])}")

print("== 7. arrow extent (thin black strokes lower-left of cube) ==")
ys, xs = np.where(dark[380:500, 600:800])
if len(xs):
    print(f"  arrow-region dark x {600+xs.min()}..{600+xs.max()}, y {380+ys.min()}..{380+ys.max()}, n={len(xs)}")
    rowa = dark[380:500, 600:800].sum(axis=1)
    print("  rows>0:", runs([int(380+y) for y in np.where(rowa > 0)[0]])[:16])

print("== 8. gap between meme and RGB stack; stack left edge ==")
for y in [250, 300, 350, 400]:
    xs = [x for x in range(340, 480) if nonwhite[y, x]]
    print(f"  row {y}: first nonwhite x in 340..480: {xs[0] if xs else None}")

print("== 9. bottom area between box bottom (491) and letterbox (519) ==")
print("  row 500 sample colors:", [tuple(im[500, x]) for x in (100, 300, 500, 700, 850)])
print("  row 510 sample colors:", [tuple(im[510, x]) for x in (100, 300, 500, 700, 850)])
print("  row 517 sample colors:", [tuple(im[517, x]) for x in (100, 300, 500, 700, 850)])
