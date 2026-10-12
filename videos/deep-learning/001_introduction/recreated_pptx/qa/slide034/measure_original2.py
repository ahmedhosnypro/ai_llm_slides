#!/usr/bin/env python3
"""Pass 2: precise stroke/region measurement for slide_034.jpg (960x540, 1px=1pt)."""
import numpy as np
from PIL import Image

im = np.asarray(Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_034.jpg").convert("RGB")).astype(int)
H, W = im.shape[:2]
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]
red = (r > 120) & (g < 110) & (b < 110)

def runs(idx):
    out, s, p = [], None, None
    for i in idx:
        if s is None: s = p = i
        elif i == p + 1: p = i
        else: out.append((s, p)); s = p = i
    if s is not None: out.append((s, p))
    return out

print("== A. vertical red strokes: per-col red count, x 40..100 and 870..910 (y 100..480, away from title) ==")
sub = red[100:480, :]
for x in list(range(40, 100)) + list(range(870, 910)):
    c = sub[:, x].sum()
    if c > 20:
        print(f"  col {x}: {c}")

print("== B. horizontal red strokes: per-row red count y 30..60, 160..180, 480..500 (x 100..850, away from vstrokes) ==")
sub2 = red[:, 100:850]
for y in list(range(30, 61)) + list(range(160, 181)) + list(range(480, 501)):
    c = sub2[y, :].sum()
    if c > 20:
        print(f"  row {y}: {c}  xruns={runs(list(np.where(red[y, 100:850])[0] + 100))[:6]}")

print("== C. row 169 x-extent ==")
xs = np.where(red[169, :])[0]
print(f"  row 169 red x {xs.min()}..{xs.max()}, n={len(xs)}, runs={runs(list(xs))[:8]}")

print("== D. gray panel E9E9E7 extent ==")
gray = (abs(r - 231) < 7) & (abs(g - 233) < 7) & (abs(b - 230) < 7)
colg = gray[60:480, :].sum(axis=0)
gcols = np.where(colg > 100)[0]
print(f"  gray cols(n>100 of 420): {gcols.min()}..{gcols.max()}" if len(gcols) else "  none")
rowg = gray[:, 300:700].sum(axis=1)
grows = np.where(rowg > 100)[0]
if len(grows):
    print(f"  gray rows(n>100 of 400): {grows.min()}..{grows.max()}, runs={runs(list(grows))[:10]}")

print("== E. white interior extent (near 255) ==")
white = (r > 246) & (g > 246) & (b > 246)
roww = white[:, 200:850].sum(axis=1)
print("  rows with >500 white px (x200..850):", runs([int(y) for y in np.where(roww > 500)[0]])[:14])

print("== F. title bbox (red, x 150..800, y 60..130) ==")
ys, xs = np.where(red[60:130, 150:800])
print(f"  title ink x {150+xs.min()}..{150+xs.max()}, y {60+ys.min()}..{60+ys.max()}")
# cap-height rows: per-row ink
for y in range(60, 130):
    c = red[y, 150:800].sum()
    if c > 0 and (y == 60 or red[y-1, 150:800].sum() == 0):
        print(f"    ink starts row {y}")
print("  row profile nonzero:", runs([int(y) for y in range(60, 130) if red[y, 150:800].sum() > 0]))

print("== G. header 'e.g. Sobel 2-D filter' dark ink, x 60..380, y 150..250 ==")
dark = (r < 130) & (g < 130) & (b < 130)
ys, xs = np.where(dark[150:250, 60:380])
print(f"  dark ink x {60+xs.min()}..{60+xs.max()}, y {150+ys.min()}..{150+ys.max()}, n={len(xs)}")
print("  row runs:", runs(sorted(set(int(150+y) for y in ys)))[:8])
# column profile for word gaps
cold = dark[150:250, 60:380].sum(axis=0)
print("  col ink first/last:", 60+np.where(cold>0)[0].min(), 60+np.where(cold>0)[0].max())

