#!/usr/bin/env python3
"""Two smaller composites (4 crops each) for the structural read."""
from PIL import Image, ImageDraw
BASE = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide055/crops"
groups = {
    "compA": ["c1_title", "c2_leftgroup", "c3_dotprod", "c4_scaling_softmax"],
    "compB": ["c5_sigma_O", "c6_rightgroup", "c7_query_zrow", "c8_caption_legend"],
}
for out_name, names in groups.items():
    imgs = []
    for n in names:
        im = Image.open(f"{BASE}/{n}.png")
        w = 1000
        h = int(im.height * w / im.width)
        imgs.append((n, im.resize((w, h), Image.LANCZOS)))
    PAD, LBL = 12, 30
    total_h = sum(im.height + LBL + PAD for _, im in imgs) + PAD
    comp = Image.new("RGB", (1000 + 2 * PAD, total_h), (255, 255, 255))
    d = ImageDraw.Draw(comp)
    y = PAD
    for i, (n, im) in enumerate(imgs, 1):
        d.text((PAD + 4, y + 6), f"{n}", fill=(200, 0, 0))
        y += LBL
        comp.paste(im, (PAD, y))
        d.rectangle([PAD, y, PAD + im.width - 1, y + im.height - 1], outline=(180, 180, 180))
        y += im.height + PAD
    p = f"{BASE.rsplit('/crops', 1)[0]}/{out_name}.png"
    comp.save(p)
    print(p, comp.size)
