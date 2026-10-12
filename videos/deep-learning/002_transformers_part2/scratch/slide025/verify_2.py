#!/usr/bin/env python3
"""Closed-loop verify v2 (corrected): render vs frame. exp_render_px = frame_px * K
(KX=2.1674, KY=2.1802). Wide windows (+-22px). Images checked via composite-at-position."""
from PIL import Image
import numpy as np

VID = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2"
R = np.asarray(Image.open(f"{VID}/recreated_pptx/qa/slide025/render_1.png").convert("RGB")).astype(int)
F = np.asarray(Image.open(f"{VID}/unique_slides/slide_025.jpg").convert("RGB")).astype(int)
KX, KY = (150 / 72) / 0.96123, (150 / 72) / 0.95556
r, g, b = R[..., 0], R[..., 1], R[..., 2]
redm = (r - g > 60) & (r - b > 50) & (r > 110)
greenm = (g - r > 30) & (g - b > 20) & (g > 70)
blue = (b - r > 40) & (b - g > 30)
darkish = (np.abs(R - 234).max(axis=2) > 60)
fails = []

def band(mask, fy0, fy1, fx0, fx1, minpix=2, label="", mar=22):
    y0, y1 = int(fy0 * KY) - mar, int(fy1 * KY) + mar
    x0, x1 = int(fx0 * KX) - mar, int(fx1 * KX) + mar
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
    # merge bands separated by <4px (JPEG-free render should be one band per line)
    merged = []
    for bd in bands:
        if merged and bd[0] - merged[-1][1] < 4:
            merged[-1] = (merged[-1][0], bd[1])
        else:
            merged.append(list(bd) if isinstance(bd, tuple) else bd)
            merged[-1] = tuple(merged[-1])
    exp = (fy0 * KY, fy1 * KY, fx0 * KX, fx1 * KX)
    if not merged:
        print(f"{label}: NO INK (exp y {exp[0]:.0f}..{exp[1]:.0f} x {exp[2]:.0f}..{exp[3]:.0f})")
        fails.append(label)
        return
    # pick the band closest in y-center to expectation
    best = min(merged, key=lambda bd: abs((bd[0] + bd[1]) / 2 - (exp[0] + exp[1]) / 2))
    bs, be = best
    cols = seg[bs - y0:be - y0 + 1].sum(axis=0)
    xs = np.nonzero(cols >= 1)[0]
    xs0, xs1 = x0 + xs.min(), x0 + xs.max()
    dy = max(abs(bs - exp[0]), abs(be - exp[1])) / 2.18  # in frame px
    dxl, dxr = (xs0 - exp[2]) / 2.17, (xs1 - exp[3]) / 2.17
    ok = abs(dy) <= 2.0 and abs(dxl) <= 2.0 and abs(dxr) <= 2.0
    if not ok:
        fails.append(label)
    print(f"{label}: {'OK ' if ok else 'OFF'} render y {bs}..{be} x {xs0}..{xs1} | exp y {exp[0]:.0f}..{exp[1]:.0f} x {exp[2]:.0f}..{exp[3]:.0f} | dY {dy:+.1f} dL {dxl:+.1f} dR {dxr:+.1f} (frame px)")

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
band(darkish, 272, 281, 726, 821, 3, "Sin/Cos signal period")
band(darkish, 411, 429, 172, 814, 3, "summary L1")
band(darkish, 433, 450, 322, 663, 3, "summary L2")
band(blue, 473, 480, 83, 155, 2, "footer L1")
band(blue, 485, 491, 108, 587, 2, "footer L2")
band(blue, 498, 504, 256, 436, 2, "footer L3")
# callout text: dark-on-tan in render (use <190 within callout zone); tan bbox check too
band((R.max(axis=2) < 190), 306, 322, 142, 213, 3, "callout L1")
band((R.max(axis=2) < 190), 328, 345, 142, 213, 3, "callout L2")
# AC Motor: dark text on white, window right of motor body top area
band((R.max(axis=2) < 170), 214, 225, 220, 286, 3, "AC Motor", mar=14)

# tan callout fill bbox in render vs expected
tanm = (r > 200) & (g > 165) & (g < 235) & (b > 120) & (b < 215) & (r - b > 40)
seg = tanm[int(295 * KY):int(365 * KY), int(110 * KX):int(240 * KX)]
ys, xs = np.nonzero(seg)
if len(xs):
    print(f"callout tan bbox: y {int(295*KY)+ys.min()}..{int(295*KY)+ys.max()} x {int(110*KX)+xs.min()}..{int(110*KX)+xs.max()} | exp y {295*KY:.0f}..{365*KY:.0f} x {110*KX:.0f}..{240*KX:.0f}")

