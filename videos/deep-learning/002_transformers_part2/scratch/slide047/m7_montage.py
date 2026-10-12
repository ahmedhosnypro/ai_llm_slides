#!/usr/bin/env python3
"""m7_montage.py — labeled 2x montage of slide_047's ambiguous regions."""
from PIL import Image, ImageDraw

F = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_047.jpg'
im = Image.open(F).convert('RGB')

bands = [
    ('A: TOP y40-100 (output row, Block Output box, badge, red arrows)', (40, 40, 915, 100)),
    ('B: TOP-UNIT y95-210 (LN bar, plus discs, cell row, labels)', (120, 95, 910, 210)),
    ('C: FFN y200-270 (container, header, 8 unit boxes)', (120, 200, 910, 270)),
    ('D: BOTTOM y462-520 (X row, block arrows, Block Input box)', (40, 462, 915, 520)),
    ('E: LEFT x40-130 (vertical title, boxes) FULL HEIGHT', (40, 40, 132, 520)),
]
S = 2
crops = []
maxw = 0
for label, box in bands:
    c = im.crop(box)
    c = c.resize((c.width * S, c.height * S), Image.LANCZOS)
    crops.append((label, c))
    maxw = max(maxw, c.width)

seph = 30
H = sum(c.height for _, c in crops) + seph * len(crops)
out = Image.new('RGB', (maxw, H), (0, 0, 0))
d = ImageDraw.Draw(out)
y = 0
for label, c in crops:
    d.text((8, y + 8), label, fill=(255, 255, 0))
    y += seph
    out.paste(c, (0, y))
    y += c.height
out.save('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide047/montage_047.png')
print('montage saved', out.size)
