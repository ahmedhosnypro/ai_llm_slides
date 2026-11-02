#!/usr/bin/env python3
"""Side-by-side quadrant crops orig vs render_18 for visual adjudication."""
import numpy as np
from PIL import Image

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
Q = NS + "/recreated_pptx/qa/rejudge_20261027/slide025"
S = 2001 / 960.0
orig = Image.open(NS + "/unique_slides/slide_025.jpg").convert("RGB")
ren = Image.open(Q + "/render_18.png").convert("RGB")

REGIONS = {
    "tl": (60, 110, 470, 295),
    "tr": (470, 110, 901, 320),
    "bl": (60, 290, 475, 535),
    "br": (470, 342, 901, 535),
}
for name, (x0, y0, x1, y1) in REGIONS.items():
    co = orig.crop((x0, y0, x1, y1))
    cr = ren.crop((int(x0*S), int(y0*S), int(np.ceil(x1*S))+1, int(np.ceil(y1*S))+1)).resize(co.size, Image.LANCZOS)
    w, h = co.size
    side = Image.new("RGB", (w*2+6, h), (255, 0, 255))
    side.paste(co, (0, 0)); side.paste(cr, (w+6, 0))
    side = side.resize((side.size[0]*2, side.size[1]*2), Image.LANCZOS)
    side.save(f"{Q}/cmp_{name}.png")
    # individual
    co.resize((w*2, h*2), Image.LANCZOS).save(f"{Q}/cmp_{name}_orig.png")
    cr.resize((w*2, h*2), Image.LANCZOS).save(f"{Q}/cmp_{name}_render.png")
    print(name, side.size)
