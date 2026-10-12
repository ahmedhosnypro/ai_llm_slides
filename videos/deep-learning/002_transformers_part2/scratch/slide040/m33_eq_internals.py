#!/usr/bin/env python3
"""m33: eq3/eq4 internals — ORIGINAL frame vs RENDER_5, same feature extraction.
Goal: exact positions of mu_B (numerator), sqrt, sigma_B^2 (denominator), fraction bar,
eps tail, eq4 right extent, sigma subscript bottom — to re-anchor highlights."""
import numpy as np
from PIL import Image

VID = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2"
fr = np.asarray(Image.open(f"{VID}/unique_slides/slide_040.jpg").convert("RGB")).astype(int)
rn = np.asarray(Image.open(f"{VID}/recreated_pptx/qa/slide040/render_5.png").convert("RGB")).astype(int)

def to_render(fx, fy): return (fx-18.63)*2.16766, fy*2.18013

def ink_runs(img, y0, y1, x0, x1, thr=185, scale=1):
    """column ink profile: per-column count of dark px -> word runs"""
    lum = (img[y0:y1, x0:x1, 0]*299 + img[y0:y1, x0:x1, 1]*587 + img[y0:y1, x0:x1, 2]*114)//1000
    cols = (lum < thr).sum(axis=0)
    runs = []
    s = None
    gap = 0
    for i, v in enumerate(cols):
        if v > 0:
            if s is None: s = i
            gap = 0
        else:
            if s is not None:
                gap += 1
                if gap >= (3 if scale == 1 else 6):
                    runs.append(((s+x0)/scale, (i-gap+x0)/scale)); s = None
    if s is not None:
        runs.append(((s+x0)/scale, (len(cols)-1+x0)/scale))
    return runs

print("== NUMERATOR zone (frame y402..419) ==")
print("ORIG  runs (frame px):", [(round(a,1), round(b,1)) for a, b in ink_runs(fr, 402, 420, 160, 300)])
rx0, ry0 = to_render(160, 402); rx1, ry1 = to_render(300, 420)
print("REN   runs (frame px):", [(round(a,1), round(b,1)) for a, b in ink_runs(rn, int(ry0), int(ry1), int(rx0), int(rx1), scale=2.16766)])

print()
print("== DENOMINATOR zone (frame y429..445) ==")
print("ORIG  runs:", [(round(a,1), round(b,1)) for a, b in ink_runs(fr, 429, 446, 160, 300)])
rx0, ry0 = to_render(160, 429); rx1, ry1 = to_render(300, 446)
print("REN   runs:", [(round(a,1), round(b,1)) for a, b in ink_runs(rn, int(ry0), int(ry1), int(rx0), int(rx1), scale=2.16766)])

print()
print("== FRACTION BAR rows (frame) ==")
def bar_rows(img, x0, x1, label, thr=150):
    for y in range(418, 432):
        lum = (img[y, x0:x1, 0]*299 + img[y, x0:x1, 1]*587 + img[y, x0:x1, 2]*114)//1000 if img.shape[1] > x1 else None
    # generic: scan y where long run
    for y in range(415, 435):
        row = img[y, x0:x1]
        L = (row[:,0]*299+row[:,1]*587+row[:,2]*114)//1000
        xs = np.where(L < thr)[0]
        if len(xs) > (x1-x0)*0.5:
            print(f"  {label} y={y}: x {xs.min()+x0}..{xs.max()+x0} n={len(xs)}")
print("ORIG:")
bar_rows(fr, 200, 300, "orig")
print("REN (rows are render y; reported as frame-equiv):")
for yr in range(int(to_render(0,415)[1]), int(to_render(0,435)[1])):
    row = rn[yr, int(to_render(200,0)[0]):int(to_render(300,0)[0])]
    L = (row[:,0]*299+row[:,1]*587+row[:,2]*114)//1000
    xs = np.where(L < 150)[0]
    if len(xs) > (300-200)*2.16766*0.5:
        fy = yr/2.18013
        fx0 = (xs.min()+int(to_render(200,0)[0]))/2.16766+18.63
        fx1 = (xs.max()+int(to_render(200,0)[0]))/2.16766+18.63
        print(f"  rendery={yr} frame_y={fy:.1f}: x {fx0:.1f}..{fx1:.1f} n={len(xs)}")

