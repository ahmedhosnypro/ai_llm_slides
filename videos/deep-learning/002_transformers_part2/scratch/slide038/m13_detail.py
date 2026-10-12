#!/usr/bin/env python3
"""Slide 038 — m13: defbox intra-line gaps (bracket starts), color cores, plus circles,
orange arrow paths, annotation line boxes, LayerNorm bar text colors."""
import numpy as np
from PIL import Image

F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_038.jpg"
img = np.asarray(Image.open(F).convert("RGB")).astype(int)
R, G, B = img[:, :, 0], img[:, :, 1], img[:, :, 2]
invx = lambda fx: round((fx - 18.63) / 0.96123, 1)
invy = lambda fy: round(fy / 0.95556, 1)
IN = lambda pt: round(pt / 72, 3)

print("== defbox intra-line word gaps (blue ink col profile, per band) ==")
blue = (B > 110) & (R < 110) & (G < 110)
for lo, hi, lab in ((118, 130, "L1"), (138, 151, "L2"), (156, 168, "L3"), (196, 208, "L4"), (215, 227, "L5")):
    seg = blue[lo:hi, 95:862]
    colprof = seg.sum(axis=0)
    runs, inr = [], False
    for i, v in enumerate(colprof):
        if v > 0 and not inr:
            s = i; inr = True
        elif v == 0 and inr:
            runs.append((s + 95, i + 95)); inr = False
    if inr: runs.append((s + 95, 862))
    merged = []
    for a, b in runs:
        if merged and a - merged[-1][1] <= 5: merged[-1] = (merged[-1][0], b)
        else: merged.append((a, b))
    gaps = [(merged[i][1], merged[i+1][0]) for i in range(len(merged)-1)]
    print(f"  {lab}: words={[(a,b) for a,b in merged]}")
    print(f"      gaps>8px: {[(a, b, round(invx(a),1), round(invx(b),1)) for a,b in gaps if b-a>8]}")

