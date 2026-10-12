#!/usr/bin/env python3
# g4_crops.py — save zoomed crops of every decision-relevant region into
# scratch/slide016/ (evidence for visual transcription; NO writes outside).
from PIL import Image

FR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_016.jpg"
OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide016/"
im = Image.open(FR).convert("RGB")

CROPS = [
    ("crop_headers.png",    (300, 108, 800, 136), 3),
    ("crop_embed_rows.png", (60, 126, 320, 316), 2),
    ("crop_matrix_h1.png",  (296, 108, 470, 316), 2),
    ("crop_output_g1.png",  (288, 324, 452, 516), 2),
    ("crop_captions.png",   (300, 480, 800, 512), 3),
    ("crop_summary.png",    (50, 400, 270, 512), 3),
    ("crop_annot1.png",     (826, 320, 915, 372), 4),
    ("crop_badge.png",      (845, 45, 905, 100), 6),
    ("crop_equals.png",     (255, 375, 310, 435), 6),
    ("crop_bracketL.png",   (296, 120, 335, 316), 3),
    ("crop_bracketR.png",   (768, 120, 800, 316), 3),
]
for name, box, zoom in CROPS:
    c = im.crop(box)
    c = c.resize((c.width * zoom, c.height * zoom), Image.LANCZOS)
    c.save(OUT + name)
    print(f"saved {name}  box={box} zoom={zoom} -> {c.width}x{c.height}")
