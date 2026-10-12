#!/usr/bin/env python3
"""Slide 038 — sheet C: high-zoom single-element crops for decisive structure reads."""
from PIL import Image, ImageDraw

F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_038.jpg"
OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide038/"
img = Image.open(F).convert("RGB")

crops = {
    "c01_top_col1":  (183, 255, 245, 300, 9),   # top bar col1 + red label + red arrow
    "c02_top_col2":  (246, 255, 308, 300, 9),   # top bar col2
    "c03_mid_col2":  (246, 348, 308, 402, 9),   # mid bar + label below + arrow top
    "c04_x_col2":    (246, 448, 308, 488, 9),   # X bar + blue label above
    "c05_plus_col2": (243, 312, 313, 356, 9),   # green arrows + plus circle + orange head
    "c06_navy_left": (146, 395, 310, 472, 6),   # navy left edge + blue block arrows + X labels
    "c07_tail_top":  (742, 256, 856, 300, 8),   # top-row tail labels Y(N-1), Y(N)
    "c08_tail_mid":  (742, 378, 856, 402, 8),   # mid-row tail labels
    "c09_tail_x":    (742, 450, 856, 488, 8),   # X-row tail labels
    "c10_orange":    (150, 333, 300, 478, 5),   # orange residual arrows col1-2
    "c11_graybar_left": (58, 286, 345, 328, 5), # container left border + bar left + text start
    "c12_toprow_wide": (180, 250, 720, 300, 3), # top row cols 1-7 wide context
}
items = []
for name, (x0, y0, x1, y1, k) in crops.items():
    c = img.crop((x0, y0, x1, y1))
    c = c.resize((c.width * k, c.height * k), Image.LANCZOS)
    items.append((name, c))
    print(name, c.size)

width = max(im.width for _, im in items) + 20
pad, lab_h = 10, 40
H = sum(im.height + lab_h + pad for _, im in items) + pad
canvas = Image.new("RGB", (width, H), (255, 255, 255))
dr = ImageDraw.Draw(canvas)
y = pad
for name, im in items:
    dr.rectangle([0, y, width, y + lab_h - 6], fill=(180, 0, 0))
    dr.text((10, y + 10), f"[{name}]", fill=(255, 255, 0))
    y += lab_h
    canvas.paste(im, (10, y))
    y += im.height + pad
canvas.save(OUT + "sheetC_zoom.png")
print("sheetC_zoom.png", canvas.size)
