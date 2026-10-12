#!/usr/bin/env python3
"""Slide 038 — m17: orange arrow paths (fine), full cell color spans, bar extents, navy arrows."""
import numpy as np
from PIL import Image

F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_038.jpg"
img = np.asarray(Image.open(F).convert("RGB")).astype(int)
R, G, B = img[:, :, 0], img[:, :, 1], img[:, :, 2]
invx = lambda fx: round((fx - 18.63) / 0.96123, 1)
invy = lambda fy: round(fy / 0.95556, 1)

print("== orange fine path, col1-2 zone (x 150..310, y 336..482): per-y orange clusters ==")
orange = (R > 140) & (G > 50) & (G < 170) & (B < 110) & (R - B > 70)
for y in range(336, 483, 4):
    seg = orange[y:y+2, 150:310]
    colprof = seg.sum(axis=0)
    runs, inr = [], False
    for i, v in enumerate(colprof):
        if v > 0 and not inr: s = i; inr = True
        elif v == 0 and inr:
            runs.append((s + 150, i + 150)); inr = False
    if inr: runs.append((s + 150, 310))
    if runs: print(f"  y={y} (slide {invy(y)}): {runs}")

print("== orange fine path, col7-8 zone (x 700..860, y 336..482) ==")
for y in range(336, 483, 8):
    seg = orange[y:y+2, 700:860]
    colprof = seg.sum(axis=0)
    runs, inr = [], False
    for i, v in enumerate(colprof):
        if v > 0 and not inr: s = i; inr = True
        elif v == 0 and inr: runs.append((s + 700, i + 700)); inr = False
    if inr: runs.append((s + 700, 860))
    if runs: print(f"  y={y} (slide {invy(y)}): {runs}")

print("== col7 top-bar raw row y=266, x 735..800 (cell spans) ==")
print("  " + " ".join(f"{x}:{tuple(img[266, x])}" for x in range(735, 801, 3)))
print("== col1 top-bar raw row y=266, x 180..250 ==")
print("  " + " ".join(f"{x}:{tuple(img[266, x])}" for x in range(180, 251, 3)))
print("== col2 top-bar raw row y=268, x 245..305 ==")
print("  " + " ".join(f"{x}:{tuple(img[268, x])}" for x in range(245, 306, 3)))

print("== X-bar vertical extent at col2 (x 262..296 non-white rows 460..490) ==")
ink = (R < 215) | (G < 215) | (B < 215)
for y in range(460, 491):
    n = ink[y, 262:297].sum()
    if n > 3: print(f"  y={y} n={n} sample={tuple(img[y, 265])},{tuple(img[y, 276])},{tuple(img[y, 290])}")

print("== mid-bar vertical extent at col2 (rows 360..385) ==")
for y in range(360, 386):
    n = ink[y, 250:300].sum()
    if n > 3: print(f"  y={y} n={n} sample x253={tuple(img[y, 253])} x270={tuple(img[y, 270])} x290={tuple(img[y, 290])}")

print("== top-bar vertical extent at col2 (rows 255..282) ==")
for y in range(255, 283):
    n = ink[y, 250:300].sum()
    if n > 3: print(f"  y={y} n={n}")

print("== navy arrows mid->plus: col2 x 274..284, rows 348..368 ==")
navy = (B > 90) & (B - R > 40) & (G < 120)
for y in range(348, 369):
    seg = navy[y, 270:290]
    cols = np.where(seg)[0]
    if len(cols): print(f"  y={y}: x {cols.min()+270}..{cols.max()+270} n={len(cols)}")

print("== red arrow head: col2 x 270..288, rows 272..300 (per-y width) ==")
red = (R > 110) & (G < 110) & (B < 110)
for y in range(272, 301):
    seg = red[y, 270:290]
    cols = np.where(seg)[0]
    if len(cols): print(f"  y={y}: x {cols.min()+270}..{cols.max()+270} n={len(cols)}")
