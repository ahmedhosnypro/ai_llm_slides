#!/usr/bin/env python3
"""Build a labeled composite crop sheet from 002:slide_008.jpg for the
build-time zoom re-checks (SOURCES.md [?] items + label/color reads)."""
from PIL import Image, ImageDraw

SRC = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_008.jpg"
OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide008/crops_orig_sheet.png"

im = Image.open(SRC).convert("RGB")

# (label, x0, y0, x1, y1, scale, caption)
CROPS = [
    ("A", 135, 208, 258, 266, 3, "W_k box row1 + K4 vector"),
    ("B", 630, 208, 762, 266, 3, "W_v box row1 + V4 vector"),
    ("C", 243, 373, 357, 482, 3, "query path: q2 / W_q box / arrows"),
    ("D", 493, 198, 662, 387, 3, "all 4 multiply nodes + stems"),
    ("E", 526, 103, 634, 157, 3, "Y output strip + label"),
    ("F", 316, 174, 380, 214, 4, "K.q corner + DP top-right"),
    ("G", 173, 438, 502, 517, 2, "sentence row X1..X4 + red arrow"),
    ("H", 158, 220, 216, 258, 6, "W_k box1 label ZOOM"),
]

panels = []
for (lbl, x0, y0, x1, y1, s, cap) in CROPS:
    c = im.crop((x0, y0, x1, y1))
    c = c.resize((c.width * s, c.height * s), Image.LANCZOS)
    panels.append((lbl, c, cap))

pad = 14
label_h = 34
rows = [
    [("A", 0), ("B", 1), ("E", 4), ("F", 5)],
    [("C", 2), ("D", 3)],
    [("G", 6)],
    [("H", 7)],
]
widths = []
total_w = 0
total_h = pad
for row in rows:
    w = pad
    h = 0
    for (lbl, idx) in row:
        c = panels[idx][1]
        w += c.width + pad
        h = max(h, c.height + label_h)
    widths.append((w, h))
    total_w = max(total_w, w)
    total_h += h + pad

sheet = Image.new("RGB", (total_w, total_h), (255, 255, 255))
draw = ImageDraw.Draw(sheet)
y = pad
for row, (w, h) in zip(rows, widths):
    x = pad
    for (lbl, idx) in row:
        c = panels[idx][1]
        cap = panels[idx][2]
        draw.rectangle([x - 2, y - 2, x + c.width + 2, y + c.height + label_h + 2], outline=(200, 0, 0), width=2)
        draw.text((x + 4, y + 2), f"[{lbl}] {cap}", fill=(0, 0, 200))
        sheet.paste(c, (x, y + label_h))
        x += c.width + pad
    y += h + pad

sheet.save(OUT)
print("sheet:", OUT, sheet.size)
