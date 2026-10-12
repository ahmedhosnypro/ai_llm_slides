#!/usr/bin/env python3
"""Round 4: softmax/pill fills (both frames), node interiors + ring centers,
W_q box edges, q2 ink, Y label color, circle (C,t) solve over two backgrounds."""
import numpy as np
from PIL import Image
from collections import Counter

ROOT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning"
f8 = np.asarray(Image.open(f"{ROOT}/002_transformers_part2/unique_slides/slide_008.jpg").convert("RGB")).astype(int)
f33 = np.asarray(Image.open(f"{ROOT}/001_transformers_part1/unique_slides/slide_033.jpg").convert("RGB")).astype(int)
r, g, b = f8[:, :, 0], f8[:, :, 1], f8[:, :, 2]

AX, SX, SY = 17.628, 0.961232, 0.955556
def sx(fx): return (fx - AX) / SX
def sy(fy): return fy / SY

def mode(y0, y1, x0, x1, im):
    px = im[y0:y1, x0:x1].reshape(-1, 3)
    return Counter(map(tuple, px)).most_common(4)

print("== softmax bar fill: f8 vs f33 (5 points each along the bar) ==")
for (x, y) in [(470, 220), (470, 270), (472, 320), (475, 360), (465, 250)]:
    print(f"  f8({x},{y})={tuple(f8[y, x])}   f33({x},{y})={tuple(f33[y, x])}")
print("  f8 bar mode y215..380 x462..488:", mode(215, 380, 462, 488, f8))
print("  f33 bar mode y215..380 x462..488:", mode(215, 380, 462, 488, f33))

print("\n== pills row: f8 vs f33 (Similarity/Probabilities/Weighted SUM) ==")
for name, (x0, x1, y0, y1) in [("Similarity", (275, 340, 158, 180)), ("Probabilities", (432, 512, 156, 178)), ("WeightedSUM", (598, 688, 156, 180))]:
    print(f"  {name}: f8 mode {mode(y0, y1, x0, x1, f8)}")
    print(f"  {name}: f33 mode {mode(y0, y1, x0, x1, f33)}")

print("\n== multiply node interiors + rings (f8) ==")
# node centers estimated from red clusters: ring extents
for i, (cy_lo, cy_hi, cx_lo, cx_hi) in enumerate([(215, 242, 505, 545), (262, 281, 535, 575), (301, 320, 560, 600), (343, 362, 590, 630)]):
    red = (r[cy_lo:cy_hi, cx_lo:cx_hi] > 120) & (r[cy_lo:cy_hi, cx_lo:cx_hi] - g[cy_lo:cy_hi, cx_lo:cx_hi] > 55) & (r[cy_lo:cy_hi, cx_lo:cx_hi] - b[cy_lo:cy_hi, cx_lo:cx_hi] > 55)
    ys, xs = np.where(red)
    if len(ys):
        print(f"  node{i+1}: red bbox x {cx_lo+xs.min()}..{cx_lo+xs.max()} y {cy_lo+ys.min()}..{cy_lo+ys.max()}")
        cx = cx_lo + (xs.min() + xs.max()) / 2; cy = cy_lo + (ys.min() + ys.max()) / 2
        print(f"    center ~({cx:.0f},{cy:.0f}) slide ({sx(cx):.1f},{sy(cy):.1f}); interior mode {mode(int(cy)-3, int(cy)+4, int(cx)-3, int(cx)+4, f8)}")

print("\n== node row: full color strip along each node centerline (x 500..650, step 2) ==")
for cy in [228, 271, 310, 352]:
    row = f8[cy, 500:650]
    s = ""
    for x in range(0, 150, 2):
        R, G, B = row[x]
        if R > 150 and R - G > 55 and R - B > 55: c = "R"
        elif R > 235 and G > 235 and B > 230: c = "W"
        elif R > 225 and G > 195 and B > 165: c = "."
        elif R < 120 and G < 120 and B < 120: c = "#"
        elif B > R + 20: c = "b"
        else: c = "?"
        s += c
    print(f"  y={cy}: {s}  (x 500..648 step2)")

print("\n== W_q box: edges inside circle blend ==")
# The box should have a border (magenta/navy?) distinct from blend. Scan rows 405..465, x 270..340 for saturated/dark pixels
sub = f8[400:470, 265:345]
R_, G_, B_ = sub[:, :, 0], sub[:, :, 1], sub[:, :, 2]
dark = (R_ < 140) & (G_ < 140)
ys, xs = np.where(dark)
if len(ys):
    print("  dark ink bbox: x", 265 + xs.min(), "..", 265 + xs.max(), " y", 400 + ys.min(), "..", 400 + ys.max(), "n=", len(ys))
# grid
def classify(px):
    R, G, B = int(px[0]), int(px[1]), int(px[2])
    if R < 120 and G < 120 and B < 120: return "#"
    if R > 140 and R - G > 60 and R - B > 40: return "R"
    if G > 150 and G - R > 20 and G - B > 30: return "G"
    if B > R + 25 and B > G + 15: return "b"
    if R > 170 and B > 150 and G < min(R, B) - 15: return "P"
    if R > 150 and G > 150 and B < 120: return "o"  # olive/yellow-green
    if R > 225 and G > 195 and B > 165: return "."
    return "?"
print("  query grid (x 265..345 step 2, y 400..470 step 2):")
for y in range(400, 471, 2):
    print(f"  {y:3d} " + "".join(classify(f8[y, x]) for x in range(265, 346, 2)))

print("\n== q2 label ink: darkest pixels in x 275..320, y 383..412 ==")
sub = f8[383:412, 275:320]
dk = sub.sum(axis=2)
ys, xs = np.where(dk < 420)
pts = sorted(zip(ys, xs))[:40]
if pts:
    print("  darkest:", [(275 + x, 383 + y, tuple(f8[383 + y, 275 + x])) for y, x in pts[:12]])
    print("  ink bbox: x", 275 + xs.min(), "..", 275 + xs.max(), " y", 383 + ys.min(), "..", 383 + ys.max(), "n=", len(ys))

print("\n== Y label color sample ==")
print("  @(577,128):", tuple(f8[128, 577]), " @(578,130):", tuple(f8[130, 578]), " @(576,126):", tuple(f8[126, 576]))
print("  strip cells mode:", mode(120, 138, 548, 610, f8))

print("\n== circle (C,t) solve: blends over 3 backgrounds ==")
# over peach (background F7E2CD): sample clean arc areas
peach_pts = [(262, 400), (262, 415), (350, 400), (350, 415), (300, 378)]
# over DP fill (DCCBBB): circle covers DP bottom y 374..384 x 265..346
dp_pts = [(285, 380), (300, 380), (320, 380)]
# over container green (E7FFE9): circle bottom over sentence row? sentence top f8~452; x 254..358
gr_pts = [(300, 460), (300, 465), (330, 460)]
for nm, pts, bg in [("peach", peach_pts, (247, 226, 205)), ("dp", dp_pts, (220, 203, 187)), ("green", gr_pts, (231, 255, 233))]:
    print(f"  {nm}: samples {[tuple(f8[y, x]) for x, y in pts]} bg={bg}")

# least squares solve for C and t per channel using peach & dp pairs
import itertools
blends = {"peach": np.array([181.0, 194.0, 202.0]), "dp": None, "green": None}
dp_samples = [f8[y, x] for x, y in dp_pts]
gr_samples = [f8[y, x] for x, y in gr_pts]
print("  dp blend mean:", np.mean(dp_samples, axis=0).round(1), " green blend mean:", np.mean(gr_samples, axis=0).round(1))
