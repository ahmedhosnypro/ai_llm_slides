#!/usr/bin/env python3
"""Final comprehensive measurements for slide_042 (all remaining unknowns)."""
from PIL import Image
import numpy as np
from scipy import ndimage

F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_042.jpg"
im = Image.open(F).convert("RGB")
W, H = im.size
a = np.asarray(im).astype(int)
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
S = 0.96055; AX = 18.66; SY = 0.95556
def mp(x, y): return ((x - AX) / S, y / SY)
def mps(x0, y0, x1, y1):
    p0 = mp(x0, y0); p1 = mp(x1, y1)
    return f"s({p0[0]:.0f},{p0[1]:.0f})..({p1[0]:.0f},{p1[1]:.0f})"

def show(name, mask, min_px=6):
    lab, n = ndimage.label(mask)
    items = []
    for i in range(1, n + 1):
        ys, xs = np.nonzero(lab == i)
        if len(xs) < min_px: continue
        items.append((int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max()), len(xs)))
    print(f"--- {name}: {len(items)} comps")
    for x0, y0, x1, y1, npx in sorted(items, key=lambda t: (t[1], t[0])):
        print(f"  f({x0},{y0})..({x1},{y1}) w{x1-x0+1} h{y1-y0+1} n{npx} {mps(x0,y0,x1,y1)}")

m = np.zeros((H, W), bool)
mag = (r > 110) & (b > 110) & (g < 100)
m[150:300, 60:900] = mag[150:300, 60:900]
show("MAGENTA text y150..300", m, 4)

m = np.zeros((H, W), bool)
blk = (r < 100) & (g < 100) & (b < 100)
m[195:235, 600:900] = blk[195:235, 600:900]
show("BLACK text right-box y195..235", m, 4)

# line 2 row profile of right box (y185..205, x600..900): all text (non-white, non-gray)
print("--- right box line bands: nonbg col profile per row y170..235, x620..880")
nonbg = (r < 200) | (g < 200) | (b < 200)
for y in range(170, 236):
    xs = np.nonzero(nonbg[y, 620:880])[0]
    if len(xs) > 3:
        print(f"  y{y}: n={len(xs)} x {620+xs.min()}..{620+xs.max()}")

print()
print("--- TARGETED SAMPLES (word colors)")
def sam(name, x, y):
    print(f"  {name} ({x},{y}) = {tuple(a[y,x])}")
# middle box line 1: 'One' ~x470-495, 'Input' ~x502-524, 'Sample' ~x545-591
sam("mid L1 'O' of One", 472, 205); sam("mid L1 'I' of Input", 505, 205)
sam("mid L1 'S' of Sample", 548, 206); sam("mid L1 'p' of Sample", 580, 205)
# right box line 2: 'FIVE' ~x688-712, 'Input' ~x716-740, 'Samples' ~x745-775
sam("right L2 'F' of FIVE", 690, 196); sam("right L2 'I' of Input", 720, 196)
sam("right L2 'S' of Samples", 748, 196)
# right box line 3: 'Using' ~x610-635?
sam("right L3 'U' of Using", 615, 210); sam("right L3 's' of Using", 630, 211)
# left box line 2 (y218-228): 'Sample (Using one filter)' — 'one filter' blue?
print("  left L2 row y222 x90..260 nonbg:")
for y in (220, 222, 224):
    xs = np.nonzero(nonbg[y, 85:280])[0]
    if len(xs): print(f"    y{y}: n={len(xs)} x {85+xs.min()}..{85+xs.max()}")
sam("left L2 mid", 150, 222); sam("left L2 mid2", 200, 222)
# middle box line 2 (y218-228)
for y in (220, 222, 224):
    xs = np.nonzero(nonbg[y, 340:600])[0]
    if len(xs): print(f"  mid L2 y{y}: n={len(xs)} x {340+xs.min()}..{340+xs.max()}")
sam("mid L2 a", 380, 222); sam("mid L2 b", 430, 222); sam("mid L2 c", 480, 222); sam("mid L2 d", 520, 222)

