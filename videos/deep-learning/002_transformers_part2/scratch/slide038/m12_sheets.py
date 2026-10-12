#!/usr/bin/env python3
"""Compose labeled contact sheets from the banked slide-038 crops for vision clarification."""
from PIL import Image, ImageDraw

D = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide038/"
OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide038/"

def sheet(items, out, width=1400):
    imgs = []
    for name in items:
        im = Image.open(D + name + ".png").convert("RGB")
        if im.width > width:
            im = im.resize((width, int(im.height * width / im.width)), Image.LANCZOS)
        imgs.append((name, im))
    pad = 8
    lab_h = 34
    H = sum(im.height + lab_h + pad for _, im in imgs) + pad
    canvas = Image.new("RGB", (width, H), (255, 255, 255))
    dr = ImageDraw.Draw(canvas)
    y = pad
    for name, im in imgs:
        dr.rectangle([0, y, width, y + lab_h - 4], fill=(180, 0, 0))
        dr.text((10, y + 8), f"[{name}]", fill=(255, 255, 0))
        y += lab_h
        canvas.paste(im, (0, y))
        y += im.height + pad
    canvas.save(OUT + out)
    print(out, canvas.size)

sheet(["z_toprow", "z_plusrow", "z_layernorm", "z_midrow", "z_xrow",
       "hh_col2_full", "hh_col2_bar", "hh_arrow_blk"], "sheetA_structure.png")
sheet(["z_tail_top", "z_tail_mid", "z_tail_x", "z_caption", "z_annotations",
       "z_title", "z_defbox1", "z_defbox2", "hh_bar_left", "hh_bar_right"], "sheetB_text.png")
