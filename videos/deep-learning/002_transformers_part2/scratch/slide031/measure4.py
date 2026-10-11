#!/usr/bin/env python3
"""Def boxes, banner text arrangement, derivation bands, highlights, callout, ribbon."""
import numpy as np
from PIL import Image

img = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_031.jpg").convert("RGB")
a = np.asarray(img).astype(int)
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]

def runs(m, minlen=1):
    out, i, n = [], 0, len(m)
    while i < n:
        if m[i]:
            j = i
            while j < n and m[j]: j += 1
            if j - i >= minlen: out.append((i, j - 1))
            i = j
        else: i += 1
    return out

# ---- DEF BOXES region x685..880 y85..200 ----
print("== DEF BOXES ==")
sub = a[85:205, 685:885]
# blue border/ink
bl = (sub[:, :, 2] - sub[:, :, 0] > 30) & (sub[:, :, 2] > 100)
rr = bl.sum(axis=1)
print("blue rows:", [(85 + r, int(n)) for r, n in enumerate(rr) if n > 3])
cc = bl.sum(axis=0)
print("blue cols:", [(685 + c, int(n)) for c, n in enumerate(cc) if n > 3])
# fill rows (cream)
cream = (sub[:, :, 0] > 240) & (sub[:, :, 1] > 240) & (sub[:, :, 0] - sub[:, :, 2] > 15)
fr = cream.sum(axis=1)
print("cream rows:", runs(fr > 50, 2), "-> y", [(85 + r0, 85 + r1) for r0, r1 in runs(fr > 50, 2)])
fc = cream.sum(axis=0)
print("cream cols:", runs(fc > 20, 2), "-> x", [(685 + c0, 685 + c1) for c0, c1 in runs(fc > 20, 2)])

# ---- BANNER text arrangement ----
print("\n== BANNER rows 224..248: red ink cols vs blue ink cols ==")
ban = a[224:249, 55:905]
redb = (ban[:, :, 0] - ban[:, :, 1] > 40) & (ban[:, :, 0] > 120)
blueb = (ban[:, :, 2] - ban[:, :, 0] > 30) & (ban[:, :, 2] > 110)
print("red col runs:", [(55 + c0, 55 + c1) for c0, c1 in runs(redb.sum(axis=0) > 0, 3)])
print("blue col runs:", [(55 + c0, 55 + c1) for c0, c1 in runs(blueb.sum(axis=0) > 0, 3)])
# banner rect: fill extent + green border lines
greenline = (ban[:, :, 1] - ban[:, :, 0] > 25) & (ban[:, :, 1] - ban[:, :, 2] > 25)
print("green-line rows:", [(224 + r, int(n)) for r, n in enumerate(greenline.sum(axis=1)) if n > 300])
# banner left/right extents: nonwhite, non-gray
nonbg = (np.abs(ban - np.array([231, 233, 230])).sum(axis=2) > 45) & (ban.mean(axis=2) > 150)
print("banner fill col runs:", [(55 + c0, 55 + c1) for c0, c1 in runs(nonbg.sum(axis=0) > 30, 3)])
nonbgr = nonbg.sum(axis=1)
print("banner fill row bands:", [(224 + r0, 224 + r1) for r0, r1 in runs(nonbgr > 300, 2)])

# ---- DERIVATION LINES: ink bands inside panel x66..852 y258..510 ----
print("\n== DERIVATION BANDS ==")
pan = a[258:512, 66:853]
ink = (pan.mean(axis=2) < 200) | ((np.abs(pan[:, :, 0] - pan[:, :, 1]) > 40) | (np.abs(pan[:, :, 2] - pan[:, :, 0]) > 40))
rowsum = ink.sum(axis=1)
bands = runs(rowsum > 2, 3)
print("ink bands (y, height):")
for y0, y1 in bands:
    seg = ink[y0:y1 + 1]
    cols = np.where(seg.any(axis=0))[0]
    print(f"  y{258+y0}..{258+y1} h={y1-y0+1} x{66+cols.min()}..{66+cols.max()} inkpx={int(rowsum[y0:y1+1].sum())}")

# highlights: saturated yellow (FFFF00) and cyan (#00CCFF) and any highlight rects
yelfull = (pan[:, :, 0] > 220) & (pan[:, :, 1] > 220) & (pan[:, :, 2] < 150)
cyan = (pan[:, :, 2] > 190) & (pan[:, :, 1] > 180) & (pan[:, :, 0] < 160)
for nm, m in [("yellow", yelfull), ("cyan", cyan)]:
    lab, n = __import__("scipy.ndimage", fromlist=["label"]).label(m)
    print(f"\n{nm} highlight components (y,x,w,h):")
    from scipy.ndimage import find_objects
    for i, sl in enumerate(find_objects(lab)):
        h = sl[0].stop - sl[0].start; w = sl[1].stop - sl[1].start
        if h * w > 40:
            print(f"  y{258+sl[0].start}..{258+sl[0].stop-1} x{66+sl[1].start}..{66+sl[1].stop-1} ({w}x{h})")

# ---- CALLOUT + RIBBON region ----
print("\n== BOTTOM RIGHT (callout + ribbon) ==")
br = a[440:518, 500:920]
yel2 = (br[:, :, 0] > 220) & (br[:, :, 1] > 220) & (br[:, :, 2] < 170)
lab, n = __import__("scipy.ndimage", fromlist=["label"]).label(yel2)
from scipy.ndimage import find_objects
for sl in find_objects(lab):
    h = sl[0].stop - sl[0].start; w = sl[1].stop - sl[1].start
    if h * w > 200:
        print(f"  yellow comp: y{440+sl[0].start}..{440+sl[0].stop-1} x{500+sl[1].start}..{500+sl[1].stop-1} ({w}x{h}) npx={h*w}")
# red text in callout/ribbon
red2 = (br[:, :, 0] - br[:, :, 1] > 60) & (br[:, :, 0] > 140)
lab2, n2 = __import__("scipy.ndimage", fromlist=["label"]).label(red2)
print("  red text comps (callout text / ribbon text):")
for sl in find_objects(lab2):
    h = sl[0].stop - sl[0].start; w = sl[1].stop - sl[1].start
    if h * w > 30:
        print(f"    y{440+sl[0].start}..{440+sl[0].stop-1} x{500+sl[1].start}..{500+sl[1].stop-1} ({w}x{h})")
# green border of callout
grn = (br[:, :, 1] - br[:, :, 0] > 40) & (br[:, :, 1] > 110) & (br[:, :, 2] < 140)
lab3, _ = __import__("scipy.ndimage", fromlist=["label"]).label(grn)
print("  green comps:")
for sl in find_objects(lab3):
    h = sl[0].stop - sl[0].start; w = sl[1].stop - sl[1].start
    if h * w > 30:
        print(f"    y{440+sl[0].start}..{440+sl[0].stop-1} x{500+sl[1].start}..{500+sl[1].stop-1} ({w}x{h})")
