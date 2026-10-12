#!/usr/bin/env python3
"""Forensics pass 7: JPEG-matched density + per-word advance fit (serif vs sans, bold vs reg)."""
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import os, io

D = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction"
a = np.asarray(Image.open(os.path.join(D, "unique_slides/slide_031.jpg")).convert("RGB")).astype(int)
lum = a.mean(axis=2)

LIB = "/usr/share/fonts/liberation"
FONTS = {
    "TNR-B": f"{LIB}/LiberationSerif-Bold.ttf",
    "TNR-R": f"{LIB}/LiberationSerif-Regular.ttf",
    "Arial-B": f"{LIB}/LiberationSans-Bold.ttf",
    "Arial-R": f"{LIB}/LiberationSans-Regular.ttf",
}
fc = {}
def load(fp, s):
    k = (fp, round(s, 1))
    if k not in fc: fc[k] = ImageFont.truetype(fp, int(round(s * 4)))
    return fc[k]

def cand_density_jpeg(fname, size, text, q=80):
    f = load(FONTS[fname], size)
    W = int(f.getlength(text) / 4) + 24
    img = Image.new("RGB", (W, int(size * 4) + 24), (255, 255, 255))
    d = ImageDraw.Draw(img)
    d.text((12, 12), text, font=f, fill=(0, 0, 128))
    # downsample to 1x then JPEG-compress like the source
    small = img.resize((W // 4, img.height // 4), Image.LANCZOS)
    buf = io.BytesIO(); small.save(buf, "JPEG", quality=q); buf.seek(0)
    s = np.asarray(Image.open(buf).convert("L")).astype(int)
    return (s < 190).sum() / (f.getlength(text) / 4.0)

def meas_density(y0, y1, x0, x1):
    return (lum[y0:y1 + 1, x0:x1 + 1] < 190).sum() / (x1 - x0)

T = "Where to Get Filters for Recognition"
L1 = "There are Several, handcrafted filters in computer vision"
Q1 = "Are they optimal for recognition?"
FP = "Filter Parameters"
print("== JPEG-matched density (target: measured) ==")
print(f"title meas {meas_density(87,120,179,778):.2f} | " +
      " | ".join(f"{n}{s} {cand_density_jpeg(n,s,T):.2f}" for n, s in (("Arial-B",35),("TNR-B",38.5),("TNR-B",38),("Arial-R",37.5),("TNR-R",40.5))))
print(f"line1 meas {meas_density(145,164,108,676):.2f} | " +
      " | ".join(f"{n}{s} {cand_density_jpeg(n,s,L1):.2f}" for n, s in (("TNR-B",23.5),("TNR-B",24),("TNR-R",25),("Arial-B",21),("Arial-R",23))))
print(f"q1 meas {meas_density(302,323,134,468):.2f} | " +
      " | ".join(f"{n}{s} {cand_density_jpeg(n,s,Q1):.2f}" for n, s in (("TNR-B",23.5),("TNR-R",25),("Arial-B",21),("Arial-R",23))))
print(f"fp meas {meas_density(445,463,389,595):.2f} | " +
      " | ".join(f"{n}{s} {cand_density_jpeg(n,s,FP):.2f}" for n, s in (("TNR-B",27),("Arial-B",25),("TNR-R",27),("Arial-R",27))))

print("\n== per-word advance fit ==")
def word_runs(y0, y1, x0, x1, thr=190):
    seg = lum[y0:y1 + 1, x0:x1 + 1]
    colink = (seg < thr).sum(axis=0)
    runs = []
    x = 0
    n = len(colink)
    while x < n:
        if colink[x] > 0:
            x2 = x
            gap = 0
            while x2 < n - 1:
                if colink[x2 + 1] > 0: gap = 0; x2 += 1
                else:
                    gap += 1
                    if gap > 4: break  # word gap > 4px
                    x2 += 1
            runs.append((x0 + x, x0 + x2)); x = x2 + 1
        else: x += 1
    return runs

def fit_words(label, words, runs, sizes):
    print(f"{label}: measured runs {runs}")
    for fname in ("TNR-B", "TNR-R", "Arial-B", "Arial-R"):
        for s in sizes:
            advs = [load(FONTS[fname], s).getlength(w) / 4 for w in words]
            if len(advs) != len(runs): continue
            err = sum(abs(av - (r[1] - r[0] + 1)) for av, r in zip(advs, runs))
            if err < 18:
                print(f"   {fname} {s}: advs {[round(x,1) for x in advs]} err {err:.1f}")

fit_words("For example:", ["For", "example:"], word_runs(195, 216, 105, 245), np.arange(21, 26.5, 0.5))
fit_words("q1", ["Are", "they", "optimal", "for", "recognition?"], word_runs(302, 323, 130, 475), np.arange(20, 26.5, 0.5))
fit_words("fp", ["Filter", "Parameters"], word_runs(445, 463, 385, 600), np.arange(23, 29.5, 0.5))
