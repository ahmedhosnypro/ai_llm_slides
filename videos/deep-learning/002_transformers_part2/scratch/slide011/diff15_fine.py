#!/usr/bin/env python3
"""Fine 30px-cell diff of frame 011 vs frame 015, both in slide coords.
Cold cells (identical pixels) => certified slide_015 measurements transfer verbatim.
Hot cells => fresh-measure from MY frame."""
from PIL import Image, ImageChops

SCR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide011"
V = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2"
AX, SX, SY = 17.628, 0.961232, 0.955556

f11 = Image.open(f"{V}/unique_slides/slide_011.jpg").convert("RGB").transform(
    (960, 540), Image.AFFINE, (SX, 0, AX, 0, SY, 0), resample=Image.BILINEAR, fillcolor=(0, 0, 0))
f15 = Image.open(f"{V}/unique_slides/slide_015.jpg").convert("RGB").transform(
    (960, 540), Image.AFFINE, (SX, 0, AX, 0, SY, 0), resample=Image.BILINEAR, fillcolor=(0, 0, 0))
f11.save(f"{SCR}/frame11_slide.png"); f15.save(f"{SCR}/frame15_slide.png")

g = ImageChops.difference(f11, f15).convert("L")
px = g.load()
W, H = g.size
TH = 40
grid = {}
for cy in range(0, H, 30):
    for cx in range(0, W, 30):
        n = tot = 0
        for y in range(cy, min(cy + 30, H)):
            for x in range(cx, min(cx + 30, W)):
                tot += 1
                if px[x, y] > TH:
                    n += 1
        grid[(cx, cy)] = n / max(tot, 1)

print("hot(>0.15) cells by row band:")
for cy in range(0, H, 30):
    xs = [cx for cx in range(0, W, 30) if grid[(cx, cy)] > 0.15]
    if xs:
        print(f"  y{cy:3d}: {xs}")
tot = sum(v for v in grid.values()) / len(grid)
print(f"mean cell hot frac: {tot:.3f}")
