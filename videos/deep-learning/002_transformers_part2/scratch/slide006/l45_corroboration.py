#!/usr/bin/env python3
"""Corroborate L4/L5 right-edge deltas: column ink-mass profile cross-correlation
original (mapped to 150dpi space) vs render. Also containment excl. all chrome strokes."""
from PIL import Image
import numpy as np

def masks(a):
    R,G,B = a[:,:,0],a[:,:,1],a[:,:,2]
    return ((R-G>30)&(R-B>30)&(R>90), (B-R>30)&(B-G>30)&(B>100))

orig = np.asarray(Image.open("videos/deep-learning/002_transformers_part2/unique_slides/slide_006.jpg").convert("RGB")).astype(int)
ren  = np.asarray(Image.open("videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide006/render_2.png").convert("RGB")).astype(int)
PX = 2000/960.0
A, SX, By, SY = 18.128, 0.961232, -0.591, 0.957576

# upsample original ink onto 150dpi grid (nearest): orig px f -> ren px (f-A)/SX*PX etc.
ored, oblu = masks(orig)
rred, rblu = masks(ren)

def profile_l4_l5():
    for name, fband in (("L4",(269,284)), ("L5",(308,323))):
        # original profile in ren-px coords
        fy0, fy1 = fband
        ry0, ry1 = int((fy0+1-By)/SY*PX), int((fy1+1-By)/SY*PX)
        o = oblu[fy0:fy1+1, :].sum(axis=0).astype(float)
        r = rblu[max(0,ry0-4):ry1+4, :].sum(axis=0).astype(float)
        # resample o to ren scale: ren_x = (f_x - A)/SX*PX
        fx = np.arange(960)
        rx = (fx - A)/SX*PX
        o_on_r = np.interp(np.arange(2001), rx, o, left=0, right=0)
        # normalize and cross-correlate over shifts -12..12
        best = None
        for sh in range(-12, 13):
            oo = np.roll(o_on_r, sh)
            # compare mass in the right-tail window (last 15% of the line)
            seg = slice(int(500), int(1000))
            c = np.corrcoef(oo[seg], r[seg])[0,1]
            if best is None or c > best[1]: best = (sh, c)
        print(f"{name}: best shift {best[0]:+d}px (corr {best[1]:.4f}) — positive = original sits right of render")

profile_l4_l5()

# containment v2: erase ALL four chrome strokes + badge, then content bbox
redm, blum = rred, rblu
content = redm | blum
pb = int(PX)  # approx
for lo, hi, axis, sl in [(int(42*PX)-8, int(42*PX)+9, 1, None)]:
    pass
content[:, int(42*PX)-8:int(42*PX)+10] = False
content[:, int(919*PX)-10:int(919*PX)+9] = False
content[int(45*PX)-8:int(45*PX)+10, :] = False
content[int(537*PX):, :] = False          # bottom chrome stroke (rows 538-539 slide pts)
content[:int(115*PX), int(845*PX):] = False  # badge
ys, xs = np.where(content)
print("\ncontainment v2 (chrome erased): content ink x %d..%d, y %d..%d px" % (xs.min(), xs.max(), ys.min(), ys.max()))
print("panel interior: x %d..%d, y %d..%d" % (int(42*PX), int(919*PX), int(45*PX), int(540*PX)))
ok = xs.min() >= int(42*PX)+2 and xs.max() <= int(919*PX)-2 and ys.min() >= int(45*PX)+2 and ys.max() <= int(540*PX)-2
print("FRAME CONTAINMENT:", "PASS" if ok else "FAIL")
