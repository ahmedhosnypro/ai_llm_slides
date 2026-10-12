#!/usr/bin/env python3
"""Closed-loop ink check v2 (offset-corrected): render (150dpi) vs mapped targets.
Usage: closed_loop2.py <render.png> [tag]"""
import sys
import numpy as np
from PIL import Image

REND = sys.argv[1]
TAG = sys.argv[2] if len(sys.argv) > 2 else "render"
a = np.asarray(Image.open(REND).convert("RGB")).astype(int)
H, W = a.shape[:2]
print(f"render {W}x{H}")
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
S = 2000 / 960.0
px = lambda v: v * S
FAILS = []

def check(name, m, y0, y1, x0, x1, tgt, tol=4):
    sub = m[int(y0):int(y1), int(x0):int(x1)]
    ys, xs = np.where(sub)
    if not len(xs):
        print(f"[{TAG}] {name}: NO INK  target {tuple(round(v,1) for v in tgt)}")
        FAILS.append(name)
        return
    gx0, gx1 = x0 + xs.min(), x0 + xs.max()
    gy0, gy1 = y0 + ys.min(), y0 + ys.max()
    d = (gx0 - tgt[0], gx1 - tgt[1], gy0 - tgt[2], gy1 - tgt[3])
    worst = max(abs(v) for v in d)
    flag = "OK " if worst <= tol else "FAIL"
    if flag == "FAIL":
        FAILS.append(name)
    print(f"[{TAG}] {name}: {flag} ink x{gx0:.0f}..{gx1:.0f} y{gy0:.0f}..{gy1:.0f} n={len(xs)} | tgt {tuple(round(v,1) for v in tgt)} | d=({d[0]:.0f},{d[1]:.0f},{d[2]:.0f},{d[3]:.0f}) worst={worst:.1f}")

redm = (r > 130) & (g < 100) & (b < 100)
bluem = (b > 120) & (r < 110) & (g < 110)
yellowm = (r > 225) & (g > 225) & (b < 100)
navyfill = (b > 140) & (b < 210) & (r < 80) & (g < 80)
pinksep = (r > 235) & (b > 235) & (g < r - 10) & (g < b - 6)
peach = (r > 240) & (g > 190) & (g < 235) & (b > 180) & (b < 225)

print("== title ==")
check("title ink", redm, 150, 230, 500, 1600, (px(299.9), px(722.4), px(81.6), px(101.5)))
print("== info panel ==")
check("panel border", bluem, 220, 760, 140, 1860, (px(80.5), px(878.6), px(115.1), px(349.5)))
for (nm, il, ir, ct, cb) in [
    ("L1 Input:", 90.9, 152.9, 124.5, 135.0),
    ("L2 body", 170.0, 696.6, 143.4, 159.1),
    ("L5 body", 170.9, 751.8, 225.0, 238.6),
    ("L7 body", 133.5, 760.1, 286.7, 302.4),
    ("L8 apply", 217.6, 360.0, 306.6, 318.1),
    ("L9 body", 131.4, 595.0, 326.5, 342.2),
]:
    check(nm, bluem, px(ct) - 6, px(cb) + 8, px(il) - 14, px(ir) + 45, (px(il), px(ir), px(ct), px(cb)))
print("== diagram ==")
check("diag border", redm, 740, 1140, 80, 1920, (px(49.3), px(910.1), px(364.2), px(534.7)))
check("banner fill", navyfill, 840, 990, 300, 1900, (px(153.3), px(901.3), px(412.3), px(464.7)))
wt = (r > 200) & (g > 200) & (b > 200)
check("banner white text", wt, px(425), px(455), px(200), px(880), (px(382.2), px(673.2), px(432.3), px(445.0)))
print("== token rows ==")
check("Y box1 cells", peach, px(370), px(400), px(150), px(220), (px(164.8), px(204.3), px(376.8), px(393.8)))
check("X box1 cells", peach, px(478), px(510), px(150), px(220), (px(164.8), px(204.3), px(484.5), px(501.3)))
check("Y1 label", redm, px(374), px(396), px(182), px(212), (px(189.8), px(201.2), px(378.9), px(391.4)))
check("X1 label", redm, px(482), px(504), px(182), px(212), (px(189.8), px(201.2), px(486.6), px(499.1)))
check("Y7 label", redm, px(374), px(396), px(748), px(795), (px(763.4), px(782.0), px(378.9), px(391.4)))
print("== dots ==")
bluedot = (b > 150) & (r < 90) & (g < 90)
greendot = (g > 180) & (r < 150) & (b < 180) & (g - r > 60)
check("blue dot1", bluedot, px(376), px(394), px(620), px(650), (px(632.0), px(638.8), px(381.7), px(388.5)))
check("green dot1", greendot, px(484), px(500), px(620), px(650), (px(632.3), px(638.5), px(489.3), px(495.6)))
print("  dot colors: blue", a[int(px(385.1)), int(px(635.4))], "green", a[int(px(492.4)), int(px(635.4))])
print("== arrows ==")
arrink = (b > 120) & (r < 110) & (g < 110)
check("arrow2 below", arrink, px(462), px(486), px(255), px(290), (px(265.0), px(279.4), px(465.7), px(481.4)))
check("arrow3 above", arrink, px(392), px(414), px(332), px(366), (px(341.0), px(355.5), px(395.6), px(410.2)))
print("== separators ==")
check("sep b1-b2 Y", pinksep, px(374), px(396), px(208), px(236), (px(216.0), px(226.5), px(378.3), px(391.9)))
check("sep b4-b5 Y", pinksep, px(374), px(396), px(436), px(464), (px(444.0), px(454.6), px(378.3), px(391.9)))
print("== caption ==")
check("caption hl", yellowm, px(504), px(532), px(270), px(600), (px(284.7), px(578.0), px(510.7), px(524.3)))
dark = (r < 190) & (g < 150) & (b < 150)
check("caption text", dark, px(505), px(530), px(275), px(600), (px(284.4), px(575.7), px(512.8), px(523.3)))
print(f"\n[{TAG}] FAILS: {FAILS if FAILS else 'none'}")
