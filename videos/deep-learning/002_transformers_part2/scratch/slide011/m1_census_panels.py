#!/usr/bin/env python3
"""slide011 m1: global color census (frame in slide coords) + locate the five
head panels by their measured fills. Frame resampled to slide coords with the
fitted mapping (same as 015): frame_x = 17.628 + 0.961232*slide_x, frame_y = 0.955556*slide_y.
"""
from PIL import Image
import json
from collections import Counter

SCR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide011"
AX, SX, SY = 17.628, 0.961232, 0.955556

frame = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_011.jpg").convert("RGB")
slideimg = frame.transform((960, 540), Image.AFFINE, (SX, 0, AX, 0, SY, 0), resample=Image.BILINEAR, fillcolor=(255, 255, 255))
slideimg.save(f"{SCR}/frame11_slide.png")
px = slideimg.load()
W, H = slideimg.size

# 1) global census of quantized colors (content area only: x 45..915, y 46..514)
census = Counter()
for y in range(46, 514, 1):
    for x in range(45, 915, 1):
        r, g, b = px[x, y]
        census[(r // 16 * 16, g // 16 * 16, b // 16 * 16)] += 1
top = census.most_common(40)
print("TOP QUANTIZED COLORS (r,g,b -> count):")
for c, n in top:
    print(f"  #{c[0]:02X}{c[1]:02X}{c[2]:02X}  {c}  {n}")

# 2) locate panels: for each target fill, bbox of pixels within tolerance
targets = {
    "h1_red": (242, 139, 139),
    "h2_lav": (185, 174, 227),
    "h3_yel": (237, 232, 126),
    "h4_grn": (143, 224, 160),
    "h5_pink": (245, 184, 184),
}
out = {}
for name, (tr, tg, tb) in targets.items():
    pts = []
    for y in range(40, 520, 2):
        for x in range(40, 920, 2):
            r, g, b = px[x, y]
            if abs(r - tr) <= 26 and abs(g - tg) <= 26 and abs(b - tb) <= 26:
                pts.append((x, y))
    if pts:
        xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
        # row/col profiles to find the panel edges (dense rows/cols)
        colcount = Counter(x for x, _ in pts)
        rowcount = Counter(y for _, y in pts)
        dense_cols = sorted(c for c, n in colcount.items() if n > 20)
        dense_rows = sorted(r for r, n in rowcount.items() if n > 20)
        out[name] = {"n": len(pts), "bbox": (min(xs), min(ys), max(xs), max(ys)),
                     "dense_cols": (dense_cols[0], dense_cols[-1]) if dense_cols else None,
                     "dense_rows": (dense_rows[0], dense_rows[-1]) if dense_rows else None}
print("\nPANEL COLOR MASKS:")
print(json.dumps(out, indent=1))
