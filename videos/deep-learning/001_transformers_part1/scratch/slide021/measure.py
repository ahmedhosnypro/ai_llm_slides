#!/usr/bin/env python3
"""PIL measurement of unique_slides/slide_021.jpg (960x540, 1px = 1pt).

Measures: title band, subtitle band, blue box border bbox, text line bands
inside the box (red header lines vs black body lines vs blue terms), line pitch.
"""
from PIL import Image
import numpy as np

im = Image.open(
    "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_021.jpg"
).convert("RGB")
a = np.asarray(im).astype(int)
H, W, _ = a.shape
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]

red = (R > 140) & (G < 90) & (B < 90)                    # C00000-ish ink
blue = (B > 120) & (R < 110) & (G < 110)                 # 3333CC-ish ink
black = (R < 90) & (G < 90) & (B < 90)                   # body ink
dark = (R < 150) & (G < 150) & (B < 150)                 # any dark ink

def bands(mask, min_gap=3, min_px=2):
    rows = np.where(mask.sum(axis=1) >= min_px)[0]
    out = []
    if len(rows) == 0:
        return out
    start = prev = rows[0]
    for r in rows[1:]:
        if r - prev > min_gap:
            out.append((start, prev))
            start = r
        prev = r
    out.append((start, prev))
    return out

def colspan(mask, y0, y1):
    sub = mask[y0:y1 + 1]
    cols = np.where(sub.sum(axis=0) >= 1)[0]
    return (int(cols[0]), int(cols[-1])) if len(cols) else None

print("== RED bands (title/subtitle/headers, whole slide) ==")
for (y0, y1) in bands(red):
    cs = colspan(red, y0, y1)
    print(f"  y {y0}..{y1} (h={y1-y0+1})  x {cs}")

print("== BLUE bands (whole slide) ==")
for (y0, y1) in bands(blue):
    cs = colspan(blue, y0, y1)
    print(f"  y {y0}..{y1} (h={y1-y0+1})  x {cs}")

print("== BLACK bands (whole slide, inside panel) ==")
for (y0, y1) in bands(black):
    cs = colspan(black, y0, y1)
    print(f"  y {y0}..{y1} (h={y1-y0+1})  x {cs}")

# blue box border: look for long horizontal blue runs
print("== BLUE box border detection (rows with long blue runs) ==")
for y in range(H):
    row = blue[y]
    if row.sum() > 300:
        xs = np.where(row)[0]
        print(f"  y={y} blue_count={row.sum()} x {xs[0]}..{xs[-1]}")
for x in range(W):
    col = blue[:, x]
    if col.sum() > 150:
        ys = np.where(col)[0]
        print(f"  x={x} blue_count={col.sum()} y {ys[0]}..{ys[-1]}")

# combined text bands inside the box (any dark or blue ink)
print("== TEXT line bands inside box region (x 70..890) ==")
box = (dark | blue).copy()
box[:, :70] = False
box[:, 890:] = False
for (y0, y1) in bands(box, min_gap=2, min_px=3):
    cs = colspan(box, y0, y1)
    sub_r = red[y0:y1+1, 70:890].sum()
    sub_b = blue[y0:y1+1, 70:890].sum()
    sub_k = black[y0:y1+1, 70:890].sum()
    print(f"  y {y0}..{y1} (h={y1-y0+1}) x {cs}  red={sub_r} blue={sub_b} black={sub_k}")
