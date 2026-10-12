#!/usr/bin/env python3
"""slide_008 frame measurement: chrome landmarks + frame->slide transform fit.

Chrome law canon (slide px = pt, from 001 slide_001.jpg):
  panel x 42..918, y0 45, bottom stroke rows 538-539; badge circle d36 center (893,71).
If this frame renders the slide scaled (like 013's frame), landmarks shift; fit
frame_x = AX + SX*slide_x, frame_y = AY + SY*slide_y from the landmarks.
"""
import numpy as np
from PIL import Image

im = np.asarray(Image.open(
    "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_008.jpg"
).convert("RGB")).astype(int)
H, W = im.shape[:2]
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]

# gray panel (E9E9E7-ish)
gray = (abs(r - 233) < 16) & (abs(g - 233) < 16) & (abs(b - 231) < 18)
# red border
red = (r > 120) & (g < 110) & (b < 110)
# badge yellow
yel = (r > 200) & (g > 200) & (b < 190)

# panel columns: rows 100..500 (well inside), columns mostly gray
band = gray[100:500, :]
cols = np.where(band.sum(axis=0) > 300)[0]
print("panel cols:", cols.min(), "..", cols.max())
# panel rows: columns 60..140 (left band inside panel, avoiding content)
lband = gray[:, 60:140]
rows = np.where(lband.sum(axis=1) > 60)[0]
print("panel rows (left band):", rows.min(), "..", rows.max())

# red border: bottom stroke rows
bot = red[520:, :]
brows = np.where(bot.sum(axis=1) > 100)[0]
print("bottom red stroke rows:", (520 + brows).tolist())
# left/right border at mid height (y 250..290)
mid = red[250:290, :]
lcols = np.where(mid[:, :100].sum(axis=0) > 5)[0]
rcols = np.where(mid[:, 860:].sum(axis=0) > 5)[0]
print("left border cols:", lcols.tolist(), " right border cols:", (860 + rcols).tolist())
# top border
topred = red[:100, 200:700]
trows = np.where(topred.sum(axis=1) > 100)[0]
print("top border rows:", trows.tolist())

# badge: search yellow near top-right
ys, xs = np.where(yel[:160, 800:])
if len(xs):
    bx0, bx1 = 800 + xs.min(), 800 + xs.max()
    by0, by1 = ys.min(), ys.max()
    print(f"badge yellow bbox: x {bx0}..{bx1} (w {bx1-bx0+1}), y {by0}..{by1} (h {by1-by0+1})")
    print(f"badge center: ({(bx0+bx1)/2:.1f}, {(by0+by1)/2:.1f})")
else:
    print("badge: no yellow found in top-right window")

# letterbox check: bottom rows darkness
for row in (516, 518, 520, 525, 535, 539):
    rowmean = im[row, :, :].mean()
    print(f"row {row} mean: {rowmean:.1f}")

# fit transform: slide px = (frame_x - AX)/SX
print()
print("CANON (slide px): panel x 42..918, y0 45, badge c (893,71) d36")