print()
print("--- LABEL BOX BORDER hunt: raw pixel scans")
# left box: expect vertical border near x~75, horizontal near y~190 and y~235
print("  row y=210, x=70..90:", [tuple(a[210, x]) for x in range(70, 91)])
print("  col x=150, y=183..195:", [tuple(a[y, 150]) for y in range(183, 196)])
print("  col x=150, y=228..240:", [tuple(a[y, 150]) for y in range(228, 241)])
print("  row y=210, x=330..350 (mid box left border?):", [tuple(a[210, x]) for x in range(330, 351)])
print("  col x=450, y=183..195:", [tuple(a[y, 450]) for y in range(183, 196)])
print("  col x=450, y=228..242:", [tuple(a[y, 450]) for y in range(228, 243)])
# right box: taller, starts ~y162
print("  col x=700, y=160..175:", [tuple(a[y, 700]) for y in range(160, 176)])
print("  col x=700, y=228..245:", [tuple(a[y, 700]) for y in range(228, 246)])
print("  row y=195, x=620..640:", [tuple(a[195, x]) for x in range(620, 641)])
print("  row y=195, x=845..865:", [tuple(a[195, x]) for x in range(845, 866)])

print()
print("--- VERTICAL ARROW 1px map x615..665, y315..480 (pure-ish red)")
red = (r > 110) & (r - g > 45) & (r - b > 45) & (g < 140)
print("     " + "".join(str(x % 10) for x in range(615, 666)))
for y in range(315, 481, 2):
    print(f"{y:4d} " + "".join("R" if red[y, x] else "." for x in range(615, 666)))

print()
print("--- HORIZONTAL ARROW 1px map x640..800, y448..478")
print("     " + "".join(str(x % 10) for x in range(640, 801, 2)))
for y in range(448, 479):
    print(f"{y:4d} " + "".join("R" if red[y, x] else "." for x in range(640, 801, 2)))

print()
print("--- DIAGONAL ARROW 1px map x790..880, y390..475")
print("     " + "".join(str(x % 10) for x in range(790, 881)))
for y in range(390, 476, 2):
    print(f"{y:4d} " + "".join("R" if red[y, x] else "." for x in range(790, 881)))

print()
print("--- RIGHT BLOCK staircase: top-strip y at x=760 and side-strip x at y=400")
# classify colors down column x=760 (y280..330) and across row y=400 (x770..860)
def cls(px):
    R, G, B = int(px[0]), int(px[1]), int(px[2])
    if R > 240 and G > 240 and B > 235: return "."
    if R > 120 and B > 120 and G < 100: return "M"
    if G > 150 and G - R > 40 and G - B > 60: return "G"
    if R > 180 and 60 < G < 180 and B < 90: return "O"
    if R > 180 and G > 180 and B < 130: return "Y"
    if B > 100 and B - R > 15: return "b"
    if R < 120 and G < 120 and B < 120: return "K"
    if R > 130 and G < 110 and B < 110 and R - G > 50: return "R"
    return "?"
print("  col x=760, y282..332:")
prev = None
for y in range(282, 333):
    c = cls(a[y, 760])
    if c != prev:
        print(f"    y{y}: {c} {tuple(a[y,760])}")
        prev = c
print("  row y=400, x770..860:")
prev = None
for x in range(770, 861):
    c = cls(a[400, x])
    if c != prev:
        print(f"    x{x}: {c} {tuple(a[400,x])}")
        prev = c
print("  col x=680 (front wall left part), y300..480:")
prev = None
for y in range(300, 481):
    c = cls(a[y, 680])
    if c != prev:
        print(f"    y{y}: {c} {tuple(a[y,680])}")
        prev = c
print("  row y=350, x630..680:")
prev = None
for x in range(630, 681):
    c = cls(a[350, x])
    if c != prev:
        print(f"    x{x}: {c} {tuple(a[350,x])}")
        prev = c

print()
print("--- STACKING SLIVER: white-ish pixels between magenta top band and green top band")
wt = (r > 190) & (g > 190) & (b > 185)
for y in range(300, 325):
    xs = np.nonzero(wt[y, 640:800])[0]
    if len(xs) > 3:
        print(f"  y{y}: n={len(xs)} x {640+xs.min()}..{640+xs.max()}")