print("== color cores (census of darkest/most-saturated px per element) ==")
def census(mask, y0, y1, x0, x1, label, topn=6):
    seg = img[y0:y1, x0:x1]
    m = mask[y0:y1, x0:x1]
    px = seg[m]
    if len(px) == 0:
        print(f"  {label}: none"); return
    # darkest 10% by luminance
    lum = 0.299*px[:,0] + 0.587*px[:,1] + 0.114*px[:,2]
    idx = np.argsort(lum)[:max(1, len(px)//10)]
    cores = px[idx]
    print(f"  {label}: n={len(px)} core mean=({cores[:,0].mean():.0f},{cores[:,1].mean():.0f},{cores[:,2].mean():.0f}) min-lum px=({cores[lum[idx].argmin(),0] if False else cores[0,0]},{cores[0,1]},{cores[0,2]})")

red = (R > 110) & (G < 110) & (B < 110)
census(red, 71, 91, 150, 850, "title red")
census(blue, 118, 130, 100, 345, "defbox L1 blue")
census(red, 263, 273, 195, 840, "top-row red glyph/label")
census(blue, 456, 466, 195, 840, "X-row blue label")
census(red, 303, 314, 320, 490, "layernorm 'Layer Normalization' red")
blk = (R < 100) & (G < 100) & (B < 100)
census(blk, 303, 314, 500, 700, "layernorm '(NOT Batch...' dark")
census((B > 100) & (R < 70) & (G < 70), 405, 445, 170, 880, "navy core")
navy = (B > 100) & (R < 70) & (G < 70) & (B - R > 60)
segm = navy[405:445, 170:880]
print(f"  navy solid mean: R={img[405:445,170:880][segm][:,0].mean():.0f} G={img[405:445,170:880][segm][:,1].mean():.0f} B={img[405:445,170:880][segm][:,2].mean():.0f}")
gray = (abs(R - G) < 14) & (abs(G - B) < 14) & (R > 185) & (R < 235)
print(f"  gray bar mean: R={img[296:320,200:800][gray[296:320,200:800]][:,0].mean():.0f} G={img[296:320,200:800][gray[296:320,200:800]][:,1].mean():.0f} B={img[296:320,200:800][gray[296:320,200:800]][:,2].mean():.0f}")
green = (G > 120) & (G - R > 40) & (G - B > 40)
census(green, 284, 290, 100, 850, "green container top border")
orange = (R > 150) & (G > 60) & (G < 160) & (B < 90) & (R - B > 90)
census(orange, 416, 438, 60, 145, "orange annotation text")
census(red, 452, 466, 60, 155, "red annotation text")
census(red, 494, 506, 270, 556, "caption red text")
yel = (R > 200) & (G > 180) & (B < 140)
seg2 = img[494:507, 272:556]
m2_ = yel[494:507, 272:556]
print(f"  caption highlight mean: ({seg2[m2_][:,0].mean():.0f},{seg2[m2_][:,1].mean():.0f},{seg2[m2_][:,2].mean():.0f})")

print("== plus circles: dark-red clusters y 332..350 ==")
darkred = (R > 100) & (R < 230) & (G < 90) & (B < 90)
seg3 = darkred[332:350, 150:880]
colprof = seg3.sum(axis=0)
runs, inr = [], False
for i, v in enumerate(colprof):
    if v > 1 and not inr:
        s = i; inr = True
    elif v <= 1 and inr:
        runs.append((s + 150, i + 150)); inr = False
if inr: runs.append((s + 150, 880))
merged = []
for a, b in runs:
    if merged and a - merged[-1][1] <= 3: merged[-1] = (merged[-1][0], b)
    else: merged.append((a, b))
print("  circle blobs:", [(a, b, round((a+b)/2,1), b-a) for a, b in merged])
rowsum = darkred[325:355, 190:220].sum(axis=1)
print("  col1 circle row extent:", {i+325: int(v) for i, v in enumerate(rowsum) if v > 0})

print("== orange arrow path: per-y orange x-clusters (y 350..470) ==")
for y in range(350, 471, 8):
    seg4 = orange[y:y+2, 150:880]
    colprof = seg4.sum(axis=0)
    cols = np.where(colprof > 0)[0]
    if len(cols):
        runs, inr = [], False
        for i, v in enumerate(colprof):
            if v > 0 and not inr:
                s = i; inr = True
            elif v == 0 and inr:
                if i - s >= 2: runs.append((s + 150, i + 150))
                inr = False
        print(f"  y={y} (slide {invy(y)}): {[(a, b) for a, b in runs][:14]}")

print("== annotation line bboxes ==")
def linebox(mask, y0, y1, x0, x1, label):
    seg5 = mask[y0:y1, x0:x1]
    rows = np.where(seg5.sum(axis=1) > 2)[0]
    if not len(rows): print(f"  {label}: none"); return
    # group rows
    groups, cur = [], [rows[0]]
    for r in rows[1:]:
        if r - cur[-1] <= 3: cur.append(r)
        else: groups.append(cur); cur = [r]
    groups.append(cur)
    for g in groups:
        band = seg5[g[0]:g[-1]+1]
        cols2 = np.where(band.sum(axis=0) > 0)[0]
        print(f"  {label}: y {g[0]+y0}..{g[-1]+y0} x {cols2.min()+x0}..{cols2.max()+x0}"
              f" -> slide y {invy(g[0]+y0)}..{invy(g[-1]+y0)} x {invx(cols2.min()+x0)}..{invx(cols2.max()+x0)}"
              f" in y {IN(invy(g[0]+y0))}..{IN(invy(g[-1]+y0))} x {IN(invx(cols2.min()+x0))}..{IN(invx(cols2.max()+x0))}")
linebox(blue, 360, 400, 55, 165, "blue ann")
linebox(orange, 410, 445, 55, 165, "orange ann")
linebox(red, 445, 485, 55, 165, "red ann")

print("== gray bar text bands (dark px inside bar y 296..320) ==")
blk2 = (R < 130) & (G < 130) & (B < 130)
seg6 = blk2[296:321, 170:870]
rows = np.where(seg6.sum(axis=1) > 2)[0]
print("  dark text rows:", rows.min()+296, rows.max()+296, "-> slide", invy(rows.min()+296), invy(rows.max()+296))
colprof = seg6.sum(axis=0)
cols3 = np.where(colprof > 0)[0]
print(f"  text x {cols3.min()+170}..{cols3.max()+170} -> slide {invx(cols3.min()+170)}..{invx(cols3.max()+170)}")

print("== caption text: exact dark-red rows + underline check ==")
red2 = (R > 110) & (G < 110) & (B < 110)
seg7 = red2[490:512, 265:565]
rows = np.where(seg7.sum(axis=1) > 1)[0]
print("  red rows:", [(r+490, int(seg7[r].sum())) for r in rows])
