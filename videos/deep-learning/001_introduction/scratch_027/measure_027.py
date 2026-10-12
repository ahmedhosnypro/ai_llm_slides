#!/usr/bin/env python3
"""Forensics pass 1 for slide_027 (title slide '[4] Introduction to Deep Learning and CNN').
Measures: red-text bands (rows/cols/ink), per-line cap heights, core text color,
panel/border geometry, black strip, cursor region. 960x540 frame, 1px = 1pt."""
from PIL import Image
import numpy as np

P = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_027.jpg"
im = Image.open(P).convert("RGB")
a = np.asarray(im).astype(int)
H, W = a.shape[:2]
print(f"frame {W}x{H}")

# red-ish ink (border + title text)
redish = (a[:, :, 0] - a[:, :, 1] > 60) & (a[:, :, 0] - a[:, :, 2] > 50)
rsum = redish.sum(axis=1)
print("rows redish>300:", [int(r) for r in np.where(rsum > 300)[0]])
csum = redish.sum(axis=0)
cols_border = np.where(csum > 300)[0]
print("cols redish>300 (border strokes):", cols_border.tolist())

# interior text bands (exclude border margins)
inner = np.zeros_like(redish)
inner[75:500, 75:885] = redish[75:500, 75:885]
irsum = inner.sum(axis=1)
rr = np.where(irsum > 2)[0]
bands = []
if len(rr):
    start = prev = rr[0]
    for r in rr[1:]:
        if r - prev > 4:
            bands.append((int(start), int(prev)))
            start = r
        prev = r
    bands.append((int(start), int(prev)))
print("TEXT bands (interior redish):")
for (b0, b1) in bands:
    seg = inner[b0:b1 + 1, :]
    cs = np.where(seg.sum(axis=0) > 0)[0]
    print(f"  band {b0}-{b1} h={b1 - b0 + 1}: cols {cs.min()}..{cs.max()} (w {cs.max() - cs.min() + 1}), ink px={int(seg.sum())}")
    # column profile: gaps inside the band (word gaps / glyph structure)
    colprof = seg.sum(axis=0)
    nz = np.where(colprof > 0)[0]
    gaps = []
    if len(nz):
        run = 0
        for c in range(nz.min(), nz.max() + 1):
            if colprof[c] == 0:
                run += 1
            else:
                if run >= 8:
                    gaps.append((c - run, c - 1, run))
                run = 0
    print(f"    gaps>=8px: {gaps[:12]}")

# per-band 5x5 core color
core_red = redish.copy()
core_red[:75, :] = False; core_red[500:, :] = False
core_red[:, :75] = False; core_red[:, 885:] = False
core = np.zeros_like(core_red)
rr2, cc2 = np.where(core_red)
for y, x in zip(rr2, cc2):
    if core_red[y - 2:y + 3, x - 2:x + 3].all():
        core[y, x] = True
ys, xs = np.where(core)
if len(ys):
    ink = a[ys, xs]
    vals, counts = np.unique(ink.reshape(-1, 3), axis=0, return_counts=True)
    topi = np.argsort(-counts)[:5]
    print("text core (5x5 all-red) modal:", [f"#{vals[i][0]:02X}{vals[i][1]:02X}{vals[i][2]:02X}({counts[i]})" for i in topi])
    print(f"core mean: #{int(ink[:, 0].mean()):02X}{int(ink[:, 1].mean()):02X}{int(ink[:, 2].mean()):02X}  n={len(ink)}")

# panel fill + canvas
print("panel fill mean (rows 100..160, cols 150..800):", a[100:160, 150:800].mean(axis=(0, 1)).round(1))
print("canvas @(row300, col10:35):", a[300, 10:35].mean(axis=0).round(1), "@(row20, col400:600):", a[20, 400:600].mean(axis=0).round(1))
row300 = a[300]
nonwhite = np.where(row300.sum(axis=1) < 720)[0]
print("row300 nonwhite cols first/last:", nonwhite.min(), nonwhite.max())
col480 = a[:, 480]
nw = np.where(col480.sum(axis=1) < 720)[0]
print("col480 nonwhite rows first/last:", nw.min(), nw.max())

# black strip at bottom
for r in range(495, 540):
    m = a[r, 200:700].mean(axis=0)
    if m.mean() < 100:
        print("dark row:", r, m.round(1))

# cursor region (spec: ~28-31% width, ~81-87% height => x~269-298, y~437-470)
cur = a[435:475, 260:310]
dark = cur.sum(axis=2) < 400
cys, cxs = np.where(dark)
if len(cys):
    print(f"cursor dark-ink bbox rows {435 + cys.min()}..{435 + cys.max()} cols {260 + cxs.min()}..{260 + cxs.max()} n={len(cys)}")
