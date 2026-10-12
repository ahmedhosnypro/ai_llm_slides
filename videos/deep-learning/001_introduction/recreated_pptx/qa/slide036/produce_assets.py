#!/usr/bin/env python3
# produce_assets.py (attempt 1) — slide 036 asset generation.
# Crops: three tiles from the ground-truth frame (edge-safety verified in measure5_out.txt):
#   A slabtop036.png   (158,160)-(402,220)  RGB label + slab top tip (intertwined ink -> one tile)
#   B slabbody036.png  (158,219)-(380,394)  slab body + cyan column + 3dims + 7 labels + dashes to x377
#   C filterunit036.png(378,240)-(499,409)  dash end + blue X + filter slab + '3'/'7' + arrow-to-3
# A/B tile at y=219/220 (B drawn after A, identical source pixels -> seamless);
# C overlaps B at x 378..380 (identical pixels). Dash phase: B ends in gap 377..383, C
# resumes at 384 -> no drawn dashes needed anywhere.
# Equation: scripts/render_eq.py '7 \;\cdot\; 7 \;\cdot\; 3 \;=\; 147' eq_147_036.png 32 #D42A2A
#   (32pt joint fit: ink w 253.4px vs measured 254, ink h 24.2 vs 22; \; spacing matches
#    the original's wide marker spacing; professional-format law 2026-10-09)
from PIL import Image
import os, subprocess
FR = "videos/deep-learning/001_introduction/unique_slides/slide_036.jpg"
A = "videos/deep-learning/001_introduction/recreated_pptx/build/assets"
im = Image.open(FR).convert("RGB")
crops = [
    ("slabtop036.png",   158, 160, 403, 221),
    ("slabbody036.png",  158, 219, 381, 395),
    ("filterunit036.png",378, 240, 500, 410),
]
for name, x1, y1, x2, y2 in crops:
    im.crop((x1, y1, x2, y2)).save(os.path.join(A, name))
    print(name, x1, y1, x2 - 1, y2 - 1, "w", x2 - x1, "h", y2 - y1)
