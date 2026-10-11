#!/usr/bin/env python3
"""Ink-band map for the diagram region of slide_017.jpg (x 560..920, y 95..535)."""
import numpy as np
from PIL import Image

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_017.jpg').convert('RGB')
A = np.asarray(im).astype(int)

# background fills in the diagram: panel peach ~ (252,237,218)/(249,235,218), green panel, white margins
# classify pixel: "ink" = notably darker or saturated vs both panels
def is_ink(px):
    r, g, b = px
    # peach panel: r>240, g in 225..245, b in 205..225
    # green panel: r in 200..225, g>235, b in 205..225
    peach = r > 238 and 222 <= g <= 246 and 202 <= b <= 228
    green = 195 <= r <= 228 and g > 232 and 202 <= b <= 228
    graypanel = abs(r-233) <= 8 and abs(g-232) <= 8 and abs(b-227) <= 8
    white = r > 246 and g > 246 and b > 246
    if peach or green or graypanel or white:
        return False
    return True

X0, X1, Y0, Y1 = 562, 920, 95, 536
rows = []
for y in range(Y0, Y1):
    n = sum(1 for x in range(X0, X1) if is_ink(A[y, x]))
    rows.append((y, n))

# find bands of consecutive rows with n >= 2
bands = []
cur = None
for y, n in rows:
    if n >= 2:
        if cur is None:
            cur = [y, y, n]
        else:
            cur[1] = y
            cur[2] = max(cur[2], n)
    else:
        if cur is not None:
            bands.append(tuple(cur))
            cur = None
if cur is not None:
    bands.append(tuple(cur))

print("ink bands (y0..y1, max ink px in row):")
for y0, y1, n in bands:
    print(f"   y{y0:3d}..{y1:3d} h={y1-y0+1:3d} maxrow={n}")
