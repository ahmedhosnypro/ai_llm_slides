#!/usr/bin/env python3
"""Closed-loop ink check: render_1.png (150dpi) vs mapped original-frame targets.
Tolerance ~4px @150dpi (= 1.92 slide pt). Prints deltas -> fixes."""
from PIL import Image
import numpy as np

ren = np.asarray(Image.open("videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide006/render_1.png").convert("RGB")).astype(int)
H, W = ren.shape[:2]
print("render size:", W, H)
R, G, B = ren[:,:,0], ren[:,:,1], ren[:,:,2]
PX = 2000/960.0  # 150dpi px per slide pt

# targets: (name, x0,x1,y0,y1) in slide pt (mapped from frame ink)
T = [
 ("TITLE", 223.46, 631.35, 71.60, 100.88),
 ("L1", 113.29, 471.24, 154.15, 168.77),
 ("L2", 113.29, 321.31, 195.94, 210.56),
 ("L3", 110.17, 370.15, 239.83, 258.59),
 ("L4", 114.34, 313.02, 281.51, 296.13),
 ("L5", 113.29, 457.62, 323.30, 337.92),
 ("L6", 114.34, 250.69, 369.35, 383.97),
]
def pt(v): return v * PX

red  = (R - G > 40) & (R - B > 40) & (R > 100)
blue = (B - R > 40) & (B - G > 40) & (B > 120)

def ink_bbox(mask, y_lo, y_hi, x_lo, x_hi):
    sub = mask[y_lo:y_hi, x_lo:x_hi]
    ys, xs = np.where(sub)
    if len(xs) == 0: return None
    return (xs.min()+x_lo, xs.max()+x_lo, ys.min()+y_lo, ys.max()+y_lo, len(xs))

print(f"{'elem':6s} {'dx0':>7s} {'dx1':>7s} {'dcx':>7s} {'dy0':>7s} {'dy1':>7s} {'dw':>7s}  (px @150dpi; tol 4)")
worst = 0
for name, tx0, tx1, ty0, ty1 in T:
    ylo, yhi = int(pt(ty0)) - 30, int(pt(ty1)) + 30
    xlo, xhi = int(pt(tx0)) - 40, int(pt(tx1)) + 60
    m = red if name == "TITLE" else blue
    bb = ink_bbox(m, max(0,ylo), min(H,yhi), max(0,xlo), min(W,xhi))
    if bb is None:
        print(f"{name:6s} NO INK FOUND  <-- BLOCKER"); worst = 999; continue
    x0, x1, y0, y1, n = bb
    dx0, dx1 = x0 - pt(tx0), x1 - pt(tx1)
    dcx = (x0+x1)/2 - (pt(tx0)+pt(tx1))/2
    dy0, dy1 = y0 - pt(ty0), y1 - pt(ty1)
    dw = (x1-x0) - (pt(tx1)-pt(tx0))
    worst = max(worst, abs(dx0), abs(dx1), abs(dy0), abs(dy1))
    flag = " <== TOL" if max(abs(dx0),abs(dx1),abs(dy0),abs(dy1)) > 4 else ""
    print(f"{name:6s} {dx0:7.1f} {dx1:7.1f} {dcx:7.1f} {dy0:7.1f} {dy1:7.1f} {dw:7.1f}  n={n}{flag}")

# containment: all content ink inside panel (slide pts 42..919 x 45..540 -> px)
allink = red | blue
ys, xs = np.where(allink)
# exclude chrome border/badge: panel border px are red C00000 too! restrict to interior
interior = allink[int(pt(50)):int(pt(530)), int(pt(46)):int(pt(915))]
iys, ixs = np.where(interior)
print("\ncontent ink bbox in px:", ixs.min()+int(pt(46)), ixs.max()+int(pt(46)), iys.min()+int(pt(50)), iys.max()+int(pt(50)))
print("panel interior bounds px:", int(pt(42)), int(pt(919)), int(pt(45)), int(pt(540)))
print("\nWORST |delta| px:", round(worst,2), "(tolerance 4.0)")
