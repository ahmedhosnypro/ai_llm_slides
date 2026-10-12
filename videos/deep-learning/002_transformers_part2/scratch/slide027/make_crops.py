#!/usr/bin/env python3
"""Create crop pairs (render + original) for dense-region comparisons.
Mapping: render_x = (fx-18.63)*2.1680 ; render_y = fy*2.1801 (render 2001x1125)."""
from PIL import Image
import os

VID = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2"
ren = Image.open(f"{VID}/recreated_pptx/qa/slide027/render_5.png").convert("RGB")
orig = Image.open(f"{VID}/unique_slides/slide_027.jpg").convert("RGB")
outd = f"{VID}/recreated_pptx/qa/slide027/crops"
os.makedirs(outd, exist_ok=True)

def rx(fx): return int(round((fx - 18.63) * 2.1680))
def ry(fy): return int(round(fy * 2.1801))

crops = {
    "eqbox": (72, 172, 226, 256),
    "topband": (440, 40, 800, 175),
    "rightband": (680, 155, 865, 325),
}
for name, (fx0, fy0, fx1, fy1) in crops.items():
    rb = (rx(fx0), ry(fy0), rx(fx1), ry(fx1) if False else ry(fy1))
    rc = ren.crop(rb)
    oc = orig.crop((fx0, fy0, fx1, fy1))
    rc2 = rc.resize((rc.width * 2, rc.height * 2), Image.LANCZOS)
    oc2 = oc.resize((oc.width * 2, oc.height * 2), Image.LANCZOS)
    rc2.save(f"{outd}/{name}_render.png")
    oc2.save(f"{outd}/{name}_original.png")
    print(name, "render", rb, rc2.size, "original", (fx0, fy0, fx1, fy1), oc2.size)
