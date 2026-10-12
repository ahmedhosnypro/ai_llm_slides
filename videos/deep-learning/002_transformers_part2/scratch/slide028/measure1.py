#!/usr/bin/env python3
"""slide_028 measurement pass 1 — verify inherited blocks vs slide_027's certified
values and measure the delta blocks (chips 5..8, heads 4..7, labels 4..7).

FRAME->SLIDE mapping (parent-certified, 002 capture zoom-out):
  frame_x = 18.63 + 0.96123*slide_x ; frame_y = 0.95556*slide_y
  -> slide_x = (frame_x-18.63)/0.96123 ; slide_y = frame_y/0.95556
"""
import numpy as np
from PIL import Image
from scipy import ndimage as ndi
import json

A = np.asarray(Image.open(
    "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_028.jpg"
).convert("RGB")).astype(int)
H, W = A.shape[:2]
r, g, b = A[:, :, 0], A[:, :, 1], A[:, :, 2]

FX0, SX_K = 18.63, 0.96123
SY_K = 0.95556
def sx(fx): return (fx - FX0) / SX_K
def sy(fy): return fy / SY_K

out = {}

# ---------- 1. chrome landmarks ----------
# panel: gray E9E9E7-ish; border red C00000. Scan mid rows/cols.
def is_gray(c): return abs(c[0]-233) < 14 and abs(c[1]-233) < 14 and abs(c[2]-231) < 14
row = A[270]
xs = [x for x in range(W) if is_gray(row[x])]
print(f"chrome: gray panel row270 x {min(xs)}..{max(xs)}")
col = A[:, 480]
ys = [y for y in range(H) if is_gray(col[y])]
print(f"chrome: gray panel col480 y {min(ys)}..{max(ys)}")
out["chrome"] = {"panel_row270_x": [int(min(xs)), int(max(xs))], "panel_col480_y": [int(min(ys)), int(max(ys))]}

# ---------- 2. title lines (red ink, top-left) ----------
red = (r > 130) & (g < 90) & (b < 90)
tit = red.copy()
tit[:, 480:] = False  # left half only (badge is right; frame border at x<45)
# restrict to y 40..170 (title zone)
tit[:40] = False; tit[170:] = False
rows_ink = tit.sum(axis=1)
print("\ntitle: red ink rows y40..170 (row: count):")
bands, inb = [], False
for y in range(40, 170):
    if rows_ink[y] > 0 and not inb:
        y0 = y; inb = True
    elif rows_ink[y] == 0 and inb:
        bands.append((y0, y - 1)); inb = False
if inb: bands.append((y0, 169))
title_lines = []
for (y0, y1) in bands:
    band = tit[y0:y1 + 1]
    xs2 = np.where(band.sum(axis=0) > 0)[0]
    title_lines.append({"frame_bbox": [int(xs2.min()), int(y0), int(xs2.max()), int(y1)],
                        "slide": [round(sx(xs2.min()), 1), round(sy(y0), 1),
                                  round(sx(xs2.max()), 1), round(sy(y1), 1)]})
    print(f"  line y {y0}..{y1}: x {xs2.min()}..{xs2.max()} w {xs2.max()-xs2.min()+1}  slide y {sy(y0):.1f}..{sy(y1):.1f} x {sx(xs2.min()):.1f}..{sx(xs2.max()):.1f}")
out["title_lines"] = title_lines

