#!/usr/bin/env python3
"""Crops for dense-region vision comparisons: same frame-px window from the render
(mapped via fx=18.63+0.96123*sx, fy=0.95556*sy) and the original frame, both scaled
to the original crop's 2x size (identical pixel dims)."""
from PIL import Image
BASE="/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2"
ren = Image.open(f"{BASE}/recreated_pptx/qa/slide029/render_1.png").convert("RGB")
org = Image.open(f"{BASE}/unique_slides/slide_029.jpg").convert("RGB")
def crop_pair(name, x0, y0, x1, y1):
    ow, oh = (x1-x0)*2, (y1-y0)*2
    o = org.crop((x0, y0, x1, y1)).resize((ow, oh), Image.LANCZOS)
    rx0 = round((x0-18.63)/0.96123*150/72); rx1 = round((x1-18.63)/0.96123*150/72)
    ry0 = round(y0*2.18028); ry1 = round(y1*2.18028)
    r = ren.crop((rx0, ry0, rx1, ry1)).resize((ow, oh), Image.LANCZOS)
    o.save(f"crops/{name}_orig.png"); r.save(f"crops/{name}_render.png")
    print(name, "orig", o.size, "render->", r.size, f"(render window {rx0},{ry0},{rx1},{ry1})")
crop_pair("callout", 48, 380, 402, 514)     # NEW callout box (dense small text)
crop_pair("bottomsector", 380, 420, 800, 514)  # arcs 8-10, heads, labels k7m/k8/k9/k10
crop_pair("title1", 55, 50, 340, 100)       # title line 1 "12" delta
