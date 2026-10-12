#!/usr/bin/env python3
"""Slide 045 — build zoom contact sheets for vision reads (sheet A text, sheet B details)."""
from PIL import Image, ImageDraw

F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_045.jpg"
img = Image.open(F).convert("RGB")

def crop_scale(box, s):
    c = img.crop(box)
    return c.resize((int(c.width * s), int(c.height * s)), Image.LANCZOS)

def sheet(name, items, out):
    # items: list of (label, PIL image)
    W = max(im.width for _, im in items) + 20
    H = sum(im.height + 34 for _, im in items) + 10
    s = Image.new("RGB", (W, H), (30, 30, 30))
    d = ImageDraw.Draw(s)
    y = 5
    for label, im in items:
        d.text((10, y), label, fill=(255, 220, 0))
        y += 24
        s.paste(im, (10, y))
        d.rectangle([9, y - 1, 10 + im.width, y + im.height], outline=(255, 80, 80))
        y += im.height + 10
    s.save(out)
    print(out, s.size)

# Sheet A: text zones
a1 = crop_scale((85, 76, 892, 160), 2.0)     # annot box
a2 = crop_scale((160, 302, 880, 342), 2.0)   # gray bar
a3 = crop_scale((260, 492, 570, 516), 3.0)   # caption
a4 = crop_scale((160, 196, 890, 222), 2.5)   # FFN title row
sheet("A", [("ZONE 1: annotation box (frame 85..892 x 76..160, x2) — read every word and each word's color",
             a1),
            ("ZONE 2: gray LayerNorm bar (frame 160..880 x 302..342, x2) — read the exact text and colors",
             a2),
            ("ZONE 3: bottom caption (frame 260..570 x 492..516, x3) — read exactly; are there UNDERSCORE characters between words?",
             a3),
            ("ZONE 4: FFN box title row (frame 160..890 x 196..222, x2.5) — read the title exactly (note double spaces)",
             a4)],
      "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide045/sheetA_text.png")

# Sheet B: detail zones
b1 = crop_scale((190, 370, 330, 402), 4.0)   # cont-row strips 1-2 + labels
b2 = crop_scale((190, 266, 330, 300), 4.0)   # mid-row strips 1-2 + labels
b3 = crop_scale((192, 340, 222, 368), 8.0)   # plus circle 1
b4 = crop_scale((180, 214, 330, 258), 5.0)   # FFN icons 1-2
b5 = crop_scale((700, 214, 890, 258), 5.0)   # FFN icons 7-8 (right end)
sheet("B", [("ZONE 1: container Y-row strips 1-2 (frame 190..330 x 370..402, x4) — read each strip's label letter+subscript EXACTLY (is there an apostrophe/prime?), the small colored cells and their order",
             b1),
            ("ZONE 2: middle Y-row strips 1-2 (frame 190..330 x 266..300, x4) — same questions",
             b2),
            ("ZONE 3: residual plus circle 1 (frame 192..222 x 340..368, x8) — describe fill, ring, and the + glyph and its color",
             b3),
            ("ZONE 4: FFN mini-network icons 1-2 (frame 180..330 x 214..258, x5) — describe each icon: tile background color, dots (how many, color, where), connecting lines (color, shape), any RELU text/pill (color, position)",
             b4),
            ("ZONE 5: FFN icons at the right end (frame 700..890 x 214..258, x5) — how many icons, the blue dots between them (how many), tile details",
             b5)],
      "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide045/sheetB_detail.png")
