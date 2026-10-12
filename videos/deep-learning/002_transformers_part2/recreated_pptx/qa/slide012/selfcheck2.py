#!/usr/bin/env python3
# selfcheck2.py — corrected closed-loop: compare render ink bboxes (slide px = render_px/S)
# against ORIGINAL ink bboxes mapped frame->slide (sx=(fx-17.628)/0.961232, sy=fy/0.955556).
# Units are consistent slide px. Usage: selfcheck2.py <render.png> [tag]
import sys
from PIL import Image
import numpy as np

S = 150 / 72.0
VID = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2'
ORG = VID + '/unique_slides/slide_012.jpg'
REN = sys.argv[1] if len(sys.argv) > 1 else VID + '/recreated_pptx/qa/slide012/render_1.png'

ren = np.asarray(Image.open(REN).convert('RGB')).astype(int)
org = np.asarray(Image.open(ORG).convert('RGB')).astype(int)
print(f"render {ren.shape[1]}x{ren.shape[0]}  org {org.shape[1]}x{org.shape[0]}")

def ink_bbox(a, x0, x1, y0, y1, kind):
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    if kind == 'red':   m = (r - np.maximum(g, b) > 45) & (r > 120)
    elif kind == 'blue':m = (b - r > 40) & (b > 110)
    elif kind == 'ink': m = (a.max(axis=2) - a.min(axis=2) > 60) | (a.max(axis=2) < 140)
    sub = m[int(y0):int(y1), int(x0):int(x1)]
    ys, xs = np.where(sub)
    if len(ys) == 0: return None
    return (xs.min() + x0, xs.max() + x0, ys.min() + y0, ys.max() + y0)

def f2s(v):  # frame px -> slide px (pair)
    return ((v[0] - 17.628) / 0.961232, (v[1] - 17.628) / 0.961232,
            v[2] / 0.955556, v[3] / 0.955556)

def cmp(name, kind, bx0, bx1, by0, by1, tol=6.0):
    # windows given in FRAME px; render window = frame ->slide px -> render px
    o = ink_bbox(org, bx0, bx1, by0, by1, kind)
    wx0 = (bx0 - 17.628) / 0.961232 * S
    wx1 = (bx1 - 17.628) / 0.961232 * S
    wy0 = by0 / 0.955556 * S
    wy1 = by1 / 0.955556 * S
    rr = ink_bbox(ren, wx0, wx1, wy0, wy1, kind)
    if o is None or rr is None:
        print(f"{name}: MISSING ink (org={o is not None}, ren={rr is not None})")
        return
    osx = f2s(o)  # slide px
    R = (rr[0] / S, rr[1] / S, rr[2] / S, rr[3] / S)  # slide px
    d = [abs(R[i] - osx[i]) for i in range(4)]
    ok = max(d) <= tol
    print(f"{name}: {'OK ' if ok else 'DIFF'} max|d|={max(d):.1f}sx  "
          f"(L{d[0]:.1f} R{d[1]:.1f} T{d[2]:.1f} B{d[3]:.1f})  "
          f"org=({osx[0]:.0f},{osx[2]:.0f})-({osx[1]:.0f},{osx[3]:.0f}) sx  "
          f"ren=({R[0]:.0f},{R[2]:.0f})-({R[1]:.0f},{R[3]:.0f}) sx")

print("=== closed-loop slide-px units (tol 6 sx ~ 4.6 render px) ===")
cmp("title", 'red', 130, 850, 48, 80)
cmp("subtitle", 'blue', 85, 855, 79, 100)
cmp("embed-label1", 'red', 100, 245, 122, 139)
cmp("embed-label2+X2", 'ink', 100, 245, 139, 158)
cmp("embed-box(rims)", 'red', 100, 240, 158, 195)
cmp("tall-brace-L", 'red', 235, 258, 150, 340)
cmp("tall-brace-R", 'red', 710, 735, 148, 342)
cmp("panel1-cells", 'ink', 247, 392, 170, 335)
cmp("panel2-cells", 'ink', 413, 558, 170, 335)
cmp("panel3-cells", 'ink', 572, 719, 170, 335)
cmp("header2", 'red', 405, 565, 133, 156)
cmp("equals", 'red', 185, 240, 345, 395)
cmp("short-brace-L", 'red', 235, 258, 345, 395)
cmp("short-brace-R", 'red', 712, 736, 345, 395)
cmp("strip1-yboxes", 'ink', 250, 395, 352, 390)
cmp("strip2-yboxes", 'ink', 412, 560, 352, 390)
cmp("strip3-yboxes", 'ink', 575, 722, 352, 390)
cmp("caption1", 'red', 250, 395, 388, 416)
cmp("caption2", 'red', 412, 560, 388, 416)
cmp("caption3", 'red', 575, 722, 388, 416)
cmp("result1", 'ink', 300, 345, 418, 448)
cmp("result2", 'ink', 475, 520, 418, 448)
cmp("result3", 'ink', 645, 690, 418, 448)
cmp("magenta", 'ink', 500, 560, 262, 320)
