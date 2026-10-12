#!/usr/bin/env python3
"""Forensics round 4: verify every bullet advance at 17pt, blue core color,
underline loose extent, border modal, cursor presence, header TNR verification."""
from PIL import Image, ImageFont
import numpy as np, collections

SRC = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_006.jpg"
im = Image.open(SRC).convert("RGB")
a = np.asarray(im).astype(int)
H, W = a.shape[:2]
R, G, B = a[..., 0], a[..., 1], a[..., 2]

ARIAL = "/usr/share/fonts/TTF/Arial.TTF"
ARIALB = "/usr/share/fonts/TTF/Arialbd.TTF"
TNR = "/usr/share/fonts/liberation/LiberationSerif-Regular.ttf"
TNRB = "/usr/share/fonts/liberation/LiberationSerif-Bold.ttf"

def adv(fp, size, text):
    return ImageFont.truetype(fp, size).getlength(text)

# ---- A. all 12 bullet lines: measured ink vs Arial advance at 17pt ----
LINES = [
    ("Spam filtering", 206, 311),
    (" Machine Translation (e.g.,  Google Translate)", 211, 562),
    ("Speech/handwriting recognition", 206, 450),
    ("Object detection/recognition", 206, 422),
    ("Weather prediction", 205, 351),
    ("Classifying DNA sequences", 205, 420),
    ("Stock market analysis", 206, 375),
    ("Automatic vehicle navigation", 205, 427),
    ("Search engines (e.g., Google)", 206, 434),
    ("Credit-card fraud detection", 205, 412),
    ("Webpage clustering (e.g., Google News)", 205, 521),
    (".. and many more", 206, 341),
]
print("-- bullet advance check (Arial 17pt; ink≈advance−bearings≈advance−3) --")
for (t, x0, x1) in LINES:
    a17 = adv(ARIAL, 17, t)
    a175 = adv(ARIAL, 17.5 if False else 17, t)  # int size only
    print(f"  '{t[:34]}' meas {x1-x0+1:4d}  arial17={a17:.0f}  diff={x1-x0+1-a17:+.0f}")

print("\n-- bullet advance at fractional sizes via scaling --")
for size in [17.0, 17.25, 17.5, 18.0]:
    errs = []
    for (t, x0, x1) in LINES:
        a17 = adv(ARIAL, 17, t)
        errs.append((x1 - x0 + 1) - a17 * size / 17.0)
    print(f"  {size}pt: mean err {np.mean(errs):+.1f}  max |err| {np.max(np.abs(errs)):.1f}")

# ---- B. blue core color: darkest blue pixels ----
blue = (B - R > 60) & (B - G > 60) & (B > 90)
ys, xs = np.nonzero(blue[195:480, 195:900])
px_ = a[ys + 195, xs + 195]
lum = px_.sum(axis=1)
idx = np.argsort(lum)[:300]
core = px_[idx]
q = (core // 4) * 4
print("\n-- blue core (darkest 300 blue px) modal:", collections.Counter(map(tuple, q)).most_common(8))

# ---- C. underline loose extent (rows 156..161) ----
dk = (R < 190) & (G < 190) & (B < 190)
print("\n-- underline rows loose --")
for y in range(154, 163):
    seg = dk[y, 90:700]
    if seg.sum() > 5:
        xr = np.nonzero(seg)[0]
        print(f"  row {y}: n={seg.sum()} x {xr.min()+90}..{xr.max()+90}")

# ---- D. content-box border modal ----
top = a[133, 100:830]
q = (top // 8) * 8
print("\n-- box top border modal:", collections.Counter(map(tuple, q)).most_common(4))
left = a[140:500, 88]
q = (left // 8) * 8
print("-- box left border modal:", collections.Counter(map(tuple, q)).most_common(4))

# ---- E. title red core ----
red = (R > 120) & (G < 100) & (B < 100) & (R - G > 70)
ys, xs = np.nonzero(red[80:126, 140:840])
px_ = a[ys + 80, xs + 140]
lum = px_.sum(axis=1)
idx = np.argsort(lum)[:400]
q = (px_[idx] // 8) * 8
print("-- title red core modal:", collections.Counter(map(tuple, q)).most_common(5))

# ---- F. cursor check around (259, 394) ----
print("\n-- cursor region scan x 225..300, y 370..415 --")
zone = a[370:415, 225:300]
blk = (zone[..., 0] < 90) & (zone[..., 1] < 90) & (zone[..., 2] < 90)
wht = (zone[..., 0] > 235) & (zone[..., 1] > 235) & (zone[..., 2] > 235)
print(f"  dark px: {int(blk.sum())}  white px: {int(wht.sum())}")
if blk.sum():
    ys2, xs2 = np.nonzero(blk)
    print(f"  dark ink bbox: x {xs2.min()+225}..{xs2.max()+225} y {ys2.min()+370}..{ys2.max()+370}")

# ---- G. header font double-check: TNR 24 mixed-wrap advances ----
print("\n-- header verification TNR/LiberationSerif 24pt --")
l1b = "Broadly applicable in many domains"
l1r = " (e.g., finance, robotics,"
l2 = "bioinformatics, vision, natural language, etc.). Some applications:"
print(f"  L1 bold={adv(TNRB,24,l1b):.0f} + reg='{l1r}'={adv(TNR,24,l1r):.0f} -> {adv(TNRB,24,l1b)+adv(TNR,24,l1r):.0f} (meas ink 600)")
print(f"  L2 = {adv(TNR,24,l2):.0f} (meas ink 626)")
for s in [" (e.g., finance,", " (e.g., finance, r", " (e.g.,"]:
    print(f"  underline cand bold+{s!r}: {adv(TNRB,24,l1b)+adv(TNR,24,s):.0f}")
# alternative: underline = bold phrase only at 26pt?
print(f"  TNRB 26 bold phrase: {adv(TNRB,26,l1b):.0f}  TNRB 25: {adv(TNRB,25,l1b):.0f}")
# header at other sizes for sanity
for size in [23, 24, 25]:
    print(f"  {size}pt L1mixed={adv(TNRB,size,l1b)+adv(TNR,size,l1r):.0f} L2={adv(TNR,size,l2):.0f}")
