#!/usr/bin/env python3
"""Forensic measurement of slide_008.jpg ground truth (960x540, 1px = 1pt = 1/72 in).

Measures: black artifact strips, top red rule, title ink, white content box,
section headers, bullet dots, bullet text lines, colors (modal sampling).
"""
from PIL import Image
import numpy as np
from collections import Counter

IMG = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_008.jpg"
im = Image.open(IMG).convert("RGB")
a = np.asarray(im).astype(int)
H, W, _ = a.shape
print(f"size: {W}x{H}")

R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]

def modal(x0, y0, x1, y1, label):
    reg = a[y0:y1, x0:x1].reshape(-1, 3)
    cnt = Counter(map(tuple, reg))
    top = cnt.most_common(4)
    print(f"{label}: modal {top}")

def row_profile(mask, label):
    rows = mask.sum(axis=1)
    nz = np.nonzero(rows)[0]
    print(f"{label}: rows with ink {nz.min()}..{nz.max()}" if len(nz) else f"{label}: none")
    return rows

# --- 1. black strips (letterbox top / player bar bottom) ---
blackish = (R < 60) & (G < 60) & (B < 60)
rows_black = blackish.sum(axis=1)
print("\n-- black strips (rows where >800 px are blackish) --")
for y in range(H):
    if rows_black[y] > 800:
        print(f"  y={y}: {rows_black[y]}")
# print boundary rows partially
for y in range(28, 50):
    if 0 < rows_black[y] <= 800:
        print(f"  (partial top) y={y}: {rows_black[y]}")
for y in range(495, H):
    if 0 < rows_black[y] <= 800:
        print(f"  (partial bottom) y={y}: {rows_black[y]}")

# --- 2. red pixels overall ---
red = (R > 120) & (G < 80) & (B < 80)
print("\n-- red ink row profile (count of red px per row, rows 0..200) --")
rows_red = red.sum(axis=1)
for y in range(0, 200):
    if rows_red[y] > 30:
        print(f"  y={y}: {rows_red[y]}")
print("  ...")
for y in range(200, H):
    if rows_red[y] > 300:
        print(f"  y={y}: {rows_red[y]}")

# top rule x extent: red rows in 20..60
print("\n-- top rule x extent per row (y 20..60) --")
for y in range(20, 62):
    if rows_red[y] > 30:
        xs = np.nonzero(red[y])[0]
        print(f"  y={y}: x {xs.min()}..{xs.max()} n={len(xs)}")

# --- 3. title ink bbox (red in y 60..160, excluding rule) ---
title = red.copy()
title[:60, :] = False
title[165:, :] = False
ys, xs = np.nonzero(title)
print(f"\ntitle red ink bbox: x {xs.min()}..{xs.max()}, y {ys.min()}..{ys.max()}")
# two lines? row profile in title band
rows_t = title.sum(axis=1)
gaps = [y for y in range(60, 165) if rows_t[y] == 0]
print("title empty rows:", gaps)
# line 1 vs line 2 bboxes
if gaps:
    # find contiguous nonzero segments
    segs = []
    start = None
    for y in range(60, 165):
        if rows_t[y] > 0 and start is None:
            start = y
        elif rows_t[y] == 0 and start is not None:
            segs.append((start, y - 1)); start = None
    if start is not None:
        segs.append((start, 164))
    for s, e in segs:
        band = title[s:e + 1]
        ys2, xs2 = np.nonzero(band)
        print(f"  title line y {s}..{e}: x {xs2.min()}..{xs2.max()} (advance {xs2.max()-xs2.min()+1})")

modal(xs.min(), ys.min(), xs.max() + 1, ys.max() + 1, "title ink region")

# --- 4. white content box ---
whiteish = (R > 235) & (G > 235) & (B > 235)
rows_w = whiteish.sum(axis=1)
print("\n-- white box rows (count > 200) --")
wrows = [y for y in range(H) if rows_w[y] > 200]
print(f"white box y extent: {min(wrows)}..{max(wrows)}")
cols_w = whiteish.sum(axis=0)
wcols = [x for x in range(W) if cols_w[x] > 100]
print(f"white box x extent (cols>100): {min(wcols)}..{max(wcols)}")

# box border: red pixels around box
box_red = red.copy()
box_red[:165, :] = False
ys_b, xs_b = np.nonzero(box_red)
print(f"red ink below title (box border+headers): x {xs_b.min()}..{xs_b.max()}, y {ys_b.min()}..{ys_b.max()}")

# --- 5. inside-box content: dark (black text) pixels ---
dark = (R < 100) & (G < 100) & (B < 100)
in_box = np.zeros_like(dark)
in_box[min(wrows):max(wrows) + 1, :] = dark[min(wrows):max(wrows) + 1, :]
rows_d = in_box.sum(axis=1)
print("\n-- dark ink rows inside white box (count>3) --")
segs = []
start = None
for y in range(H):
    if rows_d[y] > 3 and start is None:
        start = y
    elif rows_d[y] <= 3 and start is not None:
        segs.append((start, y - 1)); start = None
for s, e in segs:
    band = in_box[s:e + 1]
    ys2, xs2 = np.nonzero(band)
    print(f"  dark band y {s}..{e} (h {e-s+1}): x {xs2.min()}..{xs2.max()}")
