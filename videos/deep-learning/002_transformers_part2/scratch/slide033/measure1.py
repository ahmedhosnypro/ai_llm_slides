#!/usr/bin/env python3
"""slide033 measure-1: verify frame->slide mapping + locate the main boxes by color."""
import json
import numpy as np
from PIL import Image
from scipy import ndimage

FR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_033.jpg"
im = Image.open(FR).convert("RGB")
a = np.asarray(im).astype(int)
H, W, _ = a.shape
print("size", W, "x", H)

r, g, b = a[..., 0], a[..., 1], a[..., 2]

# --- 1) mapping check: dark-red border strokes (990000-ish) ---
red = (r > 90) & (r < 190) & (g < 60) & (b < 60)
col_red = red.sum(axis=0)
row_red = red.sum(axis=1)
# vertical border lines: columns with many red px
vcols = [x for x in range(W) if col_red[x] > 300]
hrows = [y for y in range(H) if row_red[y] > 300]
print("vertical red border columns:", vcols[:10], "...", vcols[-10:] if len(vcols) > 10 else "")
print("horizontal red border rows:", hrows[:10], "...", hrows[-10:] if len(hrows) > 10 else "")

# --- 2) background + major fill color histogram (coarse) ---
q = (a // 16 * 16)
colors, counts = np.unique(q.reshape(-1, 3), axis=0, return_counts=True)
top = sorted(zip(counts, colors.tolist()), reverse=True)[:22]
print("top quantized colors (count, rgb16):")
for c, col in top:
    print(f"  {c:7d}  #{col[0]:02x}{col[1]:02x}{col[2]:02x}")

# --- 3) box detection: connected components of border-ish saturated colors ---
def comps(mask, min_area=200):
    lab, n = ndimage.label(mask)
    out = []
    for i in range(1, n + 1):
        ys, xs = np.where(lab == i)
        if len(ys) < min_area:
            continue
        out.append({
            "x0": int(xs.min()), "x1": int(xs.max()),
            "y0": int(ys.min()), "y1": int(ys.max()),
            "area": int(len(ys)),
            "fill_med": [int(np.median(a[ys, xs, k])) for k in range(3)],
        })
    return out

# masks for: strong red (C00000/8B0000), green (00B050), orange (ED7D31), blue (0070C0/0000CC)
m_red_strong = (r > 150) & (g < 70) & (b < 70)
m_green = (g > 110) & (r < 110) & (b < 110) & (g - np.maximum(r, b) > 50)
m_orange = (r > 200) & (g > 90) & (g < 170) & (b < 90)
m_blue = (b > 150) & (r < 110) & (g > 80) & (g < 170)

for name, mask in [("RED-STRONG", m_red_strong), ("GREEN", m_green),
                   ("ORANGE", m_orange), ("BLUE", m_blue)]:
    print(f"--- {name} components (area>=400) ---")
    for c in sorted(comps(mask, 400), key=lambda c: (c["y0"], c["x0"])):
        if c["area"] >= 400:
            print("  ", json.dumps(c))
