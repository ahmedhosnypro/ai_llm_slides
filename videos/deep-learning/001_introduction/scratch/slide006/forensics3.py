#!/usr/bin/env python3
"""Forensics round 3: fonts (advance solving), 12th bullet color/x-extent,
title serif check, header underline extents."""
from PIL import Image, ImageFont
import numpy as np, collections

SRC = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_006.jpg"
im = Image.open(SRC).convert("RGB")
a = np.asarray(im).astype(int)
H, W = a.shape[:2]
R, G, B = a[..., 0], a[..., 1], a[..., 2]

# ---- A. 12th bullet: modal color + x extent (exclude border cols <65 / >835, dot <195) ----
print("-- 12th bullet text --")
zone = a[485:500, 195:836]
m = (zone[..., 0] < 160) & (zone[..., 1] < 160) & (zone[..., 2] < 160)
ys, xs = np.nonzero(m)
print(f"ink n={len(ys)} y {ys.min()+485}..{ys.max()+485} x {xs.min()+195}..{xs.max()+195}")
if len(ys):
    px_ = zone[ys, xs]
    q = (px_ // 8) * 8
    print("modal:", collections.Counter(map(tuple, q)).most_common(5))
# row profile
dk = (R < 160) & (G < 160) & (B < 160)
for y in range(484, 502):
    seg = dk[y, 195:836]
    if seg.sum():
        xr = np.nonzero(seg)[0]
        print(f"  row {y}: n={seg.sum()} x {xr.min()+195}..{xr.max()+195}")

# ---- B. bullet band x-extents for all 11 blue bands (for advance solving) ----
blue = (B > 100) & (R < 120) & (G < 120) & (B - R > 50)
print("\n-- blue bands x-extent (strict core) --")
bands = [(197,212),(223,239),(250,265),(276,288),(303,313),(328,343),(355,366),(382,392),(407,422),(433,444),(459,474)]
for (y0,y1) in bands:
    m = blue[y0:y1+1, 45:915]
    xs = np.nonzero(m.any(axis=0))[0]
    print(f"  y {y0}..{y1}: x {xs.min()+45}..{xs.max()+45} w={xs.max()-xs.min()+1}")
# core modal of blue
m = blue[197:475, 195:915]
ys, xs = np.nonzero(m)
px_ = a[ys+197, xs+195]
q = (px_ // 4) * 4
print("blue core modal:", collections.Counter(map(tuple, q)).most_common(6))

# ---- C. title: row profile + serif run stats ----
red_t = (R > 140) & (G < 90) & (B < 90)
tt = red_t[46:130, 45:915].sum(axis=1)
print("\n-- title rows --")
print([(y+46, int(tt[y])) for y in range(len(tt)) if tt[y] > 5])
print("-- title serif run stats --")
for y in [95, 100, 105, 110, 112, 113, 114, 115, 116, 120, 123]:
    mm = red_t[y, 140:840]
    n = int(mm.sum()); best = cur = 0
    for v in mm:
        cur = cur + 1 if v else 0
        best = max(best, cur)
    print(f"  y={y}: n={n} longest_run={best}")

# ---- D. header: row profile wide-view (135..190) with looser dark ----
dark = (R < 150) & (G < 150) & (B < 150)
print("\n-- header rows (loose) --")
for y in range(135, 192):
    seg = dark[y, 65:915]
    if seg.sum() > 3:
        xr = np.nonzero(seg)[0]
        print(f"  row {y}: n={seg.sum()} x {xr.min()+65}..{xr.max()+65}")

# ---- E. font advance solving ----
print("\n-- font solving --")
FONTS = {
    "Arial": "/usr/share/fonts/TTF/LiberationSans-Regular.ttf",
    "ArialB": "/usr/share/fonts/TTF/LiberationSans-Bold.ttf",
    "TNR": "/usr/share/fonts/TTF/LiberationSerif-Regular.ttf",
    "TNRB": "/usr/share/fonts/TTF/LiberationSerif-Bold.ttf",
}
import os
for k, p in FONTS.items():
    if not os.path.exists(p):
        print(f"MISSING {k} {p}")
# find alternatives
import glob
if not all(os.path.exists(p) for p in FONTS.values()):
    print(glob.glob("/usr/share/fonts/**/Liberation*", recursive=True)[:10])
    print(glob.glob("/usr/share/fonts/**/*rial*", recursive=True)[:10])

def adv(fontpath, size_pt, text):
    f = ImageFont.truetype(fontpath, int(round(size_pt)))  # 1px=1pt at 960x540
    return f.getlength(text)

title = "Machine Learning in the real-world"
meas_title = 832 - 143 + 1  # ink width ~690
print(f"\ntitle ink measured ~{meas_title}px (x 143..832)")
for size in [36, 38, 40, 42, 44]:
    print(f"  {size}pt ArialB={adv(FONTS['ArialB'], size, title):.0f} TNRB={adv(FONTS['TNRB'], size, title):.0f}")

b1 = "Spam filtering"
meas_b1 = 311 - 206 + 1
print(f"\nbullet1 'Spam filtering' ink measured ~{meas_b1}px (x 206..311)")
for size in [15, 16, 17, 18, 19, 20]:
    print(f"  {size}pt Arial={adv(FONTS['Arial'], size, b1):.0f} TNR={adv(FONTS['TNR'], size, b1):.0f}")

hdr_b = "Broadly applicable in many domains"
print(f"\nheader bold phrase candidates (underline x 93..601 = {601-93+1}px):")
for size in [20, 21, 22, 23, 24, 25]:
    print(f"  {size}pt ArialB={adv(FONTS['ArialB'], size, hdr_b):.0f} TNRB={adv(FONTS['TNRB'], size, hdr_b):.0f}")
# full candidate line 1 (wraps): try several prefixes
l1_full = "(e.g., finance, robotics, bioinformatics, vision, natural language, etc.)."
print(f"\nfull parenthetical at sizes (line1 ink 93..692={692-93+1}px, line2 ink 94..719={719-94+1}px):")
for size in [20, 21, 22, 23, 24]:
    t1 = "Broadly applicable in many domains (e.g., finance, robotics,"
    t2 = "bioinformatics, vision, natural language, etc.). Some applications:"
    t3 = "bioinformatics, vision, natural language, etc.)."
    t4 = "Some applications:"
    print(f"  {size}pt TNR: A({t1[:20]}...)={adv(FONTS['TNR'], size, t1):.0f} B={adv(FONTS['TNR'], size, t2):.0f}")
    print(f"        TNR bold-mixed L1={adv(FONTS['TNRB'], size, 'Broadly applicable in many domains') + adv(FONTS['TNR'], size, ' (e.g., finance, robotics,'):.0f}")
