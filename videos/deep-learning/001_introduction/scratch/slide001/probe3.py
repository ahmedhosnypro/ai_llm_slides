#!/usr/bin/env python3
"""Probe 3: italic-slant detection, top-line extent, logo strip, letterbox, emblem top,
plus methodology parity check on the sibling (transformers) frame."""
import numpy as np
from PIL import Image

IM = np.asarray(Image.open(
    "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_001.jpg"
).convert("RGB")).astype(int)
H, W = IM.shape[:2]
r, g, b = IM[:, :, 0], IM[:, :, 1], IM[:, :, 2]

def slant(y0, y1, x0, x1, mask, label):
    """Per-row leftmost ink x; slope of left edge over the rows = italic slant."""
    lefts = []
    for y in range(y0, y1):
        xs = np.where(mask[y, x0:x1])[0]
        if len(xs) > 2:
            lefts.append((y, x0 + xs.min()))
    if len(lefts) < 5:
        print(f"{label}: too few rows ({len(lefts)})")
        return
    ys = np.array([p[0] for p in lefts]); ls = np.array([p[1] for p in lefts])
    A = np.polyfit(ys, ls, 1)[0]
    print(f"{label}: rows {ys.min()}-{ys.max()}, left-edge slope {A:+.3f} px/row "
          f"({'ITALIC' if A > 0.08 else 'upright' if A < 0.03 else 'ambiguous'})")

core_red = (r > 140) & (g < 60) & (b < 60)
core_blue = (b > 110) & (r < 90) & (g < 90)

print("=== italic slant (left-edge slope; italic ~ +0.15..0.25 px/row) ===")
slant(290, 312, 440, 590, core_red, "'Prepared By' (red)")
slant(315, 341, 350, 680, core_blue, "prepared-by name (blue)")
slant(342, 359, 390, 640, core_blue, "prepared-by email (blue)")
slant(396, 413, 60, 215, core_red, "'Instructors:' (red)")
slant(424, 442, 105, 405, core_blue, "instructor name1 (blue)")
slant(450, 468, 105, 345, core_blue, "instructor email1 (blue)")
slant(470, 489, 105, 365, core_blue, "instructor name2 (blue)")
slant(496, 512, 105, 335, core_blue, "instructor email2 (blue)")
slant(128, 171, 240, 700, core_red, "title L1 (red)")

print("\n=== row-43 top line: extent test ===")
for x in (40, 45, 50, 55, 58, 62, 70, 890, 898, 901, 905, 910, 915, 918):
    print(f"  x={x}: {IM[43, x]}")
# where does gray panel start/end on row 100?
row = IM[100]
grayish = np.where((abs(row[:, 0] - 232) < 8) & (abs(row[:, 1] - 232) < 8))[0]
print(f"row 100 gray cols: {grayish.min()}-{grayish.max()}")
row = IM[300]
grayish = np.where((abs(row[:, 0] - 232) < 8) & (abs(row[:, 1] - 232) < 8))[0]
print(f"row 300 gray cols: {grayish.min()}-{grayish.max()}")

print("\n=== logo strip x900-930 ===")
for (yy, tag) in ((418, "above block"), (470, "mid block"), (514, "below block")):
    print(f"  y={yy} ({tag}): " + " ".join(f"{IM[yy, x].tolist()}" for x in range(900, 931, 5)))

print("\n=== letterbox start (x=300, y 512..524) ===")
for y in range(512, 525):
    print(f"  y{y}: {IM[y, 300]}")

print("\n=== emblem top rows (x 566-670) ===")
nonbg = ~((abs(r - 232) < 10) & (abs(g - 232) < 10) & (abs(b - 231) < 12))
for y in range(424, 440):
    xs = np.where(nonbg[y, 566:670])[0]
    if len(xs):
        print(f"  y{y}: n={len(xs)} x {566+xs.min()}-{566+xs.max()}")

print("\n=== sibling frame parity (same masks) ===")
S = np.asarray(Image.open(
    "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_001.jpg"
).convert("RGB")).astype(int)
sr, sg, sb = S[:, :, 0], S[:, :, 1], S[:, :, 2]
sred = (sr > 140) & (sg < 60) & (sb < 60)
ys, xs = np.where(sred[120:200, 150:850])
print(f"sib L1 ink: x {150+xs.min()}-{150+xs.max()} (w {xs.max()-xs.min()+1}), y {120+ys.min()}-{120+ys.max()}")
ys, xs = np.where(sred[190:260, 150:850])
print(f"sib L2 ink: x {150+xs.min()}-{150+xs.max()} (w {xs.max()-xs.min()+1}), y {190+ys.min()}-{190+ys.max()}")
sblue = (sb > 110) & (sr < 90) & (sg < 90)
ys, xs = np.where(sblue[300, :])  # row scan for panel?
# sibling panel edges on row 300:
srow = S[300]
g2 = np.where((abs(srow[:, 0] - 233) < 8) & (abs(srow[:, 1] - 233) < 8))[0]
print(f"sib row 300 gray cols: {g2.min()}-{g2.max()}")
# sibling letterbox?
for y in (515, 518, 520, 530, 536, 539):
    print(f"  sib y{y} @300: {S[y, 300]}")
