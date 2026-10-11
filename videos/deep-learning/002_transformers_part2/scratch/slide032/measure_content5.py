#!/usr/bin/env python3
"""v5: subtitle colors/bbox, callout rect, vector box border, L1 detail."""
from PIL import Image
import numpy as np
from collections import Counter

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_032.jpg').convert('RGB')
a = np.asarray(im).astype(int)
H, W, _ = a.shape
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]
FX0, SX, SY = 18.63, 0.96123, 0.95556
def to_slide(fx, fy): return ((fx - FX0) / SX, fy / SY)
def pr(label, fx0, fy0, fx1, fy1):
    s0 = to_slide(fx0, fy0); s1 = to_slide(fx1 + 1, fy1 + 1)
    print(f"{label:30s} frame x {fx0}..{fx1} y {fy0}..{fy1} -> slide x {s0[0]:.1f}..{s1[0]:.1f} y {s0[1]:.1f}..{s1[1]:.1f} (w {s1[0]-s0[0]:.1f} h {s1[1]-s0[1]:.1f})")

# ---- subtitle: dark pixels rows 80..102, x 200..800; print color histogram ----
band = a[80:103, 200:800]
dark = (band.sum(axis=2) < 500)
ys, xs = np.where(dark)
print(f"subtitle dark px: {len(ys)}")
if len(ys):
    cols = band[ys, xs]
    cc = Counter(map(tuple, cols))
    print("top colors:", cc.most_common(8))
    pr('subtitle ink bbox', 200 + int(xs.min()), 80 + int(ys.min()), 200 + int(xs.max()), 80 + int(ys.max()))
    # column profile with counts
    colc = dark.sum(axis=0)
    cols2 = np.where(colc >= 2)[0]
    if len(cols2):
        pr('subtitle ink (>=2/col)', 200 + int(cols2.min()), 80 + int(ys.min()), 200 + int(cols2.max()), 80 + int(ys.max()))

# ---- title: same for rows 55..78 ----
band2 = a[55:79, 300:650]
dark2 = (band2.sum(axis=2) < 500)
ys2, xs2 = np.where(dark2)
if len(ys2):
    cc2 = Counter(map(tuple, band2[ys2, xs2]))
    print("\ntitle top colors:", cc2.most_common(5))
    pr('title ink bbox', 300 + int(xs2.min()), 55 + int(ys2.min()), 300 + int(xs2.max()), 55 + int(ys2.max()))

# ---- callout: rows 105..185, orange border scan ----
zone = (slice(105, 186), slice(90, 900))
oz = a[zone]
orange = (oz[:, :, 0] - oz[:, :, 1] > 45) & (oz[:, :, 1] - oz[:, :, 2] > 15) & (oz[:, :, 0] > 140) & (oz[:, :, 2] < 130)
oy, ox = np.where(orange)
print(f"\ncallout orange px in zone: {len(oy)}")
if len(oy):
    rcount = np.bincount(oy, minlength=81)
    print("orange rows (count>8):", [(105 + i, int(rcount[i])) for i in np.where(rcount > 8)[0]])
    ccount = np.bincount(ox, minlength=810)
    print("orange cols (count>4):", [(90 + i, int(ccount[i])) for i in np.where(ccount > 4)[0]][:6], "...", [(90 + i, int(ccount[i])) for i in np.where(ccount > 4)[0]][-6:])
    pr('callout border bbox', 90 + int(ox.min()), 105 + int(oy.min()), 90 + int(ox.max()), 105 + int(oy.max()))
# callout fill bbox in zone
fill = (oz[:, :, 0] > 200) & (oz[:, :, 1] > 200) & (oz[:, :, 2] > 150) & (oz[:, :, 2] < 235) & (oz[:, :, 0] - oz[:, :, 2] > 20)
fy, fx = np.where(fill)
if len(fy):
    pr('callout fill bbox', 90 + int(fx.min()), 105 + int(fy.min()), 90 + int(fx.max()), 105 + int(fy.max()))

# ---- vector box: red border, loose, rows 95..205 cols 60..215 ----
vz = a[95:206, 60:216]
redm = (vz[:, :, 0] - vz[:, :, 1] > 60) & (vz[:, :, 0] - vz[:, :, 2] > 60) & (vz[:, :, 0] > 120)
vy, vx = np.where(redm)
print(f"\nvector red px: {len(vy)}")
if len(vy):
    rrc = np.bincount(vy, minlength=111); ccc = np.bincount(vx, minlength=156)
    print("red rows>5:", [(95 + i, int(rrc[i])) for i in np.where(rrc > 5)[0]])
    print("red cols>5:", [(60 + i, int(ccc[i])) for i in np.where(ccc > 5)[0]])
    pr('vector red bbox', 60 + int(vx.min()), 95 + int(vy.min()), 60 + int(vx.max()), 95 + int(vy.max()))
    # inner ink (exclude border rows/cols)
    r0, r1 = 95 + int(vy.min()), 95 + int(vy.max()); c0, c1 = 60 + int(vx.min()), 60 + int(vx.max())
    inner = redm[r0 - 95 + 3:r1 - 95 - 2, c0 - 60 + 3:c1 - 60 - 2]
    iy, ix = np.where(inner)
    if len(iy):
        pr('vector inner ink', c0 + 3 + int(ix.min()), r0 + 3 + int(iy.min()), c0 + 3 + int(ix.max()), r0 + 3 + int(iy.max()))

# ---- L1 ink columns x 82..200 (find text start / first glyphs) ----
ink1 = (a[:, :, 0] < 170)
m1 = ink1[225:247, 80:260]
prof = [(80 + c, int(m1[:, c].sum())) for c in range(m1.shape[1]) if m1[:, c].sum() > 0]
print("\nL1 x 80..260 col ink:", prof[:40])
