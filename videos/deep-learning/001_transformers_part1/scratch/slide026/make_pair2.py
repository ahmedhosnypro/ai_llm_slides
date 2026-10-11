#!/usr/bin/env python3
from PIL import Image, ImageDraw
PANELS = [
    ("B nodes+W labels upper", (488, 220, 700, 300), 3),
    ("B2 nodes lower", (488, 300, 700, 395), 3),
    ("C Ybox+arrow+Sigma+WSum", (480, 110, 700, 230), 3),
    ("D strip glyphs+X2", (170, 462, 350, 525), 3),
    ("H red block arrow zone", (250, 495, 320, 540), 4),
]
W = 1800
for tag, path in (("render", "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/qa/slide026/render_1.png"),
                  ("orig", "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_026.jpg")):
    IM = Image.open(path).convert("RGB")
    if IM.size != (960, 540):
        IM = IM.resize((960, 540), Image.LANCZOS)
    tiles, y = [], 0
    for label, box, sc in PANELS:
        crop = IM.crop(box)
        crop = crop.resize((crop.width * sc, crop.height * sc), Image.LANCZOS)
        tiles.append((label, crop)); y += crop.height + 30
    comp = Image.new("RGB", (W, y + 6), (255, 255, 255))
    d = ImageDraw.Draw(comp)
    y = 0
    for label, crop in tiles:
        d.rectangle([0, y, W, y + 22], fill=(228, 228, 248))
        d.text((6, y + 4), label, fill=(0, 0, 0))
        comp.paste(crop, (0, y + 26))
        y += crop.height + 30
    comp.save(f"cropcomp2_{tag}.png")
    print(f"cropcomp2_{tag}.png", comp.size)
