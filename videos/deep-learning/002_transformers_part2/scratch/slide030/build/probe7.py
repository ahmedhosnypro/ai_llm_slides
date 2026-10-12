#!/usr/bin/env python3
"""Slide 030: baselines (bottom of flat glyphs), remaining segment boundaries, note extents."""
import numpy as np
from PIL import Image

im = np.asarray(Image.open("videos/deep-learning/002_transformers_part2/unique_slides/slide_030.jpg").convert("RGB")).astype(int)
R, G, B = im[:, :, 0], im[:, :, 1], im[:, :, 2]
lum = (R + G + B) / 3
inkm = lum < 150
redm = (R > 90) & (R - G > 50) & (R - B > 50)
blum = (B > 90) & (B - R > 30) & (B - G > 30)
blam = (R < 110) & (G < 110) & (B < 110)
ym = (R > 170) & (G > 150) & (R - B > 70) & (G - B > 50)

def rowsof(x0, x1, y0, y1, mask, label):
    ys = np.where(mask[y0:y1, x0:x1].sum(axis=1) > 0)[0]
    print(f"{label}: y {ys.min()+y0}..{ys.max()+y0}" if len(ys) else f"{label}: none")

def colsof(y0, y1, x0, x1, mask, label):
    xs = np.where(mask[y0:y1, x0:x1].sum(axis=0) > 0)[0]
    print(f"{label}: x {xs.min()+x0}..{xs.max()+x0}" if len(xs) else f"{label}: none")

print("== BASELINES (flat-glyph bottoms) ==")
rowsof(217, 240, 245, 272, blam, "L1 'sin' of sin(wt +wd)")     # s,i,n flat bottoms
rowsof(223, 246, 290, 318, blam, "L2 'cos' of cos(wt +wd)")
rowsof(366, 388, 245, 272, redm, "L1 'sin' red term")
rowsof(513, 513, 519, 545, blam, "x")  # dummy
rowsof(519, 542, 290, 318, redm, "L2 'sin' red term")
rowsof(513, 540, 145, 165, blum, "remember id1 'sin'")
rowsof(513, 540, 165, 190, blum, "remember id2 'cos'")
rowsof(512, 590, 108, 128, blum, "remember header")
rowsof(125, 150, 350, 382, blam, "mx lv r1 'Sin'")
rowsof(127, 152, 390, 422, blam, "mx lv r2 'cos'")
rowsof(303, 330, 348, 380, blam, "mx r1c1 'cos'")
rowsof(305, 332, 395, 425, blam, "mx r2c1 'sin'")
rowsof(503, 530, 350, 385, redm, "rv r1 'sin'")
rowsof(503, 530, 400, 432, redm, "rv r2 'cos'")
rowsof(261, 285, 60, 95, redm, "v1 r1 'sin'")
rowsof(261, 285, 105, 142, redm, "v1 r2 'cos'")
rowsof(250, 275, 145, 180, blam, "v2 r1 'Sin'")
rowsof(250, 278, 188, 222, blam, "v2 r2 'cos'")
rowsof(102, 130, 85, 108, redm, "label1 'Vector'")
rowsof(104, 132, 178, 200, redm, "label2 'Vector'")
rowsof(98, 126, 440, 465, redm, "caption1 'Vector'")
rowsof(460, 488, 442, 470, redm, "caption2 'Vector'")
rowsof(230, 258, 476, 505, blum, "Independent 'Ind'")
rowsof(634, 662, 355, 382, redm, "noteL1 'From'")
rowsof(633, 662, 385, 410, blum, "noteL2 'Rot'")
rowsof(633, 662, 408, 432, blum, "noteL3 'Pos'")
rowsof(633, 661, 428, 455, blum, "noteL4 'e.g'")
# tops too (for size fitting)
def both(x0, x1, y0, y1, mask, label):
    ys = np.where(mask[y0:y1, x0:x1].sum(axis=1) > 0)[0]
    if len(ys): print(f"{label}: top {ys.min()+y0} bot {ys.max()+y0}")

print("== L2 boundary profile ==")
dark = (lum[291:314, 145:215] < 140).sum(axis=0)
print("L2 dark cols:", " ".join(f"{i+145}:{v}" for i, v in enumerate(dark) if v > 0))
prof = ym[290:316, 145:215].sum(axis=0)
ys = [i + 145 for i, v in enumerate(prof) if v > 5]
print("L2 yellow cols:", ys[0], "..", ys[-1])
print("== v2 r2 boundary ==")
dark = (lum[195:216, 285:360] < 140).sum(axis=0)
print("v2r2 dark cols:", " ".join(f"{i+285}:{v}" for i, v in enumerate(dark) if v > 0))
prof = ym[192:220, 285:360].sum(axis=0)
ys = [i + 285 for i, v in enumerate(prof) if v > 5]
print("v2r2 yellow cols:", ys[0], "..", ys[-1])
print("== mx lv r2 boundary ==")
dark = (lum[396:418, 165:240] < 140).sum(axis=0)
print("lvr2 dark cols:", " ".join(f"{i+165}:{v}" for i, v in enumerate(dark) if v > 0))
prof = ym[392:420, 165:240].sum(axis=0)
ys = [i + 165 for i, v in enumerate(prof) if v > 5]
print("lvr2 yellow cols:", ys[0], "..", ys[-1])
print("== L1 second-half boundaries (exact) ==")
for label, (a, b) in [("L1 sin(wt)", (366, 420)), ("L1 cos(wd)", (429, 494)), ("L1 cos(wt)", (519, 579)), ("L1 sin(wd)", (587, 647))]:
    both(a, b, 245, 272, blam | redm | blum, label)
print("== note line x-extents ==")
colsof(391, 405, 628, 890, blum, "noteL2 x")
colsof(409, 429, 628, 890, blum, "noteL3 x")
colsof(431, 451, 628, 890, blum, "noteL4 x")
colsof(361, 376, 628, 890, redm, "noteL1 x")
print("== remember extents ==")
colsof(146, 162, 505, 800, blum, "id1 x")
colsof(164, 188, 505, 800, blum, "id2 x")
both(512, 590, 108, 128, blum, "header y-extent")
print("== v2/v1 cell extents ==")
colsof(152, 176, 245, 358, blam, "v2r1 x")
colsof(195, 216, 245, 358, blam, "v2r2 x")
colsof(66, 90, 255, 340, redm, "v1r1 x")
colsof(112, 140, 255, 340, redm, "v1r2 x")
print("== matrix cell extents ==")
colsof(353, 378, 282, 470, blam, "mx r1 cells x-span")
colsof(398, 423, 282, 470, blam, "mx r2 cells x-span")
colsof(359, 377, 122, 235, blam, "lv r1 x")
colsof(396, 417, 122, 235, blam, "lv r2 x")
colsof(362, 382, 495, 570, redm, "rv r1 x")
colsof(408, 428, 495, 570, redm, "rv r2 x")
