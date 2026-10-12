#!/usr/bin/env python3
"""Slide 038 — build aligned crop sheets (render vs original) for dense-region comparisons.
Regions given in slide pt; render (2001x1125) scaled 150/72 px/pt; original (960x540) via
frame transform frame_x = 18.63 + 0.96123*slide_x, frame_y = 0.95556*slide_y."""
from PIL import Image, ImageDraw

QA = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide038/"
REN = QA + "render_1.png"
ORIG = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_038.jpg"

ren = Image.open(REN).convert("RGB")
orig = Image.open(ORIG).convert("RGB")
RW = ren.width / (150 / 72.0)  # 960.48 slide pt wide

def crop_ren(x0, y0, x1, y1):
    s = 150 / 72.0
    return ren.crop((int(x0 * s), int(y0 * s), int(x1 * s), int(y1 * s)))

def crop_orig(x0, y0, x1, y1):
    fx = lambda p: 18.63 + 0.96123 * p
    fy = lambda p: 0.95556 * p
    return orig.crop((int(fx(x0)), int(fy(y0)), int(fx(x1)), int(fy(y1))))

REGIONS = {
    "R1_title":      (200, 58, 820, 106),
    "R2_defbox":     (70, 108, 885, 254),
    "R3_graybar":    (150, 296, 890, 342),
    "R4_caption":    (245, 486, 575, 538),
    "R5_toprow":     (150, 258, 620, 298),
    "R6_plusrow12":  (165, 328, 320, 370),
    "R7_tails":      (715, 252, 885, 505),
    "R8_annotations":(35, 350, 180, 508),
}

def sheet(names, out, target_w=1500):
    imgs = []
    for n in names:
        x0, y0, x1, y1 = REGIONS[n]
        a = crop_ren(x0, y0, x1, y1)
        b = crop_orig(x0, y0, x1, y1)
        # scale both to the same width
        w = target_w if n != "R7_tails" else 700
        a = a.resize((w, int(a.height * w / a.width)), Image.LANCZOS)
        b = b.resize((w, int(b.height * w / b.width)), Image.LANCZOS)
        imgs.append((n, a, b))
    lab, pad = 30, 8
    H = sum(a.height + b.height + lab + pad + 14 for _, a, b in imgs) + pad
    canvas = Image.new("RGB", (target_w + 20, H), (255, 255, 255))
    dr = ImageDraw.Draw(canvas)
    y = pad
    for n, a, b in imgs:
        dr.rectangle([0, y, canvas.width, y + lab - 4], fill=(0, 0, 160))
        dr.text((8, y + 7), f"[{n}] TOP=RECREATION  BOTTOM=ORIGINAL  (same slide region)", fill=(255, 255, 0))
        y += lab
        canvas.paste(a, (10, y)); y += a.height + 6
        canvas.paste(b, (10, y)); y += b.height + pad + 8
    canvas.save(QA + out)
    print(out, canvas.size)

sheet(["R1_title", "R2_defbox", "R3_graybar", "R4_caption"], "crops_text.png")
sheet(["R5_toprow", "R6_plusrow12", "R7_tails", "R8_annotations"], "crops_diagram.png")
