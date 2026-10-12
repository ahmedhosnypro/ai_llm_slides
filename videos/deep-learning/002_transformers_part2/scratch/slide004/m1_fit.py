#!/usr/bin/env python3
# m1_fit.py — fit 002:4 frame -> base-render mapping from the four chrome border
# landmarks, cross-check with the badge, and check for letterbox bars.
import numpy as np
from PIL import Image

S = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide004"
frame = np.asarray(Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_004.jpg").convert("RGB"), dtype=np.float64)
render = np.asarray(Image.open(S + "/base-1.png").convert("RGB"), dtype=np.float64)
print("frame", frame.shape, "render", render.shape)

def redness(a):
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    return np.clip(r - (g + b) / 2, 0, None) * (r > 120)

def vstroke_center(a, x0, x1, y0, y1):
    """weighted x centroid of red ink inside the window (vertical stroke)"""
    w = redness(a[y0:y1, x0:x1])
    xs = np.arange(x0, x1)
    tot = w.sum()
    return (w.sum(axis=0) * xs).sum() / tot, tot

def hstroke_center(a, x0, x1, y0, y1):
    w = redness(a[y0:y1, x0:x1])
    ys = np.arange(y0, y1)
    tot = w.sum()
    return (w.sum(axis=1) * ys).sum() / tot, tot

def landmarks(a, name):
    H, W = a.shape[:2]
    # scan columns in plausible bands for long vertical red strokes
    redcol = redness(a[:, :]).sum(axis=0)  # per-column red mass
    # panel left/right: two tallest red columns in left third / right third
    left_band = redcol[: W // 3]
    right_band = redcol[2 * W // 3:]
    lx = int(left_band.argmax())
    rx = int(2 * W // 3 + right_band.argmax())
    # refine with weighted centroid over rows where the stroke lives
    lx_c, _ = vstroke_center(a, max(0, lx - 4), lx + 5, H // 6, 5 * H // 6)
    rx_c, _ = vstroke_center(a, rx - 4, rx + 5, H // 6, 5 * H // 6)
    # top border: horizontal red stroke in upper area
    redrow = redness(a[:, W // 4: 3 * W // 4]).sum(axis=1)
    ty = int(redrow[: H // 3].argmax())
    ty_c, _ = hstroke_center(a, W // 3, 2 * W // 3, ty - 4, ty + 5)
    # bottom stroke: red rows near the bottom (search lower half)
    by = int(H // 2 + redrow[H // 2:].argmax())
    by_c, _ = hstroke_center(a, W // 3, 2 * W // 3, by - 4, min(H, by + 5))
    print(f"{name}: left {lx_c:.2f} right {rx_c:.2f} top {ty_c:.2f} bottom {by_c:.2f}")
    return lx_c, rx_c, ty_c, by_c

fl, fr, ft, fb = landmarks(frame, "frame")
rl, rr, rt, rb = landmarks(render, "render")

# --- fit frame -> render per axis (least squares on 2 landmarks each) ---
sx = (rr - rl) / (fr - fl)
ax = rl - sx * fl
sy = (rb - rt) / (fb - ft)
ay = rt - sy * ft
print(f"render_x = {ax:.4f} + {sx:.6f} * frame_x")
print(f"render_y = {ay:.4f} + {sy:.6f} * frame_y")

# --- badge cross-check: yellow circle bbox in frame ---
def yellow_bbox(a):
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    m = (r > 200) & (g > 200) & (b < 190) & (np.abs(r - g) < 40)
    ys, xs = np.where(m[: a.shape[0] // 3, a.shape[1] * 3 // 4:])
    return xs.min() + a.shape[1] * 3 // 4, xs.max() + a.shape[1] * 3 // 4, ys.min(), ys.max()

fx0, fx1, fy0, fy1 = yellow_bbox(frame)
fcx, fcy = (fx0 + fx1) / 2, (fy0 + fy1) / 2
print(f"frame badge bbox x {fx0}..{fx1} y {fy0}..{fy1} center ({fcx:.1f},{fcy:.1f})")
bcx, bcy = ax + sx * fcx, ay + sy * fcy
house = (893 * 150 / 72, 71 * 150 / 72)
print(f"maps to render ({bcx:.1f},{bcy:.1f}) vs house badge {house[0]:.1f},{house[1]:.1f}")

# --- letterbox check: row means of the frame ---
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
print("frame dark row runs (start,end,mean):", runs[:6])
# where do those rows map in render space?
for r0, r1, _ in runs:
    print(f"  rows {r0}..{r1} -> render y {ay + sy * r0:.1f}..{ay + sy * (r1 + 1):.1f} (render H={render.shape[0]}, panel top {rt:.1f}, bottom {rb:.1f})")

np.save(S + "/fit.npy", np.array([ax, sx, ay, sy]))
