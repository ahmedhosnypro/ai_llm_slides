#!/usr/bin/env python3
# measure8.py — consolidated verification pass for slide_012 (resumed worker).
# Verifies/closes the gaps left by measure1-7: title+underline, subtitle span,
# embedding block (label, pink box, circles), panel bboxes + grids + colors,
# tall braces (loose red), '=' glyph, short brace, y-strips, captions, Y results,
# magenta annotation. Frame 960x540, 1px = 1pt.
from PIL import Image
import numpy as np

IM = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_012.jpg'
a = np.asarray(Image.open(IM).convert('RGB')).astype(int)
r, g, b = a[..., 0], a[..., 1], a[..., 2]

def bbox(mask, x0, x1, y0, y1, label):
    sub = mask[y0:y1, x0:x1]
    ys, xs = np.where(sub)
    if len(ys) == 0:
        print(f"{label}: EMPTY in x {x0}..{x1} y {y0}..{y1}")
        return None
    bb = (xs.min() + x0, xs.max() + x0, ys.min() + y0, ys.max() + y0, len(ys))
    print(f"{label}: fx {bb[0]}..{bb[1]}  fy {bb[2]}..{bb[3]}  n={bb[4]}")
    return bb

# masks
red   = (r - np.maximum(g, b) > 45) & (r > 120)            # red ink incl. JPEG-soft
dred  = (r > 130) & (g < 95) & (b < 95)                     # deep red
blue  = (b - r > 40) & (b > 110)                            # blue ink
mag   = (r > 130) & (b > 130) & (g < 110) & (abs(r - b) < 70)  # magenta
yel   = (r > 235) & (g > 235) & (b < 230) & (r - b > 25)    # pale yellow cell fill
grn   = (abs(r - 206) < 22) & (g > 232) & (abs(b - 227) < 26)   # H1 green fill
org   = (r > 225) & (abs(g - 222) < 25) & (abs(b - 190) < 30) & (r - b > 25)  # H2 orange fill
lav   = (abs(r - 213) < 20) & (abs(g - 211) < 20) & (b > 228)  # H3 lavender fill

print("=== TITLE / SUBTITLE ===")
bbox(red, 100, 840, 50, 80, "title red ink (excl badge)")
print("-- red row profile fy 70..92 (underline hunt), x 100..840 --")
for y in range(70, 93):
    n = red[y, 100:840].sum()
    if n > 8:
        xs = np.where(red[y, 100:840])[0] + 100
        print(f"  fy {y}: n={n} fx {xs.min()}..{xs.max()}")
bbox(blue, 100, 840, 78, 105, "subtitle blue ink")

print("\n=== EMBEDDING BLOCK ===")
bbox(red, 100, 340, 122, 140, "label line1 red")
bbox(red, 100, 340, 138, 158, "label line2 red")
bbox(blue, 100, 340, 122, 158, "label blue (X_2)")
pink = (r - g > 10) & (r > 238) & (b - g > 4) & (b < 250)
bbox(pink, 90, 340, 150, 260, "pink box (loose)")
print("-- red rims of embed circles: column profile x 100..310 --")
sub = red[150:250, 100:310]
colc = sub.sum(axis=0)
groups = []
s = None
for x in range(210):
    if colc[x] > 6:
        if s is None: s = x
        p = x
    else:
        if s is not None: groups.append((s + 100, p + 100)); s = None
if s is not None: groups.append((s + 100, p + 100))
print("  rim col groups:", groups)
for (x0, x1) in groups:
    ys2 = np.where(red[150:250, x0:x1 + 1].sum(axis=1) > 2)[0]
    if len(ys2): print(f"  group fx {x0}..{x1}: fy {ys2.min()+150}..{ys2.max()+150}")
bbox(blue, 100, 310, 160, 245, "X labels blue in circles")

print("\n=== PANELS ===")
for nm, m in [("green", grn), ("orange", org), ("lavender", lav)]:
    bb = bbox(m, 230, 780, 120, 350, f"panel fill {nm}")
for nm, m in [("green", grn), ("orange", org), ("lavender", lav)]:
    if m[150:350, 230:780].sum() == 0: continue
    ys3 = np.where(m[120:350, 230:780].sum(axis=1) > 30)[0] + 120
    xs3 = np.where(m[120:350, 230:780].sum(axis=0) > 30)[0] + 230
    if len(ys3): print(f"  {nm} heavy-rows fy {ys3.min()}..{ys3.max()}  heavy-cols fx {xs3.min()}..{xs3.max()}")

print("\n=== HEADERS (maroon text) ===")
mar = (abs(r - 136) < 45) & (g < 60) & (b < 60)
for nm, (x0, x1) in [("H1", (240, 400)), ("H2", (405, 565)), ("H3", (566, 730))]:
    bbox(mar | dred, x0, x1, 132, 160, f"header {nm}")

print("\n=== TALL BRACES (loose red, right of each panel) ===")
loose = (r - (g + b) / 2 > 25) & (r > 115)
for nm, (x0, x1) in [("after H1", (385, 420)), ("after H2", (550, 585)), ("after H3", (715, 760))]:
    sub = loose[125:350, x0:x1]
    ys4, xs4 = np.where(sub)
    if len(ys4) > 8:
        import collections
        cnt = collections.Counter(xs4 + x0)
        top = sorted(cnt.items(), key=lambda kv: -kv[1])[:6]
        print(f"{nm}: fx {xs4.min()+x0}..{xs4.max()+x0} fy {ys4.min()+125}..{ys4.max()+125} n={len(ys4)} topcols {top}")
    else:
        print(f"{nm}: none (n={len(ys4)})")

