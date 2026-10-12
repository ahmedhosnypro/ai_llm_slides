#!/usr/bin/env python3
"""Self-check attempt 1: title ink closed-loop + frame containment + no-wrap.

Original frame 960x540 (1px=1pt); render 2001x1125 @150dpi (1px = 1/150 in).
scale render->frame: *540/1125 (*0.48). Tolerance ~8 render px (~4 frame px).
Playlist white-margin containment adaptation: content ink must sit fully inside
the gray panel (frame x[38.5,920] y[43,539] incl. border) — the playlist chrome
supersedes the ml-intro house-frame bands.
"""
import sys
import numpy as np
from PIL import Image

REN = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/qa/slide013/render_1.png"
ORIG = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_013.jpg"
fails = []

ren = np.asarray(Image.open(REN).convert("RGB")).astype(int)
ori = np.asarray(Image.open(ORIG).convert("RGB")).astype(int)
HR, WR = ren.shape[:2]
scale = HR / 540.0
TOL = 8.3  # render px ~ 4 frame px

def title_ink(im, W, H):
    r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]
    ink = (r > 130) & (r - g > 60) & (r - b > 50)
    m = np.zeros_like(ink)
    m[int(0.35 * H):int(0.65 * H), int(0.08 * W):int(0.92 * W)] = True  # title band only
    ink &= m
    ys, xs = np.where(ink)
    return xs.min(), xs.max(), ys.min(), ys.max(), len(ys)

ox0, ox1, oy0, oy1, on = title_ink(ori, 960, 540)
rx0, rx1, ry0, ry1, rn = title_ink(ren, WR, HR)
print(f"ORIG title ink: x[{ox0},{ox1}] w={ox1-ox0+1}, y[{oy0},{oy1}] h={oy1-oy0+1}, px={on}")
print(f"REN  title ink: x[{rx0},{rx1}] w={rx1-rx0+1}, y[{ry0},{ry1}] h={ry1-ry0+1}, px={rn}")
# convert orig to render px
o0, o1 = ox0 * scale, (ox1 + 1) * scale
p0, p1 = oy0 * scale, (oy1 + 1) * scale
print(f"ORIG in render px: x[{o0:.1f},{o1:.1f}], y[{p0:.1f},{p1:.1f}]")
for name, rv, ov in [("x0", rx0, o0), ("x1", rx1 + 1, o1), ("y0", ry0, p0), ("y1", ry1 + 1, p1)]:
    d = rv - ov
    print(f"  {name}: render {rv} vs orig {ov:.1f} -> diff {d:+.1f} render px ({d/scale:+.1f} frame px)")
    if abs(d) > TOL:
        fails.append(f"title {name} off by {d:+.1f} render px (tol {TOL})")

# center comparison
rcx, rocx = (rx0 + rx1) / 2, (o0 + o1) / 2
rcy, rocy = (ry0 + ry1) / 2, (p0 + p1) / 2
print(f"  center: render ({rcx:.1f},{rcy:.1f}) vs orig ({rocx:.1f},{rocy:.1f})")
if abs(rcx - rocx) > TOL or abs(rcy - rocy) > TOL:
    fails.append(f"title center off: ({rcx-rocx:+.1f},{rcy-rocy:+.1f}) render px")

# FRAME CONTAINMENT (playlist white-margin adaptation): panel incl. border
# frame x[38,921] y[42,540] -> render px; content ink must be strictly inside
pl, pr_ = 38.5 * scale, 920.5 * scale
pt, pb = 42.5 * scale, 539.5 * scale
print(f"CONTAINMENT: panel interior render x[{pl:.0f},{pr_:.0f}] y[{pt:.0f},{pb:.0f}]")
if rx0 < pl + 2 or rx1 > pr_ - 2:
    fails.append("title ink crosses panel left/right boundary")
if ry0 < pt + 2 or ry1 > pb - 2:
    fails.append("title ink crosses panel top/bottom boundary")
print(f"  title ink inside panel with clearance "
      f"L{rx0-pl:.0f} R{pr_-rx1:.0f} T{ry0-pt:.0f} B{pb-ry1:.0f} render px")

# NO-WRAP / BAND check: no red ink outside the title band (would indicate wrap
# or a stray second line); badge numeral is chrome, separate zone.
r, g, b = ren[:, :, 0], ren[:, :, 1], ren[:, :, 2]
red_any = (r > 130) & (r - g > 60) & (r - b > 50)
band = np.zeros_like(red_any)
band[ry0 - 10:ry1 + 10, rx0 - 10:rx1 + 10] = True
# exclude the chrome border ring (C00000 strokes on the panel edges — expected
# red ink): ~12 render px inside every panel edge incl. the bottom stroke.
border = np.zeros_like(red_any)
bw = 12
border[int(pt) - bw:int(pt) + bw, :] = True
border[int(pb) - bw - 6:, :] = True
border[:, int(pl) - bw:int(pl) + bw] = True
border[:, int(pr_) - bw:int(pr_) + bw] = True
stray = red_any & ~band & ~border
ys, xs = np.where(stray)
if len(ys) > 20:
    fails.append(f"stray red ink outside title band: {len(ys)} px at x[{xs.min()},{xs.max()}] y[{ys.min()},{ys.max()}]")
print(f"  stray red ink outside title band: {len(ys)} px")

if fails:
    print("SELF-CHECK: FAIL")
    for f in fails:
        print("  -", f)
    sys.exit(1)
print("SELF-CHECK: PASS (title ink closed-loop within tol; containment OK; no wrap)")
