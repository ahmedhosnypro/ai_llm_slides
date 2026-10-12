#!/usr/bin/env python3
"""forensics7.py — refinement: arrows, bullets, starburst text angle/fill, legend fill,
title runs, eq term columns, per-line extents. Banked to qa/slide045/forensics7_out.txt."""
import numpy as np
from PIL import Image

im = np.asarray(Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_045.jpg").convert("RGB")).astype(int)
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]

def runs(idx):
    out, s, p = [], None, None
    for i in idx:
        if s is None: s = p = i
        elif i == p + 1: p = i
        else: out.append((s, p)); s = p = i
    if s is not None: out.append((s, p))
    return out

def bbox(mask, x0, x1, y0, y1, label):
    ys, xs = np.where(mask[y0:y1, x0:x1])
    if len(ys) == 0:
        print(f" {label}: EMPTY"); return None
    print(f" {label}: x{xs.min()+x0}..{xs.max()+x0} y{ys.min()+y0}..{ys.max()+y0} n={len(ys)}")
    return (xs.min()+x0, xs.max()+x0, ys.min()+y0, ys.max()+y0)

# --- 1. ARROWS: very soft red mask on white/gray background ---
red_very = (r - g > 22) & (r - b > 15) & (r > 150) & (g < 215)
m = red_very.copy()
m[:, :640] = False; m[:, 733:] = False   # corridor between eq interior and callouts
m[290:296, :] = False; m[497:505, :] = False
print("== ARROW corridor strokes (x640..733) ==")
ys, xs = np.where(m[300:470, 640:733])
if len(ys):
    print(f" corridor bbox: x{xs.min()+640}..{xs.max()+640} y{ys.min()+300}..{ys.max()+300} n={len(ys)}")
    for yy in range(ys.min()+300, ys.max()+301):
        rr = np.where(m[yy, 640:733])[0] + 640
        if len(rr): print(f"   y={yy}: x{rr.min()}..{rr.max()} n={len(rr)}")
print(" arrowhead search inside panel (x560..697, y330..370 / y415..470):")
bbox(red_very, 560, 697, 330, 372, "head/zone A (eq a row)")
bbox(red_very, 560, 697, 415, 470, "head/zone B (eq c row)")
# also: does the stroke cross the border? scan x694..736 explicitly
m2 = red_very.copy(); m2[:, :694] = False; m2[:, 736:] = False
print(" crossing x694..735:")
ys, xs = np.where(m2[300:470, :])
if len(ys):
    for yy in sorted(set(ys + 300)):
        rr = np.where(m2[yy, :])[0]
        if len(rr): print(f"   y={yy}: x{rr.min()}..{rr.max()} n={len(rr)}")

# --- 2. BULLETS: dark circles x294..345 ---
dark = (r < 130) & (g < 130) & (b < 130)
print("== BULLET circles ==")
for (ya, yb, lb) in [(296, 314, "b1"), (370, 394, "b2"), (418, 442, "b3")]:
    bb = bbox(dark, 294, 346, ya, yb, f"{lb} circle")
print(" bullet text bands (x346..690):")
for (ya, yb, lb) in [(296, 314, "b1"), (370, 394, "b2"), (418, 442, "b3")]:
    bb = bbox(dark | ((r - g > 22) & (r - b > 15) & (r > 150) & (g < 215)), 346, 690, ya, yb, f"{lb} text")

# --- 3. EQ term columns (dark ink column profile) ---
print("== EQ(a) col profile x440..695 y318..368 (main body) ==")
prof = dark[318:368, 440:695].sum(axis=0)
print(" cols with ink:", runs(np.where(prof > 0)[0] + 440))
print("== EQ(a) upper region y296..318 ==")
prof = dark[296:318, 440:695].sum(axis=0)
print(" cols with ink:", runs(np.where(prof > 0)[0] + 440))
print("== EQ(c) col profile x420..695 y424..492 ==")
prof = dark[424:492, 420:695].sum(axis=0)
print(" cols with ink:", runs(np.where(prof > 0)[0] + 420))
print("== EQ(b) bbox verify ==")
bbox(dark, 460, 694, 388, 418, "eq(b)")

# --- 4. TITLE runs: color per column (red vs blue) ---
red_t = (r > 120) & (r - g > 60) & (r - b > 50)
blue_t = (b > 120) & (b - r > 60) & (b - g > 40)
print("== TITLE run colors (y66..102) ==")
for (x0, x1, lb) in [(190, 290, "word1"), (290, 560, "word2-zone"), (560, 700, "word3-zone"), (700, 780, "word4-zone")]:
    n_red = red_t[66:102, x0:x1].sum(); n_blue = blue_t[66:102, x0:x1].sum()
    print(f" {lb} x{x0}..{x1}: red={n_red} blue={n_blue}")
print(" title col-runs (any ink):")
anyt = red_t[66:102, 150:800] | blue_t[66:102, 150:800] | dark[66:102, 150:800]
print(" ", runs(np.where(anyt.sum(axis=0) > 0)[0] + 150))
print(" title row bands:", runs(np.where(anyt.sum(axis=1) > 2)[0] + 66))

