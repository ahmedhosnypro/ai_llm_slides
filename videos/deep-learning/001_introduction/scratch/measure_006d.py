#!/usr/bin/env python3
"""Probe 4: font ID via mask correlation, least-squares size solves, bullet-12 forensics."""
import json
from collections import Counter

import numpy as np
from PIL import Image, ImageDraw, ImageFont

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

def adv(fontname, size, text):
    return ImageFont.truetype(FONTS[fontname], size).getlength(text)

# ---- (a) title font ID: correlate original ink mask vs PIL-rendered masks ----
TITLE = "Machine Learning in the real-world"
# original title ink mask, tight-cropped
tm = (r - np.maximum(g, b)) > 60
reg = tm[80:128, 143:833]
ys, xs = np.where(reg)
tmask = reg[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
TH, TW = tmask.shape

def render_mask(fontname, size, text):
    f = ImageFont.truetype(FONTS[fontname], size)
    img = Image.new("L", (int(f.getlength(text)) + 40, int(size * 1.6)), 0)
    d = ImageDraw.Draw(img)
    d.text((20, int(size * 0.2)), text, font=f, fill=255)
    m = np.asarray(img) > 128
    ys2, xs2 = np.where(m)
    return m[ys2.min():ys2.max() + 1, xs2.min():xs2.max() + 1]

def iou(A, B):
    # resize B to A's shape via PIL nearest
    bi = Image.fromarray((B * 255).astype(np.uint8)).resize((A.shape[1], A.shape[0]), Image.LANCZOS)
    Bm = np.asarray(bi) > 128
    inter = (A & Bm).sum()
    union = (A | Bm).sum()
    return inter / union

cands = {}
for fn, sizes in [("ArialBold", range(40, 46)), ("TNRBold", range(42, 48))]:
    best = None
    for s in sizes:
        m = render_mask(fn, s, TITLE)
        score = iou(tmask, m)
        if best is None or score > best[1]:
            best = (s, score)
    cands[fn] = best
out["title_font_id"] = {k: [v[0], round(v[1], 4)] for k, v in cands.items()}

# ---- (b) header solves ----
H1 = "Broadly applicable in many domains (e.g., finance, robotics,"
PHRASE = "Broadly applicable in many domains"
H2 = "bioinformatics, vision, natural language, etc.). Some applications:"
sols = {}
for fn in ["TNR", "TNRBold", "Arial", "ArialBold"]:
    rows = []
    for size10 in range(200, 275, 5):
        s = size10 / 10
        rows.append([s, round(adv(fn, int(round(s * 4)), H1) * (s / (int(round(s * 4)) / 4)), 1),
                     round(adv(fn, int(round(s * 4)), PHRASE) * (s / (int(round(s * 4)) / 4)), 1),
                     round(adv(fn, int(round(s * 4)), H2) * (s / (int(round(s * 4)) / 4)), 1)])
    sols[fn] = rows
out["header_solves_598_375_625"] = sols

# ---- (c) bullet solves: ink widths measured ----
BL = {
    1: ("Spam filtering", 106), 3: ("Speech/handwriting recognition", 244),
    4: ("Object detection/recognition", 217), 5: ("Weather prediction", 146),
    6: ("Classifying DNA sequences", 216), 7: ("Stock market analysis", 170),
    8: ("Automatic vehicle navigation", 222), 9: ("Search engines (e.g., Google)", 228),
    10: ("Credit-card fraud detection", 207), 11: ("Webpage clustering (e.g., Google News)", 316),
}
bsols = {}
for fn in ["Arial", "ArialBold"]:
    err_by_size = []
    for size10 in range(150, 205, 5):
        s = size10 / 10
        tot = 0.0
        for k, (txt, ink) in BL.items():
            a = adv(fn, int(round(s * 4)), txt) * (s / (int(round(s * 4)) / 4))
            tot += abs(a - 3 - ink) / ink  # advance minus ~3px bearings vs ink
        err_by_size.append([s, round(tot / len(BL) * 100, 2)])
    bsols[fn] = err_by_size
out["bullet_size_solve_pcterr"] = bsols

# ---- (d) bullet 12 forensics with looser threshold ----
nonbg = ~((r > 235) & (g > 235) & (b > 235))
reg12 = nonbg[478:503, 175:420]
ys12, xs12 = np.where(reg12)
out["b12_full_bbox"] = [int(xs12.min()) + 175, int(ys12.min()) + 478, int(xs12.max()) + 175, int(ys12.max()) + 478] if len(ys12) else None
sel12 = im[478:503, 175:420][reg12]
out["b12_ink_modal_all"] = [[int(v) for v in c] + [int(k)] for c, k in Counter(map(tuple, sel12)).most_common(8)]
# darkest quartile modal (true color estimate)
luma = sel12 @ [299, 587, 114] / 1000.0
idx = np.argsort(luma)[: max(1, int(len(luma) * 0.2))]
out["b12_dark20_modal"] = [[int(v) for v in c] + [1] for c, _ in Counter(map(tuple, sel12[idx])).most_common(5)]
out["b12_blue_any"] = int(((b - np.maximum(r, g)) > 40)[478:503, 175:420].sum())

# does an ascender exist above x-height? column profile rows 478..490 x 210..350
colprof = [(int(x) + 175, [int(v) for v in nonbg[478:494, x].nonzero()[0] + 478]) for x in range(210, 260, 2)]
out["b12_col_probe"] = colprof

# bullet12 advance solve
B12 = ".. and many more"
rows12 = []
for size10 in range(150, 205, 5):
    s = size10 / 10
    rows12.append([s, round(adv("Arial", int(round(s * 4)), B12) * (s / (int(round(s * 4)) / 4)), 1)])
out["b12_solve_ink119"] = rows12

# ---- (e) line-2 ink recheck: exclude stray pixels ----
dark = (r < 160) & (g < 160) & (b < 160)
m2 = dark[163:190, 90:760]
xs2c = np.where(m2.sum(axis=0) > 1)[0]
out["h2_x_gt1px"] = [int(xs2c.min()) + 90, int(xs2c.max()) + 90] if len(xs2c) else None
m1 = dark[138:156, 90:760]
xs1c = np.where(m1.sum(axis=0) > 1)[0]
out["h1_x_gt1px"] = [int(xs1c.min()) + 90, int(xs1c.max()) + 90] if len(xs1c) else None

# ---- (f) title ink center with 2px-count threshold ----
tmc = tm[80:128, :]
tcols = np.where(tmc.sum(axis=0) > 1)[0]
out["title_cols_gt1"] = [int(tcols.min()), int(tcols.max()), int((tcols.min() + tcols.max()) / 2)]

print(json.dumps(out, indent=1))
