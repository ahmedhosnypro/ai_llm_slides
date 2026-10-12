# v4_scan.py — annotation extents, V bar extent, Y label red check
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

print("== annotations, window x 63..166 ==")
ink = (abs(r - g) > 35) | (abs(g - b) > 35) | (abs(r - b) > 35)
for (y0, y1, tag) in [(138, 172, "pooled-note"), (218, 262, "output-seq"),
                      (384, 406, "input-seq"), (406, 452, "word-emb"), (454, 512, "position")]:
    sub = ink[y0:y1, 63:166]
    rowc = sub.sum(axis=1)
    ln = runs(rowc > 2, 2)
    print(f"  {tag}: lines={[(a+y0, c+y0) for a, c in ln]}")
    for (a, c) in ln:
        ssub = ink[a+y0:c+y0+1, 63:166]
        y2, x2 = np.where(ssub)
        print(f"    y{a+y0}..{c+y0}: x {x2.min()+63}..{x2.max()+63}")
        S(x2.min()+63, x2.max()+63, a+y0, c+y0, "      ->")

print("== V bar vertical extent (x=200, x=230, x=250) ==")
for x in [200, 230, 250]:
    print(f"  x{x}:", [(y, px(x, y)) for y in range(466, 512, 2)])

print("== Y labels red check (y 230..254, dred mask) ==")
dred = (r < 225) & (r - g > 40) & (r - b > 30) & (r > 90)
sub = dred[230:255, 150:910]
cl = runs(sub.sum(axis=0) > 1, 2)
print("  Y-row red clusters:", [(a+150, c+150) for a, c in cl])
print("  Y label probes:", [(p, px(*p)) for p in [(214, 238), (216, 240), (288, 240), (212, 242)]])

print("== X label probe cols 1-6 cores ==")
for (x, y) in [(213, 429), (287, 429), (360, 429), (434, 429), (507, 429), (580, 429)]:
    print(f"  ({x},{y}):", px(x, y))

print("== pooled row cell edges fine (row 156, x 380..640 brightness dips) ==")
row = im[156, 380:640].astype(int)
br = row.sum(axis=1)
dips = [i+380 for i in range(1, 259) if br[i] < br[i-1] - 40 and br[i] < br[i+1] - 40]
print("  local dark minima:", dips)

print("== fan line count at y=145 (just above pooled row) ==")
fan = (r > 225) & (g > 130) & (g < 215) & (b > 130) & (b < 215) & (r - b > 30)
rr = runs(fan[145, 380:660], 0)
print("  y145 runs:", [(a+380, c+380) for a, c in rr])
rr = runs(fan[143, 380:660], 0)
print("  y143 runs:", [(a+380, c+380) for a, c in rr])
