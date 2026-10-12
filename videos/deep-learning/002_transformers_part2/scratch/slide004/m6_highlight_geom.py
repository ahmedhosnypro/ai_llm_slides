#!/usr/bin/env python3
# m6_highlight_geom.py — exact highlight-rect geometry + overlay color fit +
# yellow-box positions in base render (slide pt) + arrow bbox check.
import numpy as np
from PIL import Image
from collections import deque

S = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide004"
B = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning"
frame = np.asarray(Image.open(f"{B}/002_transformers_part2/unique_slides/slide_004.jpg").convert("RGB"), dtype=np.float64)
render = np.asarray(Image.open(f"{S}/base-1.png").convert("RGB"), dtype=np.float64)
ax, sx, ay, sy = np.load(f"{S}/fit4.npy")
kx, ky = sx * 72 / 150, sy * 72 / 150
fx0 = lambda rx: (rx - ax) / sx
fy0 = lambda ry: (ry - ay) / sy
sx0 = lambda fx: -19.038 + 1.040408 * fx   # slide pt from frame px
sy0 = lambda fy: -0.669 + 1.047547 * fy

# ---- 1. yellow attention boxes in the base render, right panel (slide pt) ----
r, g, b = render[..., 0], render[..., 1], render[..., 2]
ym = (np.abs(r - 245) < 25) & (np.abs(g - 230) < 30) & (np.abs(b - 168) < 40) & (b < 200)
lab = np.zeros(ym.shape, np.int32); cur = 0; boxes = []
Hh, Ww = ym.shape
for y in range(0, Hh, 2):
    for x in range(1100, Ww, 2):
        if ym[y, x] and lab[y, x] == 0:
            cur += 1; q = deque([(y, x)]); lab[y, x] = cur
            n = 0; X0 = X1 = x; Y0 = Y1 = y
            while q:
                cy, cx = q.popleft(); n += 1
                X0 = min(X0, cx); X1 = max(X1, cx); Y0 = min(Y0, cy); Y1 = max(Y1, cy)
                for dy in (-1, 0, 1):
                    for dx in (-1, 0, 1):
                        ny, nx = cy + dy, cx + dx
                        if 0 <= ny < Hh and 0 <= nx < Ww and ym[ny, nx] and lab[ny, nx] == 0:
                            lab[ny, nx] = cur; q.append((ny, nx))
            if n >= 800:
                boxes.append((n, X0, X1, Y0, Y1))
boxes.sort(key=lambda t: (t[4], t[1]))
print("render yellow boxes (right panel) [render px -> slide pt]:")
for n, X0, X1, Y0, Y1 in boxes:
    print(f"  n={n:6d} render x {X0}..{X1} y {Y0}..{Y1}  -> slide pt x {X0*72/150:.1f}..{X1*72/150:.1f} y {Y0*72/150:.1f}..{Y1*72/150:.1f}")

# ---- 2. orange mask closing -> exact highlight bboxes (frame) ----
fr, fg, fb = frame[..., 0], frame[..., 1], frame[..., 2]
om = (fr > 200) & (fb < 175) & (fg > 130) & (fg < 225) & ((fr - fb) > 60) & ((fg - fb) > 25)
# restrict to right panel frame region x>540
om[:, :540] = False
# binary close with 7x7 (dilate then erode) to bridge text holes
def dilate(m, it=3):
    for _ in range(it):
        m2 = m.copy()
        m2[1:, :] |= m[:-1, :]; m2[:-1, :] |= m[1:, :]
        m2[:, 1:] |= m[:, :-1]; m2[:, :-1] |= m[:, 1:]
        m = m2
    return m
def erode(m, it=3):
    for _ in range(it):
        m2 = m.copy()
        m2[1:, :] &= m[:-1, :]; m2[:-1, :] &= m[1:, :]
        m2[:, 1:] &= m[:, :-1]; m2[:, :-1] &= m[:, 1:]
        m = m2
    return m
