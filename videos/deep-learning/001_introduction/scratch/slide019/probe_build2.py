#!/usr/bin/env python3
"""Probe round 2: exact border strokes, title, ellipse ring, annot border, verr, container."""
import numpy as np
from PIL import Image
from collections import Counter

IM = np.asarray(Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_019.jpg").convert("RGB")).astype(int)
r, g, b = IM[..., 0], IM[..., 1], IM[..., 2]
lum = (r * 299 + g * 587 + b * 114) // 1000

def modal(px, n=3):
    c = Counter((int(p[0]) // 16 * 16, int(p[1]) // 16 * 16, int(p[2]) // 16 * 16) for p in px)
    return [(f"#{v[0]:02X}{v[1]:02X}{v[2]:02X}", k) for v, k in c.most_common(n)]

def runs(mask1d, base):
    out, s = [], None
    for i, v in enumerate(mask1d):
        if v and s is None: s = i
        elif not v and s is not None: out.append((base + s, base + i - 1)); s = None
    if s is not None: out.append((base + s, base + len(mask1d) - 1))
    return out

print("== TITLE (red, y60..97, excluding panel border row 100) ==")
red = (r > 120) & (g < 80) & (b < 80)
m = red[60:97, 60:920]
ys, xs = np.nonzero(m)
print(" title ink:", 60 + xs.min(), "..", 60 + xs.max(), " y", 60 + ys.min(), "..", 60 + ys.max(),
      " center", (60 + xs.min() + 60 + xs.max()) / 2, " n", len(xs))

print("== BOX BORDER STROKES: row y=250 and y=220 scan for dark strokes ==")
for label, y, x0, x1 in [("input row250", 250, 55, 175), ("samples row250", 250, 800, 920),
                          ("pre row250", 250, 185, 300), ("extr row250", 250, 305, 420),
                          ("sel row250", 250, 420, 535), ("classif row250", 250, 525, 645),
                          ("pred row250", 250, 645, 745), ("verr row235", 235, 730, 815),
                          ("verr row220", 220, 730, 815)]:
    dk = lum[y, x0:x1] < 205
    print(f" {label}: dark runs {runs(dk, x0)}")
print(" col scans (vertical borders):")
for label, x, y0, y1 in [("input col100", 100, 190, 290), ("samples col845", 845, 190, 290),
                          ("pre col240", 240, 190, 290), ("extr col360", 360, 190, 290),
                          ("sel col470", 470, 190, 290), ("classif col580", 580, 195, 285),
                          ("pred col695", 695, 195, 285), ("verr col770", 770, 160, 315)]:
    dk = lum[y0:y1, x] < 205
    print(f" {label}: dark runs {runs(dk, y0)}")

print("== ELLIPSE ring color at bottom arc ==")
for y in (152, 154, 156, 158):
    xs = np.nonzero(lum[y, 360:500] < 200)[0] + 360
    if len(xs): print(f" row {y}: dark cols {runs(lum[y,360:500]<200,360)[:6]} modal", modal(IM[y, xs], 3))
print(" ellipse top arc rows:")
for y in (100, 103, 106):
    xs = np.nonzero(lum[y, 360:500] < 200)[0] + 360
    if len(xs): print(f" row {y}: dark cols {runs(lum[y,360:500]<200,360)[:6]} modal", modal(IM[y, xs], 3))

print("== ANNOT BOX: stroke scan ==")
for y in (328, 332, 336, 398, 402, 406):
    dk = lum[y, 190:820] < 225
    rr = runs(dk, 190)
    print(f" annot row {y}: {len(rr)} runs", rr[:4], "..." if len(rr) > 4 else "",
          ("modal " + modal(IM[y, [x for x0, x1 in rr[:8] for x in range(x0, x1+1)]], 3)) if rr else "")
for x in (200, 210, 250, 300, 500, 700, 790, 800):
    dk = lum[325:412, x] < 225
    rr = runs(dk, 325)
    print(f" annot col {x}: {len(rr)} runs", rr[:5], ("modal " + modal(IM[[y for y0, y1 in rr[:6] for y in range(y0, y1+1)], x], 3)) if rr else "")

print("== ANNOT fill extent (greenish tint, loose) ==")
tint = (g > r) & (g >= b) & (lum < 250) & (lum > 200)
m = tint[325:412, 180:830]
ys, xs = np.nonzero(m)
print(" tint bbox:", 180 + xs.min(), "..", 180 + xs.max(), " y", 325 + ys.min(), "..", 325 + ys.max())
row = tint[370, 180:830]
print(" row370 tint runs:", runs(row, 180)[:3], runs(row, 180)[-3:] if row.any() else "")
col = tint[325:412, 500]
print(" col500 tint runs:", runs(col, 325))

print("== VERR: pink fill extent + border check ==")
pink = (r > 230) & (g > 140) & (g < 215) & (b > 140) & (b < 220) & (r > g + 30)
m = pink[160:320, 730:820]
ys, xs = np.nonzero(m)
print(" pink bbox:", 730 + xs.min(), "..", 730 + xs.max(), " y", 160 + ys.min(), "..", 160 + ys.max(), " n", len(xs))
print(" pink row250 runs:", runs(pink[250, 730:820], 730))
print(" pink col770 runs:", runs(pink[160:320, 770], 160))
print(" verr fill modal:", modal(IM[250:270, 758:786].reshape(-1, 3), 4))

print("== CONTAINER: dash rows/cols + fill ==")
cred = (r > 130) & (g < 80) & (b < 80)
for y in (195, 196, 197, 198, 272, 273, 274, 275):
    n = cred[y, 210:620].sum()
    print(f" container row {y}: red px {n}", runs(cred[y, 210:620], 210)[:5] if n else "")
for x in (196, 198, 200, 202, 626, 628, 630, 632, 640, 650, 656):
    n = cred[200:270, x].sum()
    print(f" container col {x}: red px {n}", runs(cred[200:270, x], 200)[:4] if n else "")
print(" container fill sample (300,212):", IM[212, 300], " (620,270):", IM[270, 620], " (210,240):", IM[240, 210])
print(" container corner check row198 cols 200..230:", runs(cred[198, 195:235], 195))

print("== PANEL border cols/rows (x70,x894,y100,y464?) ==")
print(" row235 dark runs x60..100:", runs(lum[235, 60:100] < 190, 60))
print(" row235 dark runs x880..910:", runs(lum[235, 880:910] < 190, 880))
print(" col500 dark runs y92..108:", runs(lum[92:108, 500] < 190, 92))
print(" col500 dark runs y455..472:", runs(lum[455:472, 500] < 190, 455))
print(" panel border modal:", modal(IM[100, 300:600], 3), modal(IM[235, 69:72].reshape(-1, 3), 3))

print("== BLACK BAR ==")
blk = lum < 60
print(" row528 black runs:", runs(blk[528, 0:960], 0)[:3])
print(" col100 black runs:", runs(blk[500:540, 100], 500))

print("== TEXT BANDS per box (dark, excluding pencil for pre) ==")
def bands(x0, y0, x1, y1, label):
    m = lum[y0:y1, x0:x1] < 140
    rows = np.nonzero(m.any(axis=1))[0] + y0
    if not len(rows): print(f" {label}: none"); return
    br, s = [], rows[0]
    for a, bb in zip(rows, rows[1:]):
        if bb - a > 2: br.append((s, a)); s = bb
    br.append((s, rows[-1]))
    cols = np.nonzero(m.any(axis=0))[0] + x0
    print(f" {label}: bands {br} cols {cols.min()}..{cols.max()}")
bands(84, 205, 156, 262, "input text")
bands(810, 205, 885, 262, "samples text")
bands(198, 236, 290, 268, "pre text line2-only")   # below pencil (pencil ends ~234)
bands(316, 210, 410, 262, "extr text")
bands(428, 210, 515, 262, "sel text")
bands(657, 210, 740, 262, "pred text")
bands(388, 115, 450, 152, "ellipse text")
bands(536, 226, 626, 244, "classif white text")
