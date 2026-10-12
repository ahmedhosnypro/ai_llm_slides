#!/usr/bin/env python3
"""Precise geometry of 002:slide_008 delta elements via 1px profiles."""
import numpy as np
from PIL import Image

F8 = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_008.jpg"
im = np.asarray(Image.open(F8).convert("RGB")).astype(int)
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]
H, W = im.shape[:2]

AX, SX, SY = 17.628, 0.961232, 0.955556
def sx(fx): return (fx - AX) / SX
def sy(fy): return fy / SY

def runs_of(idx, minlen=2):
    out, s, p = [], None, None
    for i in idx:
        if s is None: s = p = i
        elif i == p + 1: p = i
        else:
            out.append((s, p)); s = p = i
    if s is not None: out.append((s, p))
    return [(a, z) for a, z in out if z - a + 1 >= minlen]

# ---- W_k green boxes: greenish mask in column x 160..215
greenish = (g > 130) & (g - r > 18) & (g - b > 8) & (r < 230)
col = greenish[:, 160:216]
rowcount = col.sum(axis=1)
rr = runs_of(np.where(rowcount > 12)[0], 3)
print("W_k box row runs (frame y):", rr)
for (a, z) in rr:
    sub = greenish[a:z + 1, 130:250]
    ys, xs = np.where(sub)
    x0, x1 = 130 + xs.min(), 130 + xs.max()
    print(f"  box y {a}..{z} (h {z-a+1}) x {x0}..{x1} (w {x1-x0+1}) | slide x {sx(x0):.1f}..{sx(x1):.1f} y {sy(a):.1f}..{sy(z):.1f}")
    # interior fill sample: center row, away from text (left quarter)
    cy = (a + z) // 2
    q = im[cy, x0 + 4]
    q2 = im[a + 3, (x0 + x1) // 2]
    print(f"    fill samples: {tuple(q)} {tuple(q2)}")

# text ink (dark) inside the first box -> label bbox
a, z = rr[0]
sub = (r[a:z+1, 160:216] < 110) & (g[a:z+1, 160:216] < 110)
ys, xs = np.where(sub)
if len(xs): print(f"  box1 dark-ink bbox: x {160+xs.min()}..{160+xs.max()} y {a+ys.min()}..{a+ys.max()}")

# ---- W_v boxes: non-peach mask in column x 688..740 (interior pale + border)
reg_x0, reg_x1 = 686, 742
nonbg = ~(((r > 225) & (g > 195) & (b > 165)) | ((r > 235) & (g > 235) & (b > 235)))
col = nonbg[:, reg_x0:reg_x1]
rowcount = col.sum(axis=1)
rr2 = runs_of(np.where(rowcount > 16)[0], 3)
print("\nW_v box row runs (frame y):", rr2)
for (a, z) in rr2:
    sub = nonbg[a:z + 1, 660:760]
    ys, xs = np.where(sub)
    x0, x1 = 660 + xs.min(), 660 + xs.max()
    print(f"  box y {a}..{z} (h {z-a+1}) x {x0}..{x1} (w {x1-x0+1}) | slide x {sx(x0):.1f}..{sx(x1):.1f} y {sy(a):.1f}..{sy(z):.1f}")
    cy = (a + z) // 2
    print(f"    fill samples: {tuple(im[cy, x0+5])} {tuple(im[a+4, (x0+x1)//2])} border-top {tuple(im[a+1, (x0+x1)//2])}")

# ---- W_q box: region x 270..340, y 400..460
reg_x0, reg_x1, reg_y0, reg_y1 = 265, 345, 398, 468
nonbg2 = ~(((r > 225) & (g > 195) & (b > 165)) | ((r > 235) & (g > 235) & (b > 235)))
sub = nonbg2[reg_y0:reg_y1, reg_x0:reg_x1]
ys, xs = np.where(sub)
if len(xs):
    print(f"\nW_q region ink bbox: x {reg_x0+xs.min()}..{reg_x0+xs.max()} y {reg_y0+ys.min()}..{reg_y0+ys.max()} n={len(xs)}")
    print(f"  slide x {sx(reg_x0+xs.min()):.1f}..{sx(reg_x0+xs.max()):.1f} y {sy(reg_y0+ys.min()):.1f}..{sy(reg_y0+ys.max()):.1f}")
rowc = sub.sum(axis=1)
print("  row profile:", [(reg_y0 + i, int(v)) for i, v in enumerate(rowc) if v > 5][:70])

# ---- multiply nodes: red rings in x 500..645, y 215..390
red = (r > 120) & (r - g > 55) & (r - b > 55)
reg = red[215:395, 495:650]
ys, xs = np.where(reg)
print("\nred ink clusters in multiply region (frame):")
if len(ys):
    # cluster by connected y-runs
    yvals = sorted(set(ys))
    groups, cur = [], [yvals[0]]
    for v in yvals[1:]:
        if v - cur[-1] <= 4: cur.append(v)
        else: groups.append(cur); cur = [v]
    groups.append(cur)
    for gr in groups:
        m = np.isin(ys, gr)
        gxs = xs[m]
        print(f"  y {215+min(gr)}..{215+max(gr)}: x {495+gxs.min()}..{495+gxs.max()} n={m.sum()}")

# ---- blue circle boundary: bluish-lavender blend over peach, region x 220..400 y 320..517
reg_x0, reg_x1, reg_y0, reg_y1 = 220, 400, 320, 516
R_, G_, B_ = r[reg_y0:reg_y1, reg_x0:reg_x1], g[reg_y0:reg_y1, reg_x0:reg_x1], b[reg_y0:reg_y1, reg_x0:reg_x1]
blue = (B_ > R_ + 20) & (B_ > G_ + 8) & (B_ > 150)
print("\nblue-circle blob rows (per-row x extent):")
for yy in range(reg_y1 - reg_y0):
    xr = np.where(blue[yy])[0]
    if len(xr) > 6:
        print(f"  y {reg_y0+yy}: x {reg_x0+xr.min()}..{reg_x0+xr.max()} (w {xr.max()-xr.min()+1})")