closed = erode(dilate(om, 4), 4)
lab = np.zeros(closed.shape, np.int32); cur = 0; hl = []
H, W = closed.shape
for y in range(0, H, 2):
    for x in range(540, W, 2):
        if closed[y, x] and lab[y, x] == 0:
            cur += 1; q = deque([(y, x)]); lab[y, x] = cur
            n = 0; X0 = X1 = x; Y0 = Y1 = y
            while q:
                cy, cx = q.popleft(); n += 1
                X0 = min(X0, cx); X1 = max(X1, cx); Y0 = min(Y0, cy); Y1 = max(Y1, cy)
                for dy in (-1, 0, 1):
                    for dx in (-1, 0, 1):
                        ny, nx = cy + dy, cx + dx
                        if 0 <= ny < H and 0 <= nx < W and closed[ny, nx] and lab[ny, nx] == 0:
                            lab[ny, nx] = cur; q.append((ny, nx))
            if n >= 3000:
                hl.append((n, X0, X1, Y0, Y1))
hl.sort(key=lambda t: -t[0])
print("\nhighlight rects (closed orange mask, frame px):")
for n, X0, X1, Y0, Y1 in hl:
    print(f"  n={n:6d} frame x {X0}..{X1} y {Y0}..{Y1}  -> slide pt x {sx0(X0):.1f}..{sx0(X1):.1f} y {sy0(Y0):.1f}..{sy0(Y1):.1f}")

# ---- 3. overlay color fit: obs = a*C + (1-a)*bg over known backgrounds ----
# pick clean highlight-interior spots (frame coords) + their bg (render at mapped spot)
def patch(a, x, y, rad=4):
    return a[int(y)-rad:int(y)+rad+1, int(x)-rad:int(x)+rad+1].reshape(-1, 3).mean(axis=0)
spots = [  # (frame x, y, label) — interior of highlights over known bg
    (610, 350, "enc hl over peach"),
    (700, 380, "enc hl over peach2"),
    (600, 384, "enc hl over peach3"),
    (860, 300, "dec hl over mint"),
    (770, 270, "dec hl over mint2"),
]
print("\noverlay fit (frame patch vs render patch at mapped location):")
for a_try in [0.4, 0.5, 0.6, 0.7]:
    Cs = []
    for x, y, lbl in spots:
        obs = patch(frame, x, y)
        rp = patch(render, ax + sx * x, ay + sy * y)
        C = (obs - (1 - a_try) * rp) / a_try
        Cs.append(C)
    Cs = np.array(Cs)
    print(f"  a={a_try}: implied overlay RGB per patch:\n    {np.round(Cs.mean(axis=0),1)} ± {np.round(Cs.std(axis=0),1)}")

# ---- 4. cell-median tint map of right panel (drift check, excl. highlight bands) ----
diff = np.load(f"{S}/diff4.npy")
warp = np.asarray(Image.open(f"{S}/frame_warped4.png").convert("RGB"), dtype=np.float64)
tint = (warp - render)
print("\nmedian tint per 64px cell, right panel render x 1200..1860 y 110..1100 (R,G,B):")
for cy in range(110, 1100, 96):
    row = []
    for cx in range(1200, 1860, 96):
        cell = tint[cy:cy+96, cx:cx+96].reshape(-1, 3)
        row.append(np.median(cell, axis=0).round(0).astype(int))
    print("  " + "  ".join(f"({t[0]:4d},{t[1]:4d},{t[2]:4d})" for t in row))

# ---- 5. arrow: red bbox in frame vs render ----
def redbox(a, x0, x1, y0, y1, tag, sc=1.0):
    rr_, gg, bb = a[..., 0], a[..., 1], a[..., 2]
    m = (rr_ > 150) & (gg < 90) & (bb < 90)
    m[:y0, :] = False; m[y1:, :] = False; m[:, :x0] = False; m[:, x1:] = False
    ys, xs = np.where(m)
    if len(xs):
        print(f"  {tag}: x {xs.min()}..{xs.max()} y {ys.min()}..{ys.max()}  n={len(xs)}")
    else:
        print(f"  {tag}: none")
print("\narrow census:")
redbox(frame, 430, 550, 250, 340, "frame arrow region")
redbox(render, 900, 1120, 520, 700, "render arrow region")
