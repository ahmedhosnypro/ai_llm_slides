#!/usr/bin/env python3
"""Closed-loop verify attempt 1: render_1.png (150dpi, 2001x1125) vs slide_025.jpg frame.
render_px = frame_px * (150/72)/scale  (x: /0.96123, y: /0.95556). Tolerance ~4 render px."""
from PIL import Image
import numpy as np

R = np.asarray(Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide025/render_1.png").convert("RGB")).astype(int)
F = np.asarray(Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_025.jpg").convert("RGB")).astype(int)
KX = (150 / 72) / 0.96123
KY = (150 / 72) / 0.95556
print(f"render {R.shape}, KX={KX:.4f} KY={KY:.4f}")

r, g, b = R[..., 0], R[..., 1], R[..., 2]
redm = (r - g > 60) & (r - b > 50) & (r > 110)
greenm = (g - r > 30) & (g - b > 20) & (g > 70)
blue = (b - r > 40) & (b - g > 30)
darkish = (np.abs(R - 234).max(axis=2) > 60)

def band(mask, fy0, fy1, fx0, fx1, minpix=2, label=""):
    """Find the ink band(s) of an element in the render, given its frame-px window."""
    y0, y1 = int(fy0 * KY) - 8, int(fy1 * KY) + 8
    x0, x1 = int(fx0 * KX) - 8, int(fx1 * KX) + 8
    seg = mask[y0:y1, x0:x1]
    rows = seg.sum(axis=1)
    bands = []
    inb = False
    for i, c in enumerate(rows):
        if c >= minpix and not inb:
            s, inb = i, True
        elif c < minpix and inb:
            bands.append((y0 + s, y0 + i - 1)); inb = False
    if inb:
        bands.append((y0 + s, y0 + len(rows) - 1))
    out = []
    for (bs, be) in bands:
        cols = seg[bs - y0:be - y0 + 1].sum(axis=0)
        xs = np.nonzero(cols >= 1)[0]
        out.append((bs, be, x0 + int(xs.min()), x0 + int(xs.max())))
    exp = (fy0 * KY, fy1 * KY, fx0 * KX, fx1 * KX)
    if not out:
        print(f"{label}: NO INK  (expected band y {exp[0]:.0f}..{exp[1]:.0f} x {exp[2]:.0f}..{exp[3]:.0f})")
    else:
        for (bs, be, xs0, xs1) in out:
            dy = max(abs(bs - exp[0]), abs(be - exp[1]))
            dx = max(abs(xs0 - exp[2]), abs(xs1 - exp[3]))
            flag = "OK " if (dy <= 4.5 and dx <= 4.5) else "OFF"
            print(f"{label}: {flag} render y {bs}..{be} x {xs0}..{xs1} vs exp y {exp[0]:.0f}..{exp[1]:.0f} x {exp[2]:.0f}..{exp[3]:.0f}  (dY {dy:.1f} dX {dx:.1f})")

# frame-measured ink windows per element
band(redm, 72, 87, 351, 573, 3, "title")
band(blue, 96, 114, 208, 721, 3, "subtitle")
band(darkish, 214, 225, 220, 286, 3, "AC Motor")
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
# callout text (dark on tan): dark mask within callout
band((R.max(axis=2) < 190), 306, 322, 142, 207, 3, "callout L1")
band((R.max(axis=2) < 190), 328, 345, 142, 213, 3, "callout L2")

# panel borders: green heavy rows/cols in render vs expected (frame 450/834/140/389; 101/304/171/366)
gm = greenm
for nm, fy0, fy1, fx0, fx1 in (("left panel", 171, 366, 101, 304), ("right panel", 140, 389, 450, 834)):
    y0, y1 = int(fy0 * KY) - 12, int(fy1 * KY) + 12
    x0, x1 = int(fx0 * KX) - 12, int(fx1 * KX) + 12
    seg = gm[y0:y1, x0:x1]
    ys, xs = np.nonzero(seg)
    if len(xs):
        print(f"{nm} green bbox: y {y0+ys.min()}..{y0+ys.max()} x {x0+xs.min()}..{x0+xs.max()} vs exp y {fy0*KY:.0f}..{fy1*KY:.0f} x {fx0*KX:.0f}..{fx1*KX:.0f}")
    else:
        print(f"{nm}: NO GREEN BORDER INK")

# ring: IoU of red/green in the right-panel region (render) vs frame region
def iou_region(nm, rmask, fmask, fy0, fy1, fx0, fx1):
    ry0, ry1 = int(fy0 * KY), int(fy1 * KY)
    rx0, rx1 = int(fx0 * KX), int(fx1 * KX)
    A = rmask[ry0:ry1, rx0:rx1]
    B = fmask[fy0:fy1, fx0:fx1]
    Aimg = np.asarray(Image.fromarray(A.astype(np.uint8) * 255).resize((fx1 - fx0, fy1 - fy0), Image.NEAREST)) > 127
    inter = (Aimg & B).sum()
    union = Aimg.sum() + B.sum() - inter
    print(f"ring {nm}: gen {(Aimg).sum()} orig {B.sum()} IoU {inter/max(union,1):.3f}")

fr, fg, fb = F[..., 0], F[..., 1], F[..., 2]
fred = (fr - fg > 60) & (fr - fb > 50) & (fr > 110)
fgreen = (fg - fr > 30) & (fg - fb > 20) & (fg > 70)
fred[199:233, 718:755] = False; fgreen[199:233, 718:755] = False
iou_region("red", redm, fred, 150, 385, 470, 740)
iou_region("green", greenm, fgreen, 150, 385, 470, 740)
# motor: ink in left panel (render) vs frame
inkr = (np.abs(R - 255).max(axis=2) > 45)
inkf = (np.abs(F - 255).max(axis=2) > 45)
A = inkr[int(174*KY):int(301*KY), int(103*KX):int(301*KX)]
B = inkf[174:301, 103:301]
Aimg = np.asarray(Image.fromarray(A.astype(np.uint8) * 255).resize((B.shape[1], B.shape[0]), Image.NEAREST)) > 127
inter = (Aimg & B).sum(); union = Aimg.sum() + B.sum() - inter
print(f"motor ink IoU: {inter/max(union,1):.3f} gen {Aimg.sum()} orig {B.sum()}")
