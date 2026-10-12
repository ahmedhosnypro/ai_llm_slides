#!/usr/bin/env python3
"""m08_crops.py — generate zoomed crops (x2) of ambiguous regions for vision probes."""
from PIL import Image
import os

FR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_051.jpg"
OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide051/crops"
os.makedirs(OUT, exist_ok=True)
im = Image.open(FR).convert("RGB")

CROPS = {
    # name: (x0, y0, x1, y1)
    "enc_stack":    (176, 226, 312, 350),   # yellow box, text, container, boxes, red shapes, QKV
    "enc_midleft":  (138, 290, 218, 354),   # green check, red shape (Nx?)
    "enc_lower":    (176, 338, 302, 406),   # PE icon + label + marks
    "enc_bottom":   (148, 394, 302, 502),   # Output Embedding + side text + arrow + labels
    "dec_top":      (700, 98, 892, 200),    # Output, Probabilities, Softmax, Linear, ellipses
    "dec_stacktop": (712, 184, 852, 318),   # container top: blue band, dark block, gray, yellow bar
    "dec_stackbot": (712, 298, 852, 402),   # blue box, purple MaskedMHA, QKV
    "dec_bottom":   (712, 394, 856, 506),   # brown box, texts, yellow box
    "callout34":    (558, 278, 748, 372),   # callouts 3+4 + arrows
    "title":        (180, 46, 792, 94),     # title text
}
for name, (x0, y0, x1, y1) in CROPS.items():
    c = im.crop((x0, y0, x1, y1))
    w, h = c.size
    c2 = c.resize((w * 2, h * 2), Image.LANCZOS)
    p = f"{OUT}/{name}.png"
    c2.save(p)
    print(name, (x0, y0, x1, y1), "->", c2.size, p)
