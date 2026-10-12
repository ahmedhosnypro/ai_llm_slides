#!/usr/bin/env python3
"""Closed-loop geometry self-check: render_1.png (150dpi) vs PIL-measured frame geometry.
Frame->render mapping (fitted from this frame's chrome landmarks):
  rx = (fx - 18.628) * 150 / (0.96123*72) ;  ry = fy * 150 / (0.95556*72)
Tolerance ~4 render px. Prints per-element expected vs measured ink bbox and deltas."""
import numpy as np
from PIL import Image

R = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide049/render_1.png"
KX = 150 / (0.96123 * 72)
KY = 150 / (0.95556 * 72)
MX = 18.628

def RX(fx): return (fx - MX) * KX
def RY(fy): return fy * KY

im = np.asarray(Image.open(R).convert("RGB")).astype(int)
H, W = im.shape[:2]
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]

TOL = 4.0
results = []

def ink_bbox(y0, y1, x0, x1, mask_fn, name, exp):
    """exp = (fx0,fx1,fy0,fy1) frame px expected ink bbox; window given in frame px."""
    wy0, wy1 = int(RY(y0)), int(RY(y1))
    wx0, wx1 = int(RX(x0)), int(RX(x1))
    sub = mask_fn(r[wy0:wy1, wx0:wx1], g[wy0:wy1, wx0:wx1], b[wy0:wy1, wx0:wx1])
    ys, xs = np.where(sub)
    if len(xs) == 0:
        results.append((name, "NO INK", exp, None, "FAIL"))
        return
    bx0, bx1 = wx0 + xs.min(), wx0 + xs.max()
    by0, by1 = wy0 + ys.min(), wy0 + ys.max()
    e = [RX(exp[0]), RX(exp[1]), RY(exp[2]), RY(exp[3])]
    d = [bx0 - e[0], bx1 - e[1], by0 - e[2], by1 - e[3]]
    ok = all(abs(v) <= TOL for v in d)
    results.append((name, f"render bbox x{bx0}..{bx1} y{by0}..{by1}",
                    f"expected x{e[0]:.0f}..{e[1]:.0f} y{e[2]:.0f}..{e[3]:.0f}",
                    f"deltas {['%+.1f'%v for v in d]}", "PASS" if ok else "FAIL"))

redm = lambda r, g, b: (r - g > 40) & (r - b > 35) & (r > 110)
navym = lambda r, g, b: (b - r > 45) & (b - g > 35) & (b > 80) & (r < 130)
darkm = lambda r, g, b: (r + g + b < 330)
bluem = lambda r, g, b: (b - r > 30) & (b - g > 25) & (b > 120)
greenm = lambda r, g, b: (g - r > 25) & (g - b > 25) & (g > 130)
graym = lambda r, g, b: (abs(r - g) < 16) & (abs(g - b) < 16) & (r > 110) & (r < 205)
tanm = lambda r, g, b: (r > 225) & (g > 205) & (r - b > 25) & (g - b > 20)
cyanm = lambda r, g, b: (g > 225) & (b > 225) & (r < 225) & (g - r > 15)

