#!/usr/bin/env python3
# m5_delta_census.py — borders-based fit (robust), warp, diff census: classify
# diff blocks into orange-highlight (expected delta) vs structural (unexpected).
import numpy as np
from PIL import Image
from collections import deque

S = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide004"
B = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning"
frame_im = Image.open(f"{B}/002_transformers_part2/unique_slides/slide_004.jpg").convert("RGB")
render = np.asarray(Image.open(f"{S}/base-1.png").convert("RGB"), dtype=np.float64)
frame = np.asarray(frame_im, dtype=np.float64)

# borders fit: x on (58.46->87.05, 901.54->1914.44, badge 875.87->1857.35)
#              y on (43.5->93.54, 515.62->1123.89)
sx = (1914.44 - 87.05) / (901.54 - 58.46)
ax = 87.05 - sx * 58.46
sy = (1123.89 - 93.54) / (515.62 - 43.5)
ay = 93.54 - sy * 43.5
print(f"FIT x: {ax:.3f} + {sx:.6f}*fx   y: {ay:.3f} + {sy:.6f}*fy")
print(f"slide_pt: x = {ax*72/150:.3f} + {sx*72/150:.6f}*fx ; y = {ay*72/150:.3f} + {sy*72/150:.6f}*fy")
fbx = (1857.35 - ax) / sx; fby = (148.17 - ay) / sy
print(f"badge under fit: frame ({fbx:.1f},{fby:.1f}) vs measured (875.9,70.7) -> dy {fby-70.7:.1f} frame px")

warp = np.asarray(frame_im.transform((render.shape[1], render.shape[0]), Image.AFFINE,
    (1/sx, 0, -ax/sx, 0, 1/sy, -ay/sy), resample=Image.BILINEAR), dtype=np.float64)
Image.fromarray(warp.astype(np.uint8)).save(f"{S}/frame_warped4.png")
diff = np.abs(warp - render).sum(axis=2)
valid = np.zeros(diff.shape, bool)
valid[100:1118, 93:1908] = True
np.save(f"{S}/diff4.npy", diff)
np.save(f"{S}/fit4.npy", np.array([ax, sx, ay, sy]))
print(f"diff: mean {diff[valid].mean():.2f} median {np.median(diff[valid]):.2f} p95 {np.percentile(diff[valid],95):.1f}")

# connected diff regions (thr 120 sum-abs), min 900 px
hot = (diff > 120) & valid
lab = np.zeros(hot.shape, np.int32); cur = 0
comps = []
Hh, Ww = hot.shape
for y in range(0, Hh, 2):
    for x in range(0, Ww, 2):
        if hot[y, x] and lab[y, x] == 0:
            cur += 1
            q = deque([(y, x)]); lab[y, x] = cur
            n = 0; x0 = x1 = x; y0 = y1 = y; osum = np.zeros(3)
            while q:
                cy, cx = q.popleft(); n += 1
                x0 = min(x0, cx); x1 = max(x1, cx); y0 = min(y0, cy); y1 = max(y1, cy)
                for dy, dx in ((1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)):
                    ny, nx = cy + dy, cx + dx
                    if 0 <= ny < Hh and 0 <= nx < Ww and hot[ny, nx] and lab[ny, nx] == 0:
                        lab[ny, nx] = cur; q.append((ny, nx))
            if n >= 900:
                comps.append((n, x0, x1, y0, y1))
comps.sort(reverse=True)
print(f"\nbig diff regions (render px): n | x0..x1 y0..y1 | frame-px equiv | mean RGB of warp-render delta tint")
for n, x0, x1, y0, y1 in comps[:18]:
    fx0, fx1 = (x0-ax)/sx, (x1-ax)/sx
    fy0, fy1 = (y0-ay)/sy, (y1-ay)/sy
    sel = diff[y0:y1+1, x0:x1+1] > 120
    dt = (warp[y0:y1+1, x0:x1+1] - render[y0:y1+1, x0:x1+1])[sel].mean(axis=0)
    print(f"  n={n:7d}  x {x0:4d}..{x1:4d} y {y0:4d}..{y1:4d} | frame x {fx0:5.0f}..{fx1:5.0f} y {fy0:5.0f}..{fy1:5.0f} | tint {dt.round(0)}")
