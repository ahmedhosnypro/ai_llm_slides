#!/usr/bin/env python3
"""Probe 5: bullet stem-width mode (regular vs bold), Carlito check, marker geometry."""
import json
from collections import Counter

import numpy as np
from PIL import Image

IM = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_006.jpg"
im = np.asarray(Image.open(IM).convert("RGB")).astype(int)
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]
out = {}

# bullet text mask: blue-ish ink (loose) — stems of lowercase letters
blue = (b - np.maximum(r, g)) > 30
BANDS = {1: (197, 212), 3: (250, 265), 6: (328, 343), 8: (382, 395), 11: (459, 474)}
allruns = Counter()
for k, (y0, y1) in BANDS.items():
    for yy in range(y0 + 3, y1 - 2):
        m = blue[yy, 205:560]
        idx = np.where(m)[0]
        if not len(idx):
            continue
        s = p = idx[0]
        rr = []
        for v in idx[1:]:
            if v <= p + 1:
                p = v
            else:
                rr.append(p - s + 1)
                s = p = v
        rr.append(p - s + 1)
        allruns.update(rr)
out["bullet_run_width_hist"] = sorted((int(k), int(v)) for k, v in allruns.items())

# header stem widths for comparison (TNR 24 known)
dark = (r < 140) & (g < 140) & (b < 140)
hruns = Counter()
for yy in range(145, 154):
    idx = np.where(dark[yy, 94:700])[0]
    if not len(idx):
        continue
    s = p = idx[0]
    for v in idx[1:]:
        if v <= p + 1:
            p = v
        else:
            hruns[p - s + 1] += 1
            s = p = v
    hruns[p - s + 1] += 1
out["header_run_width_hist"] = sorted((int(k), int(v)) for k, v in hruns.items())

# marker geometry precise: all 12 markers, threshold r<170, x 176..190
dk = (r < 170) & (g < 170) & (b < 170)
rows = [201, 228, 254, 280, 306, 332, 359, 385, 411, 437, 463, 489]
mks = []
for cy in rows:
    win = dk[cy - 5:cy + 6, 174:192]
    ys, xs = np.where(win)
    if len(ys):
        mks.append({
            "bbox": [int(xs.min()) + 174, int(ys.min()) + cy - 5, int(xs.max()) + 174, int(ys.max()) + cy - 5],
            "cx": round(float(xs.min() + xs.max()) / 2 + 174, 1),
            "cy": round(float(ys.min() + ys.max()) / 2 + cy - 5, 1),
            "d": int(max(xs.max() - xs.min(), ys.max() - ys.min()) + 1),
        })
out["markers"] = mks

print(json.dumps(out, indent=1))
