#!/usr/bin/env python3
"""Generate zoom crops of slide_049 regions for visual inspection."""
from PIL import Image

F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_049.jpg"
im = Image.open(F).convert("RGB")

def crop(name, x0, y0, x1, y1, scale=6):
    c = im.crop((x0, y0, x1, y1))
    c = c.resize((c.width * scale, c.height * scale), Image.LANCZOS)
    c.save(f"/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide049/crop_{name}.png")
    print(name, c.size)

crop("gray_arrow", 195, 452, 290, 482, 8)
crop("red_arrow_mid", 190, 262, 290, 286, 8)
crop("green_arrow", 190, 100, 290, 128, 8)
crop("blue_arrow", 190, 393, 290, 418, 8)
crop("xtoken1", 168, 368, 245, 400, 8)
crop("ytoken1", 168, 80, 245, 112, 8)
crop("xtail", 715, 368, 880, 400, 5)
crop("ytail", 715, 80, 880, 112, 5)
crop("dots_row_y", 600, 82, 740, 108, 6)
crop("dots_row_x", 600, 372, 740, 398, 6)
crop("wordrow_1", 160, 472, 330, 512, 5)
crop("leftcol_top", 52, 45, 155, 130, 5)
crop("leftcol_mid", 52, 120, 155, 380, 3)
crop("leftcol_bot", 52, 375, 155, 520, 5)
crop("title", 240, 42, 790, 82, 2)
crop("emb_bars", 155, 408, 885, 470, 2)
crop("blockM_text", 380, 128, 660, 165, 4)
crop("x_row_full", 155, 370, 890, 400, 2)
crop("y_row_full", 155, 82, 890, 112, 2)
