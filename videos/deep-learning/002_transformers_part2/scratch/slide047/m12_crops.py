#!/usr/bin/env python3
"""m12_crops.py — compose labeled crop sheets for gate vision reads."""
from PIL import Image, ImageDraw

F = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_047.jpg'
im = Image.open(F).convert('RGB')
OUT = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide047/'

def crop(x0, y0, x1, y1, scale=4):
    c = im.crop((x0, y0, x1, y1))
    return c.resize((c.width * scale, c.height * scale), Image.LANCZOS)

def sheet(name, parts, gap=14, labels=True):
    """parts: list of (PIL image, caption). Stack vertically."""
    W = max(p.width for p, _ in parts) + 20
    H = sum(p.height + (34 if labels else 0) for p, _ in parts) + gap * (len(parts) + 1)
    s = Image.new('RGB', (W, H), (255, 255, 255))
    d = ImageDraw.Draw(s)
    y = gap
    for p, cap in parts:
        if labels:
            d.text((10, y), cap, fill=(0, 0, 0))
            y += 34
        s.paste(p, (10, y))
        d.rectangle([9, y - 1, 10 + p.width, y + p.height], outline=(200, 60, 60))
        y += p.height + gap
    s.save(OUT + name)
    print(name, s.size)

# Sheet 1: label rows
sheet('sheet_labels.png', [
    (crop(150, 40, 345, 95, 4), 'TOP OUTPUT ROW cols1-2 (x150-345, y40-95) x4'),
    (crop(150, 474, 345, 520, 4), 'BOTTOM INPUT ROW cols1-2 (x150-345, y474-520) x4'),
    (crop(150, 168, 345, 200, 4), 'INTERNAL ROW A cols1-2 (x150-345, y168-200) x4'),
    (crop(150, 380, 345, 420, 4), 'INTERNAL ROW C cols1-2 + block arrows (x150-345, y380-420) x4'),
])

# Sheet 2: texts
t = im.crop((70, 115, 130, 510)).rotate(-90, expand=True)  # vertical title -> horizontal
t = t.resize((t.width * 2, t.height * 2), Image.LANCZOS)
sheet('sheet_texts.png', [
    (crop(380, 96, 680, 136, 3), 'LAYER NORM BAR 1 TEXT (x380-680, y96-136) x3'),
    (crop(240, 202, 820, 234, 2), 'FFN HEADER TEXT (x240-820, y202-234) x2'),
    (crop(360, 420, 700, 470, 2), 'MHA BAR TEXT (x360-700, y420-470) x2'),
    (t, 'VERTICAL TITLE x70-130 y115-510, rotated to horizontal, x2'),
    (crop(48, 40, 185, 88, 4), 'BLOCK OUTPUT BOX (x48-185, y40-88) x4'),
    (crop(48, 474, 185, 520, 4), 'BLOCK INPUT BOX (x48-185, y474-520) x4'),
])

# Sheet 3: details
sheet('sheet_details.png', [
    (crop(150, 222, 258, 268, 5), 'FFN TILE 1 (x150-258, y222-268) x5'),
    (crop(140, 88, 330, 178, 3), 'DASHED CONTAINER 1 top-left + PLUS disc + residual curve (x140-330, y88-178) x3'),
    (crop(590, 50, 740, 82, 3), 'TOP ROW ELLIPSIS DOTS (x590-740, y50-82) x3'),
    (crop(590, 168, 740, 200, 3), 'ROW A ELLIPSIS DOTS (x590-740, y168-200) x3'),
    (crop(590, 475, 740, 515, 3), 'BOTTOM ROW ELLIPSIS DOTS (x590-740, y475-515) x3'),
])
