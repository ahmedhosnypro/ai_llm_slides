#!/usr/bin/env python3
"""Closed-loop ink check v2: MATCHED loose masks on render AND original-derived targets.
Targets updated: L1 bottom incl. p-descender (frame y165), L4 bottom (y284)."""
from PIL import Image
import numpy as np

def bbox_of(a, y0,y1,x0,x1, mask_fn):
    R,G,B = a[:,:,0],a[:,:,1],a[:,:,2]
    m = mask_fn(R,G,B)
    sub = m[y0:y1, x0:x1]
    ys,xs = np.where(sub)
    if len(xs)==0: return None
    return (xs.min()+x0, xs.max()+x0, ys.min()+y0, ys.max()+y0, len(xs))

loose_blue = lambda R,G,B: (B - R > 30) & (B - G > 30) & (B > 100)
loose_red  = lambda R,G,B: (R - G > 30) & (R - B > 30) & (R > 90)

orig = np.asarray(Image.open("videos/deep-learning/002_transformers_part2/unique_slides/slide_006.jpg").convert("RGB")).astype(int)
ren  = np.asarray(Image.open("videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide006/render_1.png").convert("RGB")).astype(int)
A, SX = 18.128, 0.961232
By, SY = -0.591, 0.957576
def mx(f): return (f - A)/SX
def my(f): return (f - By)/SY
PX = 2000/960.0
def pt(v): return v*PX

# measure ORIGINAL loose bboxes per element (window: generous)
wins = [
 ("TITLE", 60,110, 200,700, loose_red),
 ("L1", 140,170, 100,500, loose_blue),
 ("L2", 180,210, 100,400, loose_blue),
 ("L3", 222,252, 100,420, loose_blue),
 ("L4", 262,290, 100,360, loose_blue),
 ("L5", 302,330, 100,500, loose_blue),
 ("L6", 346,374, 100,300, loose_blue),
]
print("re-derived targets (loose, orig):")
targets = []
for name,y0,y1,x0,x1,fn in wins:
    bb = bbox_of(orig, y0,y1,x0,x1, fn)
    fx0,fx1,fy0,fy1,n = bb
    t = (name, mx(fx0), mx(fx1), my(fy0), my(fy1))
    targets.append(t)
    print(f"  {name}: frame x {fx0}..{fx1} y {fy0}..{fy1} -> slide x {t[1]:.1f}..{t[2]:.1f} (w {t[2]-t[1]:.1f}) y {t[3]:.1f}..{t[4]:.1f} (h {t[4]-t[3]:.1f})")

print(f"\n{'elem':6s} {'dx0':>6s} {'dx1':>6s} {'dcx':>6s} {'dy0':>6s} {'dy1':>6s} {'dw':>6s}  (px @150dpi, matched loose masks; tol 4)")
H, W = ren.shape[:2]
worst = 0
for name, tx0, tx1, ty0, ty1 in targets:
    ylo, yhi = int(pt(ty0))-28, int(pt(ty1))+28
    xlo, xhi = int(pt(tx0))-30, int(pt(tx1))+40
    fn = loose_red if name=="TITLE" else loose_blue
    bb = bbox_of(ren, max(0,ylo), min(H,yhi), max(0,xlo), min(W,xhi), fn)
    x0,x1,y0,y1,n = bb
    dx0, dx1 = x0-pt(tx0), x1-pt(tx1)
    dcx = (x0+x1)/2 - (pt(tx0)+pt(tx1))/2
    dy0, dy1 = y0-pt(ty0), y1-pt(ty1)
    dw = (x1-x0)-(pt(tx1)-pt(tx0))
    m = max(abs(dx0),abs(dx1),abs(dy0),abs(dy1)); worst = max(worst,m)
    print(f"{name:6s} {dx0:6.1f} {dx1:6.1f} {dcx:6.1f} {dy0:6.1f} {dy1:6.1f} {dw:6.1f}  n={n}{' <== TOL' if m>4 else ''}")
print("\nWORST |delta| px:", round(worst,2), "(tol 4.0)")
