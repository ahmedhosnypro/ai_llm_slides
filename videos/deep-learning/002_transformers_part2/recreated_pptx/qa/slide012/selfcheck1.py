#!/usr/bin/env python3
# selfcheck1.py — closed-loop verify: render_1.png (150dpi) vs slide_012.jpg (frame).
# render px = frame px * 150/72 (2.0833). Tolerance ~4 frame px = ~8.3 render px.
from PIL import Image
import numpy as np

REN = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide012/render_1.png'
ORG = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_012.jpg'
S = 150 / 72.0

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

def cmp(name, kind, bx0, bx1, by0, by1, tol=8.3):
    # box given in FRAME px; compare ink bboxes render-vs-org (mapped to frame px)
    o = ink_bbox(org, bx0, bx1, by0, by1, kind)
    R0 = (bx0 * S, bx1 * S, by0 * S, by1 * S)
    rr = ink_bbox(ren, *R0, kind)
    if o is None or rr is None:
        print(f"{name}: MISSING ink (org={o is not None}, ren={rr is not None})")
        return
    d = [abs(rr[0] / S - o[0]), abs(rr[1] / S - o[1]), abs(rr[2] / S - o[2]), abs(rr[3] / S - o[3])]
    ok = max(d) <= tol
    print(f"{name}: {'OK ' if ok else 'DIFF'} max|d|={max(d):.1f}fp  (L{d[0]:.1f} R{d[1]:.1f} T{d[2]:.1f} B{d[3]:.1f})  org=({o[0]},{o[2]})-({o[1]},{o[3]})")

print("=== closed-loop render-vs-frame (frame px units) ===")
cmp("title", 'red', 100, 845, 50, 79)
cmp("subtitle", 'blue', 100, 845, 79, 100)
cmp("embed-label1", 'red', 100, 245, 122, 139)
cmp("embed-label2+X2", 'ink', 100, 245, 139, 158)
cmp("embed-box(red rims)", 'red', 100, 240, 158, 195)
cmp("tall-brace-L", 'red', 235, 258, 150, 340)
cmp("tall-brace-R", 'red', 710, 735, 148, 342)
cmp("panel1(cells)", 'ink', 247, 392, 170, 335)
cmp("panel2(cells)", 'ink', 413, 558, 170, 335)
cmp("panel3(cells)", 'ink', 572, 719, 170, 335)
cmp("header1", 'red', 240, 400, 133, 156)
cmp("header2", 'red', 405, 565, 133, 156)
cmp("header3", 'red', 566, 730, 133, 156)
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

print("\n=== color spot checks (render vs org, medians) ===")
def med(a, x0, x1, y0, y1):
    z = a[int(y0):int(y1), int(x0):int(x1)].reshape(-1, 3)
    return tuple(int(v) for v in np.median(z, axis=0))
for nm, fx0, fx1, fy0, fy1 in [("H1 fill", 300, 340, 195, 210), ("H2 fill", 470, 510, 195, 210),
                               ("H3 fill", 630, 670, 195, 210), ("pink box", 108, 118, 165, 172),
                               ("strip1 fill", 288, 292, 358, 382), ("canvas", 400, 430, 340, 350),
                               ("panel-gap gray", 800, 830, 300, 320)]:
    print(f"{nm}: org {med(org, fx0, fx1, fy0, fy1)}  ren {med(ren, fx0*S, fx1*S, fy0*S, fy1*S)}")