# panel borders
for nm, fy0, fy1, fx0, fx1 in (("left panel", 171, 366, 101, 304), ("right panel", 140, 389, 450, 834)):
    y0, y1 = int(fy0 * KY) - 14, int(fy1 * KY) + 14
    x0, x1 = int(fx0 * KX) - 14, int(fx1 * KX) + 14
    seg = greenm[y0:y1, x0:x1]
    ys, xs = np.nonzero(seg)
    if len(xs):
        by0, by1 = y0 + ys.min(), y0 + ys.max()
        bx0, bx1 = x0 + xs.min(), x0 + xs.max()
        ok = abs(by0 - fy0 * KY) < 7 and abs(bx0 - fx0 * KX) < 7 and abs(bx1 - fx1 * KX) < 7 and abs(by1 - fy1 * KY) < 7
        if not ok:
            fails.append(nm)
        print(f"{nm} border: {'OK ' if ok else 'OFF'} render y {by0}..{by1} x {bx0}..{bx1} | exp y {fy0*KY:.0f}..{fy1*KY:.0f} x {fx0*KX:.0f}..{fx1*KX:.0f}")

# images via composite-at-intended-position
def img_check(name, png, fy0, fy1, fx0, fx1, chan):
    px0, px1 = fx2pt(fx0) * 150 / 72, fx2pt(fx1) * 150 / 72
    py0, py1 = fy2pt(fy0) * 150 / 72, fy2pt(fy1) * 150 / 72
    img = Image.open(png).convert("RGBA")
    tgt = img.resize((max(1, int(round(px1 - px0))), max(1, int(round(py1 - py0)))), Image.LANCZOS)
    canvas = Image.new("RGB", (2001, 1125), (234, 234, 234))
    canvas.paste(tgt, (int(round(px0)), int(round(py0))), tgt)
    C = np.asarray(canvas).astype(int)
    cr, cg, cb = C[..., 0], C[..., 1], C[..., 2]
    if chan == "red":
        cm = (cr - cg > 60) & (cr - cb > 50) & (cr > 110)
    else:
        cm = (cg - cr > 30) & (cg - cb > 20) & (cg > 70)
    x0, x1, y0, y1 = int(px0), int(px1), int(py0), int(py1)
    A = cm[y0:y1, x0:x1]
    B = (redm if chan == "red" else greenm)[y0:y1, x0:x1]
    if chan == "red":
        cz = max(0, int(718 * KX) - x0)
        cut = max(0, int(233 * KY) - y0)
        A[:cut, cz:] = False; B[:cut, cz:] = False
    inter = (A & B).sum(); union = A.sum() + B.sum() - inter
    ok = inter / max(union, 1) > 0.35
    if not ok:
        fails.append(name)
    print(f"{name}: composite-vs-render IoU {inter/max(union,1):.3f} (comp {A.sum()} render {B.sum()})")

def fx2pt(fx): return (fx - 18.628) / 0.96123
def fy2pt(fy): return fy / 0.95556

img_check("ring red", f"{VID}/recreated_pptx/build/assets/s025_ring.png", 147, 385, 477, 733, "red")
img_check("ring green", f"{VID}/recreated_pptx/build/assets/s025_ring.png", 147, 385, 477, 733, "green")

# motor: grayscale ink IoU via composite
png = f"{VID}/recreated_pptx/build/assets/s025_motor.png"
px0, px1 = fx2pt(103) * 150 / 72, fx2pt(301) * 150 / 72
py0, py1 = fy2pt(174) * 150 / 72, fy2pt(301) * 150 / 72
img = Image.open(png).convert("RGBA")
tgt = img.resize((int(round(px1 - px0)), int(round(py1 - py0))), Image.LANCZOS)
canvas = Image.new("RGB", (2001, 1125), (255, 255, 255))
canvas.paste(tgt, (int(round(px0)), int(round(py0))), tgt)
C = np.asarray(canvas).astype(int)
cink = (np.abs(C - 255).max(axis=2) > 60)
rink = (np.abs(R - 255).max(axis=2) > 60)
x0, x1, y0, y1 = int(px0), int(px1), int(py0), int(py1)
A = cink[y0:y1, x0:x1]; B = rink[y0:y1, x0:x1]
inter = (A & B).sum(); union = A.sum() + B.sum() - inter
ok = inter / max(union, 1) > 0.5
if not ok:
    fails.append("motor")
print(f"motor: composite-vs-render ink IoU {inter/max(union,1):.3f} (comp {A.sum()} render {B.sum()})")

print("\nFAILS:", fails if fails else "none")
