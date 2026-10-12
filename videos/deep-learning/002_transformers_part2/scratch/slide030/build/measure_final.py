#!/usr/bin/env python3
"""Slide 030: final comprehensive measurement -> measurements.json (frame px)."""
import json
import numpy as np
from PIL import Image

im = np.asarray(Image.open("videos/deep-learning/002_transformers_part2/unique_slides/slide_030.jpg").convert("RGB")).astype(int)
R, G, B = im[:, :, 0], im[:, :, 1], im[:, :, 2]
lum = (R + G + B) / 3

redm = (R > 90) & (R - G > 50) & (R - B > 50)
blum = (B > 90) & (B - R > 30) & (B - G > 30)
blam = (R < 110) & (G < 110) & (B < 110)
gren = (G > 100) & (G - R > 20) & (G - B > 20)
inkm = lum < 150

out = {}

def bb(x0, y0, x1, y1, mask, label, minpx=3):
    ys, xs = np.where(mask[y0:y1, x0:x1])
    if len(xs) < minpx:
        return None
    return [int(xs.min() + x0), int(ys.min() + y0), int(xs.max() + x0), int(ys.max() + y0)]

def core_bright(x0, y0, x1, y1, sel, label):
    """Brightest-quartile median = truest stroke color (least JPEG darkening)."""
    reg = im[y0:y1, x0:x1]
    m = sel[y0:y1, x0:x1]
    if m.sum() == 0:
        return None
    px = reg[m]
    s = px.sum(axis=1)
    idx = np.argsort(-s)[:max(1, len(s) // 3)]
    return tuple(int(v) for v in np.median(px[idx], axis=0))

def colspans(x0, y0, x1, y1, mask, gap=4, minpx=1):
    """Ink column spans (token boundaries) in a band."""
    prof = mask[y0:y1, x0:x1].sum(axis=0)
    spans, s = [], None
    gaprun = 0
    for i, v in enumerate(prof):
        if v >= minpx:
            if s is None:
                s = i
            gaprun = 0
        else:
            if s is not None:
                gaprun += 1
                if gaprun >= gap:
                    spans.append((s + x0, i - gaprun + x0))
                    s = None
    if s is not None:
        spans.append((s + x0, len(prof) - 1 + x0))
    return spans

def rowspans(x0, y0, x1, y1, mask, gap=3, minpx=1):
    prof = mask[y0:y1, x0:x1].sum(axis=1)
    spans, s = [], None
    gaprun = 0
    for i, v in enumerate(prof):
        if v >= minpx:
            if s is None:
                s = i
            gaprun = 0
        else:
            if s is not None:
                gaprun += 1
                if gaprun >= gap:
                    spans.append((s + y0, i - gaprun + y0))
                    s = None
    if s is not None:
        spans.append((s + y0, len(prof) - 1 + y0))
    return spans

print("== VECBOX ==")
print("top border rows:", rowspans(100, 45, 370, 75, blum, gap=2))
print("v1 red strokes x262..375:", {x: int(redm[60:140, x].sum()) for x in range(262, 376) if redm[60:140, x].sum() > 20})
print("v1 red rowspans (x240..366):", rowspans(240, 55, 367, 145, redm, gap=3))
print("v1 text rowspans (x250..340):", rowspans(250, 55, 341, 145, inkm & ~redm, gap=4))
print("v1 text colspans r1 (y62..100):", colspans(250, 62, 341, 100, inkm & ~redm, gap=4))
print("v1 text colspans r2 (y100..140):", colspans(250, 100, 341, 140, inkm & ~redm, gap=4))
print("label1 cols (y75..110, x95..240):", colspans(95, 75, 240, 110, redm, gap=6))
print("label1 rows (x102..232):", rowspans(102, 70, 233, 115, redm, gap=4))
print("v2 black strokes x340..375 y145..235:", {x: int(blam[145:235, x].sum()) for x in range(340, 376) if blam[145:235, x].sum() > 20})
print("v2 black rowspans (x240..365):", rowspans(240, 142, 366, 238, blam, gap=3))
print("v2 text rowspans (x250..340):", rowspans(250, 142, 341, 238, blam, gap=4))
print("v2 text colspans r1 (y150..185):", colspans(250, 150, 341, 185, blam, gap=4))
print("v2 text colspans r2 (y190..230):", colspans(250, 190, 341, 230, blam, gap=4))
print("label2 rows (x104..230):", rowspans(104, 175, 231, 215, redm, gap=4))
print("label2 cols (y180..200):", colspans(95, 180, 240, 200, redm, gap=6))

print("== REMEMBER ==")
print("box borders: top", rowspans(510, 95, 840, 110, blum, gap=2), "bottom", rowspans(510, 175, 840, 195, blum, gap=2))
print("box sides:", {x: int(blum[105:190, x].sum()) for x in list(range(495, 515)) + list(range(838, 860)) if blum[105:190, x].sum() > 30})
print("header rows (x505..600):", rowspans(505, 105, 600, 145, blum, gap=3))
print("underline rows (x505..600, y120..140):", rowspans(505, 120, 600, 140, blum, gap=2))
print("id1 rows (x510..780):", rowspans(510, 140, 780, 165, blum, gap=3))
print("id2 rows (x510..850):", rowspans(510, 160, 850, 190, blum, gap=3))
print("id1 cols:", colspans(505, 143, 850, 160, blum, gap=5)[:3], "...")
print("remember blue core:", core_bright(505, 108, 850, 190, blum, "remember"))

print("== DERIV ==")
print("L1 rows (x100..655):", rowspans(100, 243, 656, 280, inkm, gap=4))
print("L2 rows (x100..650):", rowspans(100, 283, 651, 320, inkm, gap=4))
print("L1 tokens:", colspans(92, 246, 658, 270, inkm, gap=5))
print("L2 tokens:", colspans(92, 292, 650, 315, inkm, gap=5))

print("== MATRIX ==")
print("left-vec text rows (x125..232):", rowspans(125, 348, 233, 438, blam, gap=4))
print("left-vec tokens r1 (y353..380):", colspans(125, 353, 233, 380, blam, gap=5))
print("left-vec tokens r2 (y390..420):", colspans(125, 390, 233, 420, blam, gap=5))
print("equals bbox:", bb(242, 350, 278, 435, blam, "eq"))
print("mx blue strokes y345..435 x255..300:", {x: int(blum[345:435, x].sum()) for x in range(255, 301) if blum[345:435, x].sum() > 20})
print("mx blue strokes x460..500:", {x: int(blum[345:435, x].sum()) for x in range(460, 501) if blum[345:435, x].sum() > 20})
print("mx r1 rows (x285..468):", rowspans(285, 345, 469, 392, inkm, gap=4))
print("mx r2 rows (x285..468):", rowspans(285, 388, 469, 435, inkm, gap=4))
print("mx r1 tokens (y353..378):", colspans(282, 353, 470, 378, inkm, gap=5))
print("mx r2 tokens (y394..420):", colspans(282, 394, 470, 420, inkm, gap=5))
print("r2c1 minus probe cols x282..305 y400..415:", {x: int(inkm[400:415, x].sum()) for x in range(282, 306)})
print("right-vec text rows (x495..570):", rowspans(495, 348, 571, 438, inkm & ~redm, gap=4))
print("right-vec tokens r1 (y353..380):", colspans(495, 353, 571, 380, inkm & ~redm, gap=5))
print("right-vec tokens r2 (y390..420):", colspans(495, 390, 571, 420, inkm & ~redm, gap=5))
print("cap1 rows (x98..300):", rowspans(98, 438, 301, 472, redm, gap=4))
print("cap2 rows (x460..596):", rowspans(460, 438, 597, 472, redm, gap=4))
print("brace rows (x272..470):", rowspans(272, 440, 471, 478, redm, gap=2))
print("brace col profile detail:")
prof = redm[440:478, 272:471].sum(axis=0)
print("  spine row candidates:", {y: int(redm[y, 272:471].sum()) for y in range(440, 478) if redm[y, 272:471].sum() > 60})
print("Independent rows (x230..480):", rowspans(230, 475, 481, 508, blum, gap=4))
print("independent blue core:", core_bright(230, 478, 480, 502, blum, "ind"))

print("== NOTE ==")
print("box borders: left", {x: int(gren[360:465, x].sum()) for x in range(618, 632) if gren[360:465, x].sum() > 30},
      "right", {x: int(gren[360:465, x].sum()) for x in range(862, 878) if gren[360:465, x].sum() > 30})
print("top/bottom:", rowspans(640, 345, 860, 480, gren, gap=2))
# text lines: use any-dark ink
for label, (yy0, yy1) in [("L1", (378, 408)), ("L2", (405, 438)), ("L3", (435, 470))]:
    r = bb(628, yy0, 890, yy1, inkm, f"note {label}")
    redc = int(redm[yy0:yy1, 628:890].sum())
    bluc = int(blum[yy0:yy1, 628:890].sum())
    print(f"   {label}: redpx={redc} bluepx={bluc}")
print("note red core (L1):", core_bright(628, 380, 890, 408, redm, "noteL1"))
print("note blue core (L2/L3):", core_bright(628, 405, 890, 470, blum, "noteL23"))
print("note fill exact:", tuple(int(v) for v in np.median(im[420:460, 660:850].reshape(-1, 3), axis=0)))
print("remember fill exact:", tuple(int(v) for v in np.median(im[130:170, 600:820].reshape(-1, 3), axis=0)))
print("border blue core (bright):", core_bright(87, 380, 90, 470, blum, "mxL"))
print("border green core (bright):", core_bright(624, 400, 628, 460, gren, "noteL"))
print("highlight yellow core (bright):", core_bright(148, 247, 188, 266, (R > 170) & (G > 150) & (R - B > 70), "hlY"))
print("highlight green core (bright):", core_bright(434, 250, 490, 266, gren, "hlG"))
