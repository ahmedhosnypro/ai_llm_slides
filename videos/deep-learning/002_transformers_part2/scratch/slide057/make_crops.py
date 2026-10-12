#!/usr/bin/env python3
"""Zoom crops (z_*.png) of slide_057 dense regions, 2-6x nearest-neighbor."""
import os
from PIL import Image
BASE = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2"
OUT = os.path.join(BASE, "scratch", "slide057")
im = Image.open(os.path.join(BASE, "unique_slides", "slide_057.jpg")).convert("RGB")

CROPS = [
    # name           box (l, t, r, b)            zoom
    ("z_badge",          (850, 40, 915, 105),     6),
    ("z_panel_topleft",  (28, 30, 90, 90),        6),
    ("z_panel_topright", (880, 30, 940, 90),      6),
    ("z_encoder_label",  (44, 230, 100, 380),     4),
    ("z_y_row",          (95, 105, 460, 140),     3),
    ("z_stack_top",      (95, 130, 460, 230),     2),
    ("z_stack_mid",      (95, 230, 460, 340),     2),
    ("z_stack_bottom",   (95, 330, 460, 385),     2),
    ("z_x_row",          (95, 375, 460, 410),     3),
    ("z_words_bars",     (95, 405, 460, 515),     3),
    ("z_column_top",     (445, 95, 560, 200),     4),
    ("z_column_kv",      (495, 145, 565, 290),    4),
    ("z_column_lower",   (495, 290, 565, 430),    4),
    ("z_caption",        (455, 420, 545, 500),    4),
    ("z_decoder_top",    (555, 40, 860, 130),     3),
    ("z_decoder_blk1",   (555, 125, 860, 215),    3),
    ("z_decoder_blk2",   (555, 210, 860, 300),    3),
    ("z_decoder_blk3",   (555, 295, 860, 400),    3),
    ("z_decoder_blk4",   (555, 395, 860, 515),    3),
    ("z_decoder_label",  (830, 220, 870, 350),    4),
    ("z_q_badge",        (815, 380, 860, 450),    6),
    ("z_bottom_strip",   (0, 500, 960, 540),      2),
]
for name, box, z in CROPS:
    c = im.crop(box)
    c = c.resize((c.width * z, c.height * z), Image.NEAREST)
    c.save(os.path.join(OUT, name + ".png"))
    print(f"{name}.png  box={box} zoom={z} -> {c.size}")
print("DONE")
