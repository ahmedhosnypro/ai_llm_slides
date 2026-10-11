#!/usr/bin/env python3
"""Probe render_1.png: title true size, hatch presence, bar1 artifact, plus frame banner band L/W."""
import numpy as np
from PIL import Image
import math

im = np.asarray(Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/qa/slide005/render_1.png").convert("RGB")).astype(int)
H, W = im.shape[:2]
S = 960 / 2000.0
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]

# 1. title: red ink in y60-200 render, full width
red = (r > 140) & (g < 110) & (b < 110)
m = red[60:200, 200:1800]
ys, xs = np.where(m)
print(f"title ink: x {(xs.min()+200)*S:.1f}-{(xs.max()+200)*S:.1f} frame (tgt 261-653), y {(ys.min()+60)*S:.1f}-{(ys.max()+60)*S:.1f} (tgt 59-76)")
rows = np.where(m.sum(axis=1) > 3)[0]
print(f"title ink rows: {(rows.min()+60)*S:.1f}..{(rows.max()+60)*S:.1f} frame; cap height {(rows.max()-rows.min()+1)*S:.1f}px (24pt -> 17.2)")

# 2. hatch presence: red-ish pixels in y940-1060 render, x250-1750
redl = (r > 150) & (g < 160) & (b < 160) & (r - g > 40)
m = redl[940:1060, 250:1750]
ys, xs = np.where(m)
print(f"\nhatch zone red px: {len(xs)}", f"x {(xs.min()+250)*S:.1f}-{(xs.max()+250)*S:.1f} y {(ys.min()+940)*S:.1f}-{(ys.max()+940)*S:.1f}" if len(xs) else "")

# 3. bar1 artifact: what's at render x860-890, y880-1090
patch = im[880:1090, 860:890]
rr, gg, bb = patch[:, :, 0], patch[:, :, 1], patch[:, :, 2]
odd = (abs(rr - 233) > 12) | (abs(gg - 233) > 12) | (abs(bb - 231) > 12)
ys, xs = np.where(odd)
if len(xs):
    print(f"\nbar1-below odd px: {len(xs)}, y {(ys.min()+880)*S:.1f}-{(ys.max()+880)*S:.1f} frame, sample {tuple(int(v) for v in patch[ys[0], xs[0]])}")
else:
    print("\nbar1-below: clean")

# 4. frame banner band: per-column yellow min/max -> midline + thickness + true L/W
fr = np.asarray(Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_005.jpg").convert("RGB")).astype(int)
frr, frg, frb = fr[:, :, 0], fr[:, :, 1], fr[:, :, 2]
yel = (frg > 225) & (frr > 225) & (frb < 190)
pts = []
for x in range(575, 920, 5):
    col = np.where(yel[320:520, x])[0] + 320
    if len(col) > 3:
        pts.append((x, col.min(), col.max(), (col.min() + col.max()) / 2))
if pts:
    xs_ = [p[0] for p in pts]
    mids = [p[3] for p in pts]
    # fit midline
    A = np.polyfit(xs_, mids, 1)
    ang = math.degrees(math.atan(A[0]))
    ths = [p[2] - p[1] for p in pts]
    th_med = sorted(ths)[len(ths) // 2]
    print(f"\nframe banner: midline slope {ang:.1f} deg; median vert thickness {th_med}px -> perp {th_med*math.cos(math.radians(ang)):.1f}px")
    print(f"yellow x-extent {xs_[0]}..{xs_[-1]}; midline at x575: {A[0]*575+A[1]:.0f}, at x915: {A[0]*915+A[1]:.0f}")
    # band length: extreme corners along midline direction
    ux, uy = math.cos(math.radians(ang)), math.sin(math.radians(ang))
    proj = [p[0] * ux + p[3] * uy for p in pts]
    print(f"band length along midline: {max(proj)-min(proj):.0f}px")
