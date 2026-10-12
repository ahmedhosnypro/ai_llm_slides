#!/usr/bin/env python3
"""prep_crops.py — dense-region crop pairs (render vs original) + pixel measures.
Pattern: dense-region-crop-compare. Same region box in both spaces (render box =
frame box x 150/72), upscaled x4 (A,B) / x2 (C)."""
import numpy as np
from PIL import Image

QA = "videos/deep-learning/001_introduction/recreated_pptx/qa/slide035"
REND = f"{QA}/render_2.png"
FR = "videos/deep-learning/001_introduction/unique_slides/slide_035.jpg"
S = 150 / 72.0

ren = Image.open(REND).convert("RGB")
fr = Image.open(FR).convert("RGB")

REGIONS = {
    "A_filter_grid":   ((262, 210, 372, 298), 4),
    "B_panel_yellow3x3": ((398, 193, 585, 335), 4),
    "C_caption_l2":    ((75, 472, 515, 508), 2),
}

def measure(a, label):
    r, g, b = a[:, :, 0].astype(int), a[:, :, 1].astype(int), a[:, :, 2].astype(int)
    out = {}
    out["yellow"] = int(((r > 200) & (g > 190) & (b < 160)).sum())
    out["green"] = int(((g - r > 60) & (g - b > 40) & (g > 90)).sum())
    out["red"] = int(((r - g > 50) & (r - b > 50) & (r > 110)).sum())
    out["navy"] = int(((b - r > 40) & (b > 100)).sum())
    out["dark"] = int(((r < 110) & (g < 110) & (b < 110)).sum())
    print(f"  {label}: " + " ".join(f"{k}={v}" for k, v in out.items()))
    return out

print("=== crop pairs + pixel measures (rebuttal numbers) ===")
for name, ((x0, y0, x1, y1), up) in REGIONS.items():
    rx0, ry0, rx1, ry1 = [int(round(v * S)) for v in (x0, y0, x1, y1)]
    rc = ren.crop((rx0, ry0, rx1, ry1))
    fc = fr.crop((x0, y0, x1, y1))
    rc2 = rc.resize((rc.width * up, rc.height * up), Image.LANCZOS)
    fc2 = fc.resize((fc.width * up, fc.height * up), Image.LANCZOS)
    rc2.save(f"{QA}/crop_render_{name}.png")
    fc2.save(f"{QA}/crop_orig_{name}.png")
    print(f"{name}: frame box ({x0},{y0})-({x1},{y1}) render box ({rx0},{ry0})-({rx1},{ry1}) upscale x{up}")
    print(f"  sizes: render crop {rc2.size}, orig crop {fc2.size}")
    measure(np.asarray(rc2), "render")
    measure(np.asarray(fc2), "orig  ")
print("done")
