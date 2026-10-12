#!/usr/bin/env python3
"""m2: fine 20px-block diff between 011 and 015 frames (both in slide coords) ->
which certified-015 blocks moved on 011. Also verify 015-build landmark structures
(pills, boxes) against the 011 frame directly."""
from PIL import Image, ImageChops
SCR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide011"

a = Image.open(f"{SCR}/frame11_slide.png").convert("RGB")
b = Image.open(f"{SCR}/frame15_slide.png").convert("RGB")
d = ImageChops.difference(a, b).convert("L")
px = d.load()
W, H = d.size
B = 20
print("HOT 20px blocks (frac>0.15) as row bands (y: x-ranges):")
rows = {}
for cy in range(0, H, B):
    for cx in range(0, W, B):
        n = tot = 0
        for y in range(cy, min(cy + B, H), 2):
            for x in range(cx, min(cx + B, W), 2):
                tot += 1
                if px[x, y] > 48:
                    n += 1
        if n / max(tot, 1) > 0.15:
            rows.setdefault(cy, []).append(cx)
for cy in sorted(rows):
    xs = sorted(rows[cy])
    # compress to ranges
    rngs = []
    s = e = xs[0]
    for x in xs[1:]:
        if x == e + B:
            e = x
        else:
            rngs.append((s, e + B)); s = e = x
    rngs.append((s, e + B))
    print(f"  y{cy:3d}..{cy+B:3d}: " + " ".join(f"{r[0]}-{r[1]}" for r in rngs))
tot = sum(1 for y in range(0, H, 2) for x in range(0, W, 2) if px[x, y] > 48)
print(f"overall hot: {tot / ((W // 2) * (H // 2)):.4f}")
