#!/usr/bin/env python3
"""Closed-loop fidelity diff: render_1.png (2001x1125 @150dpi) vs slide_017.jpg frame.
frame->render mapping: rx = (fx-AX)/SX * (2001/960); ry = (fy-AY)/SY * (1125/540).
Reports changed-pixel density per slide-coordinate tile (40x30px tiles) so deltas
outside the 4 known zones are enumerable. READ-ONLY (does not touch banked evidence)."""
from PIL import Image
import numpy as np

VID = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2"
R = np.asarray(Image.open(f"{VID}/recreated_pptx/qa/slide017/render_1.png").convert("RGB")).astype(np.int16)
F = np.asarray(Image.open(f"{VID}/unique_slides/slide_017.jpg").convert("RGB")).astype(np.int16)
AX, SX, AY, SY = 18.250, 0.96150, 1.950, 0.95500
KW, KH = R.shape[1] / 960.0, R.shape[0] / 540.0  # render px per slide pt

# resample render to slide grid (960x540)
Rs = np.asarray(Image.open(f"{VID}/recreated_pptx/qa/slide017/render_1.png").convert("RGB")
                .resize((960, 540), Image.LANCZOS)).astype(np.int16)

# frame resampled onto the slide grid via the mapping
xs = (np.arange(960) * SX + AX).round().astype(int).clip(0, 959)
ys = (np.arange(540) * SY + AY).round().astype(int).clip(0, 539)
Fs = F[np.ix_(ys, xs)]

diff = np.abs(Rs - Fs).sum(axis=2)
changed = diff > 90  # strong ink-level differences only

print("total changed px (slide grid):", int(changed.sum()))
zones = {
    "title+numeral": (490, 40, 915, 105),
    "ff_left": (86, 295, 262, 450),
    "ff_right": (415, 295, 625, 450),
    "swoosh_zone": (545, 300, 815, 500),
    "label_zone": (595, 370, 725, 430),
}
mask = np.zeros_like(changed)
for name, (x0, y0, x1, y1) in zones.items():
    mask[y0:y1, x0:x1] = True
outside = changed & ~mask
print("changed inside zones:", int((changed & mask).sum()), " OUTSIDE:", int(outside.sum()))
print("\nper-tile hotspot map (40x30 tiles, >=60 changed px marked #):")
for ty in range(0, 540, 30):
    row = ""
    for tx in range(0, 960, 40):
        n = int(outside[ty:ty+30, tx:tx+40].sum())
        row += "#" if n >= 60 else ("+" if n >= 20 else ".")
    print(f"  y{ty:3d} {row}")
print("\ntiles with >=60 px (slide coords):")
for ty in range(0, 540, 30):
    for tx in range(0, 960, 40):
        n = int(outside[ty:ty+30, tx:tx+40].sum())
        if n >= 60:
            print(f"  tile x{tx}..{tx+40} y{ty}..{ty+30}: {n}")