# --- 5. STARBURST: text ink + angle + fill ---
print("== STARBURST ==")
red_strict = (r > 120) & (g < 90) & (b < 90)
# text-only: interior x798..880 y70..130, red
ys, xs = np.where(red_strict[70:130, 798:880])
if len(ys):
    X = xs + 798; Y = ys + 70
    print(f" text-red bbox: x{X.min()}..{X.max()} y{Y.min()}..{Y.max()} n={len(ys)}")
    # PCA angle (y down; positive angle = text descends to the right = CW rotation)
    Xc, Yc = X - X.mean(), Y - Y.mean()
    cov = np.cov(np.vstack([Xc, Yc]))
    evals, evecs = np.linalg.eigh(cov)
    v = evecs[:, -1]
    ang = np.degrees(np.arctan2(v[1], v[0]))
    print(f" PCA major-axis angle (deg, y-down): {ang:.1f}  (negative = rises to the right = CCW)")
    # row-band extents at slices for slope check
    for sl in [(0, 20), (20, 40), (40, 62)]:
        sel = (Y >= Y.min()+sl[0]) & (Y < Y.min()+sl[1])
        if sel.sum() > 10:
            print(f"  slice rows+{sl}: x {X[sel].min()}..{X[sel].max()}  y-mean {Y[sel].mean():.1f}")
# fill color: clean patch right-lower inside (x855..885, y115..140)
samp = im[115:140, 855:885].reshape(-1, 3)
ym = samp[(samp[:, 0] > 220) & (samp[:, 1] > 220)]
if len(ym): print(f" fill clean-patch median: {tuple(np.median(ym, axis=0).astype(int))} n={len(ym)}")
# spike stroke color: red on the perimeter
samp = im[52:60, 810:830].reshape(-1, 3)
rm = samp[(samp[:, 0] > 130) & (samp[:, 0] - samp[:, 1] > 60)]
if len(rm): print(f" spike-stroke median: {tuple(np.median(rm, axis=0).astype(int))} n={len(rm)}")

# --- 6. LEGEND fill + symbol colors ---
print("== LEGEND ==")
samp = im[371:381, 90:250].reshape(-1, 3)
bright = samp[samp.sum(axis=1) > 640]
if len(bright): print(f" legend fill median: {tuple(np.median(bright, axis=0).astype(int))} n={len(bright)}")
# symbol column color (x76..115, rows 359..368 & 419..429)
samp = np.vstack([im[359:368, 76:115].reshape(-1, 3), im[419:429, 76:115].reshape(-1, 3)])
dm = samp[samp.sum(axis=1) < 450]
if len(dm): print(f" legend symbol ink median: {tuple(np.median(dm, axis=0).astype(int))} n={len(dm)}")
# meaning text color
samp = im[383:390, 117:250].reshape(-1, 3)
dm = samp[samp.sum(axis=1) < 300]
if len(dm): print(f" legend meaning ink median: {tuple(np.median(dm, axis=0).astype(int))} n={len(dm)}")
# per-line col extents
darkl = (r < 150) & (g < 150) & (b < 150)
for (ya, yb, lb) in [(356, 372, "L1"), (376, 394, "L2"), (396, 412, "L3"), (415, 432, "L4")]:
    bb = bbox(darkl, 70, 260, ya, yb, f"legend {lb}")

# --- 7. DEFBOX per-line extents + bold-core color ---
print("== DEFBOX lines ==")
for (ya, yb, lb) in [(117, 150, "L1"), (150, 175, "L2"), (176, 205, "L3")]:
    bb = bbox(darkl, 76, 880, ya, yb, f"defbox {lb}")
samp = im[182:198, 81:130].reshape(-1, 3)  # 'Input:' bold lead of L3
dm = samp[samp.sum(axis=1) < 260]
if len(dm): print(f" defbox L3 bold-core median: {tuple(np.median(dm, axis=0).astype(int))} n={len(dm)}")

# --- 8. REMEMBER lines ---
print("== REMEMBER lines ==")
rem = (r - g > 40) & (r - b > 30) & (r > 110) & (r < 230)
for (ya, yb, lb) in [(230, 250, "L1"), (250, 274, "L2")]:
    bb = bbox(rem, 74, 880, ya, yb, f"remember {lb}")
samp = im[235:247, 85:200].reshape(-1, 3)
dm = samp[(samp[:, 0] > 100) & (samp[:, 0] - samp[:, 1] > 60)]
if len(dm): print(f" remember text-core median: {tuple(np.median(dm, axis=0).astype(int))} n={len(dm)}")

# --- 9. CALLOUT text extents ---
print("== CALLOUT text ==")
for (ya, yb, xa, xb, lb) in [(367, 390, 738, 893, "weights"), (424, 448, 737, 876, "input")]:
    bb = bbox(darkl, xa, xb, ya, yb, f"{lb} dark")
    bb = bbox(blue_t, xa, xb, ya, yb, f"{lb} blue-lead")

# --- 10. EQ ink color + defbox border stroke profile ---
print("== misc ==")
samp = im[330:360, 480:560].reshape(-1, 3)
dm = samp[samp.sum(axis=1) < 260]
if len(dm): print(f" eq(a) ink median: {tuple(np.median(dm, axis=0).astype(int))} n={len(dm)}")
# defbox border: vertical slice colors at y112..118, x300..320
samp = im[112:118, 300:320].reshape(-1, 3)
bm = samp[(samp[:, 2] - samp[:, 0] > 15)]
if len(bm): print(f" defbox top-border blue median: {tuple(np.median(bm, axis=0).astype(int))} n={len(bm)}")
# eqpanel border core
samp = im[289:295, 350:650].reshape(-1, 3)
rm = samp[(samp[:, 0] > 110) & (samp[:, 0] - samp[:, 1] > 70)]
if len(rm): print(f" eqpanel top-border red median: {tuple(np.median(rm, axis=0).astype(int))} n={len(rm)}")
