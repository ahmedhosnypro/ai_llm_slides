#!/usr/bin/env python3
"""probe7 — final consolidated PIL measurements for slide 025 build.
Resumes from forensics_025_* + qa/slide025/measure2-5 (never re-derive what exists).
Answers: panel edges, col0 circle cx, fan lines, eq-box borders/ink, arrow/callout
column profiles, blackbar, error-class gap blob, crop dims for vision montage.
"""
from PIL import Image
import numpy as np

SRC = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_025.jpg"
im = Image.open(SRC).convert("RGB")
a = np.asarray(im).astype(int)
H, W = a.shape[:2]
print(f"size {W}x{H}")

def runs(mask_1d):
    idx = np.where(mask_1d)[0]
    if len(idx) == 0:
        return []
    out, s, p = [], idx[0], idx[0]
    for v in idx[1:]:
        if v == p + 1:
            p = v
        else:
            out.append((int(s), int(p))); s, p = v, v
    out.append((int(s), int(p)))
    return out

# 1) panel edges: strict beige (218,208,196) +/-12 on clean rows
print("== panel beige row extents (clean rows) ==")
beige = (abs(a[:,:,0]-218)<=12) & (abs(a[:,:,1]-208)<=12) & (abs(a[:,:,2]-196)<=12)
for y in [136, 140, 145, 148, 155, 395, 400, 405]:
    r = runs(beige[y])
    print(f"  y{y}: {r[:4]}")
print("  per-column first/last beige row:")
for x in [70, 100, 300, 500, 590, 600, 605, 610]:
    c = np.where(beige[:, x])[0]
    print(f"   x{x}: {c.min() if len(c) else None}..{c.max() if len(c) else None} n={len(c)}")

# 2) col0 circle outline: dark ring pixels x140..190, rows 160..205 etc.
print("== col0 circle outlines (dark px x138..195 per row band) ==")
dark = (a.sum(axis=2) < 330)
for (y0, y1) in [(158, 210), (230, 282), (312, 364)]:
    sub = dark[y0:y1, 138:196]
    ys, xs = np.where(sub)
    if len(xs):
        print(f"  band {y0}..{y1}: x {138+xs.min()}..{138+xs.max()}, y {y0+ys.min()}..{y0+ys.max()}, n={len(xs)}")
        # horizontal center estimate: midpoint of leftmost/rightmost dark cols
        print(f"    cx est {(138+xs.min()+138+xs.max())/2:.1f}")

# 3) fan lines: grayish px x84..146 between dots and col0 rim
print("== fan lines (non-beige, non-dark px x84..146) ==")
r_, g_, b_ = a[:,:,0], a[:,:,1], a[:,:,2]
grayish = (abs(r_-172)<38) & (abs(g_-162)<38) & (abs(b_-152)<38)
for (y0, y1) in [(160, 210), (232, 284), (314, 366)]:
    sub = grayish[y0:y1, 84:147]
    ys, xs = np.where(sub)
    if len(xs):
        print(f"  band {y0}..{y1}: n={len(xs)}, x {84+xs.min()}..{84+xs.max()}, y {y0+ys.min()}..{y0+ys.max()}")
        # y positions at a few x columns
        for xc in [90, 110, 130, 143]:
            col = np.where(grayish[y0:y1, xc])[0]
            print(f"    x{xc}: rows {[y0+int(v) for v in col[:8]]}")

# 4) eq boxes: dark border bbox per window + fill + ink
print("== eq boxes ==")
darkish = (a.sum(axis=2) < 420)
creamish = (r_>235) & (g_>235) & (b_>195) & (b_<245)
for i, (x0, x1) in enumerate([(55, 285), (285, 515), (515, 790)]):
    win = darkish[435:520, x0:x1]
    ys, xs = np.where(win)
    print(f"  box{i+1} dark-border bbox: ({x0+xs.min()}, {435+ys.min()}, {x0+xs.max()}, {435+ys.max()})")
    winc = creamish[435:520, x0:x1]
    ys2, xs2 = np.where(winc)
    print(f"  box{i+1} cream fill bbox: ({x0+xs2.min()}, {435+ys2.min()}, {x0+xs2.max()}, {435+ys2.max()})")
    # ink inside fill (dark px strictly inside border)
    fx0, fy0, fx1, fy1 = x0+xs2.min()+3, 435+ys2.min()+3, x0+xs2.max()-3, 435+ys2.max()-3
    sub = darkish[fy0:fy1, fx0:fx1]
    ys3, xs3 = np.where(sub)
    if len(xs3):
        print(f"  box{i+1} ink bbox: ({fx0+xs3.min()}, {fy0+ys3.min()}, {fx0+xs3.max()}, {fy0+ys3.max()})")

# 5) arrows vs callouts column profiles (i region x225..315, j region x380..480)
print("== bottom region column profiles (fill-classified per row) ==")
i_fill = (abs(r_-228)<14) & (abs(g_-234)<14) & (b_>246)
j_fill = (abs(r_-215)<12) & (g_>246) & (abs(b_-178)<14)
prev_fill = (abs(r_-222)<10) & (abs(g_-235)<10) & (abs(b_-244)<8)
curr_fill = (abs(r_-214)<10) & (g_>246) & (abs(b_-180)<12)
def prof(mask, x0, x1, y0, y1, label):
    print(f"  {label}:")
    for y in range(y0, y1, 3):
        r = runs(mask[y, x0:x1])
        if r:
            print(f"    y{y}: {[(x0+s, x0+e) for s, e in r]}")
prof(i_fill, 225, 315, 366, 440, "i arrow fill")
prof(j_fill, 380, 480, 366, 440, "j arrow fill")
prof(prev_fill, 205, 320, 390, 440, "prev callout fill")
prof(curr_fill, 375, 485, 390, 440, "curr callout fill")

# 6) error-class gap blob x603..612
print("== gap x602..614, red-ish px ==")
redish = (r_>140) & (g_<120) & (b_<130)
for y in range(160, 200, 4):
    r = runs(redish[y, 602:615])
    if r:
        print(f"  y{y}: {[(602+s, 602+e) for s, e in r]}")

# 7) blackbar
print("== blackbar ==")
nearblack = (a.sum(axis=2) < 180)
rows = [y for y in range(500, 540) if nearblack[y, 100:900].sum() > 700]
print(f"  rows: {rows[0] if rows else None}..{rows[-1] if rows else None}")
if rows:
    y = rows[0]
    r = runs(nearblack[y])
    print(f"  x extent at y{y}: {r[:3]}")

# 8) crop dims (for vision montage planning)
import os
D = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/scratch/slide025"
print("== crop dims ==")
for f in sorted(os.listdir(D)):
    if f.endswith(".png"):
        w, h = Image.open(os.path.join(D, f)).size
        print(f"  {f}: {w}x{h}")
