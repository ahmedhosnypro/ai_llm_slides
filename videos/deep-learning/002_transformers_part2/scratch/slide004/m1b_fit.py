#!/usr/bin/env python3
# m1b_fit.py — refined chrome landmark detection: border strokes = rows/cols where
# red ink covers ~continuously; title text has gaps.
import numpy as np
from PIL import Image

S = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide004"
frame = np.asarray(Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_004.jpg").convert("RGB"), dtype=np.float64)
render = np.asarray(Image.open(S + "/base-1.png").convert("RGB"), dtype=np.float64)

def redmask(a):
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    return (r > 120) & (r - (g + b) / 2 > 40)

def vcentroid(a, x0, x1, y0, y1):
    m = redmask(a[y0:y1, x0:x1]).astype(np.float64)
    xs = np.arange(x0, x1)
    w = m.sum(axis=0)
    return (w * xs).sum() / w.sum()

def hcentroid(a, x0, x1, y0, y1):
    m = redmask(a[y0:y1, x0:x1]).astype(np.float64)
    ys = np.arange(y0, y1)
    w = m.sum(axis=1)
    return (w * ys).sum() / w.sum()

def landmarks(a, name):
    H, W = a.shape[:2]
    m = redmask(a)
    colcov = m[:, :].mean(axis=0)   # fraction of red per column (over full height)
    rowcov = m[:, :].mean(axis=1)
    # left/right: columns with high coverage in outer thirds
    lx = int(np.argmax(colcov[: W // 3]))
    rx = int(W // 3 * 2 + np.argmax(colcov[2 * W // 3:]))
    lx_c = vcentroid(a, lx - 3, lx + 4, H // 4, 3 * H // 4)
    rx_c = vcentroid(a, rx - 3, rx + 4, H // 4, 3 * H // 4)
    # top: topmost row with coverage > 0.5 in the upper band (border is continuous)
    cand = np.where(rowcov[: H // 3] > 0.5)[0]
    ty = int(cand[0])
    ty_c = hcentroid(a, W // 3, 2 * W // 3, ty - 3, ty + 4)
    # bottom: bottommost row with coverage > 0.5
    cand = np.where(rowcov[H // 2:] > 0.5)[0] + H // 2
    by = int(cand[-1])
    by_c = hcentroid(a, W // 3, 2 * W // 3, by - 3, min(H, by + 4))
    print(f"{name}: left {lx_c:.2f} right {rx_c:.2f} top {ty_c:.2f} bottom {by_c:.2f}  (raw lx {lx} rx {rx} ty {ty} by {by})")
    return lx_c, rx_c, ty_c, by_c

fl, fr, ft, fb = landmarks(frame, "frame")
rl, rr, rt, rb = landmarks(render, "render")

sx = (rr - rl) / (fr - fl)
ax = rl - sx * fl
sy = (rb - rt) / (fb - ft)
ay = rt - sy * ft
print(f"render_x = {ax:.4f} + {sx:.6f} * frame_x")
print(f"render_y = {ay:.4f} + {sy:.6f} * frame_y")
print(f"scale check: 150/72 / 0.958 = {150/72/0.958:.6f}")

fcx, fcy = 875.5, 71.0
bcx, bcy = ax + sx * fcx, ay + sy * fcy
house = (893 * 150 / 72, 71 * 150 / 72)
print(f"badge maps to render ({bcx:.1f},{bcy:.1f}) vs house {house[0]:.1f},{house[1]:.1f} (d {bcx-house[0]:+.1f},{bcy-house[1]:+.1f})")

rowmean = frame.mean(axis=(1, 2))
dark = rowmean < 60
runs = []
i = 0
while i < len(dark):
    if dark[i]:
        j = i
        while j < len(dark) and dark[j]:
            j += 1
        runs.append((i, j - 1, float(rowmean[i:j].mean())))
        i = j
    else:
        i += 1
print("frame dark row runs:", runs)
for r0, r1, _ in runs:
    print(f"  rows {r0}..{r1} -> render y {ay + sy * r0:.1f}..{ay + sy * (r1 + 1):.1f} (render H={render.shape[0]}, panel top {rt:.1f})")

np.save(S + "/fit.npy", np.array([ax, sx, ay, sy]))
