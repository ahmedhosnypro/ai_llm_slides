#!/usr/bin/env python3
"""Closed-loop ink check: render (150dpi, 2000x1125) vs mapped original-frame targets.
1 px @150dpi = 1/200 in = 0.72 pt; tolerance ~4 px @150dpi (law). Original targets are
frame-px measurements mapped to slide pt (sx=(fx-17.63)/0.96123, sy=fy/0.95556), then
to render px (x2.0833). Checks chrome, title, panel+lines, diagram, banner, boxes,
labels, dots, arrows, separators, caption. Usage: closed_loop.py <render.png> [tag]"""
import sys
import numpy as np
from PIL import Image

REND = sys.argv[1]
TAG = sys.argv[2] if len(sys.argv) > 2 else "render"
im = Image.open(REND).convert("RGB")
a = np.asarray(im).astype(int)
H, W = a.shape[:2]
print(f"render {W}x{H}")
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
S = 2000 / 960.0  # slide pt -> render px (13.333in slide at 150dpi = 2000px wide)

def box(m):
    ys, xs = np.where(m)
    if not len(xs):
        return None
    return (xs.min(), xs.max(), ys.min(), ys.max(), len(xs))

def report(name, target_px, got, tol=4):
    if got is None:
        print(f"[{TAG}] {name}: NO INK  (target {target_px})")
        return
    x0, x1, y0, y1, n = got
    tx0, tx1, ty0, ty1 = target_px
    dx0, dx1, dy0, dy1 = x0 - tx0, x1 - tx1, y0 - ty0, y1 - ty1
    worst = max(abs(dx0), abs(dx1), abs(dy0), abs(dy1))
    flag = "OK " if worst <= tol else "FAIL"
    print(f"[{TAG}] {name}: {flag} ink x{x0}..{x1} y{y0}..{y1} n={n} | target x{tx0}..{tx1} y{ty0}..{ty1} | d=({dx0},{dx1},{dy0},{dy1}) worst={worst:.1f}")

def px(v):
    return v * S

# masks on the render
redm = (r > 130) & (g < 100) & (b < 100)
bluem = (b > 120) & (r < 110) & (g < 110)
yellowm = (r > 225) & (g > 225) & (b < 100)
navyfill = (b > 140) & (b < 210) & (r < 80) & (g < 80)
pinksep = (r > 235) & (b > 235) & (g < r - 10) & (g < b - 6)
peach = (r > 240) & (g > 190) & (g < 235) & (b > 180) & (b < 225)

# ---- chrome (via shared checker separately); quick border check here
print("== chrome ==")
colc = redm[:, :].sum(axis=0)
left_cols = [x for x in range(60, 140) if colc[x] > 500]
right_cols = [x for x in range(1830, 1920) if colc[x] > 500]
print(f"  panel border cols: left {left_cols[:3]} (target ~{px(42):.0f}) right {right_cols[-3:]} (target ~{px(919):.0f})")

# ---- title
print("== title ==")
report("title ink", (px(299.9), px(722.4), px(81.6), px(101.5)), box(redm[150:230, 500:1600]))

# ---- info panel
print("== info panel ==")
report("panel border box", (px(80.5), px(878.6), px(115.1), px(349.5)), box(bluem[220:760, 140:1860]))
# text lines: (name, inkL_pt, inkR_pt, capTop_pt, capBot_pt)  targets from original
lines = [
    ("L2 body", 170.0, 696.6, 143.4, 159.1),
    ("L5 body", 170.9, 751.8, 225.0, 238.6),
    ("L7 body", 133.5, 760.1, 286.7, 302.4),
    ("L8 apply", 217.6, 360.0, 306.6, 318.1),
    ("L1 Input:", 90.9, 152.9, 124.5, 135.0),
]
for (nm, il, ir, ct, cb) in lines:
    sub = bluem[int(px(ct)) - 6:int(px(cb)) + 8, int(px(il)) - 12:int(px(ir)) + 40]
    report(nm, (px(il), px(ir), px(ct), px(cb)), box(sub))

# ---- diagram panel + banner
print("== diagram ==")
report("diag border box", (px(49.3), px(910.1), px(364.2), px(534.7)), box(redm[740:1140, 80:1920]))
report("banner fill", (px(153.3), px(901.3), px(412.3), px(464.7)), box(navyfill[840:990, 300:1900]))
wt = (r > 200) & (g > 200) & (b > 200)
report("banner white text", (px(382.2), px(673.2), px(432.3), px(445.0)), box(wt[int(px(425)):int(px(455)), int(px(200)):int(px(880))]))

# ---- token rows
print("== token rows ==")
report("Y box1 cells", (px(164.8), px(204.3), px(376.8), px(393.8)), box(peach[int(px(370)):int(px(400)), int(px(150)):int(px(220))]))
report("X box1 cells", (px(164.8), px(204.3), px(484.5), px(501.3)), box(peach[int(px(478)):int(px(510)), int(px(150)):int(px(220))]))
# label ink (red) box1
report("Y1 label", (px(189.8), px(201.2), px(378.9), px(391.4)), box(redm[int(px(374)):int(px(396)), int(px(182)):int(px(210))]))
report("X1 label", (px(189.8), px(201.2), px(486.6), px(499.1)), box(redm[int(px(482)):int(px(504)), int(px(182)):int(px(210))]))
# tails
report("Y7 label", (px(763.4), px(782.0), px(378.9), px(391.4)), box(redm[int(px(374)):int(px(396)), int(px(750)):int(px(795))]))

# ---- dots
print("== dots ==")
bluedot = (b > 150) & (r < 90) & (g < 90)
report("blue dot1", (px(632.0), px(638.8), px(381.7), px(388.5)), box(bluedot[int(px(376)):int(px(394)), int(px(620)):int(px(650))]))

greendot = (g > 180) & (r < 150) & (b < 180) & (g - r > 60)
report("green dot1", (px(632.3), px(638.5), px(489.3), px(495.6)), box(greendot[int(px(484)):int(px(500)), int(px(620)):int(px(650))]))
print("  green dot color sample:", a[int(px(492.4)), int(px(635.4))], " blue dot:", a[int(px(385.1)), int(px(635.4))])

# ---- arrows
print("== arrows ==")
arrink = ((b > 120) & (r < 110) & (g < 110))
report("arrow2 below", (px(265.0), px(279.4), px(465.7), px(481.4)), box(arrink[int(px(462)):int(px(486)), int(px(255)):int(px(290))]))
report("arrow3 above", (px(341.0), px(355.5), px(395.6), px(410.2)), box(arrink[int(px(392)):int(px(414)), int(px(332)):int(px(366))]))

# ---- separators
print("== separators ==")
report("sep b1-b2 Y", (px(216.0), px(226.5), px(378.3), px(391.9)), box(pinksep[int(px(374)):int(px(396)), int(px(208)):int(px(236))]))
report("sep b4-b5 Y", (px(444.0), px(454.6), px(378.3), px(391.9)), box(pinksep[int(px(374)):int(px(396)), int(px(436)):int(px(464))]))

# ---- caption
print("== caption ==")
report("caption hl", (px(284.7), px(578.0), px(510.7), px(524.3)), box(yellowm[int(px(504)):int(px(532)), int(px(270)):int(px(600))]))
dark = (r < 190) & (g < 150) & (b < 150)
report("caption text", (px(284.4), px(575.7), px(512.8), px(523.3)), box(dark[int(px(505)):int(px(530)), int(px(275)):int(px(600))]))
