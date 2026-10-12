#!/usr/bin/env python3
# diff1.py — 002:4 vs 001:15 frame diff + vs imported-base render diff.
# Frame space: 960x540 (1px = 1pt). Renders are 150dpi (2000x1125) → downscale to 960x540.
from PIL import Image
import numpy as np

R = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning"
f004 = np.asarray(Image.open(f"{R}/002_transformers_part2/unique_slides/slide_004.jpg").convert("RGB"), dtype=np.int16)
f015 = np.asarray(Image.open(f"{R}/001_transformers_part1/unique_slides/slide_015.jpg").convert("RGB"), dtype=np.int16)
print("frame sizes:", f004.shape, f015.shape)

base = Image.open(f"{R}/002_transformers_part2/scratch/slide004/base-1.png").convert("RGB")
r015 = Image.open(f"{R}/001_transformers_part1/recreated_pptx/qa/slide015/render_1.png").convert("RGB")
print("render sizes:", base.size, r015.size)
b004 = np.asarray(base.resize((960, 540), Image.LANCZOS), dtype=np.int16)
r015s = np.asarray(r015.resize((960, 540), Image.LANCZOS), dtype=np.int16)

def griddiff(a, b, tag, thr=28):
    d = np.abs(a - b).max(axis=2)
    H, W = d.shape
    cell = 16
    hot = []
    for cy in range(0, H, cell):
        for cx in range(0, W, cell):
            blk = d[cy:cy+cell, cx:cx+cell]
            frac = (blk > thr).mean()
            if frac > 0.30:
                hot.append((cx, cy, round(float(frac), 2), int(blk.mean())))
    print(f"\n== {tag}: {len(hot)} hot cells (16px grid, >30% px over diff {thr})")
    # cluster rows for readability
    for (cx, cy, frac, dm) in hot:
        print(f"   cell ({cx:3d},{cy:3d})-({cx+cell:3d},{cy+cell:3d})  frac={frac}  meandiff={dm}")
    return d, hot

d_true, hot_true = griddiff(f015, f004, "A: 001:15 FRAME vs 002:4 FRAME (true delta)")
d_base, hot_base = griddiff(r015s, b004, "B: 001:15 RENDER vs BASE RENDER(num4) (import check: should be ~zero)")
d_render, hot_render = griddiff(f015, r015s, "C: 001:15 FRAME vs 001:15 RENDER (accepted rendering baseline)")

# save diff visualizations
for name, d in [("A_frame_true_delta", d_true), ("C_render_baseline", d_render)]:
    vis = np.clip(d * 3, 0, 255).astype(np.uint8)
    Image.fromarray(vis).save(f"/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide004/diff_{name}.png")
print("\nsaved diff maps")
