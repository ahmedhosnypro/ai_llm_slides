#!/usr/bin/env python3
"""Final content forensics for slide_003.jpg:
- any ink outside title/subtitle bands (excluding chrome, badge, letterbox, cursor zone)?
- core color of blue ink (median), gray panel, red border samples
- exact baseline rows (last ink row) per band
"""
import numpy as np
from PIL import Image
import json

SRC = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_003.jpg"
im = Image.open(SRC).convert("RGB")
W, H = im.size
a = np.asarray(im).astype(int)
R, G, B = a[..., 0], a[..., 1], a[..., 2]

# blue-ish (wider net to catch halo): B - R > 40 and B - G > 40
blueish = (B - R > 40) & (B - G > 40) & (B > 100)
ys, xs = np.nonzero(blueish)
out = {"blueish_count": int(len(xs))}
# row histogram -> bands
rowh = np.bincount(ys, minlength=H)
bands = []
inb = False
for y in range(H):
    if rowh[y] > 0 and not inb: s = y; inb = True
    elif rowh[y] == 0 and inb: bands.append((s, y-1)); inb = False
if inb: bands.append((s, H-1))
out["blueish_bands"] = bands
for (y0, y1) in bands:
    m = (ys >= y0) & (ys <= y1)
    out[f"band_{y0}_{y1}"] = {"x0": int(xs[m].min()), "x1": int(xs[m].max())}

# core color of blue ink: pixels with strong blue in the two bands, median
core = blueish & (B - R > 120) & (B > 150)
cys, cxs = np.nonzero(core)
if len(cxs):
    med = [int(np.median(a[cys, cxs, i])) for i in range(3)]
    out["blue_core_median_rgb"] = med
    out["blue_core_hex"] = "".join(f"{v:02X}" for v in med)
    out["blue_core_count"] = int(len(cxs))

# any non-background ink outside bands+chrome? scan y 330..510, x 60..900 for
# pixels far from E9E9E7 gray and not blue (excluding cursor zone x 420..480, y 335..375)
region = a[330:511, 60:901]
rr, gg, bb = region[..., 0], region[..., 1], region[..., 2]
far = (np.abs(rr - 0xE9) > 45) | (np.abs(gg - 0xE9) > 45) | (np.abs(bb - 0xE7) > 45)
# zero out cursor zone (frame ~x 420..480 -> region cols 360..420; y 335..375 -> rows 5..45)
far[5:46, 360:421] = False
count = int(far.sum())
out["nongray_pixels_y330_510_excl_cursor"] = count
if count:
    fys, fxs = np.nonzero(far)
    out["nongray_bbox"] = {"x0": int(fxs.min())+60, "x1": int(fxs.max())+60,
                           "y0": int(fys.min())+330, "y1": int(fys.max())+330}
    # sample a few
    samp = {}
    for i in range(0, min(count, len(fys)), max(1, count//10)):
        samp[f"{fxs[i]+60},{fys[i]+330}"] = [int(v) for v in region[fys[i], fxs[i]]]
    out["nongray_samples"] = samp

# gray panel sample (center-left empty area)
out["gray_sample"] = [int(v) for v in a[400, 200]]
# red border sample
out["red_border_sample"] = [int(v) for v in a[300, 58]], [int(v) for v in a[300, 902]]
# badge fill + ring samples
out["badge_fill_sample"] = [int(v) for v in a[71, 866]]
out["badge_ring_top"] = [int(v) for v in a[56, 875]]
# white margin
out["white_margin_sample"] = [int(v) for v in a[20, 480]]
# black strip
out["black_strip_sample"] = [int(v) for v in a[530, 480]]
# cursor zone ink extent (dark strokes in zone)
cz = a[330:380, 415:485]
cr, cg, cb = cz[...,0], cz[...,1], cz[...,2]
dark = (cr < 120) & (cg < 120) & (cb < 120)
dys, dxs = np.nonzero(dark)
if len(dxs):
    out["cursor_dark_bbox"] = {"x0": int(dxs.min())+415, "x1": int(dxs.max())+415,
                               "y0": int(dys.min())+330, "y1": int(dys.max())+330, "n": int(len(dxs))}

print(json.dumps(out, indent=1))
