#!/usr/bin/env python3
"""Forensics pass 4: cross-frame chrome check + fine measurements + font fitting."""
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from collections import Counter
import os

D = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides"

# --- A. cross-frame: red vertical lines in several frames of this deck
for name in ("slide_030.jpg", "slide_032.jpg", "slide_005.jpg", "slide_002.jpg", "slide_001.jpg"):
    a = np.asarray(Image.open(os.path.join(D, name)).convert("RGB")).astype(int)
    red = (a[:,:,0] > 120) & (a[:,:,1] < 80) & (a[:,:,2] < 80)
    cols = [(x, int(red[:, x].sum())) for x in range(a.shape[1]) if red[:, x].sum() > 80]
    rows = [(y, int(red[y].sum())) for y in range(a.shape[0]) if red[y].sum() > 200]
    print(name, "red cols>80:", cols, "red rows>200:", rows[:6])

P = os.path.join(D, "slide_031.jpg")
im = Image.open(P).convert("RGB")
a = np.asarray(im).astype(int)
lum = a.mean(axis=2)

# --- B. panel border of THIS frame: red count col 42..70 full height, row 44..47
red = (a[:,:,0] > 120) & (a[:,:,1] < 80) & (a[:,:,2] < 80)
print("col 42..70 red counts:", {x: int(red[:, x].sum()) for x in range(42, 71) if red[:, x].sum() > 20})
print("rows 43..47 red counts:", {y: int(red[y].sum()) for y in range(43, 48)})
# col 58 below 494?
print("col 57-59 rows 490..518 lums:", [round(lum[y, 58], 1) for y in range(490, 518, 2)])

# --- C. content-box border core colors
print("content border px (99,250):", tuple(a[250, 99]), "(885,250):", tuple(a[250, 885]), "(886,250):", tuple(a[250, 886]))
print("content border row134 (500):", tuple(a[134, 500]), " row366:", tuple(a[366, 500]))
print("title red core:", tuple(a[105, 300]))

# --- D. fp box borders: scan x 350..630 y 425..485
sub = lum[425:485, 350:635]
for x in range(350, 635):
    col = lum[430:480, x]
    if (col < 210).sum() > 35:
        print("fp vline col", x, int((col < 210).sum()), tuple(a[455, x]))
# fp text ink excluding borders (inside x 386..616)
inner = lum[437:473, 380:618]
ys, xs = np.where(inner < 150)
print("fp text ink bbox:", 380+xs.min(), 437+ys.min(), 380+xs.max(), 437+ys.max())

# --- E. matrix internals: ink bands (rows) and col runs inside box (x 627..840, y 389..502)
mb = lum[389:502, 627:840]
rowink = (mb < 150).sum(axis=1)
bands = []
y = 0
while y < len(rowink):
    if rowink[y] > 0:
        y2 = y
        while y2 < len(rowink)-1 and rowink[y2+1] > 0: y2 += 1
        bands.append((389+y, 389+y2)); y = y2+1
    else: y += 1
print("matrix row bands:", bands)
for b in bands:
    seg = lum[b[0]:b[1]+1, 627:840]
    xs = np.where((seg < 150).any(axis=0))[0]
    print(f"  band {b}: x {627+xs.min()}..{627+xs.max()}")
# bracket strokes: col ink profile over full height
colink = (mb < 150).sum(axis=0)
strong = [(627+x, int(c)) for x, c in enumerate(colink) if c > 60]
print("matrix strong cols (bracket strokes):", strong)
