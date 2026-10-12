#!/usr/bin/env python3
"""Composite crop sheet of slide_055.jpg ambiguous regions, upscaled x4, labeled."""
from PIL import Image, ImageDraw

SRC = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_055.jpg"
img = Image.open(SRC).convert("RGB")

# (name, x0, y0, x1, y1, zoom)
crops = [
    ("A-left-hatch+arrow", 60, 168, 200, 222, 4),
    ("B-right-hatch+arrow", 755, 168, 900, 222, 4),
    ("C-left-Ycontainer", 95, 215, 190, 385, 3),
    ("D-Wk+Kstrips", 195, 215, 295, 385, 3),
    ("E-Wvboxes", 690, 215, 780, 385, 3),
    ("F-right-Ycontainer", 770, 215, 865, 385, 3),
    ("G-dotprod-top+Kq+pill", 280, 148, 410, 240, 3),
    ("H-fraction", 438, 178, 488, 225, 5),
    ("I-O-sigma-squares", 515, 100, 700, 245, 3),
    ("J-Zrow", 210, 450, 530, 515, 3),
    ("K-Wq-q2", 280, 385, 375, 460, 4),
    ("L-caption+arrow", 510, 450, 690, 500, 3),
    ("M-legend", 720, 425, 890, 505, 3),
]
Z = 4
tiles = []
for name, x0, y0, x1, y1, z in crops:
    c = img.crop((x0, y0, x1, y1))
    c = c.resize((c.width * z, c.height * z), Image.LANCZOS)
    tiles.append((name, c))

cols = 3
pad = 14
label_h = 26
colw = []
rows = [[] for _ in range((len(tiles) + cols - 1) // cols)]
for i, (name, c) in enumerate(tiles):
    rows[i // cols].append((name, c))
W = max(sum(c.width for _, c in r) + pad * (len(r) + 1) for r in rows) + 10
H = sum(max(c.height for _, c in r) + label_h + pad for r in rows) + pad
sheet = Image.new("RGB", (W, H), (255, 255, 255))
d = ImageDraw.Draw(sheet)
y = pad
for r in rows:
    x = pad
    rh = max(c.height for _, c in r)
    for name, c in r:
        d.rectangle([x, y, x + c.width, y + label_h - 4], fill=(200, 30, 30))
        d.text((x + 6, y + 6), name, fill=(255, 255, 255))
        sheet.paste(c, (x, y + label_h))
        d.rectangle([x, y + label_h, x + c.width, y + label_h + c.height], outline=(120, 120, 120), width=2)
        x += c.width + pad
    y += rh + label_h + pad
out = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide055/composite_055.png"
sheet.save(out)
print(out, sheet.size)
