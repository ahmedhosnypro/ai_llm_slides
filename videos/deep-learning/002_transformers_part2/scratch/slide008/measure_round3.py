#!/usr/bin/env python3
"""Round 3: exact edges/fills of W_k & W_v boxes, blue circle fit, Y strip,
q2/K.q ink, inherited anchors."""
import numpy as np
from PIL import Image
from collections import Counter

F8 = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_008.jpg"
im = np.asarray(Image.open(F8).convert("RGB")).astype(int)
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]

AX, SX, SY = 17.628, 0.961232, 0.955556
def sx(fx): return (fx - AX) / SX
def sy(fy): return fy / SY

def mode_color(y0, y1, x0, x1, exclude_dark=True):
    px = im[y0:y1, x0:x1].reshape(-1, 3)
    if exclude_dark:
        keep = ~((px[:, 0] < 150) & (px[:, 1] < 150))
        px = px[keep]
    cnt = Counter(map(tuple, px))
    return cnt.most_common(3)

# ---- W_k boxes: column profile of "boxy" pixels in y-band of each box
print("== W_k boxes ==")
BANDS = [(225, 251), (264, 291), (304, 330), (346, 372)]
for (a, z) in BANDS:
    band = im[a:z, 150:230]
    # non-peach, non-white
    nonbg = ~(((band[:, :, 0] > 225) & (band[:, :, 1] > 195) & (band[:, :, 2] > 165)) |
              ((band[:, :, 0] > 235) & (band[:, :, 1] > 235) & (band[:, :, 2] > 235)))
    colc = nonbg.sum(axis=0)
    xs = np.where(colc > (z - a) * 0.5)[0]
    if len(xs):
        x0, x1 = 150 + xs.min(), 150 + xs.max()
        print(f"band y {a}..{z}: x {x0}..{x1} (w {x1-x0+1}) | slide x {sx(x0):.1f}..{sx(x1):.1f} y {sy(a):.1f}..{sy(z):.1f}")
        print("   fill mode:", mode_color(a + 3, z - 3, x0 + 4, x1 - 3))
        print("   border sample top:", tuple(im[a + 1, (x0 + x1) // 2]), " left:", tuple(im[(a + z) // 2, x0 + 1]))

# ---- W_v boxes: column profile
print("\n== W_v boxes ==")
for (a, z) in BANDS:
    band = im[a:z, 640:745]
    nonbg = ~(((band[:, :, 0] > 225) & (band[:, :, 1] > 195) & (band[:, :, 2] > 165)) |
              ((band[:, :, 0] > 235) & (band[:, :, 1] > 235) & (band[:, :, 2] > 235)))
    colc = nonbg.sum(axis=0)
    xs = np.where(colc > (z - a) * 0.5)[0]
    if len(xs):
        x0, x1 = 640 + xs.min(), 640 + xs.max()
        print(f"band y {a}..{z}: x {x0}..{x1} (w {x1-x0+1}) | slide x {sx(x0):.1f}..{sx(x1):.1f} y {sy(a):.1f}..{sy(z):.1f}")
        print("   fill mode:", mode_color(a + 4, z - 4, x0 + 4, x1 - 3))
        print("   border sample top:", tuple(im[a + 1, (x0 + x1) // 2]))

# ---- blue circle: full row extents 370..510
print("\n== blue circle rows ==")
reg_x0 = 200
R_, G_, B_ = r, g, b
blue = (b > r + 20) & (b > g + 8) & (b > 150)
ext = {}
for yy in range(370, 512):
    xr = np.where(blue[yy, reg_x0:420])[0]
    if len(xr) > 6:
        ext[yy] = (reg_x0 + xr.min(), reg_x0 + xr.max())
ys_sorted = sorted(ext)
print("first/last rows:", ys_sorted[0], ys_sorted[-1])
widest = max(ext, key=lambda k: ext[k][1] - ext[k][0])
print("widest row:", widest, ext[widest])
for yy in ys_sorted[::6]:
    print(f"  y {yy}: x {ext[yy][0]}..{ext[yy][1]} (w {ext[yy][1]-ext[yy][0]+1})")
# circle blend color over peach (left arc area)
print("blend samples:", tuple(im[400, 265]), tuple(im[430, 262]), tuple(im[390, 300]))

# ---- Y output strip: cells + label + subscript check
print("\n== Y output strip ==")
# green cells mask
grnc = (g > 150) & (g - r > 25) & (g - b > 25)
ys, xs = np.where(grnc[110:145, 540:620])
if len(xs):
    print("green cells bbox: x", 540 + xs.min(), "..", 540 + xs.max(), " y", 110 + ys.min(), "..", 110 + ys.max())
# any ink right/below of the Y label (subscript 2?) within strip
strip = im[112:145, 540:620]
dk = (strip[:, :, 0] < 150) & (strip[:, :, 1] < 170) & (strip[:, :, 2] < 150)
ys2, xs2 = np.where(dk)
if len(xs2):
    print("dark ink in strip bbox: x", 540 + xs2.min(), "..", 540 + xs2.max(), " y", 112 + ys2.min(), "..", 112 + ys2.max(), "n=", len(xs2))
# classify grid of strip
def classify(px):
    R, G, B = int(px[0]), int(px[1]), int(px[2])
    if R < 110 and G < 140 and B < 110: return "#"
    if G > 140 and G - R > 25 and G - B > 25: return "G"
    if B > R + 20 and B > G + 8: return "b"
    if R > 225 and G > 195 and B > 165: return "."
    if R > 150 and R - G > 50 and R - B > 50: return "R"
    return "?"
print("strip grid (x 540..625 step 3, y 112..148 step 3):")
for y in range(112, 149, 3):
    print(f"{y:3d} " + "".join(classify(im[y, x]) for x in range(540, 626, 3)))

# ---- q2 label region (above W_q, below DP): x 275..330, y 380..412
print("\n== q2 label region grid (x 272..330, y 378..412) ==")
for y in range(378, 413, 2):
    print(f"{y:3d} " + "".join(classify(im[y, x]) for x in range(272, 331, 2)))

# ---- K.q corner (right of DP box top): x 340..370, y 185..205
print("\n== K.q corner grid (x 338..372, y 183..208) ==")
for y in range(183, 209, 2):
    print(f"{y:3d} " + "".join(classify(im[y, x]) for x in range(338, 373, 2)))

# ---- inherited anchors: DP box, softmax, sigma, containers, sentence row, legend, pills
print("\n== anchor samples (frame px: expected content) ==")
anchors = [
    ("DP fill @(300,250)", 300, 250, (220, 203, 187)),
    ("DP fill @(290,320)", 290, 320, (220, 203, 187)),
    ("softmax @(472,300)", 472, 300, (248, 221, 252)),
    ("sigma @(560,200)", 560, 200, (234, 254, 252)),
    ("left container @(75,300)", 75, 300, (231, 255, 233)),
    ("right container @(790,300)", 790, 300, (231, 255, 233)),
    ("sentence row @(200,480)", 200, 480, (231, 255, 233)),
    ("legend @(760,480)", 760, 480, (231, 255, 233)),
    ("pill Similarity @(300,172)", 300, 172, (255, 255, 227)),
    ("peach panel @(120,150)", 120, 150, (247, 226, 205)),
    ("peach panel @(600,430)", 600, 430, (247, 226, 205)),
]
for name, x, y, exp in anchors:
    got = tuple(im[y, x])
    d = max(abs(got[i] - exp[i]) for i in range(3))
    print(f"{name}: {got} expected~{exp} maxdiff={d}")
