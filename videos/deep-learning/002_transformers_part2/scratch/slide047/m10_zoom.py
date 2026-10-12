#!/usr/bin/env python3
"""m10_zoom.py — high-zoom strips of slide_047 for structural disambiguation."""
from PIL import Image, ImageDraw

F = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_047.jpg'
im = Image.open(F).convert('RGB')
crops = [
    ('Z1 col1 x185-235 y128-215 (post-FFN row: cells+below-zone+FFN top) 6x', (185, 128, 235, 215), 6),
    ('Z2 col1 x185-235 y340-425 (plus disc, out-row, below-zone, MHA top) 6x', (185, 340, 235, 425), 6),
    ('Z3 col8 x810-865 y128-215 6x', (810, 128, 865, 215), 6),
    ('Z4 FFN unit1 x192-248 y224-266 6x', (192, 224, 248, 266), 6),
    ('Z5 plus disc col1 x188-228 y134-166 8x', (188, 134, 228, 166), 8),
    ('Z6 zone2 arrow col1 x185-235 y462-495 6x', (185, 462, 235, 495), 6),
    ('Z7 X row col1 x178-242 y474-516 6x', (178, 474, 242, 516), 6),
    ('Z8 output row col1 x178-242 y48-94 6x', (178, 48, 242, 94), 6),
    ('Z9 LN bar left end x150-260 y96-136 5x', (150, 96, 260, 136), 5),
]
S_default = 6
imgs = []
maxw = 0
for label, box, S in crops:
    c = im.crop(box)
    c = c.resize((c.width * S, c.height * S), Image.LANCZOS)
    imgs.append((label, c))
    maxw = max(maxw, c.width)
seph = 26
H = sum(c.height for _, c in imgs) + seph * len(imgs)
out = Image.new('RGB', (maxw, H), (0, 0, 0))
d = ImageDraw.Draw(out)
y = 0
for label, c in imgs:
    d.text((6, y + 6), label, fill=(255, 255, 0))
    y += seph
    out.paste(c, (0, y))
    y += c.height
out.save('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide047/zoom_047.png')
print('saved', out.size)
