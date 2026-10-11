#!/usr/bin/env python3
"""Create upscaled crops for vision reads."""
from PIL import Image
import os

IMG = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_033.jpg"
OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/scratch/slide033/crops"
os.makedirs(OUT, exist_ok=True)
im = Image.open(IMG).convert("RGB")

CROPS = [
    # name, (x0, y0, x1, y1), scale
    ("A_weightedsum_row1", (480, 212, 700, 262), 6),
    ("B_dotproduct", (248, 188, 352, 410), 4),
    ("C_leftbox_row1", (56, 230, 146, 264), 7),
    ("D_vrow1", (628, 224, 752, 248), 7),
    ("E_krow1", (198, 226, 262, 264), 7),
    ("F_wkbox1", (146, 224, 204, 294), 7),
    ("G_y2box", (534, 108, 624, 174), 7),
    ("H_legend", (730, 458, 912, 538), 5),
    ("I_sentence", (168, 456, 500, 540), 4),
    ("J_q2wq", (258, 394, 352, 476), 6),
    ("K_pills", (262, 152, 692, 192), 4),
    ("L_softmax_bar", (452, 190, 496, 408), 5),
    ("M_sigma_box", (506, 188, 668, 236), 6),
    ("N_title", (180, 50, 830, 102), 2),
    ("O_wsum_all_rows", (480, 212, 700, 400), 4),
    ("P_rightbox_row1", (758, 230, 850, 264), 7),
    ("Q_kcol_labels", (198, 226, 262, 396), 5),
    ("R_inputcol_left", (52, 220, 146, 400), 4),
]
for name, box, scale in CROPS:
    c = im.crop(box)
    w, h = c.size
    c = c.resize((w * scale, h * scale), Image.LANCZOS)
    p = f"{OUT}/{name}.png"
    c.save(p)
    print(name, box, "->", c.size, p)
