#!/usr/bin/env python3
# m3_census.py — find orange-family pixels (highlight rectangles) in frame vs base
# render; ASCII diff map; black-stroke alignment probes.
import numpy as np
from PIL import Image

S = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide004"
frame = np.asarray(Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_004.jpg").convert("RGB"), dtype=np.float64)
render = np.asarray(Image.open(S + "/base-1.png").convert("RGB"), dtype=np.float64)
warped = np.asarray(Image.open(S + "/frame_warped.png").convert("RGB"), dtype=np.float64)
diff = np.load(S + "/diff.npy")
ax, sx, ay, sy = np.load(S + "/fit2.npy")

def orange_census(a, name):
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    # orange family: strong R, medium G, low B; excludes attention yellow (B high),
    # peach (B high), red (G low)
    m = (r > 200) & (b < 175) & (g > 130) & (g < 225) & ((r - b) > 60) & ((g - b) > 25)
    ys, xs = np.where(m)
    print(f"{name}: {len(xs)} orange px", end="")
    if len(xs):
        print(f"  bbox x {xs.min()}..{xs.max()} y {ys.min()}..{ys.max()}")
        # cluster by x halves
        for tag, sel in [("x<1000", xs < 1000), ("x>=1000", xs >= 1000)]:
            if sel.sum() > 50:
                print(f"   cluster {tag}: n={sel.sum()} x {xs[sel].min()}..{xs[sel].max()} y {ys[sel].min()}..{ys[sel].max()}")
    else:
        print()

orange_census(frame, "frame(960x540)")
orange_census(render, "render(2001x1125)")
orange_census(warped, "warped frame")

# ASCII diff map (valid area), 40x24 cells
H, W = diff.shape
print("\ndiff map (each cell = mean abs diff, . <20, - <60, + <150, # >=150):")
y0, y1, x0, x1 = 100, 1120, 90, 1910
for cy in range(24):
    row = ""
    for cx in range(50):
        cell = diff[y0 + (y1 - y0) * cy // 24: y0 + (y1 - y0) * (cy + 1) // 24,
                    x0 + (x1 - x0) * cx // 50: x0 + (x1 - x0) * (cx + 1) // 50]
        m = cell.mean()
        row += "." if m < 20 else ("-" if m < 60 else ("+" if m < 150 else "#"))
    print(row)

# black vertical stroke probes: left panel border in frame vs render
def dark_vstroke(a, x0, x1, y0, y1, thr=100):
    ink = (a[y0:y1, x0:x1].mean(axis=2) < thr).sum(axis=0)
    xs = np.arange(x0, x1)
    return xs[ink > (y1 - y0) * 0.5]

# frame: left panel box border — search cols 70..120, rows 150..450
print("\nframe dark vertical strokes rows 150..450:", dark_vstroke(frame, 60, 130, 150, 450))
print("render dark vertical strokes rows 300..900:", dark_vstroke(render, 120, 280, 300, 900))
# green card border in render: green stroke
def green_vstroke(a, x0, x1, y0, y1):
    r, g, b = a[y0:y1, x0:x1, 0], a[y0:y1, x0:x1, 1], a[y0:y1, x0:x1, 2]
    ink = ((g > 100) & (g - r > 40) & (g - b > 20)).sum(axis=0)
    xs = np.arange(x0, x1)
    return xs[ink > (y1 - y0) * 0.4]
print("render green vertical strokes rows 300..900:", green_vstroke(render, 1150, 1250, 300, 900))
print("frame green vertical strokes rows 150..450:", green_vstroke(frame, 545, 610, 150, 450))