print()
print("== SIGMA_B subscript bottom (denominator) ==")
# original: sigma_B region x225..260, find lowest dark row
def lowest_ink(img, x0, x1, y0, y1, thr=170):
    lowest = None
    for y in range(y0, y1):
        L = (img[y, x0:x1, 0]*299+img[y, x0:x1, 1]*587+img[y, x0:x1, 2]*114)//1000
        if (L < thr).sum() >= 2:
            lowest = y
    return lowest
print("ORIG sigma_B lowest ink row (x225..262, y424..455):", lowest_ink(fr, 225, 262, 424, 455))
rx0, ry0 = to_render(225, 424); rx1, ry1 = to_render(262, 455)
low_r = lowest_ink(rn, int(rx0), int(rx1), int(ry0), int(ry1))
print("REN  sigma_B lowest ink row:", low_r, "-> frame-equiv y = %.1f" % (low_r/2.18013) if low_r else "none")

print()
print("== EQ4 right extent (math only, excluding comment; frame y452..474, x300..560) ==")
L4 = (fr[452:475, 300:560, 0]*299+fr[452:475, 300:560, 1]*587+fr[452:475, 300:560, 2]*114)//1000
xs = np.where((L4 < 190).any(axis=0))[0]
print("ORIG eq4 math+comment ink cols (frame):", 300+xs.min(), "..", 300+xs.max())
# math-only: the ')' of (x_i) — find last ink col left of comment start (comment x438..)
L4m = (fr[452:475, 300:430, 0]*299+fr[452:475, 300:430, 1]*587+fr[452:475, 300:430, 2]*114)//1000
xs2 = np.where((L4m < 190).any(axis=0))[0]
print("ORIG eq4 math-only to x430: last col", 300+xs2.max())
rx0, ry0 = to_render(300, 452); rx1, ry1 = to_render(560, 475)
L4r = (rn[int(ry0):int(ry1), int(rx0):int(rx1), 0]*299+rn[int(ry0):int(ry1), int(rx0):int(rx1), 1]*587+rn[int(ry0):int(ry1), int(rx0):int(rx1), 2]*114)//1000
xs3 = np.where((L4r < 190).any(axis=0))[0]
print("REN eq4 ink cols frame-equiv:", round(300+xs3.min()/2.16766,1), "..", round(300+xs3.max()/2.16766,1))

print()
print("== eq4 math-only right end (exclude comment x>420 frame) ==")
rx0, ry0 = to_render(300, 452); rx1, ry1 = to_render(420, 475)
L4r2 = (rn[int(ry0):int(ry1), int(rx0):int(rx1), 0]*299+rn[int(ry0):int(ry1), int(rx0):int(rx1), 1]*587+rn[int(ry0):int(ry1), int(rx0):int(rx1), 2]*114)//1000
xs4 = np.where((L4r2 < 190).any(axis=0))[0]
print("REN eq4 math-only last col (frame-equiv):", round(300+xs4.max()/2.16766,1), "(orig: 371)")

print()
print("== NUM mu_B bottom vs top border (original mu_B x254..280) ==")
print("ORIG mu_B ink rows (x254..280):", end=" ")
rows_ = [y for y in range(395, 425) if ((fr[y,254:281,0]*299+fr[y,254:281,1]*587+fr[y,254:281,2]*114)//1000 < 170).sum() >= 2]
print(rows_[0] if rows_ else None, "..", rows_[-1] if rows_ else None)
rx0, ry0 = to_render(254, 395); rx1, ry1 = to_render(281, 425)
rows_r = [y for y in range(int(ry0), int(ry1)) if ((rn[y,int(rx0):int(rx1),0]*299+rn[y,int(rx0):int(rx1),1]*587+rn[y,int(rx0):int(rx1),2]*114)//1000 < 170).sum() >= 2]
print("REN  mu_B ink rows:", rows_r[0] if rows_r else None, "..", rows_r[-1] if rows_r else None,
      "-> frame-equiv %.1f..%.1f" % (rows_r[0]/2.18013, rows_r[-1]/2.18013) if rows_r else "")