# ---------- 3. equation box (pale yellow FFFFCC + border) ----------
eqy = (r > 235) & (g > 235) & (b > 170) & (b < 225)
eqy[:, 300:] = False; eqy[150:] = False; eqy[:150] = False
lab, n = ndi.label(eqy)
if n:
    sizes = ndi.sum(eqy, lab, range(1, n + 1))
    big = int(np.argmax(sizes)) + 1
    ys3, xs3 = np.where(lab == big)
    print(f"\neq box: frame x {xs3.min()}..{xs3.max()} y {ys3.min()}..{ys3.max()}  "
          f"slide x {sx(xs3.min()):.1f}..{sx(xs3.max()):.1f} y {sy(ys3.min()):.1f}..{sy(ys3.max()):.1f}")
    out["eqbox"] = {"frame": [int(xs3.min()), int(ys3.min()), int(xs3.max()), int(ys3.max())],
                    "slide": [round(sx(xs3.min()), 1), round(sy(ys3.min()), 1),
                              round(sx(xs3.max()), 1), round(sy(ys3.max()), 1)]}
    # text lines inside
    sub = A[ys3.min():ys3.max() + 1, xs3.min():xs3.max() + 1]
    sr, sg, sb = sub[:, :, 0], sub[:, :, 1], sub[:, :, 2]
    ink = ((sb > 130) & (sr < 120) & (sg < 120)) | ((sr > 140) & (sg < 100) & (sb < 100) & (sr - sg > 60)) | ((sg > 110) & (sg - sr > 40) & (sg - sb > 40))
    rws = ink.sum(axis=1)
    inb = False; lns = []
    for yy in range(ink.shape[0]):
        if rws[yy] > 0 and not inb: yy0 = yy; inb = True
        elif rws[yy] == 0 and inb: lns.append((yy0, yy - 1)); inb = False
    if inb: lns.append((yy0, ink.shape[0] - 1))
    for i, (yy0, yy1) in enumerate(lns):
        bnd = ink[yy0:yy1 + 1]
        xs4 = np.where(bnd.sum(axis=0) > 0)[0]
        print(f"  eq L{i+1}: y {ys3.min()+yy0}..{ys3.min()+yy1} x {xs3.min()+xs4.min()}..{xs3.min()+xs4.max()}")

# ---------- 4. circle (FBFCC9 fill) ----------
cf = (r > 240) & (g > 240) & (b > 180) & (b < 225)
lab, n = ndi.label(cf)
if n:
    sizes = ndi.sum(cf, lab, range(1, n + 1))
    big = int(np.argmax(sizes)) + 1
    ys5, xs5 = np.where(lab == big)
    cx_f = (xs5.min() + xs5.max()) / 2.0; cy_f = (ys5.min() + ys5.max()) / 2.0
    rad_f = ((xs5.max() - xs5.min()) + (ys5.max() - ys5.min())) / 4.0
    print(f"\ncircle: frame center ({cx_f:.1f},{cy_f:.1f}) r {rad_f:.1f}  "
          f"slide center ({sx(cx_f):.1f},{sy(cy_f):.1f}) r {rad_f:.1f}")
    out["circle"] = {"frame_c": [round(cx_f, 1), round(cy_f, 1)], "frame_r": round(rad_f, 1),
                     "slide_c": [round(sx(cx_f), 1), round(sy(cy_f), 1)]}
    CXf, CYf = cx_f, cy_f
else:
    CXf, CYf = 577.0, 284.0

# ---------- 5. word chips (green CCFFCC fill / 009933 border/text) ----------
ch = ((g - r) > 25) & ((g - b) > 25)
ch[:, :200] = False  # exclude eq-box greens (text) on the left? eq text is at x<250; chips start x>640. Actually Word 6 at 180deg is x~440. eq box x<250.
ch[:, :300] = False
lab, n = ndi.label(ch)
chips = []
for i in range(1, n + 1):
    ys6, xs6 = np.where(lab == i)
    if len(ys6) < 150: continue
    h = ys6.max() - ys6.min(); w = xs6.max() - xs6.min()
    if h < 10 or h > 45 or w > 90: continue
    cx_f2 = (xs6.min() + xs6.max()) / 2.0; cy_f2 = (ys6.min() + ys6.max()) / 2.0
    dx = cx_f2 - CXf; dy = cy_f2 - CYf
    ang = np.degrees(np.arctan2(-dy, dx)) % 360
    chips.append({"frame_c": [round(cx_f2, 1), round(cy_f2, 1)],
                  "slide_c": [round(sx(cx_f2), 1), round(sy(cy_f2), 1)],
                  "ang_deg": round(float(ang), 1),
                  "rad_pt": round(float(np.hypot(dx, dy)), 1),
                  "wh": [int(w), int(h)], "n": int(len(ys6))})
