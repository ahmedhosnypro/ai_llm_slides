#!/usr/bin/env python3
"""slide033 selfcheck: closed-loop render-vs-original comparison (slide-pt space).
Render: 2001x1125 @150dpi -> slide_pt = px*72/150 = px*0.48.
Original: frame px -> slide via MAPX/MAPY."""
import numpy as np
from PIL import Image
from scipy import ndimage

REN = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide033/render_1.png"
FR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_033.jpg"

ra = np.asarray(Image.open(REN).convert("RGB")).astype(int)
fa = np.asarray(Image.open(FR).convert("RGB")).astype(int)
RPT = 72 / 150.0          # render px -> slide pt
MAPX = lambda fx: (fx - 18.63) / 0.96123
MAPY = lambda fy: fy / 0.95556

def bands_in(a, x0, x1, y0, y1, kind, gap, min_area, conv_x, conv_y, scale=1):
    sub = a[y0:y1 + 1, x0:x1 + 1]
    r, g, b = sub[..., 0], sub[..., 1], sub[..., 2]
    if kind == "red": m = (r > 130) & (g < 95) & (b < 95)
    elif kind == "navy": m = (b > 100) & (r < 100) & (b - r > 40) & (g < 120)
    elif kind == "dark": m = (r < 120) & (g < 120) & (b < 120)
    elif kind == "blue": m = (b > 110) & (r < 100) & (b - r > 50)
    elif kind == "purple": m = (r > 80) & (r < 170) & (b > 110) & (b < 200) & (g < 90)
    elif kind == "green": m = (g > 100) & (g < 190) & (r < 110) & (b < 120) & (g - r > 40)
    elif kind == "orange": m = (r > 170) & (g > 70) & (g < 175) & (b < 120) & (r - b > 70)
    elif kind == "any": m = sub.mean(axis=2) < 185
    lab, n = ndimage.label(m, structure=np.ones((3, 3)))
    boxes = []
    for i in range(1, n + 1):
        ys, xs = np.where(lab == i)
        if len(ys) < min_area: continue
        boxes.append([int(xs.min()) + x0, int(ys.min()) + y0, int(xs.max()) + x0, int(ys.max()) + y0])
    boxes.sort(key=lambda t: (t[1], t[0]))
    out, cur = [], None
    for t in boxes:
        if cur is None or t[1] - cur[3] > gap:
            if cur: out.append(cur)
            cur = [t[0], t[1], t[2], t[3]]
        else:
            cur[0] = min(cur[0], t[0]); cur[1] = min(cur[1], t[1])
            cur[2] = max(cur[2], t[2]); cur[3] = max(cur[3], t[3])
    if cur: out.append(cur)
    res = []
    for bd in out:
        sx0, sx1 = conv_x(bd[0]) * scale, conv_x(bd[2]) * scale
        sy0, sy1 = conv_y(bd[1]) * scale, conv_y(bd[3]) * scale
        res.append((round(sx0, 1), round(sx1, 1), round(sy0, 1), round(sy1, 1)))
    return res

def cmp(label, ren, orig, tol=4.0):
    d = max(max(abs(a - b) for a, b in zip(rn, og)) for rn, og in zip(ren, orig)) if (ren and orig) else 999
    flag = "OK " if d <= tol else "DIFF"
    print(f"[{flag}] {label:34s} d={d:5.1f}")
    for rn, og in zip(ren, orig):
        print(f"      ren {rn}  vs orig {og}")
    if len(ren) != len(orig):
        print(f"      COUNT MISMATCH ren={len(ren)} orig={len(orig)}")
    return d

print("== TITLE / SUBTITLE ==")
cmp("title", bands_in(ra, 300, 750, 40, 110, "red", 4, 4, lambda p: p * RPT, lambda p: p * RPT, 1),
              bands_in(fa, 320, 620, 44, 68, "red", 4, 4, MAPX, MAPY))
cmp("subtitle", bands_in(ra, 60, 850, 68, 120, "navy", 5, 6, lambda p: p * RPT, lambda p: p * RPT, 1),
              bands_in(fa, 140, 810, 69, 95, "navy", 5, 6, MAPX, MAPY))

