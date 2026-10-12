#!/usr/bin/env python3
"""Closed-loop geometry self-check v2: render vs PIL-measured frame geometry.
Windows are chosen to ISOLATE each element (no chrome border, no neighbors).
Frame->render: rx=(fx-18.628)*150/(0.96123*72); ry=fy*150/(0.95556*72). Tol 4 render px."""
import numpy as np
from PIL import Image

R = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide049/render_1.png"
KX = 150 / (0.96123 * 72)
KY = 150 / (0.95556 * 72)
MX = 18.628
def RX(fx): return (fx - MX) * KX
def RY(fy): return fy * KY

im = np.asarray(Image.open(R).convert("RGB")).astype(int)
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]
TOL = 4.0
results = []

def ink_bbox(fy0, fy1, fx0, fx1, mask_fn, name, exp, tol=TOL):
    wy0, wy1, wx0, wx1 = int(RY(fy0)), int(RY(fy1)), int(RX(fx0)), int(RX(fx1))
    sub = mask_fn(r[wy0:wy1, wx0:wx1], g[wy0:wy1, wx0:wx1], b[wy0:wy1, wx0:wx1])
    ys, xs = np.where(sub)
    if len(xs) == 0:
        results.append((name, "NO INK", f"exp x{RX(exp[0]):.0f}..{RX(exp[1]):.0f} y{RY(exp[2]):.0f}..{RY(exp[3]):.0f}", "FAIL"))
        return
    bx0, bx1, by0, by1 = wx0 + xs.min(), wx0 + xs.max(), wy0 + ys.min(), wy0 + ys.max()
    e = [RX(exp[0]), RX(exp[1]), RY(exp[2]), RY(exp[3])]
    d = [bx0 - e[0], bx1 - e[1], by0 - e[2], by1 - e[3]]
    ok = all(abs(v) <= tol for v in d)
    results.append((name, f"x{bx0}..{bx1} y{by0}..{by1}", f"x{e[0]:.0f}..{e[1]:.0f} y{e[2]:.0f}..{e[3]:.0f}",
                    f"d={['%+.1f' % v for v in d]}", "PASS" if ok else "FAIL"))

redm   = lambda r, g, b: (r - g > 40) & (r - b > 35) & (r > 110)
navym  = lambda r, g, b: (b - r > 45) & (b - g > 35) & (b > 80) & (r < 130)
bluem  = lambda r, g, b: (b - r > 30) & (b - g > 25) & (b > 120)
greenm = lambda r, g, b: (g - r > 25) & (g - b > 25) & (g > 130)
graym  = lambda r, g, b: (abs(r - g) < 16) & (abs(g - b) < 16) & (r > 110) & (r < 205)
tanm   = lambda r, g, b: (r > 235) & (g > 210) & (r - b > 25) & (g - b > 8) & (b < 235)
blackm = lambda r, g, b: (r < 90) & (g < 90) & (b < 90)

