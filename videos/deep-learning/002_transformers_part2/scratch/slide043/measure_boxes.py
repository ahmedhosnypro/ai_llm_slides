#!/usr/bin/env python3
"""Slide 043: callout box + bottom box precise geometry + text line census."""
from PIL import Image
import numpy as np

F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_043.jpg"
im = Image.open(F).convert("RGB")
a = np.asarray(im).astype(int)
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]

def runs(mask_1d, off=0):
    out, s = [], None
    for i, v in enumerate(mask_1d):
        if v and s is None: s = i
        if not v and s is not None: out.append((s + off, i - 1 + off)); s = None
    if s is not None: out.append((s + off, len(mask_1d) - 1 + off))
    return out

# --- callout box red border: scan for long horizontal red strokes in x 300..660, y 150..290
red = (r > 130) & (r - g > 60) & (r - b > 60)
print("CALLOUT horizontal red strokes (rowfrac over x330..610 >0.8):")
sub = red[140:300, 330:610]
for y in range(sub.shape[0]):
    fr = sub[y].mean()
    if fr > 0.8: print("  y", 140 + y, round(fr, 2))
print("CALLOUT vertical red strokes (colfrac over y175..265 >0.8):")
subv = red[175:265, 300:660]
for x in range(subv.shape[1]):
    fr = subv[:, x].mean()
    if fr > 0.8: print("  x", 300 + x, round(fr, 2))

# text line bands inside callout (dark+colored ink, x 335..610)
ink = (r < 160) | (g < 120) | (b < 120)
ink[:170, :] = False; ink[275:, :] = False
band = ink[:, 335:612]
print("CALLOUT text rows (frac>0.03):")
prev = False
for y in range(170, 280):
    fr = band[y].mean()
    if fr > 0.03 and not prev: start = y
    if fr <= 0.03 and prev: print(f"  band y {start}..{y-1}")
    prev = fr > 0.03

# --- bottom box green border
grn = (g > 110) & (g - r > 50) & (g - b > 50)
print("BOTTOM box horizontal green strokes (rowfrac over x150..800 >0.8):")
sub = grn[340:520, 150:800]
for y in range(sub.shape[0]):
    fr = sub[y].mean()
    if fr > 0.8: print("  y", 340 + y, round(fr, 2))
print("BOTTOM box vertical green strokes (colfrac over y365..495 >0.8):")
subv = grn[365:495, 40:920]
for x in range(subv.shape[1]):
    fr = subv[:, x].mean()
    if fr > 0.8: print("  x", 40 + x, round(fr, 2))

# bottom box text lines (dark ink) + color census per line
ink2 = (r < 160) | (g < 120) | (b < 120)
ink2[:370, :] = False; ink2[505:, :] = False
band2 = ink2[:, 90:870]
print("BOTTOM text rows (frac>0.02):")
prev = False
for y in range(370, 510):
    fr = band2[y].mean()
    if fr > 0.02 and not prev: start = y
    if fr <= 0.02 and prev: print(f"  band y {start}..{y-1}")
    prev = fr > 0.02

def census(y0, y1, x0=80, x1=880, tag=""):
    reg = slice(y0, y1 + 1)
    rr, gg, bb = r[reg, x0:x1], g[reg, x0:x1], b[reg, x0:x1]
    blue = ((bb - rr > 40) & (bb - gg > 20) & (bb > 80)).sum()
    redc = ((rr - gg > 60) & (rr - bb > 60) & (gg < bb + 35)).sum()
    black = ((rr < 110) & (gg < 110) & (bb < 110)).sum()
    green = ((gg - rr > 30) & (gg - bb > 30)).sum()
    print(f"  {tag} y{y0}..{y1}: blue {blue} red {redc} black {black} green {green}")

print("BOTTOM line color census:")
census(373, 403, tag="L1a")
census(404, 425, tag="L1b")
census(430, 452, tag="L2")
census(462, 490, tag="L3")

# word-start color census: bottom L1/L2/L3 left x, and per-word stems for L2 tail
print("BOTTOM per-line ink x-extents:")
for (y0, y1, tag) in [(373, 403, "L1a"), (404, 425, "L1b"), (430, 452, "L2"), (462, 490, "L3")]:
    cols = ink2[y0:y1 + 1, :].mean(axis=0)
    nz = [x for x in range(60, 900) if cols[x] > 0.04]
    print(f"  {tag}: x {nz[0]}..{nz[-1]}" if nz else f"  {tag}: none")
