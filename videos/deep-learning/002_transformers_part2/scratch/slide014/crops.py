#!/usr/bin/env python3
# crops.py — zoom crops (z_*.png) of every dense region, 2-6x, for gated reads.
import os
os.environ.setdefault("TMPDIR", os.path.dirname(os.path.abspath(__file__)))
from PIL import Image

BASE = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2'
OUT = os.path.dirname(os.path.abspath(__file__))
im = Image.open(BASE + '/unique_slides/slide_014.jpg').convert('RGB')

CROPS = [
    # name, (fx0, fy0, fx1, fy1), zoom
    ("z_badge",        (852, 46, 912, 96), 6),
    ("z_title",        (180, 46, 822, 80), 2),
    ("z_subtitle_L",   (110, 72, 460, 108), 3),
    ("z_subtitle_R",   (455, 72, 910, 108), 3),
    ("z_fanlabels",    (52, 48, 175, 180), 4),
    ("z_nn_top",       (60, 110, 300, 210), 3),
    ("z_nn_mid",       (60, 210, 300, 320), 3),
    ("z_nn_bottom",    (60, 320, 300, 516), 3),
    ("z_weights_top",  (130, 130, 230, 220), 4),
    ("z_sigma1",       (215, 135, 300, 200), 4),
    ("z_sigma4_clip",  (215, 440, 300, 516), 4),
    ("z_wheatbox",     (300, 122, 910, 256), 2),
    ("z_wheat_lines",  (310, 138, 660, 250), 3),
    ("z_y_row1",       (292, 258, 462, 310), 4),
    ("z_y_linear",     (292, 335, 540, 385), 4),
    ("z_connector1",   (440, 265, 545, 300), 5),
    ("z_x_row1",       (525, 258, 670, 305), 4),
    ("z_x_row3",       (525, 335, 670, 382), 4),
    ("z_x_col_labels", (520, 250, 560, 515), 4),
    ("z_matrix_full",  (660, 280, 845, 470), 3),
    ("z_matrix_row3",  (660, 385, 845, 445), 5),
    ("z_zero_plus",    (830, 285, 912, 470), 4),
    ("z_brace_R",      (872, 245, 912, 515), 4),
    ("z_brace_L",      (508, 240, 556, 516), 4),
    ("z_container_TL", (56, 70, 180, 145), 4),
    ("z_container_TR", (870, 70, 910, 145), 4),
    ("z_container_BL", (56, 480, 180, 518), 4),
    ("z_left_panel_div", (280, 110, 310, 516), 4),
]
for name, (x0, y0, x1, y1), z in CROPS:
    c = im.crop((x0, y0, x1, y1))
    c = c.resize((c.width * z, c.height * z), Image.LANCZOS)
    c.save(os.path.join(OUT, name + ".png"))
    print(name, c.size, f"fx{x0}..{x1} fy{y0}..{y1} x{z}")
