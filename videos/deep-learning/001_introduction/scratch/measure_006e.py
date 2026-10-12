#!/usr/bin/env python3
"""Probe 4b: clean unhinted advance solves (large-size / N trick) + bullet-12 forensics."""
import json
from collections import Counter

import numpy as np
from PIL import Image, ImageFont

IM = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_006.jpg"
im = np.asarray(Image.open(IM).convert("RGB")).astype(int)
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]
out = {}

FONTS = {
    "Arial": "/usr/share/fonts/liberation/LiberationSans-Regular.ttf",
    "ArialBold": "/usr/share/fonts/liberation/LiberationSans-Bold.ttf",
    "TNR": "/usr/share/fonts/liberation/LiberationSerif-Regular.ttf",
    "TNRBold": "/usr/share/fonts/liberation/LiberationSerif-Bold.ttf",
}
BIG = 720  # 10x scale: getlength(BIG)/10 = unhinted pt advance

def adv(fn, size, text):
    return ImageFont.truetype(FONTS[fn], BIG).getlength(text) * size / BIG / 10.0 if False else \
        ImageFont.truetype(FONTS[fn], int(BIG * size / 72)).getlength(text) * 72 / (BIG * size / 72) * size / 72

# simpler: em-units via huge render then scale
def adv2(fn, size, text):
    f = ImageFont.truetype(FONTS[fn], 2880)  # 2880pt = 40x of 72
    return f.getlength(text) / 2880 * size

# sanity
out["sanity"] = {
    "TNR24_H1": round(adv2("TNR", 24, "Broadly applicable in many domains (e.g., finance, robotics,"), 1),
    "ArialBold42_TITLE": round(adv2("ArialBold", 42, "Machine Learning in the real-world"), 1),
}

H1 = "Broadly applicable in many domains (e.g., finance, robotics,"
PHRASE = "Broadly applicable in many domains"
H2 = "bioinformatics, vision, natural language, etc.). Some applications:"
sols = {}
for fn in ["TNR", "TNRBold", "Arial", "ArialBold"]:
    rows = []
    for s10 in range(195, 265, 5):
        s = s10 / 10
        rows.append([s, round(adv2(fn, s, H1), 1), round(adv2(fn, s, PHRASE), 1), round(adv2(fn, s, H2), 1)])
    sols[fn] = rows
out["header_solves"] = sols

BL = {
    1: ("Spam filtering", 106), 3: ("Speech/handwriting recognition", 244),
    4: ("Object detection/recognition", 217), 5: ("Weather prediction", 146),
    6: ("Classifying DNA sequences", 216), 7: ("Stock market analysis", 170),
    8: ("Automatic vehicle navigation", 222), 9: ("Search engines (e.g., Google)", 228),
    10: ("Credit-card fraud detection", 207), 11: ("Webpage clustering (e.g., Google News)", 316),
}
bsols = {}
for fn in ["Arial", "ArialBold"]:
    rows = []
    for s10 in range(150, 205, 5):
        s = s10 / 10
        tot = 0.0
        for k, (txt, ink) in BL.items():
            a = adv2(fn, s, txt)
            tot += abs(a - 3 - ink) / ink
        rows.append([s, round(tot / len(BL) * 100, 2)])
    bsols[fn] = rows
out["bullet_solve_pcterr"] = bsols

# per-line advances at candidate sizes for the best font (filled after inspection)
A16 = {k: round(adv2("Arial", 16, t), 1) for k, (t, i) in BL.items()}
A17 = {k: round(adv2("Arial", 17, t), 1) for k, (t, i) in BL.items()}
A18 = {k: round(adv2("Arial", 18, t), 1) for k, (t, i) in BL.items()}
out["a16"] = A16
out["a17"] = A17
out["a18"] = A18

# bullet 12
B12 = ".. and many more"
out["b12_adv"] = {s: round(adv2("Arial", s, B12), 1) for s in [16, 17, 17.5, 18, 19]}

# bullet-12 full forensics (looser threshold)
nonbg = ~((r > 235) & (g > 235) & (b > 235))
reg12 = nonbg[476:503, 175:420]
ys12, xs12 = np.where(reg12)
out["b12_full_bbox"] = [int(xs12.min()) + 175, int(ys12.min()) + 476, int(xs12.max()) + 175, int(ys12.max()) + 476] if len(ys12) else None
sel12 = im[476:503, 175:420][reg12]
darkest = sel12[np.argsort(sel12 @ [299, 587, 114])[: max(1, int(len(sel12) * 0.2))]]
out["b12_dark20_modal"] = [[int(v) for v in c] + [1] for c, _ in Counter(map(tuple, darkest)).most_common(5)]

# header recheck with threshold 160
dark = (r < 160) & (g < 160) & (b < 160)
m1 = dark[138:157, 90:760]
xs1c = np.where(m1.sum(axis=0) > 1)[0]
out["h1_x_gt1"] = [int(xs1c.min()) + 90, int(xs1c.max()) + 90] if len(xs1c) else None
m2 = dark[163:190, 90:760]
xs2c = np.where(m2.sum(axis=0) > 1)[0]
out["h2_x_gt1"] = [int(xs2c.min()) + 90, int(xs2c.max()) + 90] if len(xs2c) else None

# title columns with >1 count
tm = (r - np.maximum(g, b)) > 60
tcols = np.where(tm[80:128, :].sum(axis=0) > 1)[0]
out["title_cols_gt1"] = [int(tcols.min()), int(tcols.max()), int((int(tcols.min()) + int(tcols.max())) / 2)]

# title cap exact: rows with >5 red px
trows = np.where(tm[80:128, 143:833].sum(axis=1) > 5)[0] + 80
out["title_rows_gt5"] = [int(trows.min()), int(trows.max())]

print(json.dumps(out, indent=1))
