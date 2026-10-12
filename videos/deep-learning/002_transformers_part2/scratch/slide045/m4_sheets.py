#!/usr/bin/env python3
"""Slide 045 — high-zoom label sheets for text disambiguation (0-based vs 1-based, underscores)."""
from PIL import Image

F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_045.jpg"
img = Image.open(F)
D = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide045/"

def sheet(name, boxes, zoom):
    """boxes: list of (x0,y0,x1,y1) stitched horizontally with separators."""
    crops = [img.crop(b) for b in boxes]
    zc = [c.resize((c.width * zoom, c.height * zoom), Image.LANCZOS) for c in crops]
    W = sum(c.width for c in zc) + 12 * (len(zc) - 1)
    H = max(c.height for c in zc)
    out = Image.new("RGB", (W, H), (40, 40, 40))
    x = 0
    for c in zc:
        out.paste(c, (x, 0)); x += c.width + 12
    out.save(D + name)
    print(name, out.size)

# Row C (container Y row) labels: stacks at approx frame cx 106,179,252,326,398,471 | dots ~500..640 | 660,733
# bar band y 376..398 -> crop label band y 374..400, width 70 around each center
cols = [106, 179, 252, 326, 398, 471, 660, 733]
sheet("sheet_rowC.png", [(c - 38, 372, c + 38, 400) for c in cols], 6)
# Row D (X row): y 478..500
sheet("sheet_rowD.png", [(c - 38, 477, c + 38, 502) for c in cols], 6)
# Row A (top Y row): y 165..188
sheet("sheet_rowA.png", [(c - 38, 163, c + 38, 190) for c in cols], 6)
# Row B (mid Y row): y 271..293
sheet("sheet_rowB.png", [(c - 38, 270, c + 38, 295) for c in cols], 6)
# caption zoom
sheet("sheet_caption.png", [(300, 492, 490, 514)], 6)
# left annotations
sheet("sheet_leftann.png", [(58, 375, 165, 500)], 4)
# FFN title
sheet("sheet_ffntitle.png", [(230, 202, 740, 222)], 3)