print("\n=== '=' glyph region map (fx 180..250, fy 345..400) ===")
for y in range(345, 400):
    xs5 = np.where(red[y, 180:250] | dred[y, 180:250])[0]
    if len(xs5):
        print(f"  fy {y}: fx {xs5.min()+180}..{xs5.max()+180} n={len(xs5)}")

print("\n=== SHORT BRACE after strip3 (fx 700..770, fy 340..400) ===")
for y in range(340, 400):
    xs6 = np.where(loose[y, 700:770])[0]
    if len(xs6) > 0:
        print(f"  fy {y}: fx {xs6.min()+700}..{xs6.max()+700} n={len(xs6)}")

print("\n=== Y-STRIPS (fy 350..390) ===")
for nm, (x0, x1) in [("strip1", (250, 395)), ("strip2", (415, 560)), ("strip3", (575, 720))]:
    # strip fill modal color
    zone = a[358:384, x0:x1].reshape(-1, 3)
    print(f"{nm}: fill modal sample mid-gap:")
    # sample between boxes: strip1 gaps at 287-292 etc — take row fy 358-360 (above boxes)
    top = a[356:360, x0:x1].reshape(-1, 3)
    med = np.median(top, axis=0).astype(int)
    print(f"   top band median {tuple(med)}")
    # y-box interiors: modal of each box zone
    for i, (bx0, bx1) in enumerate([(0,0)]):
        pass

print("\n=== Y-BOX interiors + glyphs ===")
boxes = {"s1": [(257,286),(293,316),(329,350),(365,386)],
         "s2": [(420,446),(456,481),(491,511),(528,550)],
         "s3": [(582,606),(619,642),(655,675),(691,711)]}
for s, bs in boxes.items():
    for i, (x0, x1) in enumerate(bs):
        zone = a[363:380, x0+2:x1-2].reshape(-1, 3)
        # fill = most common bright pixel; glyph = saturated dark
        bright = zone[(zone.min(axis=1) > 180)]
        fill = tuple(np.median(bright, axis=0).astype(int)) if len(bright) else None
        dark = zone[(zone.max(axis=1) - zone.min(axis=1) > 70) | (zone.max(axis=1) < 140)]
        glyph = tuple(np.median(dark, axis=0).astype(int)) if len(dark) else None
        print(f"  {s} y{i+1} box fx {x0}..{x1}: fill {fill} glyph {glyph} (n_dark {len(dark)})")

print("\n=== CAPTIONS + RESULTS ===")
bbox(red, 250, 730, 388, 402, "caption line1 (red)")
bbox(red, 250, 730, 402, 416, "caption line2 (red)")
bbox(blue, 250, 730, 418, 448, "Y results (blue)")
print("-- Y result blue col groups --")
sub = blue[418:448, 250:730]
colc = sub.sum(axis=0)
groups = []
s = None
for x in range(480):
    if colc[x] > 1:
        if s is None: s = x
        p = x
    else:
        if s is not None: groups.append((s + 250, p + 250)); s = None
if s is not None: groups.append((s + 250, p + 250))
print("  groups:", groups)

print("\n=== MAGENTA ANNOTATION (fx 470..580, fy 265..350) ===")
bbox(mag, 470, 580, 265, 350, "magenta")
for y in range(265, 350):
    xs7 = np.where(mag[y, 470:580])[0]
    if len(xs7):
        print(f"  fy {y}: fx {xs7.min()+470}..{xs7.max()+470} n={len(xs7)}")

print("\n=== CELL GRID GEOMETRY (H1) ===")
# yellow cell fills in H1: col groups + row bands
sub = yel[160:340, 235:400]
colc = sub.sum(axis=0)
groups = []
s = None
for x in range(165):
    if colc[x] > 4:
        if s is None: s = x
        p = x
    else:
        if s is not None: groups.append((s + 235, p + 235)); s = None
if s is not None: groups.append((s + 235, p + 235))
print("H1 yellow-cell col groups:", groups)
rowc = sub.sum(axis=1)
bands = []
for i, n in enumerate(rowc):
    y = i + 160
    if n > 15:
        if bands and y - bands[-1][1] <= 3: bands[-1] = (bands[-1][0], y)
        else: bands.append((y, y))
print("H1 yellow-cell row bands:", bands)

print("\n=== CANVAS (white roundrect) ===")
wht = (r > 243) & (g > 243) & (b > 243)
sub = wht[110:500, 60:920]
xs8 = np.where(sub.sum(axis=0) > 200)[0] + 60
ys8 = np.where(sub.sum(axis=1) > 300)[0] + 110
print(f"white canvas: fx {xs8.min()}..{xs8.max()}  fy {ys8.min()}..{ys8.max()}")

print("\n=== badge/checks ===")
print("badge yellow sample (875,71):", tuple(a[71, 875]))
print("chrome border sample (58,300):", tuple(a[300, 58]), " (901,300):", tuple(a[300, 901]))
