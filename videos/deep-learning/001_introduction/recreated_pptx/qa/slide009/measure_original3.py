# stage 3: color-run scans to nail geometry
from PIL import Image
import numpy as np
from collections import Counter

im = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_009.jpg").convert("RGB")
a = np.asarray(im).astype(int)
H, W, _ = a.shape

def runs(vals, minlen=3):
    # vals: list of (x, (r,g,b)) — collapse into color runs by quantized color
    out = []
    cur = None; start = None
    for x, c in vals:
        q = tuple(v//24*24 for v in c)
        if cur is None or q != cur:
            if cur is not None and x - start >= minlen:
                out.append((start, x-1, cur))
            cur = q; start = x
    if cur is not None:
        out.append((start, vals[-1][0], cur))
    return out

def rowruns(y, x0=0, x1=960):
    vals = [(x, tuple(a[y, x])) for x in range(x0, x1)]
    rr = runs(vals)
    print(f"row y={y}:")
    for s, e, c in rr:
        if e - s >= 2:
            print(f"   x {s}..{e}  ({e-s+1}px)  {c}")

def colruns(x, y0, y1):
    vals = [(y, tuple(a[y, x])) for y in range(y0, y1)]
    rr = runs(vals)
    print(f"col x={x}:")
    for s, e, c in rr:
        if e - s >= 2:
            print(f"   y {s}..{e}  ({e-s+1}px)  {c}")

print("=== chain band scanlines ===")
rowruns(236)   # through chain boxes
print()
rowruns(150)   # through Training Data ellipse
print()
rowruns(310)   # through gray labels
print()
rowruns(345)   # through Final Result ellipse
print("=== vertical scans ===")
colruns(200, 90, 480)    # through Pre processing box
print()
colruns(650, 90, 480)    # through 4th chain box region
print()
colruns(120, 120, 280)   # through Training Data ellipse
print()
colruns(860, 240, 400)   # through curved arrow + Final Result
print("=== title band rows ===")
for y in [44, 46, 50, 55, 60, 64, 66, 68, 70, 75, 80, 84, 87, 90, 93]:
    row = a[y]
    red = [(x) for x in range(960) if row[x][0] > 120 and row[x][0] - max(row[x][1], row[x][2]) > 55]
    if red:
        print(f"y={y}: red x {min(red)}..{max(red)} n={len(red)}")
    else:
        print(f"y={y}: no red")
