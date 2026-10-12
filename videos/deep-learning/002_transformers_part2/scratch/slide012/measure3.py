#!/usr/bin/env python3
# measure3.py — row/col profiles with tight masks + point sampling
from PIL import Image
import numpy as np

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_012.jpg').convert('RGB')
a = np.asarray(im).astype(int)
H, W = a.shape[:2]
r, g, b = a[..., 0], a[..., 1], a[..., 2]
mx = np.maximum(np.maximum(r, g), b)
mn = np.minimum(np.minimum(r, g), b)
sat = mx - mn
dark = mx < 150
ink = (sat > 55) | dark

def spans(m, minlen=2):
    v = m.any(axis=1) if m.ndim == 1 else m
    out = []
    s = None
    for i, vv in enumerate(v):
        if vv and s is None: s = i
        if not vv and s is not None:
            if i - s >= minlen: out.append((s, i - 1))
            s = None
    if s is not None and len(v) - s >= minlen: out.append((s, len(v) - 1))
    return out

print("=== per-row ink count (x 30..930), fy 50..150 ===")
for y in range(50, 150):
    n = int(ink[y, 30:930].sum())
    if n > 8:
        xs = np.where(ink[y, 30:930])[0]
        px_ = a[y, 30:930]
        # dominant ink color on this row
        mrow = ink[y, 30:930]
        sub = px_[mrow]
        med = np.median(sub, axis=0).astype(int)
        print(f"fy {y}: n={n:4d} fx {xs.min()+30:3d}..{xs.max()+30:3d} medink {med.tolist()}")

print("\n=== point samples ===")
pts = {
    "bg(20,300)": (20, 300), "badge(893,71)": (893, 71),
}
for k, (x, y) in pts.items():
    print(k, a[y, x].tolist())

# panels: sample a grid of points to find pastel regions
print("\n=== pastel panel detection (strict) ===")
green = (np.abs(r - 201) < 25) & (np.abs(g - 239) < 20) & (np.abs(b - 201) < 25) & (sat < 70)
orange = (np.abs(r - 245) < 20) & (np.abs(g - 223) < 20) & (np.abs(b - 192) < 25) & (sat < 80)
lav = (np.abs(r - 201) < 25) & (np.abs(g - 201) < 25) & (np.abs(b - 242) < 20) & (sat < 70)
pink = (np.abs(r - 248) < 20) & (np.abs(g - 215) < 25) & (np.abs(b - 232) < 25) & (sat < 80)
for name, m in [("green", green), ("orange", orange), ("lavender", lav), ("pink", pink)]:
    ys, xs = np.where(m)
    if len(ys) < 100:
        print(f"{name}: n={len(ys)}")
        continue
    # largest connected region approx: use percentile bounds
    x0, x1 = np.percentile(xs, [1, 99]).astype(int)
    y0, y1 = np.percentile(ys, [1, 99]).astype(int)
    print(f"{name}: n={len(ys)} fx {x0}..{x1} fy {y0}..{y1} (core)")

print("\n=== white canvas ===")
white = (r > 240) & (g > 240) & (b > 240)
wrows = white[:, 100:900].sum(axis=1)
cand = [(y, int(wrows[y])) for y in range(40, 540) if wrows[y] > 200]
if cand:
    print("white-dominant rows fy:", cand[0][0], "..", cand[-1][0])
    y0 = cand[0][0]
    m = white[y0 + 50, :]
    xs = np.where(m)[0]
    if len(xs): print("row fy", y0 + 50, "white fx:", xs.min(), "..", xs.max())

print("\n=== deep red (braces, =) mask fy 340..500 ===")
br = (r > 140) & (g < 80) & (b < 80)
rows = []
for y in range(335, 505):
    n = int(br[y, 30:930].sum())
    if n > 3:
        xs = np.where(br[y, 30:930])[0]
        rows.append((y, n, xs.min() + 30, xs.max() + 30))
# compress into bands
bands = []
for y, n, x0, x1 in rows:
    if bands and y - bands[-1][1] <= 2:
        b0, b1, nx0, nx1 = bands[-1]
        bands[-1] = (b0, y, min(nx0, x0), max(nx1, x1))
    else:
        bands.append((y, y, x0, x1))
for b0, b1, x0, x1 in bands:
    print(f"red band fy {b0}..{b1} fx {x0}..{x1}")

print("\n=== magenta X_2 annotation ===")
mag = (r > 130) & (b > 130) & (g < 100)
ys, xs = np.where(mag)
if len(ys) > 10:
    print(f"n={len(ys)} fx {xs.min()}..{xs.max()} fy {ys.min()}..{ys.max()}")
else:
    print("none found", len(ys))
