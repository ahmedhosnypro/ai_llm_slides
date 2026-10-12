#!/usr/bin/env python3
"""Build labeled contact sheets from the existing zoom crops of slide_049."""
from PIL import Image, ImageDraw
import os

BASE = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide049"

def sheet(name, panels, target_w=1400):
    imgs = []
    for label, fname in panels:
        im = Image.open(os.path.join(BASE, fname)).convert("RGB")
        if im.width > target_w:
            ratio = target_w / im.width
            im = im.resize((target_w, int(im.height * ratio)), Image.LANCZOS)
        imgs.append((label, im))
    # label strip height 34
    strips = 34
    total_h = sum(im.height + strips + 8 for _, im in imgs) + 8
    canvas = Image.new("RGB", (target_w, total_h), (255, 255, 255))
    d = ImageDraw.Draw(canvas)
    y = 8
    for label, im in imgs:
        d.rectangle([0, y, target_w, y + strips - 4], fill=(20, 20, 20))
        d.text((10, y + 8), label, fill=(255, 255, 0))
        y += strips
        canvas.paste(im, (0, y))
        y += im.height + 8
    out = os.path.join(BASE, name)
    canvas.save(out)
    print(name, canvas.size)

sheet("sheetA_chips.png", [
    ("PANEL 1: Y row, token chip 0 closeup (original frame, zoomed 8x)", "crop_ytoken1.png"),
    ("PANEL 2: X row, token chip 0 closeup (original frame, zoomed 8x)", "crop_xtoken1.png"),
    ("PANEL 3: Y row right tail - last two chips Y(N-2) Y(N-1), zoomed 5x", "crop_ytail.png"),
    ("PANEL 4: X row right tail - last two chips X(N-2) X(?), zoomed 5x", "crop_xtail.png"),
    ("PANEL 5: Y row ellipsis dots between chip 5 and chip N-2, zoomed 6x", "crop_dots_row_y.png"),
    ("PANEL 6: X row ellipsis dots between chip 5 and chip N-2, zoomed 6x", "crop_dots_row_x.png"),
])

sheet("sheetB_leftcol.png", [
    ("PANEL 1: left column top (Encoder Output box area), zoomed 5x", "crop_leftcol_top.png"),
    ("PANEL 2: left column middle (Transformer Encoder vertical text), zoomed 3x", "crop_leftcol_mid.png"),
    ("PANEL 3: left column bottom (Encoder Input, Embedding Words & Pos., Input Seq), zoomed 5x", "crop_leftcol_bot.png"),
    ("PANEL 4: title band, zoomed 2x", "crop_title.png"),
    ("PANEL 5: top dark bar text (Encoder Block M), zoomed 4x", "crop_blockM_text.png"),
])

sheet("sheetC_arrows.png", [
    ("PANEL 1: green up-arrow (above Y row), zoomed 8x", "crop_green_arrow.png"),
    ("PANEL 2: blue up-arrow (between embedding bars and X row), zoomed 8x", "crop_blue_arrow.png"),
    ("PANEL 3: arrow between Encoder Block 2 and Block 1 (inside stack), zoomed 8x", "crop_red_arrow_mid.png"),
    ("PANEL 4: gray arrow zone between cyan bar and Word row, zoomed 8x", "crop_gray_arrow.png"),
    ("PANEL 5: embedding bars band (Word Embedding tan bar + Positional Encoding cyan bar), zoomed 2x", "crop_emb_bars.png"),
    ("PANEL 6: word row, first two boxes (Word 0, Word 1), zoomed 5x", "crop_wordrow_1.png"),
])