chips.sort(key=lambda c: c["ang_deg"])
print(f"\nchips found: {len(chips)}")
for c in chips:
    print(f"  ang {c['ang_deg']:6.1f} rad {c['rad_pt']:6.1f} slide ({c['slide_c'][0]:6.1f},{c['slide_c'][1]:6.1f}) wh {c['wh']} n {c['n']}")
out["chips"] = chips

# ---------- 6. arrowheads (orange E06010) ----------
ah = (r > 170) & ((r - g) > 90) & ((g - b) > 50)
lab, n = ndi.label(ah)
heads = []
for i in range(1, n + 1):
    ys7, xs7 = np.where(lab == i)
    if len(ys7) < 20 or len(ys7) > 400: continue
    h = ys7.max() - ys7.min(); w = xs7.max() - xs7.min()
    if h > 30 or w > 30: continue
    cx_f3 = (xs7.min() + xs7.max()) / 2.0; cy_f3 = (ys7.min() + ys7.max()) / 2.0
    dx = cx_f3 - CXf; dy = cy_f3 - CYf
    ang = np.degrees(np.arctan2(-dy, dx)) % 360
    heads.append({"frame_c": [round(cx_f3, 1), round(cy_f3, 1)],
                  "slide_c": [round(sx(cx_f3), 1), round(sy(cy_f3), 1)],
                  "ang_deg": round(float(ang), 1),
                  "rad_pt": round(float(np.hypot(dx, dy)), 1), "wh": [int(w), int(h)]})
heads.sort(key=lambda c: c["ang_deg"])
print(f"\nheads found: {len(heads)}")
for c in heads:
    print(f"  ang {c['ang_deg']:6.1f} rad {c['rad_pt']:6.1f} slide ({c['slide_c'][0]:6.1f},{c['slide_c'][1]:6.1f}) wh {c['wh']}")
out["heads"] = heads

# ---------- 7. '+w' labels (red CC0000, in annulus r 200..300 frame px) ----------
rl = (r > 140) & ((r - g) > 60) & (g < 110) & (b < 110)
Y, X = np.mgrid[0:H, 0:W]
rr = np.hypot(X - CXf, Y - CYf)
ann = rl & (rr > 200) & (rr < 310)
lab, n = ndi.label(ann)
labels8 = []
for i in range(1, n + 1):
    ys8, xs8 = np.where(lab == i)
    if len(ys8) < 12: continue
    h = ys8.max() - ys8.min(); w = xs8.max() - xs8.min()
    if h > 25 or w > 45: continue
    cx_f4 = (xs8.min() + xs8.max()) / 2.0; cy_f4 = (ys8.min() + ys8.max()) / 2.0
    dx = cx_f4 - CXf; dy = cy_f4 - CYf
    ang = np.degrees(np.arctan2(-dy, dx)) % 360
    labels8.append({"frame_c": [round(cx_f4, 1), round(cy_f4, 1)],
                    "slide_c": [round(sx(cx_f4), 1), round(sy(cy_f4), 1)],
                    "ang_deg": round(float(ang), 1),
                    "rad_pt": round(float(np.hypot(dx, dy)), 1), "wh": [int(w), int(h)]})
labels8.sort(key=lambda c: c["ang_deg"])
print(f"\nlabels found: {len(labels8)}")
for c in labels8:
    print(f"  ang {c['ang_deg']:6.1f} rad {c['rad_pt']:6.1f} slide ({c['slide_c'][0]:6.1f},{c['slide_c'][1]:6.1f}) wh {c['wh']}")
out["labels"] = labels8

json.dump(out, open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide028/measure1.json", "w"), indent=1)
print("\nsaved measure1.json")
