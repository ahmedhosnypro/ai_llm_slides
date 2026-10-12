#!/usr/bin/env python3
"""Slide 030: text-line bboxes, border/fill cores, bracket strokes."""
import numpy as np
from PIL import Image

im = np.asarray(Image.open("videos/deep-learning/002_transformers_part2/unique_slides/slide_030.jpg").convert("RGB")).astype(int)
R, G, B = im[:, :, 0], im[:, :, 1], im[:, :, 2]

lum = (R + G + B) / 3
ink = lum < 150  # any dark ink (text/black)
redm = (R > 90) & (R - G > 50) & (R - B > 50)
blum = (B > 90) & (B - R > 30) & (B - G > 30)

def bb(x0, y0, x1, y1, mask, label):
    ys, xs = np.where(mask[y0:y1, x0:x1])
    if len(xs) == 0:
        print(f"{label}: EMPTY"); return None
    r = (int(xs.min() + x0), int(ys.min() + y0), int(xs.max() + x0), int(ys.max() + y0))
    print(f"{label}: x {r[0]}..{r[2]} y {r[1]}..{r[3]} (w {r[2]-r[0]+1} h {r[3]-r[1]+1})")
    return r

def core(x0, y0, x1, y1, sel, label):
    reg = im[y0:y1, x0:x1]
    m = sel[y0:y1, x0:x1]
    if m.sum() == 0:
        print(f"{label}: none"); return
    px = reg[m]
    s = px.sum(axis=1)
    idx = np.argsort(s)[:max(1, len(s) // 4)]
    print(f"{label}: n={int(m.sum())} core={tuple(np.median(px[idx], axis=0).astype(int))}")

print("=== BORDERS + FILLS ===")
core(87, 400, 90, 480, blum, "matrix box LEFT border core")
core(615, 400, 618, 480, blum, "matrix box RIGHT border core")
core(200, 497, 500, 500, blum, "matrix box BOTTOM border core")
core(88, 250, 91, 320, blum, "deriv box LEFT border core")
core(659, 250, 662, 320, blum, "deriv box RIGHT border core")
core(200, 240, 500, 244, blum, "deriv box TOP border core")
core(90, 100, 93, 220, blum, "vecbox LEFT border core")
core(373, 100, 376, 220, blum, "vecbox RIGHT border core")
core(150, 231, 350, 235, blum, "vecbox BOTTOM border core(y231-235)")
core(505, 102, 840, 106, blum, "remember TOP border core")
core(505, 180, 840, 190, blum, "remember BOTTOM border core")
gren = (G > 100) & (G - R > 20) & (G - B > 20)
core(624, 400, 628, 460, gren, "note LEFT border core")
core(867, 400, 872, 460, gren, "note RIGHT border core")
core(660, 351, 840, 356, gren, "note TOP border core")
core(660, 468, 840, 475, gren, "note BOTTOM border core")

def fillmode(x0, y0, x1, y1, label):
    reg = im[y0:y1, x0:x1].reshape(-1, 3)
    keys, counts = np.unique(reg, axis=0, return_counts=True)
    o = np.argsort(-counts)[:2]
    print(f"{label}: " + "  ".join(f"({keys[i][0]},{keys[i][1]},{keys[i][2]})x{counts[i]}" for i in o))
fillmode(600, 120, 820, 175, "remember fill")
fillmode(660, 400, 850, 460, "note fill")
fillmode(120, 120, 220, 170, "vecbox fill")
fillmode(120, 260, 400, 310, "deriv fill")
fillmode(120, 430, 250, 470, "matrix fill")

print("=== VECBOX ===")
bb(95, 75, 260, 110, redm, "label1 'Vector of Pos t'")
bb(95, 175, 270, 210, redm, "label2 'Vector of Pos t+d'")
# red bracket strokes of v1: vertical strokes near x235-250
for x in range(228, 262):
    c = int(redm[62:230, x].sum())
    if c > 20:
        print(f"  red v-bracket stroke col x={x} count={c}")
bb(255, 60, 372, 230, ink & ~redm, "v1+v2 text+black brackets")
bb(258, 62, 372, 140, ink & ~redm, "v1 cell text")
bb(258, 140, 372, 230, ink & ~redm, "v2 cell text")
# black bracket strokes v2
blam2 = (R < 110) & (G < 110) & (B < 110)
for x in list(range(236, 262)) + list(range(340, 375)):
    c = int(blam2[140:230, x].sum())
    if c > 25:
        print(f"  black v2-bracket stroke col x={x} count={c}")

print("=== REMEMBER ===")
bb(505, 108, 840, 130, blum, "Remember: header")
bb(505, 130, 845, 158, blum, "identity 1")
bb(505, 155, 845, 185, blum, "identity 2")

print("=== DERIVATION ===")
bb(95, 240, 660, 275, ink, "deriv L1 full")
bb(95, 285, 660, 320, ink, "deriv L2 full")

print("=== MATRIX BOX ===")
bb(115, 350, 240, 435, ink & ~redm, "left vec text")
blam2 = (R < 110) & (G < 110) & (B < 110)
for x in list(range(115, 145)) + list(range(215, 250)):
    c = int(blam2[350:435, x].sum())
    if c > 25:
        print(f"  black left-vec bracket stroke col x={x} count={c}")
bb(255, 350, 500, 390, ink, "matrix r1 cells")
bb(255, 390, 500, 430, ink, "matrix r2 cells")
# matrix brackets: BLUE strokes?
for x in list(range(255, 300)) + list(range(440, 500)):
    c = int(blum[350:430, x].sum())
    if c > 25:
        print(f"  blue mx-bracket stroke col x={x} count={c}")
# find the bold '=' between
bb(240, 360, 280, 430, ink, "equals region")
bb(495, 350, 615, 435, ink & ~redm, "right vec text")
for x in range(480, 620):
    c = int(redm[350:435, x].sum())
    if c > 25:
        print(f"  red right-vec bracket stroke col x={x} count={c}")
bb(95, 435, 300, 470, redm, "caption1")
bb(460, 435, 625, 470, redm, "caption2")
bb(250, 445, 470, 495, redm, "brace")
bb(230, 470, 480, 505, blum, "Independent text")

print("=== NOTE ===")
redn = (R > 110) & (R - G > 60) & (R - B > 60)
bb(630, 380, 890, 412, redn, "note L1 'From Computer Graphics:'")
bb(630, 405, 890, 440, blum, "note L2")
bb(630, 435, 890, 470, blum, "note L3")
