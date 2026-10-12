#!/usr/bin/env python3
"""Composite of the 8 zoomed crops, labeled C1..C8, for the batched structural vision read."""
from PIL import Image, ImageDraw

BASE = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide055/crops"
names = ["c1_title", "c2_leftgroup", "c3_dotprod", "c4_scaling_softmax",
         "c5_sigma_O", "c6_rightgroup", "c7_query_zrow", "c8_caption_legend"]
imgs = []
for n in names:
    im = Image.open(f"{BASE}/{n}.png")
    # normalize width to 1200 for legibility
    w = 1200
    h = int(im.height * w / im.width)
    imgs.append((n, im.resize((w, h), Image.LANCZOS)))

PAD = 14
LBL = 34
total_h = sum(im.height + LBL + PAD for _, im in imgs) + PAD
comp = Image.new("RGB", (1200 + 2 * PAD, total_h), (255, 255, 255))
d = ImageDraw.Draw(comp)
y = PAD
for i, (n, im) in enumerate(imgs, 1):
    d.text((PAD + 4, y + 8), f"C{i}  ({n})", fill=(200, 0, 0))
    y += LBL
    comp.paste(im, (PAD, y))
    d.rectangle([PAD, y, PAD + im.width - 1, y + im.height - 1], outline=(180, 180, 180))
    y += im.height + PAD
out = f"{BASE.rsplit('/crops', 1)[0]}/composite_055.png"
comp.save(out)
print(out, comp.size)
