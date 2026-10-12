# v3_scan.py — final details: plus disc, annotations, dashed rects, Y labels, V cells
from PIL import Image
import numpy as np

im = np.asarray(Image.open('unique_slides/slide_059.jpg').convert('RGB')).astype(int)
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]

def sx(fx): return (fx - 18.63) / 0.96123
def sy(fy): return fy / 0.95556
def S(x0, x1, y0, y1, tag):
    print(f"  {tag}: slide x {sx(x0):.1f}..{sx(x1):.1f} y {sy(y0):.1f}..{sy(y1):.1f} "
          f"(w {sx(x1)-sx(x0):.1f} h {sy(y1)-sy(y0):.1f})")

def runs(bools, min_len=1):
    out, s = [], None
    for i, v in enumerate(bools):
        if v and s is None: s = i
        if not v and s is not None:
            if i - s >= min_len: out.append((s, i - 1))
            s = None
    if s is not None: out.append((s, len(bools) - 1))
    return out

def px(x, y): return tuple(int(v) for v in im[y, x])

print("== 1. PLUS disc vertical/horizontal ==")
print("  x=500:", [(y, px(500, y)) for y in range(430, 475, 2)])
print("  y=452:", [(x, px(x, 452)) for x in range(480, 525, 2)])
print("  y=460:", [(x, px(x, 460)) for x in range(480, 525, 2)])

print("== 2. annotations per-line extents (x 63..300) ==")
ink = (abs(r - g) > 35) | (abs(g - b) > 35) | (abs(r - b) > 35)
def ann(y0, y1, tag):
    sub = ink[y0:y1, 63:300]
    rowc = sub.sum(axis=1)
    ln = runs(rowc > 2, 2)
    print(f"  {tag}: lines={[(a+y0, c+y0) for a, c in ln]}")
    for (a, c) in ln:
        ssub = ink[a+y0:c+y0+1, 63:300]
        y2, x2 = np.where(ssub)
        print(f"    y{a+y0}..{c+y0}: x {x2.min()+63}..{x2.max()+63}")
        S(x2.min()+63, x2.max()+63, a+y0, c+y0, f"      ")
ann(138, 172, "pooled-note")
ann(216, 264, "output-seq")
ann(382, 406, "input-seq")
ann(406, 454, "word-emb")
ann(454, 514, "position")

print("== 3. green dashed rect: dash rows/cols ==")
grn = (g - r > 30) & (g - b > 30) & (g > 90) & (g < 220)
for x in [200, 350, 500, 650, 800]:
    print(f"  col {x} rows:", runs(grn[:, x], 0))
for y in [409, 410, 411, 412, 440, 441, 442, 443, 444, 445, 446]:
    rr = runs(grn[y, 150:900], 0)
    print(f"  row {y}: n={len(rr)} first3={[(a+150, c+150) for a, c in rr[:3]]}")

print("== 4. orange dashed rect: dash rows/cols ==")
org = (r > 185) & (g > 85) & (g < 190) & (b < 120) & (r - b > 95)
for x in [200, 350, 500, 650, 800]:
    print(f"  col {x} rows:", runs(org[:, x], 0))
for y in [467, 468, 469, 470, 505, 506, 507, 508, 509, 510, 511]:
    rr = runs(org[y, 150:900], 0)
    print(f"  row {y}: n={len(rr)} first3={[(a+150, c+150) for a, c in rr[:3]]}")

print("== 5. Y labels looser mask ==")
bt = (b - r > 30) & (b - g > 20) & (b > 130) & (r < 190)
sub = bt[230:256, 150:910]
cl = runs(sub.sum(axis=0) > 2, 3)
print("  Y-row blue clusters n>2:", [(a+150, c+150) for a, c in cl])

print("== 6. V cells probes ==")
for x in [195, 205, 215, 225, 235, 245, 255, 265, 275, 285, 295]:
    print(f"  V y481 x{x}: {px(x, 481)}")

print("== 7. X cells vertical structure col1 (x=190 yellow, x=214 label, x=228 lav, x=240 q) ==")
for x in [190, 214, 228, 240, 252]:
    print(f"  x{x}:", [(y, px(x, y)) for y in range(408, 450, 3)])

print("== 8. Y cells vertical structure col1 ==")
for x in [190, 214, 228, 240, 252]:
    print(f"  x{x}:", [(y, px(x, y)) for y in range(224, 264, 3)])

print("== 9. mint band exact rows at col 420 (between boxes) ==")
print("  x=420:", [(y, px(420, y)) for y in range(404, 452, 1)])

print("== 10. peach band rows at col 420 ==")
print("  x=420:", [(y, px(420, y)) for y in range(464, 512, 1)])

print("== 11. Y band rows at col 420 ==")
print("  x=420:", [(y, px(420, y)) for y in range(220, 266, 1)])

print("== 12. GAP text ink rows at col 445 (G glyph) ==")
print("  x=445:", [(y, px(445, y)) for y in range(186, 212, 1)])
