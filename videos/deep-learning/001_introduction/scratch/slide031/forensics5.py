#!/usr/bin/env python3
"""Forensics pass 5: font metric fitting (Liberation = metric-compatible Arial/TNR),
bullet dots, fills, wrap-point decoding for line 3."""
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from collections import Counter
import os

D = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction"
P = os.path.join(D, "unique_slides/slide_031.jpg")
im = Image.open(P).convert("RGB")
a = np.asarray(im).astype(int)
lum = a.mean(axis=2)

LIB = "/usr/share/fonts/liberation"
FONTS = {
    "TNR-B": f"{LIB}/LiberationSerif-Bold.ttf",
    "TNR-R": f"{LIB}/LiberationSerif-Regular.ttf",
    "Arial-B": f"{LIB}/LiberationSans-Bold.ttf",
    "Arial-R": f"{LIB}/LiberationSans-Regular.ttf",
}
cache = {}
def load(fp, s):
    k = (fp, s)
    if k not in cache: cache[k] = ImageFont.truetype(fp, int(round(s * 4)))  # 4x for precision
    return cache[k]
def advance(fp, s, text):
    f = load(fp, s)
    return f.getlength(text) / 4.0

def fit(name, text, target, sizes):
    best = []
    for fname, fp in FONTS.items():
        for s in sizes:
            adv = advance(fp, s, text)
            best.append((abs(adv - target), fname, s, round(adv, 1)))
    best.sort()
    print(f"{name!r} target {target}:")
    for b in best[:5]:
        print(f"   {b[1]:8s} {b[2]:5.1f}pt adv {b[3]}  err {b[0]:.1f}")

# title: ink 179..778 -> advance 599; cap 87, baseline ~112 (desc to 120)
fit("title 'Where to Get Filters for Recognition'", "Where to Get Filters for Recognition", 599.0, np.arange(30, 44, 0.5))
# line1: 108..676 -> 568; cap 145 baseline ~160
fit("line1 'There are Several, handcrafted filters in computer vision'",
    "There are Several, handcrafted filters in computer vision", 568.0, np.arange(20, 30, 0.5))
# For example: 108..238 -> 130
fit("'For example:'", "For example:", 130.0, np.arange(20, 30, 0.5))
# bullet q1 text 134..468 -> 334
fit("q1 'Are they optimal for recognition?'", "Are they optimal for recognition?", 334.0, np.arange(18, 28, 0.5))
# q2 135..480 -> 345
fit("q2 'Can we learn them from our data?'", "Can we learn them from our data?", 345.0, np.arange(18, 28, 0.5))
# fp label 389..595 -> 206
fit("'Filter Parameters'", "Filter Parameters", 206.0, np.arange(18, 30, 0.5))

# wrap candidates for line 3 (measured part1 adv 649: 109..758; part2 adv 377: 109..486)
L3 = "Canny, Sobel, Gaussian blur, smoothing, low- level segmentation, morphological filters, Gabor filters,..."
words = L3.split(" ")
print("\nline3 full-string advances:")
for fname in ("TNR-B", "Arial-B"):
    for s in (22, 23, 24, 25):
        print(f"  {fname} {s}: {advance(FONTS[fname], s, L3):.0f}")
# find wrap point: part1 = prefix ending after word k (+trailing space not inked)
print("wrap candidates (part1/p rt2 advances):")
for k in range(6, len(words)):
    p1 = " ".join(words[:k])
    p2 = " ".join(words[k:])
    a1 = advance(FONTS["TNR-B"], 24, p1)
    a2 = advance(FONTS["TNR-B"], 24, p2)
    if abs(a1 - 649) < 60:
        print(f"  TNR-B 24 k={k}: p1 '{p1[:50]}...' adv {a1:.0f} (t 649) | p2 '{p2[:40]}' adv {a2:.0f} (t 377)")
for fname, s in (("Arial-B", 24), ("TNR-B", 23)):
    for k in range(6, len(words)):
        p1 = " ".join(words[:k]); p2 = " ".join(words[k:])
        a1 = advance(FONTS[fname], s, p1); a2 = advance(FONTS[fname], s, p2)
        if abs(a1 - 649) < 50 and abs(a2 - 377) < 50:
            print(f"  MATCH {fname} {s} k={k}: p1 adv {a1:.0f} p2 adv {a2:.0f}")

# --- details
print("\nbullet dot px (312,112):", tuple(a[312, 112]), "(349,112):", tuple(a[349, 112]))
# dot y extent col 112
for (y0, y1, label) in ((295, 330, "q1"), (335, 365, "q2")):
    col = lum[y0:y1, 112]
    ys = np.where(col < 200)[0]
    if len(ys): print(f"dot {label} col112 rows {y0+ys.min()}..{y0+ys.max()}")
# dot x extent at its center row
print("dot q1 row312 x-run:", [x for x in range(100, 130) if lum[312, x] < 200])
print("dot q2 row349 x-run:", [x for x in range(100, 130) if lum[349, x] < 200])
# fills
print("content box fill (700,250):", tuple(a[250, 700]), "fp fill (500,445):", tuple(a[445, 500]),
      "matrix box fill (700,400):", tuple(a[400, 700]))
# baseline probes: line1 x-height/baseline rows at x 108..676: bottom of non-descender glyphs
sub = lum[145:170, 108:300]  # 'There are Sever' region, no descenders
prof = (sub < 190).sum(axis=1)
rows = [145 + i for i, v in enumerate(prof) if v > 0]
print("line1 ink rows (no-desc region):", rows[0], "..", rows[-1], "-> baseline", rows[-1])
sub = lum[195:220, 108:238]
prof = (sub < 190).sum(axis=1)
rows = [195 + i for i, v in enumerate(prof) if v > 0]
print("'For example:' ink rows:", rows[0], "..", rows[-1])
# title: 'W' region x 179..230 (no descender)
sub = lum[80:125, 179:235]
prof = (sub < 190).sum(axis=1)
rows = [80 + i for i, v in enumerate(prof) if v > 0]
print("title 'W' ink rows:", rows[0], "..", rows[-1])
