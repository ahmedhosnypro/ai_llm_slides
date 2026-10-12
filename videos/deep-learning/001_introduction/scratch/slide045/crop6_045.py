#!/usr/bin/env python3
"""crop6_045.py — attempt-6 dense-region crops (mandatory self-check 6) for the three
equation regions on render_6 (the tokens were re-rendered in attempt 5 — the banked
cropcmp4_* crops of render_4 are stale for eq regions). Legend unchanged -> skipped.
Regions identical to crop4_045.py; original crop upscaled x2 (LANCZOS)."""
from PIL import Image

QA = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/qa/slide045"
REN = f"{QA}/render_6.png"
ORG = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_045.jpg"

REGIONS = {
    "eq_a": (460, 700, 292, 378),
    "eq_b": (495, 665, 376, 424),
    "eq_c": (415, 700, 410, 499),
}

ren = Image.open(REN).convert("RGB")
org = Image.open(ORG).convert("RGB")
s = ren.height / 540.0
for name, (x0, x1, y0, y1) in REGIONS.items():
    oc = org.crop((x0, y0, x1, y1)).resize(((x1 - x0) * 2, (y1 - y0) * 2), Image.LANCZOS)
    oc.save(f"{QA}/cropcmp6_{name}_original.png")
    rc = ren.crop((round(x0 * s), round(y0 * s), round(x1 * s) + 1, round(y1 * s) + 1))
    rc.save(f"{QA}/cropcmp6_{name}_render.png")
    print(name, "orig", oc.size, "render", rc.size)
