#!/usr/bin/env python3
"""Font metric-solve for slide_032: title, 6 body lines, '2-D Image' label.
Solves LiberationSerif (Times metrics) and Arial, regular+bold, against measured
ink widths; prints per-band row profiles for baseline detection; runs the
ascender-above-cap discriminator on the title.
"""
from PIL import Image, ImageFont
import numpy as np

IM = np.asarray(Image.open(
    "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_032.jpg"
).convert("RGB")).astype(int)
r, g, b = IM[:, :, 0], IM[:, :, 1], IM[:, :, 2]

SERIF = "/usr/share/fonts/liberation/LiberationSerif-Regular.ttf"
SERIFB = "/usr/share/fonts/liberation/LiberationSerif-Bold.ttf"
ARIAL = "/usr/share/fonts/TTF/Arial.TTF"
ARIALB = "/usr/share/fonts/TTF/Arialbd.TTF"
import os
for p in (SERIF, SERIFB, ARIAL, ARIALB):
    print(p, "exists" if os.path.exists(p) else "MISSING")

TARGETS = [
    ("title", "Where to Get Filters for Recognition", 598, True),
    ("L1", "If images are 2-D,", 286 - 95, None),
    ("L2", "parameters should also be organized in 2-D", 573 - 88, None),
    ("L3", "That way they can learn the local", 452 - 88, None),
    ("L4", "correlations between input variables", 493 - 88, None),
    ("L5", "That way they can \u201Cexploit\u201D the spatial", 516 - 88, None),
    ("L6", "nature of images", 274 - 88, None),
    ("label", "2-D Image", 807 - 692, True),
]

def solve(text, target, path):
    best = None
    for size10 in range(140, 481):
        f = ImageFont.truetype(path, size10)
        bb = f.getbbox(text)
        w = bb[2] - bb[0]
        if best is None or abs(w - target * 10) < best[0]:
            best = (abs(w - target * 10), size10 / 10.0, w / 10.0, bb)
    return best

for name, text, target, bold in TARGETS:
    out = [name]
    for label, path in (("serif", SERIFB if bold else SERIF),
                        ("arial", ARIALB if bold else ARIAL)):
        err, size, w, bb = solve(text, target, path)
        out.append(f"{label}: {size:.1f}pt w={w:.1f} (err {err/10:.1f}) bbox={bb}")
    print(" | ".join(out))

# ---- ascender discriminator on the title: 'l' of 'Recognition' vs cap ----
red = (r > 120) & (g < 110) & (b < 110)
# 'Recognition' x 576..773; find its letters: 'l' around x~610..620? print col profile peaks
print("\nRecognition columns (x576..773) red rows per 6px col:")
for x in range(576, 774, 6):
    ys = np.where(red[60:150, x])[0] + 60
    if len(ys):
        print(f"  x={x}: y {ys.min()}..{ys.max()} n={len(ys)}")

# ---- row profiles for baseline detection ----
def profile(y0, y1, x0, x1, mask, label):
    sub = mask[y0:y1+1, x0:x1+1]
    print(f"\n{label} row profile (y: count):")
    for i, y in enumerate(range(y0, y1+1)):
        n = sub[i].sum()
        if n:
            print(f"  {y}: {n}")

blue = (b > 120) & (b > r + 50) & (b > g + 40)
tm = np.zeros_like(red); tm[60:150, 60:900] = red[60:150, 60:900]
profile(78, 114, 176, 774, tm, "title")
lm = np.zeros_like(red); lm[220:262, 620:960] = red[220:262, 620:960]
profile(226, 254, 692, 808, lm, "label '2-D Image'")
bands = [(149, 170, 88, 574), (175, 196, 88, 574), (238, 259, 88, 574),
         (263, 285, 88, 574), (326, 348, 88, 574), (352, 374, 88, 574)]
for i, (y0, y1, x0, x1) in enumerate(bands):
    bm = np.zeros_like(blue); bm[y0:y1+1, x0:x1] = blue[y0:y1+1, x0:x1]
    profile(y0, y1, x0, x1, bm, f"L{i+1}")
