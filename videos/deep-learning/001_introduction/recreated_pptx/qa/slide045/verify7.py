#!/usr/bin/env python3
"""verify7: closed-loop checks on render_8 (attempt 3). Frame px * s = render px, s=H/540."""
import numpy as np
from PIL import Image

Q = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/qa/slide045"
VID = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction"
ren = np.asarray(Image.open(Q + "/render_8.png").convert("RGB")).astype(int)
org = np.asarray(Image.open(VID + "/unique_slides/slide_045.jpg").convert("RGB")).astype(int)
H = ren.shape[0]
s = H / 540.0


def rimg(m, x0, x1, y0, y1):
    """frame-px slice of a mask, render resolution"""
    return m[int(y0 * s):int(y1 * s), int(x0 * s):int(x1 * s)]


rr, rg, rb = ren[:, :, 0], ren[:, :, 1], ren[:, :, 2]
rred = (rr > 120) & (rg < 110) & (rb < 110)
rdark = (rr < 110) & (rg < 110) & (rb < 110)
rgray = (abs(rr - 191) < 30) & (abs(rg - 187) < 30) & (abs(rb - 184) < 30) & (rb < rr)

print("== 1. connector A (gray line 708,357->735.5,376.5) ==")
m = rimg(rgray, 700, 745, 350, 385)
ys, xs = np.where(m)
if len(ys):
    print(f"  gray ink n={len(ys)} bbox frame x{700+xs.min()/s:.1f}..{700+xs.max()/s:.1f} y{350+ys.min()/s:.1f}..{350+ys.max()/s:.1f}")
else:
    print("  MISSING")

print("== 2. connector B (gray line 702,409->735.5,431) ==")
m = rimg(rgray, 695, 745, 400, 440)
ys, xs = np.where(m)
if len(ys):
    print(f"  gray ink n={len(ys)} bbox frame x{695+xs.min()/s:.1f}..{695+xs.max()/s:.1f} y{400+ys.min()/s:.1f}..{400+ys.max()/s:.1f}")
else:
    print("  MISSING")

print("== 3. wedge (D2 regression): red bbox + dark clearance ==")
m = rimg(rred, 595, 635, 335, 365)
ys, xs = np.where(m)
if len(ys):
    bx = (595 + xs.min() / s, 595 + xs.max() / s, 335 + ys.min() / s, 335 + ys.max() / s)
    print(f"  red wedge bbox frame x{bx[0]:.1f}..{bx[1]:.1f} y{bx[2]:.1f}..{bx[3]:.1f}  (org x608..622 y345..357)")
mo = rimg(rdark, 595, 635, 335, 365)
# min clearance red<->dark in the wedge zone
redm = rimg(rred, 595, 635, 335, 365)
dkm = rimg(rdark, 595, 635, 335, 365)
from scipy import ndimage  # noqa
try:
    dt = ndimage.distance_transform_edt(~dkm)
    clearance = dt[redm].min() / s if redm.any() else None
    print(f"  min red->dark clearance: {clearance:.2f} frame px (org 1px)")
except Exception as e:
    print("  clearance skipped:", e)

print("== 4. region_b compact ink (target x571..601 y404..415; org ink x571..612 y407..410) ==")
m = rimg(rdark, 545, 620, 398, 418)
ys, xs = np.where(m)
if len(ys):
    print(f"  dark ink bbox frame x{545+xs.min()/s:.1f}..{545+xs.max()/s:.1f} y{398+ys.min()/s:.1f}..{398+ys.max()/s:.1f}")

print("== 5. D1: def line-1 ink under star zone ==")
m = rimg(rdark, 780, 900, 112, 148)
ys, xs = np.where(m)
print(f"  dark ink n={len(ys)}" + (f" bbox frame x{780+xs.min()/s:.1f}..{780+xs.max()/s:.1f} y{112+ys.min()/s:.1f}..{112+ys.max()/s:.1f}" if len(ys) else ""))

print("== 6. star bboxes ==")
ryel = (rr > 200) & (rg > 200) & (rb < 190)
m = rimg(ryel, 770, 900, 40, 160)
ys, xs = np.where(m)
if len(ys):
    print(f"  star yellow frame x{770+xs.min()/s:.1f}..{770+xs.max()/s:.1f} y{40+ys.min()/s:.1f}..{40+ys.max()/s:.1f} (org 786..895, 48..151)")
m = rimg(rred, 760, 910, 40, 160)
ys, xs = np.where(m)
if len(ys):
    print(f"  star red    frame x{760+xs.min()/s:.1f}..{760+xs.max()/s:.1f} y{40+ys.min()/s:.1f}..{40+ys.max()/s:.1f} (org 770..898, 44..154)")

print("== 7. badge-window dust (checker-yellow outside disc bbox x875..911 y53..89) ==")
win = np.s_[int(35 * s):int(107 * s), int(857 * s):int(929 * s)]
yel = ryel[win].copy()
disc = np.zeros_like(yel)
d0x, d1x = int((875 - 857) * s), int((911 - 857) * s)
d0y, d1y = int((53 - 35) * s), int((89 - 35) * s)
disc[max(d0y - 4, 0):d1y + 4, max(d0x - 4, 0):d1x + 4] = True
dust = yel & ~disc
print(f"  dust px n={dust.sum()}")

print("== 8. whole-frame containment (ink vs panel x42..918 y45..538) ==")
ink = rred | rdark | ryel
ys, xs = np.where(ink[int(50 * s):int(500 * s), :])
print(f"  ink extent frame x{xs.min()/s:.1f}..{xs.max()/s:.1f} y{50+ys.min()/s:.1f}..{50+ys.max()/s:.1f}")
