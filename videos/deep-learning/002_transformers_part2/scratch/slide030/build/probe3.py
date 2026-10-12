#!/usr/bin/env python3
"""Slide 030: final detail probes (v1 text color, note lines, brace anatomy, brackets, =)."""
import numpy as np
from PIL import Image

im = np.asarray(Image.open("videos/deep-learning/002_transformers_part2/unique_slides/slide_030.jpg").convert("RGB")).astype(int)
R, G, B = im[:, :, 0], im[:, :, 1], im[:, :, 2]
lum = (R + G + B) / 3
redm = (R > 90) & (R - G > 50) & (R - B > 50)
blum = (B > 90) & (B - R > 30) & (B - G > 30)
blam = (R < 110) & (G < 110) & (B < 110)
inkm = lum < 150
gren = (G > 100) & (G - R > 20) & (G - B > 20)

def core_dark(x0, y0, x1, y1, sel, label):
    reg = im[y0:y1, x0:x1]
    m = sel[y0:y1, x0:x1]
    if m.sum() == 0:
        print(f"{label}: none"); return
    px = reg[m]
    s = px.sum(axis=1)
    idx = np.argsort(s)[:max(1, len(s) // 4)]
    print(f"{label}: n={int(m.sum())} darkest-quartile={tuple(np.median(px[idx], axis=0).astype(int))}")

def rowspans(x0, y0, x1, y1, mask, gap=3, minpx=1):
    prof = mask[y0:y1, x0:x1].sum(axis=1)
    spans, s, gaprun = [], None, 0
    for i, v in enumerate(prof):
        if v >= minpx:
            if s is None: s = i
            gaprun = 0
        else:
            if s is not None:
                gaprun += 1
                if gaprun >= gap:
                    spans.append((s + y0, i - gaprun + y0)); s = None
    if s is not None: spans.append((s + y0, len(prof) - 1 + y0))
    return spans

def colspans(x0, y0, x1, y1, mask, gap=4, minpx=1):
    prof = mask[y0:y1, x0:x1].sum(axis=0)
    spans, s, gaprun = [], None, 0
    for i, v in enumerate(prof):
        if v >= minpx:
            if s is None: s = i
            gaprun = 0
        else:
            if s is not None:
                gaprun += 1
                if gaprun >= gap:
                    spans.append((s + x0, i - gaprun + x0)); s = None
    if s is not None: spans.append((s + x0, len(prof) - 1 + x0))
    return spans

print("== V1 TEXT COLOR ==")
core_dark(261, 68, 330, 88, redm, "v1 r1 'sin(wt)' red-mask")
core_dark(261, 68, 330, 88, blam, "v1 r1 black-mask")
core_dark(261, 114, 330, 138, redm, "v1 r2 'cos(wt)' red-mask")
print("v1 r1 rows via red:", rowspans(255, 60, 335, 140, redm, gap=4))
print("v1 r1 cols via red (y66..90):", colspans(255, 66, 335, 90, redm, gap=4))

print("== NOTE LINES ==")
print("rows (blue):", rowspans(630, 360, 890, 470, blum, gap=3))
print("rows (red):", rowspans(630, 360, 890, 470, redm, gap=3))
print("L-header cols (red, y365..390):", colspans(628, 365, 890, 390, redm, gap=6)[:2], "...")
print("note header red core:", end=" ")
reg = im[365:390, 640:850]; m = redm[365:390, 640:850]
px = reg[m]; s = px.sum(axis=1); idx = np.argsort(s)[:max(1, len(s)//4)]
print(tuple(np.median(px[idx], axis=0).astype(int)) if len(px) else "none")

print("== REMEMBER ==")
print("id rows tight:", rowspans(510, 140, 850, 190, blum, gap=2))
print("id1 cols:", colspans(505, 145, 850, 162, blum, gap=5))
print("id2 cols:", colspans(505, 163, 850, 190, blum, gap=5))
print("header cols:", colspans(505, 108, 850, 127, blum, gap=4))
print("underline row extent x:", colspans(505, 121, 850, 126, blum, gap=8))

print("== BRACE ANATOMY ==")
print("rows:", rowspans(272, 442, 471, 475, redm, gap=2))
print("arm cols:", {x: int(redm[442:470, x].sum()) for x in list(range(270, 292)) + list(range(452, 472)) if redm[442:470, x].sum() > 3})
print("cusp cols x365..385:", {x: int(redm[458:470, x].sum()) for x in range(360, 390) if redm[458:470, x].sum() > 2})
print("brace red core:", end=" ")
reg = im[447:468, 272:470]; m = redm[447:468, 272:470]
px = reg[m]; s = px.sum(axis=1); idx = np.argsort(s)[:max(1, len(s)//4)]
print(tuple(np.median(px[idx], axis=0).astype(int)))

print("== BRACKETS ==")
# v1 red bracket: left stroke x242-244 y58..137; right stroke x329? find tick extents
print("v1 left stroke tick rows (x242..252):", rowspans(242, 55, 253, 145, redm, gap=2))
print("v1 right stroke rows (x325..340):", rowspans(325, 55, 341, 145, redm, gap=2))
print("v1 right stroke cols (y58..137):", {x: int(redm[58:137, x].sum()) for x in range(320, 345) if redm[58:137, x].sum() > 20})
print("v1 stroke width sample row 100:", {x: int(redm[100, x]) for x in range(240, 250)})
print("v2 left stroke cols (y150..230):", {x: int(blam[150:230, x].sum()) for x in range(238, 252) if blam[150:230, x].sum() > 20})
print("v2 left tick rows (x243..255):", rowspans(243, 145, 256, 238, blam, gap=2))
print("v2 stroke width sample row 190:", {x: int(blam[190, x]) for x in range(240, 250)})
# matrix blue brackets
print("mx L stroke cols:", {x: int(blum[345:435, x].sum()) for x in range(276, 292) if blum[345:435, x].sum() > 20})
print("mx L tick rows (x279..290):", rowspans(279, 345, 291, 435, blum, gap=2))
print("mx R stroke cols:", {x: int(blum[345:435, x].sum()) for x in range(465, 480) if blum[345:435, x].sum() > 20})
print("mx bracket blue core:", end=" ")
reg = im[350:430, 279:282]; px = reg.reshape(-1, 3); s = px.sum(axis=1); idx = np.argsort(s)[:max(1, len(s)//3)]
print(tuple(np.median(px[idx], axis=0).astype(int)))
# left-vec black brackets
print("lv L stroke cols (y350..435):", {x: int(blam[350:435, x].sum()) for x in range(115, 128) if blam[350:435, x].sum() > 20})
print("lv R stroke cols:", {x: int(blam[350:435, x].sum()) for x in range(230, 245) if blam[350:435, x].sum() > 20})
print("lv L tick rows (x120..132):", rowspans(120, 345, 133, 438, blam, gap=2))
# right-vec red brackets
print("rv L stroke cols:", {x: int(redm[350:435, x].sum()) for x in range(480, 492) if redm[350:435, x].sum() > 20})
print("rv R stroke cols:", {x: int(redm[350:435, x].sum()) for x in range(565, 578) if redm[350:435, x].sum() > 20})
print("rv L tick rows (x484..496):", rowspans(484, 345, 497, 438, redm, gap=2))

print("== EQUALS ==")
print("eq bbox wide band:", end=" ")
ys, xs = np.where(blam[370:410, 244:278])
print(f"x {xs.min()+244}..{xs.max()+244} y {ys.min()+370}..{ys.max()+370}" if len(xs) else "none")
print("eq rows:", rowspans(244, 370, 278, 412, blam, gap=2))

print("== DERIV FONT METRICS ==")
print("L1 'sin(omega(t+delta))' bbox:", end=" ")
ys, xs = np.where(inkm[246:270, 100:196])
print(f"x {xs.min()+100}..{xs.max()+100} y {ys.min()+246}..{ys.max()+246}")
print("L2 'cos(omega(t+delta))' bbox:", end=" ")
ys, xs = np.where(inkm[290:316, 100:202])
print(f"x {xs.min()+100}..{xs.max()+100} y {ys.min()+290}..{ys.max()+290}")
# v2 cell r1 exact rows/cols for 'Sin (omega(t+delta))'
print("v2 r1 bbox (non-highlight rows):", end=" ")
ys, xs = np.where(blam[150:180, 245:358])
print(f"x {xs.min()+245}..{xs.max()+245} y {ys.min()+150}..{ys.max()+150}")
print("v2 r2 bbox:", end=" ")
ys, xs = np.where(blam[190:222, 245:358])
print(f"x {xs.min()+245}..{xs.max()+245} y {ys.min()+190}..{ys.max()+190}")