# title (chrome top border ends ~render 98; window starts below it)
ink_bbox(52, 78, 240, 800, redm, "title ink", (256, 782, 51, 71))
# tall container lines (probed windows away from badge/bars)
ink_bbox(74, 87, 300, 800, navym, "top line", (300, 800, 79, 82))
ink_bbox(505, 514, 300, 800, navym, "bottom rule", (300, 800, 508, 511))
ink_bbox(150, 250, 155, 172, navym, "left line", (163, 167, 150, 250))
ink_bbox(150, 250, 870, 888, navym, "right line", (876, 880, 150, 250))
# stack container top/bottom borders (narrow x window between arrows)
ink_bbox(122, 132, 600, 640, navym, "stack top border", (600, 640, 126, 128))
ink_bbox(360, 368, 600, 640, navym, "stack bottom border", (600, 640, 363, 365))
# bars: interior x window 300..700, excluding border rows via y windows
ink_bbox(130, 162, 300, 700, lambda r, g, b: (r + g + b < 420) & (b - r > 40), "bar M", (300, 700, 132, 159))
ink_bbox(236, 268, 300, 700, lambda r, g, b: (r + g + b < 420) & (b - r > 40), "bar 2", (300, 700, 238, 266))
ink_bbox(328, 360, 300, 700, lambda r, g, b: (r + g + b < 420) & (b - r > 40), "bar 0", (300, 700, 330, 357))
# arrows (column 1 isolated)
ink_bbox(103, 127, 196, 216, greenm, "green arrow c1", (199, 212, 107, 123))
ink_bbox(398, 419, 196, 216, bluem, "blue arrow c1", (198, 213, 401, 416))
ink_bbox(464, 484, 196, 216, bluem, "word arrow c1", (197, 212, 467, 482))
ink_bbox(265, 286, 196, 216, redm, "red arrow c1 (2->1)", (199, 212, 269, 283))
ink_bbox(310, 331, 196, 216, redm, "red arrow c1 (1->0)", (199, 212, 314, 328))
# dots
ink_bbox(85, 106, 615, 712, navym, "Y dots", (624, 700, 89, 98))
ink_bbox(383, 400, 615, 712, greenm, "X dots", (624, 702, 387, 395))
ink_bbox(486, 502, 618, 710, graym, "word dots", (626, 703, 490, 498))
# token labels + cells (chip 1 isolated)
ink_bbox(84, 106, 195, 214, redm, "Y label c1", (198, 211, 88, 104))
ink_bbox(380, 400, 195, 214, redm, "X label c1", (198, 211, 383, 399))
ink_bbox(86, 105, 174, 240, lambda r, g, b: (r > 240) & (g > 240) & (b > 180) & (b < 235), "Y chip yellow cell", (176, 186, 88, 103))
ink_bbox(381, 401, 174, 240, lambda r, g, b: (r > 240) & (g > 240) & (b > 180) & (b < 235), "X chip yellow cell", (176, 186, 383, 399))
# X row tabs: triangle band and stub band separately
ink_bbox(366.5, 373, 196, 216, navym, "X tab triangle c1", (197, 212, 366.5, 372))
ink_bbox(376, 383, 196, 216, navym, "X tab stub c1", (200, 209, 375, 381))
# embedding box borders (x window mid, y isolated)
ink_bbox(414, 421, 400, 700, blackm, "emb top border", (400, 700, 417, 419), tol=4)
ink_bbox(461, 469, 400, 700, blackm, "emb bottom border", (400, 700, 464, 466))
ink_bbox(421, 441, 400, 700, tanm, "tan bar fill", (400, 700, 419, 442))
ink_bbox(444, 463, 400, 700, lambda r, g, b: (g > 235) & (b > 235) & (r < 225), "cyan bar fill", (400, 700, 442, 464))
# word row (box 1 isolated)
ink_bbox(479, 486, 250, 306, redm, "word box top border b1", (249, 306, 482, 483))
ink_bbox(487, 501, 255, 302, redm, "word label b1", (260, 302, 486, 498))
ink_bbox(500, 506, 250, 306, redm, "word box bottom border b1", (249, 306, 502, 503))
# left column (x window excludes chrome border at 57..59)
ink_bbox(73, 122, 62, 150, redm, "EO box", (65, 145, 75, 120))
ink_bbox(375, 424, 62, 150, redm, "EI box", (65, 145, 377, 422))
ink_bbox(158, 325, 70, 150, bluem, "vert text", (85, 134, 163, 320))
ink_bbox(430, 466, 62, 150, redm, "embedding text", (65, 145, 432, 462))
ink_bbox(479, 514, 62, 150, redm, "InputSeq box", (65, 145, 482, 511))

print(f"{'element':26s} {'measured':30s} {'expected':30s} {'delta':28s} verdict")
nfail = 0
for row in results:
    name, m, e, d, v = row
    if v == "FAIL":
        nfail += 1
    print(f"{name:26s} {m:30s} {e:30s} {str(d):28s} {v}")
print(f"\n{nfail}/{len(results)} FAIL (tol {TOL} render px)")
