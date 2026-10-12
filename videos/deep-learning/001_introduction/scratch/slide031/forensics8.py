#!/usr/bin/env python3
"""Pass 8: title + fp word-level fit; line3 part advances at TNR-B 23.5."""
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import os

D = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction"
a = np.asarray(Image.open(os.path.join(D, "unique_slides/slide_031.jpg")).convert("RGB")).astype(int)
lum = a.mean(axis=2)
LIB = "/usr/share/fonts/liberation"
FONTS = {"TNR-B": f"{LIB}/LiberationSerif-Bold.ttf", "Arial-B": f"{LIB}/LiberationSans-Bold.ttf",
         "TNR-R": f"{LIB}/LiberationSerif-Regular.ttf", "Arial-R": f"{LIB}/LiberationSans-Regular.ttf"}
fc = {}
def load(fp, s):
    k = (fp, round(s, 1))
    if k not in fc: fc[k] = ImageFont.truetype(fp, int(round(s * 4)))
    return fc[k]

def word_runs(y0, y1, x0, x1, thr=190, gap=4):
    seg = lum[y0:y1 + 1, x0:x1 + 1]
    colink = (seg < thr).sum(axis=0)
    runs, x, n = [], 0, len(colink)
    while x < n:
        if colink[x] > 0:
            x2, g = x, 0
            while x2 < n - 1:
                if colink[x2 + 1] > 0: g = 0; x2 += 1
                else:
                    g += 1
                    if g > gap: break
                    x2 += 1
            runs.append((x0 + x, x0 + x2)); x = x2 + 1
        else: x += 1
    return runs

def fit(label, words, runs, fonts, sizes):
    print(f"{label}: measured {[r[1]-r[0]+1 for r in runs]} (abs {runs})")
    res = []
    for fname in fonts:
        for s in sizes:
            advs = [load(FONTS[fname], s).getlength(w) / 4 for w in words]
            err = sum(abs(av - (r[1] - r[0] + 1)) for av, r in zip(advs, runs))
            res.append((err, fname, s, [round(x, 1) for x in advs]))
    res.sort()
    for r in res[:6]: print(f"   {r[1]} {r[2]}: {r[3]} err {r[0]:.1f}")

TW = "Where to Get Filters for Recognition".split(" ")
fit("title", TW, word_runs(87, 120, 175, 782, gap=4), ("TNR-B", "Arial-B", "TNR-R", "Arial-R"), np.arange(34, 42, 0.5))
fit("fp", ["Filter", "Parameters"], word_runs(445, 463, 383, 602), ("TNR-B", "Arial-B"), np.arange(24, 30, 0.5))

f = load(FONTS["TNR-B"], 23.5)
p1 = "Canny, Sobel, Gaussian blur, smoothing, low- level segmentation,"
p2 = "morphological filters, Gabor filters,..."
print(f"\nline3 @TNR-B23.5: p1 {f.getlength(p1)/4:.1f} (t 649)  p2 {f.getlength(p2)/4:.1f} (t 377)")
f24 = load(FONTS["TNR-B"], 24)
print(f"line3 @TNR-B24:   p1 {f24.getlength(p1)/4:.1f}  p2 {f24.getlength(p2)/4:.1f}")
# line1 baseline region recheck + line3 band baselines (no-desc substrings)
for label, y0, y1, xa, xb in (("line3a", 221, 242, 109, 200), ("line3b", 247, 268, 109, 200),
                              ("q1", 302, 323, 134, 174), ("q2", 341, 357, 135, 148)):
    seg = lum[y0:y1 + 1, xa:xb]
    rows = np.where((seg < 190).any(axis=1))[0]
    print(f"{label}: ink rows {y0+rows.min()}..{y0+rows.max()}")