print("== H. left meme photo box: per-row frac of 'photoish' px in x 70..350 ==")
photoish = ((abs(r - g) > 14) | (abs(g - b) > 14) | (r < 205) | (r > 252)) & ~red & ~dark
for y in range(180, 500, 4):
    c = photoish[y, 70:350].sum()
    if c > 60:
        print(f"  row {y}: {c}")
print("  (scan for top/bottom edges)")
colp = photoish[250:460, 70:350].sum(axis=0)
print("  cols with photoish>60:", runs([int(70+x) for x in np.where(colp > 60)[0]])[:10])

print("== I. red matrix bbox (left, x 60..360, y 200..500) ==")
ys, xs = np.where(red[200:500, 60:360])
print(f"  red ink x {60+xs.min()}..{60+xs.max()}, y {200+ys.min()}..{200+ys.max()}, n={len(xs)}")
print("  row runs:", runs(sorted(set(int(200+y) for y in ys)))[:14])

print("== J. RGB stack tints (lower threshold), x 380..820, y 180..480 ==")
tint = ((r - g > 22) & (r - b > 22)) | ((g - r > 18) & (g - b > 18)) | ((b - r > 22) & (b - g > 22))
ys, xs = np.where(tint[180:480, 380:820])
print(f"  tint ink x {380+xs.min()}..{380+xs.max()}, y {180+ys.min()}..{180+ys.max()}, n={len(xs)}")
colt = tint[180:480, 380:820].sum(axis=0)
print("  tint col runs>40:", runs([int(380+x) for x in np.where(colt > 40)[0]])[:12])
rowt = tint[180:480, 380:820].sum(axis=1)
print("  tint row runs>40:", runs([int(180+y) for y in np.where(rowt > 40)[0]])[:12])

print("== K. '3-D Filter' red text, x 750..890, y 170..250 ==")
ys, xs = np.where(red[170:250, 750:890])
print(f"  red ink x {750+xs.min()}..{750+xs.max()}, y {170+ys.min()}..{170+ys.max()}, n={len(xs)}")
print("  row runs:", runs(sorted(set(int(170+y) for y in ys))))

print("== L. cube black ink, x 690..920, y 240..480 ==")
ys, xs = np.where(dark[240:480, 690:920])
print(f"  black ink x {690+xs.min()}..{690+xs.max()}, y {240+ys.min()}..{240+ys.max()}, n={len(xs)}")
rowb = dark[240:480, 690:920].sum(axis=1)
print("  black row runs>8:", runs([int(240+y) for y in np.where(rowb > 8)[0]])[:12])
colb = dark[240:480, 690:920].sum(axis=0)
print("  black col runs>8:", runs([int(690+x) for x in np.where(colb > 8)[0]])[:12])

print("== M. yellow 'Third D' + arrow region, x 640..840, y 330..500 ==")
yel = (r > 200) & (g > 170) & (b < 150)
ys, xs = np.where(yel[330:500, 640:840])
print(f"  yellow x {640+xs.min()}..{640+xs.max()}, y {330+ys.min()}..{330+ys.max()}, n={len(xs)}")
# black arrow strokes near yellow
ys2, xs2 = np.where(dark[330:500, 640:840])
print(f"  black(arrow/label outline) x {640+xs2.min()}..{640+xs2.max()}, y {330+ys2.min()}..{330+ys2.max()}, n={len(xs2)}")

print("== N. color samples (fine) ==")
for (x, y, tag) in [(480, 140, "between title and y169"), (480, 175, "just below y169"),
                    (100, 180, "left of x169? row180"), (300, 470, "below meme?"),
                    (480, 500, "below box bottom 491"), (50, 300, "x50 (outside?)"),
                    (46, 300, "x46"), (40, 300, "x40"), (920, 300, "x920"), (905, 300, "x905"),
                    (480, 44, "y44"), (480, 46, "y46"), (200, 525, "letterbox edge"), (500, 516, "above letterbox")]:
    print(f"  ({x},{y}) {tag}: {tuple(im[y, x])}")
