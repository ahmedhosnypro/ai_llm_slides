#!/usr/bin/env python3
"""Slide 055 dense-region crop pairs — EQUAL SCALE (P4 §8): resize the RENDER crop to the
ORIGINAL crop's pixel grid, then upscale both x3. Pairs: fraction, Kstrips, Zrow, Legend, QWq."""
from PIL import Image
import os, json

VID = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2"
ORIG = f"{VID}/unique_slides/slide_055.jpg"
REN = f"{VID}/recreated_pptx/qa/slide055/render_8.png"
OUT = f"{VID}/scratch/slide055/crops"
os.makedirs(OUT, exist_ok=True)

# render is 150dpi (2001x1125); map frame->render via rx/ry
X0, SX, SY = 18.63, 0.96123, 0.95556
F = 2001 / 960.0
def rx(fx): return (fx - X0) / SX * F
def ry(fy): return fy / SY * F

REGIONS = {
    "pair_frac":    (404, 179, 476, 226),
    "pair_kstrip":  (228, 214, 300, 366),
    "pair_zrow":    (208, 434, 542, 502),
    "pair_legend":  (730, 420, 905, 512),
    "pair_qwq":     (293, 384, 372, 456),
}
orig = Image.open(ORIG).convert("RGB")
ren = Image.open(REN).convert("RGB")
manifest = {}
for name, (fx0, fy0, fx1, fy1) in REGIONS.items():
    oc = orig.crop((fx0, fy0, fx1, fy1))
    # render crop on the same slide region
    rb = (int(rx(fx0)), int(ry(fy0)), int(rx(fx1)), int(ry(fy1)))
    rc = ren.crop(rb).resize(oc.size, Image.LANCZOS)
    z = 3
    oc3 = oc.resize((oc.width * z, oc.height * z), Image.LANCZOS)
    rc3 = rc.resize((oc.width * z, oc.height * z), Image.LANCZOS)
    pair = Image.new("RGB", (oc3.width * 2 + 12, oc3.height + 8), (255, 255, 255))
    pair.paste(oc3, (0, 4))
    pair.paste(rc3, (oc3.width + 12, 4))
    p = f"{OUT}/{name}.png"
    pair.save(p)
    manifest[name] = {"box": [fx0, fy0, fx1, fy1], "pair": p}
print(json.dumps(manifest, indent=1))