print("== DEFS BOX LINES (red+navy+blue+purple+green merged bands) ==")
def allbands_def(a, conv_x, conv_y, X0, X1, Y0, Y1):
    subs = a[Y0:Y1 + 1, X0:X1 + 1]
    r, g, b = subs[..., 0], subs[..., 1], subs[..., 2]
    m = ((r > 130) & (g < 95) & (b < 95)) | ((b > 100) & (r < 100) & (b - r > 40)) | ((r < 120) & (g < 120) & (b < 120)) | ((r > 80) & (r < 170) & (b > 110) & (b < 200) & (g < 90)) | ((g > 100) & (g < 190) & (r < 110) & (b < 120) & (g - r > 40))
    lab, n = ndimage.label(m, structure=np.ones((3, 3)))
    boxes = []
    for i in range(1, n + 1):
        ys, xs = np.where(lab == i)
        if len(ys) < 6: continue
        boxes.append([int(xs.min()) + X0, int(ys.min()) + Y0, int(xs.max()) + X0, int(ys.max()) + Y0])
    boxes.sort(key=lambda t: (t[1], t[0]))
    out, cur = [], None
    for t in boxes:
        if cur is None or t[1] - cur[3] > 5:
            if cur: out.append(cur)
            cur = [t[0], t[1], t[2], t[3]]
        else:
            cur[0] = min(cur[0], t[0]); cur[1] = min(cur[1], t[1])
            cur[2] = max(cur[2], t[2]); cur[3] = max(cur[3], t[3])
    if cur: out.append(cur)
    return [(round(conv_x(b[0]), 1), round(conv_x(b[2]), 1), round(conv_y(b[1]), 1), round(conv_y(b[3]), 1)) for b in out]

cmp("defs lines", allbands_def(ra, lambda p: p * RPT, lambda p: p * RPT, 880, 1490, 205, 610),
                 allbands_def(fa, MAPX, MAPY, 432, 758, 104, 286))

print("== EXAMPLE BOX LINES ==")
cmp("example lines", allbands_def(ra, lambda p: p * RPT, lambda p: p * RPT, 1600, 1870, 205, 610),
                    allbands_def(fa, MAPX, MAPY, 780, 885, 104, 290))

print("== OMEGA BOX LINES (navy body) ==")
cmp("omega lines", bands_in(ra, 950, 1800, 640, 1090, "navy", 5, 6, lambda p: p * RPT, lambda p: p * RPT, 1),
                  bands_in(fa, 478, 878, 302, 510, "navy", 5, 6, MAPX, MAPY))

print("== INFO BOX LINES (dark) ==")
cmp("info lines", bands_in(ra, 90, 440, 480, 700, "dark", 5, 6, lambda p: p * RPT, lambda p: p * RPT, 1),
                 bands_in(fa, 70, 208, 228, 318, "dark", 5, 6, MAPX, MAPY))

print("== VECTOR VALUES (dark) ==")
cmp("vec values", bands_in(ra, 420, 560, 250, 1090, "dark", 5, 4, lambda p: p * RPT, lambda p: p * RPT, 1),
                 bands_in(fa, 220, 258, 126, 510, "dark", 5, 4, MAPX, MAPY))

print("== INDEX VALUES (red) ==")
cmp("index values", bands_in(ra, 540, 660, 250, 1120, "red", 6, 2, lambda p: p * RPT, lambda p: p * RPT, 1),
                   bands_in(fa, 270, 308, 124, 514, "red", 6, 2, MAPX, MAPY))

print("== PAIR LINES (any dark-ish in pair col) ==")
cmp("pair lines", bands_in(ra, 660, 850, 250, 1130, "any", 6, 8, lambda p: p * RPT, lambda p: p * RPT, 1),
                 bands_in(fa, 320, 404, 126, 512, "any", 6, 8, MAPX, MAPY))

print("== EQUATION INTERNALS ==")
print(" render:")
for k in ["red", "navy", "dark"]:
    for bd in bands_in(ra, 1490, 1830, 740, 880, k, 4, 3, lambda p: p * RPT, lambda p: p * RPT, 1):
        print(f"   {k:5s} {bd}")
print(" original:")
for k in ["red", "navy", "dark"]:
    for bd in bands_in(fa, 712, 862, 349, 392, k, 4, 3, MAPX, MAPY):
        print(f"   {k:5s} {bd}")

print("== GENERAL PAIR TEXT ==")
cmp("paircard", bands_in(ra, 150, 360, 270, 470, "red", 8, 8, lambda p: p * RPT, lambda p: p * RPT, 1),
               bands_in(fa, 104, 172, 132, 208, "red", 8, 8, MAPX, MAPY))

print("== FILLS (median sample) ==")
def fill(a, sx, sy, conv, half=6):
    cx, cy = conv
    px = a[int(cy(sy)):int(cy(sy)) + half, int(cx(sx)):int(cx(sx)) + half]
    return tuple(int(v) for v in np.median(px.reshape(-1, 3), axis=0))
cxr = lambda x: x / RPT; cyr = lambda y: y / RPT
cxf = lambda x: 18.63 + 0.96123 * x; cyf = lambda y: 0.95556 * y
for name, sx, sy in [("defs", 600, 200), ("example", 850, 200), ("omega", 600, 470),
                     ("eqbox", 800, 390), ("info", 125, 300), ("card", 120, 200),
                     ("vec-g", 227, 150), ("vec-t", 227, 230), ("pair-g", 359, 150),
                     ("pair-t", 359, 230), ("index", 275, 200)]:
    print(f"  {name:8s} ren {fill(ra, sx, sy, (cxr, cyr))}  orig {fill(fa, sx, sy, (cxf, cyf))}")
