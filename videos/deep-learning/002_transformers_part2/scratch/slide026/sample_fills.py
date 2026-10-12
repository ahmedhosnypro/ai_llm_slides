#!/usr/bin/env python3
"""Sample exact pixel colors at suspected block centers + find white panel edges."""
from PIL import Image
import numpy as np

F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_026.jpg"
img = Image.open(F).convert("RGB")
a = np.asarray(img).astype(int)

pts = {
    "blue_box_fill": (300, 300), "white_subblock": (300, 262), "white_subblock2": (300, 375),
    "host_mcu_bar": (403, 300), "tida_fill": (550, 300), "dual_adc": (497, 262),
    "amp_tri_up": (560, 262), "amp_tri_mid": (560, 335), "comparators": (520, 412),
    "power_supplies": (492, 432), "box24V": (403, 432), "enc_conn_bar": (657, 320),
    "right_round_fill": (760, 300), "diff_box": (760, 256), "syncos_box": (765, 412),
    "ac_motor": (805, 378), "pos_arrow": (170, 300), "white_panel": (600, 200),
    "panel_bg": (300, 150), "canvas_bg": (30, 30),
    "title_ink": (300, 67), "subtitle_ink": (300, 92),
    "caption_l1": (400, 498), "caption_l2": (400, 511),
}
for k, (x, y) in pts.items():
    print(f"{k:>18} ({x},{y}): {tuple(a[y, x])}")

# white panel bbox: pure white region boundaries. Scan row y=200 and column x=600
r, g, b = a[..., 0], a[..., 1], a[..., 2]
white = (r > 235) & (g > 235) & (b > 235)
row = white[200, :]
xs = np.nonzero(row)[0]
print("\nwhite row y=200 x-extent:", xs.min(), xs.max())
col = white[:, 600]
ys = np.nonzero(col[100:520])[0] + 100
print("white col x=600 y-extent (in 100..520):", ys.min(), ys.max())
# panel edge more precisely: check row y=170 (above blocks) and y=460
for yy in (160, 170, 460, 466):
    xs2 = np.nonzero(white[yy, :])[0]
    if len(xs2):
        print(f"white row y={yy}: x {xs2.min()}..{xs2.max()} n={len(xs2)}")
for xx in (250, 850):
    ys2 = np.nonzero(white[100:520, xx])[0] + 100
    if len(ys2):
        print(f"white col x={xx}: y {ys2.min()}..{ys2.max()} n={len(ys2)}")