# title
ink_bbox(40, 80, 240, 800, redm, "title", (256, 782, 51, 71))
# tall container: top line, bottom rule, side lines
ink_bbox(70, 90, 170, 870, navym, "container top line", (164, 878, 80, 81))
ink_bbox(500, 516, 170, 870, navym, "container bottom rule", (164, 878, 508, 511))
ink_bbox(200, 340, 150, 180, navym, "container left line", (164, 166, 200, 340))
ink_bbox(200, 340, 860, 895, navym, "container right line", (877, 879, 200, 340))
# stack container border + bars
ink_bbox(115, 370, 150, 895, navym, "stack container+bars", (166, 877, 126, 365))
ink_bbox(125, 165, 200, 850, lambda r, g, b: ((r + g + b < 400) & (b - r > 40)), "bar M", (174, 870, 132, 159))
ink_bbox(230, 272, 200, 850, lambda r, g, b: ((r + g + b < 400) & (b - r > 40)), "bar 2", (174, 870, 238, 266))
ink_bbox(325, 362, 200, 850, lambda r, g, b: ((r + g + b < 400) & (b - r > 40)), "bar 0", (174, 870, 330, 357))
# green arrows band (col 1)
ink_bbox(100, 128, 190, 222, greenm, "green arrow c1", (199, 212, 107, 123))
# Y row cells + dots
ink_bbox(80, 110, 590, 740, navym, "Y ellipsis dots", (624, 700, 89, 98))
ink_bbox(80, 112, 165, 250, redm, "Y label c1", (198, 211, 88, 104))
# X row
ink_bbox(368, 388, 190, 222, navym, "X tab c1", (197, 212, 366, 381))
ink_bbox(378, 402, 165, 250, redm, "X label c1", (198, 211, 383, 399))
ink_bbox(378, 404, 590, 740, greenm, "X ellipsis dots", (624, 702, 387, 395))
# blue arrows up (c1) + word arrows (c1)
ink_bbox(395, 420, 190, 222, bluem, "blue arrow c1", (198, 213, 401, 416))
ink_bbox(462, 484, 190, 222, bluem, "word arrow c1", (197, 212, 467, 482))
# embedding box borders + bars
ink_bbox(410, 422, 300, 700, darkm, "emb top border", (172, 871, 417, 419))
ink_bbox(460, 470, 300, 700, darkm, "emb bottom border", (172, 871, 464, 466))
ink_bbox(420, 442, 300, 700, tanm, "tan bar fill", (174, 869, 419, 442))
ink_bbox(443, 464, 300, 700, cyanm, "cyan bar fill", (174, 869, 442, 464))
# word row: box borders + label + gray dots
ink_bbox(478, 488, 165, 250, redm, "word box c1 top border", (176, 235, 482, 483))
ink_bbox(486, 502, 165, 250, redm, "word label c1", (187, 235, 486, 498))
ink_bbox(486, 502, 600, 730, graym, "word gray dots", (626, 703, 490, 498))
# left column
ink_bbox(60, 130, 55, 160, redm, "EO box", (65, 145, 75, 120))
ink_bbox(370, 430, 55, 160, redm, "EI box", (65, 145, 377, 422))
ink_bbox(155, 330, 70, 150, bluem, "vert text", (85, 134, 163, 320))
ink_bbox(425, 470, 55, 160, redm, "embedding text", (65, 145, 432, 462))
ink_bbox(478, 515, 55, 160, redm, "InputSeq box", (65, 145, 482, 511))
# badge (chrome)
ink_bbox(50, 95, 850, 905, lambda r, g, b: (r > 200) & (g > 200) & (b < 190), "badge yellow", (860, 892, 56, 79))

print(f"{'element':26s} {'measured':38s} {'expected':38s} {'delta':30s} verdict")
nfail = 0
for name, m, e, d, v in results:
    if v == "FAIL":
        nfail += 1
    print(f"{name:26s} {m:38s} {e:38s} {str(d):30s} {v}")
print(f"\n{nfail}/{len(results)} FAIL (tol {TOL} render px)")

# color sample checks (render vs frame cores, JPEG-loose)
def csample(fy, fx, name, frame_rgb, tol=60):
    ry, rx = int(RY(fy)), int(RX(fx))
    px = im[ry, rx]
    d = max(abs(int(px[i]) - frame_rgb[i]) for i in range(3))
    print(f"color {name:22s} render@({rx},{ry})={tuple(px)} frame={frame_rgb} maxdiff={d} {'PASS' if d<=tol else 'FAIL'}")

csample(146, 520, "bar fill", (53, 59, 183))
csample(224, 700, "stack fill", (213, 227, 238))
csample(430, 700, "tan bar", (247, 229, 209))
csample(452, 700, "cyan bar", (218, 253, 247))
csample(60, 400, "title red", (160, 20, 30), 80)
csample(97, 100, "EO box fill", (249, 232, 214))
csample(250, 70, "left col bg (gray)", (232, 232, 230), 25)
csample(30, 480, "canvas white", (254, 255, 253), 12)
