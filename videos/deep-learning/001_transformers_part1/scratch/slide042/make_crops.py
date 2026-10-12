#!/usr/bin/env python3
"""Self-check 6 (dense-region crops): cut IDENTICAL frame-px regions from the
original frame and the 150dpi render, upscale x4, save paired crops for
analyze_image.py comparison. Also prints per-crop ink-band numbers."""
import sys
import numpy as np
from PIL import Image

ORIG = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_042.jpg"
REND = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/qa/slide042/render_1.png"
OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/scratch/slide042"

S = 1125 / 540.0  # render px per frame px

REGIONS = [
    # (name, x0, y0, x1, y1) in frame px
    ("line2_math", 415, 276, 625, 318),
    ("line1_quote", 355, 226, 415, 258),
    ("line3_Yr", 770, 338, 835, 372),
]

o = Image.open(ORIG).convert("RGB")
r = Image.open(REND).convert("RGB")

for name, x0, y0, x1, y1 in REGIONS:
    w, h = x1 - x0, y1 - y0
    oc = o.crop((x0, y0, x1, y1)).resize((w * 4, h * 4), Image.LANCZOS)
    rc = r.crop((int(x0 * S), int(y0 * S), int(x1 * S), int(y1 * S))).resize((w * 4, h * 4), Image.LANCZOS)
    oc.save(f"{OUT}/cmp_{name}_orig.png")
    rc.save(f"{OUT}/cmp_{name}_rend.png")
    print(f"{name}: orig crop {w*4}x{h*4}, render crop {w*4}x{h*4} (region x{x0}-{x1} y{y0}-{y1})")

# ink-band numbers per region (red/green/blue masks, both images)
def masks(a, scale):
    im = np.asarray(a).astype(int)
    rr, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]
    red = (rr - g > 60) & (rr - b > 60) & (rr > 110)
    green = (g - rr > 40) & (g - b > 40) & (g > 90)
    blue = (b - rr > 50) & (b - g > 30)
    return red, green, blue

mo = masks(o, 1.0)
mr = masks(r, S)
for name, x0, y0, x1, y1 in REGIONS:
    print(f"-- {name} region x{x0}-{x1} y{y0}-{y1}")
    for lbl, m1, m2 in [("red", mo[0], mr[0]), ("green", mo[1], mr[1]), ("blue", mo[2], mr[2])]:
        b1 = m1[y0:y1, x0:x1]
        b2 = m2[int(y0 * S):int(y1 * S), int(x0 * S):int(x1 * S)]
        n1, n2 = b1.sum(), b2.sum()
        def ext(mm, sc, yo, xo):
            ys, xs = np.where(mm)
            if not len(ys):
                return None
            return (round(xs.min() / sc + xo, 1), round(xs.max() / sc + xo, 1),
                    round(ys.min() / sc + yo, 1), round(ys.max() / sc + yo, 1))
        print(f"   {lbl}: orig n={n1} bbox={ext(b1, 1.0, y0, x0)}  render n={n2} bbox={ext(b2, S, y0, x0)}")
