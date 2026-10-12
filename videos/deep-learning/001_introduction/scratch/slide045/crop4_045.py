#!/usr/bin/env python3
"""crop4_045.py — attempt-4 dense-region crops for slide 045 (mandatory self-check 6).
Crops BOTH render_4.png (150dpi) and the original frame at 4 documented frame-px
regions; the original crop is upscaled x2 (LANCZOS) per the banked crop-payload
convention (crop_payload_eq.txt). Banked as cropcmp4_* in qa/slide045/.
Regions (frame px, 1px=1pt):
  eq_a    x460..700  y292..378   (eq (a) whole: tokens x471..694 y312..366)
  eq_b    x495..665  y376..424   (eq (b) whole: tokens x510..654 y386..415.7)
  eq_c    x415..700  y410..499   (eq (c) whole: tokens x423..677 y423..490.6)
  legend  x62..268   y346..442   (legend box x71..261 y354..435 + margin)
"""
from PIL import Image

QA = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/qa/slide045"
REN = f"{QA}/render_4.png"
ORG = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_045.jpg"

REGIONS = {
    "eq_a": (460, 700, 292, 378),
    "eq_b": (495, 665, 376, 424),
    "eq_c": (415, 700, 410, 499),
    "legend": (62, 268, 346, 442),
}

ren = Image.open(REN).convert("RGB")
org = Image.open(ORG).convert("RGB")
s = ren.height / 540.0
for name, (x0, x1, y0, y1) in REGIONS.items():
    oc = org.crop((x0, y0, x1, y1)).resize(((x1 - x0) * 2, (y1 - y0) * 2), Image.LANCZOS)
    oc.save(f"{QA}/cropcmp4_{name}_original.png")
    rc = ren.crop((round(x0 * s), round(y0 * s), round(x1 * s) + 1, round(y1 * s) + 1))
    rc.save(f"{QA}/cropcmp4_{name}_render.png")
    print(name, "orig", oc.size, "render", rc.size)
