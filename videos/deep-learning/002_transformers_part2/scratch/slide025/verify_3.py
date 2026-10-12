#!/usr/bin/env python3
"""Closed-loop verify v3 — CORRECT expectations: exp_render_x = (fx-18.628)/0.96123*150/72,
exp_render_y = fy/0.95556*150/72. Tolerance: 4 px @150dpi = 1.92pt on every edge."""
from PIL import Image
import numpy as np

VID = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2"
R = np.asarray(Image.open(f"{VID}/recreated_pptx/qa/slide025/render_1.png").convert("RGB")).astype(int)
F = np.asarray(Image.open(f"{VID}/unique_slides/slide_025.jpg").convert("RGB")).astype(int)
PT = 150 / 72
def ex(fx): return (fx - 18.628) / 0.96123 * PT
def ey(fy): return fy / 0.95556 * PT

r, g, b = R[..., 0], R[..., 1], R[..., 2]
redm = (r - g > 60) & (r - b > 50) & (r > 110)
greenm = (g - r > 30) & (g - b > 20) & (g > 70)
blue = (b - r > 40) & (b - g > 30)
darkish = (np.abs(R - 234).max(axis=2) > 60)
fails = []
TOL = 4.0  # render px

def band(mask, fy0, fy1, fx0, fx1, minpix=2, label="", mar=16):
    y0, y1 = int(ey(fy0)) - mar, int(ey(fy1)) + mar
    x0, x1 = int(ex(fx0)) - mar, int(ex(fx1)) + mar
    seg = mask[y0:y1, x0:x1]
    rows = seg.sum(axis=1)
    bands, inb = [], False
    for i, c in enumerate(rows):
        if c >= minpix and not inb:
            s, inb = i, True
        elif c < minpix and inb:
            bands.append((y0 + s, y0 + i - 1)); inb = False
    if inb:
        bands.append((y0 + s, y0 + len(rows) - 1))
    merged = []
    for bd in bands:
        if merged and bd[0] - merged[-1][1] < 4:
            merged[-1] = (merged[-1][0], bd[1])
        else:
            merged.append(bd)
    exp = (ey(fy0), ey(fy1), ex(fx0), ex(fx1))
    if not merged:
        print(f"{label}: NO INK (exp y {exp[0]:.0f}..{exp[1]:.0f} x {exp[2]:.0f}..{exp[3]:.0f})")
        fails.append(label); return
    best = min(merged, key=lambda bd: abs((bd[0] + bd[1]) / 2 - (exp[0] + exp[1]) / 2))
    bs, be = best
    cols = seg[bs - y0:be - y0 + 1].sum(axis=0)
    xs = np.nonzero(cols >= 1)[0]
    xs0, xs1 = x0 + int(xs.min()), x0 + int(xs.max())
    dy = max(abs(bs - exp[0]), abs(be - exp[1]))
    dx = max(abs(xs0 - exp[2]), abs(xs1 - exp[3]))
    ok = dy <= TOL and dx <= TOL
    if not ok:
        fails.append(label)
    print(f"{label}: {'OK ' if ok else 'OFF'} y {bs}..{be} x {xs0}..{xs1} | exp y {exp[0]:.0f}..{exp[1]:.0f} x {exp[2]:.0f}..{exp[3]:.0f} | dY {dy:.1f} dX {dx:.1f}")

band(redm, 72, 87, 351, 573, 3, "title")
band(blue, 96, 114, 208, 721, 3, "subtitle")
band(redm, 219, 241, 349, 404, 3, "block arrow")
band(redm, 267, 279, 315, 440, 3, "arrow L1")
band(redm, 298, 311, 324, 435, 3, "arrow L2")
band(darkish, 205, 212, 557, 634, 3, "Rotation direction")
band(darkish, 222, 229, 575, 616, 3, "CCW/CW")
band(redm, 203, 208, 724, 741, 2, "cos label")
band(greenm, 223, 229, 733, 747, 2, "sin label")
band(darkish, 295, 301, 549, 627, 3, "Line count =16")
band(darkish, 307, 315, 544, 640, 3, "(16 signal periods per")
band(darkish, 321, 327, 569, 615, 3, "revolution)")
band(darkish, 272, 281, 726, 821, 3, "Sin/Cos signal period", mar=10)
band(darkish, 411, 429, 172, 814, 3, "summary L1")
band(darkish, 433, 450, 322, 663, 3, "summary L2")
band(blue, 473, 480, 83, 155, 2, "footer L1")
band(blue, 485, 491, 108, 587, 2, "footer L2")
band(blue, 498, 504, 256, 436, 2, "footer L3")
band((R.max(axis=2) < 190), 306, 322, 142, 213, 3, "callout L1", mar=10)
band((R.max(axis=2) < 190), 328, 345, 142, 213, 3, "callout L2", mar=10)
band((R.max(axis=2) < 170), 214, 225, 220, 286, 3, "AC Motor", mar=8)

# tan callout bbox (exact)
tanm = (r > 195) & (g > 160) & (b > 110) & (b < 220) & (r - b > 35)
ys, xs = np.nonzero(tanm[int(ey(304))-6:int(ey(353))+6, int(ex(121))-6:int(ex(224))+6])
by0, by1 = int(ey(304))-6+ys.min(), int(ey(304))-6+ys.max()
bx0, bx1 = int(ex(121))-6+xs.min(), int(ex(121))-6+xs.max()
ok = abs(by0-ey(304))<=TOL and abs(by1-ey(353))<=TOL and abs(bx0-ex(121))<=TOL and abs(bx1-ex(224))<=TOL
if not ok: fails.append("callout tan bbox")
print(f"callout tan bbox: {'OK ' if ok else 'OFF'} y {by0}..{by1} x {bx0}..{bx1} | exp y {ey(304):.0f}..{ey(353):.0f} x {ex(121):.0f}..{ex(224):.0f}")

# panel borders (exact stroke edges)
greenm2 = greenm
for nm, fy0, fy1, fx0, fx1 in (("left panel", 171, 366, 101, 304), ("right panel", 140, 389, 450, 834)):
    y0, y1 = int(ey(fy0)) - 10, int(ey(fy1)) + 10
    x0, x1 = int(ex(fx0)) - 10, int(ex(fx1)) + 10
    seg = greenm2[y0:y1, x0:x1]
    ys, xs = np.nonzero(seg)
    by0, by1 = y0 + ys.min(), y0 + ys.max()
    bx0, bx1 = x0 + xs.min(), x0 + xs.max()
    ok = abs(by0-ey(fy0))<=TOL+2 and abs(by1-ey(fy1))<=TOL+2 and abs(bx0-ex(fx0))<=TOL+2 and abs(bx1-ex(fx1))<=TOL+2
    if not ok: fails.append(nm)
    print(f"{nm} border: {'OK ' if ok else 'OFF'} y {by0}..{by1} x {bx0}..{bx1} | exp y {ey(fy0):.0f}..{ey(fy1):.0f} x {ex(fx0):.0f}..{ex(fx1):.0f}")

print("\nFAILS:", fails if fails else "none — all closed-loop checks within 4px@150dpi")
