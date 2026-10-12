#!/usr/bin/env python3
"""Probe 3: header underline structure, bullet-12 extent, font metric solving."""
import json
from collections import Counter

import numpy as np
from PIL import Image

IM = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_006.jpg"
im = np.asarray(Image.open(IM).convert("RGB")).astype(int)
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]
out = {}
dark = (r < 140) & (g < 140) & (b < 140)

# 1. header rows 135..190: per-row dark runs (>=4 px)
def runs_in_row(yy, x0=90, x1=740, minrun=4):
    m = dark[yy, x0:x1]
    idx = np.where(m)[0]
    if not len(idx):
        return []
    rr = []
    s = p = idx[0]
    for v in idx[1:]:
        if v <= p + 2:
            p = v
        else:
            if p - s >= minrun:
                rr.append((int(s) + x0, int(p) + x0))
            s = p = v
    if p - s >= minrun:
        rr.append((int(s) + x0, int(p) + x0))
    return rr

out["header_runs"] = {str(yy): runs_in_row(yy) for yy in range(135, 192)}

# 2. bullet 12: dark ink rows 482..502, x 175..420 columns with ink
m12 = dark[482:503, 175:420]
ys, xs = np.where(m12)
out["b12_bbox"] = [int(xs.min()) + 175, int(ys.min()) + 482, int(xs.max()) + 175, int(ys.max()) + 482] if len(ys) else None
out["b12_runs"] = {str(yy): runs_in_row(yy, 175, 420, 2) for yy in range(482, 503)}
sel = im[482:503, 175:420][m12]
out["b12_dark_modal"] = [[int(v) for v in c] + [int(k)] for c, k in Counter(map(tuple, sel)).most_common(5)]
# check for any blue in line 12 region
blue = (b > 130) & (r < 130) & (g < 130)
out["b12_blue_count"] = int(blue[482:503, 175:420].sum())

# 3. marker 12 center rows 485..497 x 175..190
mm = dark[485:498, 175:192]
ys2, xs2 = np.where(mm)
out["marker12_bbox"] = [int(xs2.min()) + 175, int(ys2.min()) + 485, int(xs2.max()) + 175, int(ys2.max()) + 485] if len(ys2) else None

# 4. font metric solving with PIL
from PIL import ImageFont

def text_advance(fontpath, size, text):
    f = ImageFont.truetype(fontpath, size)
    return f.getlength(text)

FONTS = {
    "Arial": "/usr/share/fonts/liberation/LiberationSans-Regular.ttf",
    "ArialBold": "/usr/share/fonts/liberation/LiberationSans-Bold.ttf",
    "TNR": "/usr/share/fonts/liberation/LiberationSerif-Regular.ttf",
    "TNRBold": "/usr/share/fonts/liberation/LiberationSerif-Bold.ttf",
}
import os
missing = [k for k, v in FONTS.items() if not os.path.exists(v)]
if missing:
    # try alternative dirs
    for k, v in list(FONTS.items()):
        if not os.path.exists(v):
            alt = v.replace("/TTF/", "/truetype/liberation/")
            if os.path.exists(alt):
                FONTS[k] = alt
                missing.remove(k)
out["fonts_missing"] = missing

TITLE = "Machine Learning in the real-world"
sols = {}
for name in ["ArialBold", "TNRBold"]:
    fp = FONTS.get(name)
    if not fp:
        continue
    best = None
    for size in range(36, 50):
        adv = text_advance(fp, size, TITLE)
        d = abs(adv - 689)
        if best is None or d < best[1]:
            best = (size, adv, d)
    sols[name] = best
out["title_solve_689px"] = sols

# bullet solves: line 11 "Webpage clustering (e.g., Google News)" x 205..521 -> 316px ink
# ink width vs advance: advance includes right side bearing; approximate ink ~ advance - ~2px
B11 = "Webpage clustering (e.g., Google News)"
sols2 = {}
for name in ["Arial", "ArialBold"]:
    fp = FONTS.get(name)
    if not fp:
        continue
    rows = []
    for size in range(14, 24):
        adv = text_advance(fp, size, B11)
        rows.append((size, round(adv, 1)))
    sols2[name] = rows
out["b11_solve_316px"] = sols2

B9 = "Search engines (e.g., Google)"  # x 206..434 -> 228px
sols3 = {}
for name in ["Arial", "ArialBold"]:
    fp = FONTS.get(name)
    if not fp:
        continue
    rows = []
    for size in range(14, 24):
        adv = text_advance(fp, size, B9)
        rows.append((size, round(adv, 1)))
    sols3[name] = rows
out["b9_solve_228px"] = sols3

# header line 2 "bioinformatics, vision, natural language, etc.). Some applications:" x 94..719 -> 625px
H2 = "bioinformatics, vision, natural language, etc.). Some applications:"
sols4 = {}
for name in ["TNR", "Arial"]:
    fp = FONTS.get(name)
    if not fp:
        continue
    rows = []
    for size in range(16, 26):
        adv = text_advance(fp, size, H2)
        rows.append((size, round(adv, 1)))
    sols4[name] = rows
out["h2_solve_625px"] = sols4

# header line 1 "Broadly applicable in many domains (e.g., finance, robotics," x 94..? (text-only extent)
# text ink rows 140..154: extent
m1 = dark[140:155, 90:740]
ys3, xs3 = np.where(m1)
out["h1_textonly_x"] = [int(xs3.min()) + 90, int(xs3.max()) + 90] if len(ys3) else None
H1 = "Broadly applicable in many domains (e.g., finance, robotics,"
if len(ys3):
    w1 = int(xs3.max()) - int(xs3.min())
    sols5 = {}
    for name in ["TNR", "Arial"]:
        fp = FONTS.get(name)
        if not fp:
            continue
        rows = []
        for size in range(16, 26):
            adv = text_advance(fp, size, H1)
            rows.append((size, round(adv, 1)))
        sols5[name] = rows
    out["h1_solve"] = {"ink_w": w1, "advances": sols5}

print(json.dumps(out, indent=1))
