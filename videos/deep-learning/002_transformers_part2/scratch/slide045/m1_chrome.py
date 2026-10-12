#!/usr/bin/env python3
"""Slide 045 — chrome landmarks, frame->slide transform fit from THIS frame's borders."""
import numpy as np
from PIL import Image

F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_045.jpg"
img = np.asarray(Image.open(F).convert("RGB")).astype(int)
H, W, _ = img.shape
print(f"frame {W}x{H}")

R, G, B = img[:, :, 0], img[:, :, 1], img[:, :, 2]
red = (R > 120) & (G < 90) & (B < 90)

# left border: red column near x=59, scan rows 100..400
for x in range(45, 80):
    col = red[100:400, x]
    if col.mean() > 0.8:
        print("left border col:", x, f"redfrac={col.mean():.2f}")
        break
for x in range(W - 45, W - 80, -1):
    col = red[100:400, x]
    if col.mean() > 0.8:
        print("right border col:", x, f"redfrac={col.mean():.2f}")
        break
for y in range(30, 60):
    row = red[y, 100:850]
    if row.mean() > 0.8:
        print("top border row:", y, f"redfrac={row.mean():.2f}")
        break
for y in range(505, 535):
    row = red[y, 100:850]
    if row.mean() > 0.5:
        print("bottom border row:", y, f"redfrac={row.mean():.2f}")

blackrow = (R < 40) & (G < 40) & (B < 40)
for y in range(500, H):
    if blackrow[y, 100:850].mean() > 0.9:
        print("letterbox first full-black row:", y)
        break

# badge yellow bbox (cross-check vs house (893,71) d36)
yel = (R > 220) & (G > 220) & (B < 160)
ys, xs = np.where(yel[40:110, 840:915])
if len(xs):
    print("badge yellow bbox x", xs.min() + 840, xs.max() + 840, "y", ys.min() + 40, ys.max() + 40,
          "center", (xs.min() + xs.max()) / 2 + 840, (ys.min() + ys.max()) / 2 + 40)

# Fit mapping: slide chrome landmarks are panel x 42..918 (border cols), y 45 (top), 540 (bottom).
# Use left col L, right col Rr, top row T, bottom row Bm.
# frame_x = ox + sx * slide_x with slide 42 -> L, 918 -> Rr  => sx=(Rr-L)/876, ox=L-42*sx
# frame_y = oy + sy * slide_y with slide 45 -> T, 540 -> Bm  => sy=(Bm-T)/495, oy=T-45*sy
