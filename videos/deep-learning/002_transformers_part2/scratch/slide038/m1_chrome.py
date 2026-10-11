#!/usr/bin/env python3
"""Slide 038 — chrome landmarks, frame->slide transform check, coarse content regions."""
import numpy as np
from PIL import Image

F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_038.jpg"
img = np.asarray(Image.open(F).convert("RGB")).astype(int)
H, W, _ = img.shape
print(f"frame {W}x{H}")

R, G, B = img[:, :, 0], img[:, :, 1], img[:, :, 2]

# --- 1) chrome border landmarks (playlist template: left 59, right ~902, top 43, bottom ~516)
# left border: red column near x=59, scan rows 100..400
red = (R > 120) & (G < 90) & (B < 90)
for x in range(45, 75):
    col = red[100:400, x]
    if col.mean() > 0.8:
        print("left border col:", x, f"redfrac={col.mean():.2f}")
        break
for x in range(W - 45, W - 75, -1):
    col = red[100:400, x]
    if col.mean() > 0.8:
        print("right border col:", x, f"redfrac={col.mean():.2f}")
        break
for y in range(30, 60):
    row = red[y, 100:850]
    if row.mean() > 0.8:
        print("top border row:", y, f"redfrac={row.mean():.2f}")
        break
# bottom border of the slide panel: red row near 516
for y in range(505, 530):
    row = red[y, 100:850]
    if row.mean() > 0.5:
        print("bottom border row:", y, f"redfrac={row.mean():.2f}")
# letterbox strip: black rows at the very bottom
blackrow = (R < 40) & (G < 40) & (B < 40)
for y in range(500, H):
    if blackrow[y, 100:850].mean() > 0.9:
        print("letterbox first full-black row:", y)
        break

# --- 2) badge yellow bbox (cross-check vs house (893,71) d36, ring 6A5ACD)
yel = (R > 220) & (G > 220) & (B < 160)
ys, xs = np.where(yel[40:110, 840:915])
if len(xs):
    print("badge yellow bbox x", xs.min() + 840, xs.max() + 840, "y", ys.min() + 40, ys.max() + 40,
          "center", (xs.min() + xs.max()) / 2 + 840, (ys.min() + ys.max()) / 2 + 40)

# --- 3) transform (from certified 002/039): frame = 18.63 + 0.96123*slide_x ; frame_y = 0.95556*slide_y
# inverse:
invx = lambda fx: (fx - 18.63) / 0.96123
invy = lambda fy: fy / 0.95556
print("inverse: frame 59 ->", round(invx(59), 1), " 902 ->", round(invx(902), 1),
      " 43 ->", round(invy(43), 1), " 516 ->", round(invy(516), 1))

# --- 4) coarse content: title ink (red, rows 60..110 inside panel)
seg = red[60:115, 100:850]
rows = np.where(seg.any(axis=1))[0]
cols = np.where(seg.any(axis=0))[0]
print("title red ink x", cols.min() + 100, cols.max() + 100, "y", rows.min() + 60, rows.max() + 60,
      "-> slide", round(invx(cols.min() + 100), 1), round(invx(cols.max() + 100), 1),
      round(invy(rows.min() + 60), 1), round(invy(rows.max() + 60), 1))

# --- 5) def box (blue border) + diagram panel (red border) rectangles
blue = (B > 120) & (R < 100) & (G < 100)
seg = blue[95:250, 60:900]
rows = np.where(seg.any(axis=1))[0]
cols = np.where(seg.any(axis=0))[0]
print("defbox blue ink x", cols.min() + 60, cols.max() + 60, "y", rows.min() + 95, rows.max() + 95)

# diagram panel: search red horizontal long lines below y=250
for y in range(250, 540):
    row = red[y, 80:880]
    if row.mean() > 0.8:
        print("long red row:", y, f"frac={row.mean():.2f}")
