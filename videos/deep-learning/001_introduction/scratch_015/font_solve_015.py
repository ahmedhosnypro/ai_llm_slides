#!/usr/bin/env python3
"""Font solve for slide_015 (section divider): candidates x sizes fit measured ink
widths + cap heights; IoU correlation on L1/L3/vs crops; 5x5-core modal color."""
import numpy as np, os
from PIL import Image, ImageFont, ImageDraw

IM = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_015.jpg"
im = np.asarray(Image.open(IM).convert("RGB")).astype(int)
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]
red = (r > 120) & (g < 110) & (b < 110)

def crop_mask(y0, y1, x0, x1):
    m = red[y0:y1+1, x0:x1+1]
    ys, xs = np.where(m)
    return m[ys.min():ys.max()+1, xs.min():xs.max()+1], (ys.min()+y0, ys.max()+y0, xs.min()+x0, xs.max()+x0)

L1m, L1box = crop_mask(180, 250, 200, 780)
L3m, L3box = crop_mask(310, 380, 290, 690)
VSm, VSbox = crop_mask(260, 300, 460, 520)
print("L1 box rows/cols:", L1box, "mask", L1m.shape)
print("L3 box rows/cols:", L3box, "mask", L3m.shape)
print("VS box rows/cols:", VSbox, "mask", VSm.shape)

# cap height: 'D' of Deep (L3 first glyph) - column-scan the left 40 cols of L3
dcols = L3m[:, :int(L3m.shape[1]*0.12)]
dys = np.where(dcols.sum(axis=1) > 0)[0]
print("L3 'D' vertical extent within band:", dys.min(), dys.max(), "cap h =", dys.max()-dys.min()+1)
# 'M' of Machine in L1: text is "[2] Machine Learning" - find the gap after '] '
colprof = L1m.sum(axis=0)
# print col profile transitions to find glyph clusters
gaps = np.where(colprof == 0)[0]
print("L1 zero-gap col ranges (first 12):", end=" ")
runs = []
if len(gaps):
    s = p = gaps[0]
    for i in gaps[1:]:
        if i == p+1: p = i
        else: runs.append((s,p)); s = p = i
    runs.append((s,p))
print(runs[:12])
