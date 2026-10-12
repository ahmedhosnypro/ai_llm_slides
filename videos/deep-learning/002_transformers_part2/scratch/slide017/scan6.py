#!/usr/bin/env python3
"""Concat bar segment boundaries, LT box edges, drop-lines, title metrics."""
from PIL import Image
import numpy as np

F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_017.jpg"
im = Image.open(F).convert("RGB")
a = np.asarray(im).astype(int)

# --- concat bar: y 124..148, x 186..687. Scan the middle row for segment color changes
print("== concat bar interior scan y=136 (segment colors by x) ==")
row = a[136]
prev = None
for x in range(186, 688):
    c = tuple(np.median(a[130:143, x], axis=0).astype(int))
    key = (c[0] // 24, c[1] // 24, c[2] // 24)
    if key != prev:
        print(f"  x={x}: #%02X%02X%02X" % c)
        prev = key

print("\n== concat bar left label zone: rows y=128..146, x=186..310 ==")
for y in [128, 131, 134, 137, 140, 143, 146]:
    r = a[y, 186:312]
    dark = (r.max(axis=1) < 150) | (r.min(axis=1) < 120)
    xs = np.nonzero(dark)[0]
    if len(xs): print(f"  y={y}: ink x {xs.min()+186}..{xs.max()+186} n={len(xs)}")
    else: print(f"  y={y}: no ink")

# --- LT box: precise top/bottom/left/right. scan col x=400 for border rows y=78..120
print("\n== LT box vertical extent (col x=420, dark rows y=75..125) ==")
col = a[75:125, 420]
for y in range(50):
    r, g, b = col[y]
    if max(r, g, b) < 170: print(f"  y={y+75} dark")
print("== LT box row extent (row y=98, dark cols x=300..570) ==")
row = a[98, 300:570]
xs = [x + 300 for x in range(270) if max(row[x]) < 170]
print(f"  dark cols: {xs[:6]}...{xs[-6:] if len(xs)>6 else ''}")
# fill color sample
print(f"  LT fill sample (430,95): #%02X%02X%02X" % tuple(a[95, 430]))
print(f"  LT fill sample (340,105): #%02X%02X%02X" % tuple(a[105, 340]))
print(f"  beyond-518 sample (540,95): #%02X%02X%02X" % tuple(a[95, 540]))
print(f"  beyond-518 sample (540,105): #%02X%02X%02X" % tuple(a[105, 540]))

# --- d x H . d red annotation: red-ish pixels near LT box bottom-right (x430..560, y95..120)
print("\n== red ink near LT box bottom-right (x400..570, y88..125) ==")
m = (a[:, :, 0] > 150) & (a[:, :, 1] < 110) & (a[:, :, 2] < 110)
sub = m[88:126, 400:570]
ys, xs = np.nonzero(sub)
if len(xs):
    print(f"  red ink bbox: ({xs.min()+400},{ys.min()+88})-({xs.max()+400},{ys.max()+88}) n={len(xs)}")
    # row profile
    for yy in sorted(set(ys)):
        xr = xs[ys == yy]
        print(f"    y={yy+88}: x {xr.min()+400}..{xr.max()+400} n={len(xr)}")

# --- top strip: precise bbox + cell colors (y48..76, x395..480)
print("\n== top embedding strip: col scans ==")
for x in [404, 410, 420, 430, 440, 446, 452, 458, 464, 470]:
    col = a[46:78, x]
    runs = []
    s = None
    for y in range(32):
        r, g, b = col[y]
        key = (r // 28, g // 28, b // 28)
        if s is None: s = (y, key, [(r, g, b)])
        elif key != s[1]:
            med = np.median(np.array(s[2]), axis=0).astype(int)
            runs.append((s[0] + 46, y - 1 + 46, "#%02X%02X%02X" % tuple(med)))
            s = (y, key, [(r, g, b)])
        else: s[2].append((r, g, b))
    med = np.median(np.array(s[2]), axis=0).astype(int)
    runs.append((s[0] + 46, 77, "#%02X%02X%02X" % tuple(med)))
    runs = [r for r in runs if r[1] - r[0] >= 1]
    print(f"  x={x}: {runs}")

# --- title: dark ink bbox in title zone y45..105 x500..870
print("\n== title ink rows (x505..850, y45..105) ==")
sub = a[45:105, 505:850]
dark = sub.max(axis=2) < 120
for yy in range(60):
    xs = np.nonzero(dark[yy])[0]
    if len(xs) > 3:
        print(f"  y={yy+45}: x {xs.min()+505}..{xs.max()+505} n={len(xs)}")

# --- drop lines below bar y150..185
print("\n== thin marks y=150..186 (non-bg runs len 2..8) ==")
for y in range(150, 187, 4):
    row = a[y, 180:700]
    out = []
    s = None
    for x in range(520):
        r, g, b = row[x]
        sat = max(r, g, b) - min(r, g, b)
        nb = (sat >= 20) or (max(r, g, b) < 165)
        if nb and s is None: s = x
        elif not nb and s is not None:
            if 1 <= x - s <= 9: out.append(s + 180)
            s = None
    print(f"  y={y}: {out}")
