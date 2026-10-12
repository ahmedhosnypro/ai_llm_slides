#!/usr/bin/env python3
"""Forensics pass 2 — slide_025.jpg. Chrome landmarks, title metrics, top strip.

(a) chrome: raw samples + red border column/row profiles (original deck chrome,
    replaced by canonical playlist chrome in the recreation — measured for the record)
(b) title 'Neural Network Model': red ink mask bbox, per-word splits, cap/baseline,
    modal color, advance fits vs Liberation Sans Regular/Bold (Arial proxies)
(c) top strip: pink box bboxes + borders, dotted magenta line y/dash pattern/arrowheads
"""
import numpy as np
from PIL import Image, ImageFont

ORIG = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_025.jpg"
im = Image.open(ORIG).convert("RGB")
W, H = im.size
a = np.asarray(im).astype(int)
R, G, B = a[..., 0], a[..., 1], a[..., 2]

print("== (a) chrome raw samples ==")
for (x, y) in [(5, 5), (30, 270), (50, 270), (56, 270), (58, 270), (62, 270),
               (957, 270), (930, 270), (920, 270), (910, 270), (905, 270), (900, 270),
               (480, 10), (480, 41), (480, 43), (480, 45), (480, 50),
               (480, 470), (480, 510), (480, 516), (480, 519), (480, 535)]:
    print(f"  ({x:3d},{y:3d}) rgb {tuple(int(v) for v in a[y, x])}")

print("\n== red border columns: per-column count of any-red (R>120, G<80, B<80), full height ==")
anyred = (R > 120) & (G < 80) & (B < 80)
cols = anyred.sum(axis=0)
for x in range(40, 80):
    if cols[x] > 20:
        print(f"  x{x}: {int(cols[x])}")
print("  right side:")
for x in range(880, 930):
    if cols[x] > 20:
        print(f"  x{x}: {int(cols[x])}")
print("  left border column x57..60: rows with ink:")
lb = anyred[:, 57:61].sum(axis=1)
ys = np.where(lb >= 2)[0]
if len(ys):
    # contiguous runs
    runs = []
    s = ys[0]; p = ys[0]
    for y in ys[1:]:
        if y - p > 3:
            runs.append((s, p)); s = y
        p = y
    runs.append((s, p))
    print(f"    runs: {runs[:10]}")
rb = anyred[:, 898:903].sum(axis=1)
ys = np.where(rb >= 2)[0]
if len(ys):
    runs = []
    s = ys[0]; p = ys[0]
    for y in ys[1:]:
        if y - p > 3:
            runs.append((s, p)); s = y
        p = y
    runs.append((s, p))
    print(f"    right border x898..902 runs: {runs[:10]}")

print("\n== top rule row y42..46: x extent ==")
for y in range(41, 47):
    xs = np.where(anyred[y])[0]
    if len(xs):
        print(f"  y{y}: x {xs.min()}..{xs.max()} n={len(xs)}")
