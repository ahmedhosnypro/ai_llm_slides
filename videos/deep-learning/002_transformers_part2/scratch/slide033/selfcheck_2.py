#!/usr/bin/env python3
"""slide033 selfcheck_2: clean re-probe of render_2 (border-free windows)."""
import numpy as np
from PIL import Image
import scipy.ndimage as ndi

ra = np.asarray(Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide033/render_4.png").convert("RGB")).astype(int)
fa = np.asarray(Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_033.jpg").convert("RGB")).astype(int)
RPT = 72 / 150.0
MAPX = lambda fx: (fx - 18.63) / 0.96123
MAPY = lambda fy: fy / 0.95556

navy = lambda r, g, b: (b > 100) & (r < 100) & (b - r > 40)
red = lambda r, g, b: (r > 130) & (g < 100) & (b < 100)
dark = lambda r, g, b: (r < 120) & (g < 120) & (b < 120)
green_t = lambda r, g, b: (r < 150) & (g > 120) & (g < 210) & (g - r > 40) & (g - b > 40)
orange_t = lambda r, g, b: (r > 170) & (g > 80) & (g < 175) & (b < 120) & (r - b > 70)
blue_t = lambda r, g, b: (b > 110) & (r < 100) & (b - r > 50)
purple_t = lambda r, g, b: (r > 80) & (r < 175) & (b > 110) & (b < 210) & (g < 95)

def rowbands(a, X0, X1, Y0, Y1, mask, convx, convy, gap=5, minpx=4, minarea=4):
    sub = a[Y0:Y1 + 1, X0:X1 + 1]
    m = mask(sub[..., 0], sub[..., 1], sub[..., 2])
    lab, n = ndi.label(m, structure=np.ones((3, 3)))
    boxes = []
    for i in range(1, n + 1):
        ys, xs = np.where(lab == i)
        if len(ys) < minarea: continue
        boxes.append([int(xs.min()) + X0, int(ys.min()) + Y0, int(xs.max()) + X0, int(ys.max()) + Y0])
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
    return [(round(convx(b[0]), 1), round(convx(b[2]), 1), round(convy(b[1]), 1), round(convy(b[3]), 1)) for b in out]

def show(label, ren, orig):
    print(f"--- {label} ---")
    for i in range(max(len(ren), len(orig))):
        r = ren[i] if i < len(ren) else None
        o = orig[i] if i < len(orig) else None
        d = max(abs(a - b) for a, b in zip(r, o)) if (r and o) else None
        print(f"  ren {r}  orig {o}  d={d}")

# render windows in slide pt -> px
R = lambda x0, x1, y0, y1: (int(x0 / RPT), int(x1 / RPT), int(y0 / RPT), int(y1 / RPT))
F = lambda x0, x1, y0, y1: (int(x0), int(x1), int(y0), int(y1))  # frame px windows from slide pt
fw = lambda x0, x1, y0, y1: (int(18.63 + 0.96123 * x0), int(18.63 + 0.96123 * x1), int(0.95556 * y0), int(0.95556 * y1))

print("=== SUBTITLE ===")
w = R(100, 850, 70, 100); x0, x1, y0, y1 = w
show("subtitle", rowbands(ra, x0, x1, y0, y1, navy, lambda p: p * RPT, lambda p: p * RPT),
              rowbands(fa, *fw(100, 850, 70, 100), navy, MAPX, MAPY))

print("=== DEFS LINES (merged colors, interior) ===")
def anymask(r, g, b):
    return (red(r, g, b) | navy(r, g, b) | dark(r, g, b) | green_t(r, g, b) | blue_t(r, g, b) | purple_t(r, g, b))
w = R(430, 768, 110, 299); x0, x1, y0, y1 = w
show("defs", rowbands(ra, x0, x1, y0, y1, anymask, lambda p: p * RPT, lambda p: p * RPT, gap=4, minarea=6),
             rowbands(fa, *fw(430, 768, 110, 299), anymask, MAPX, MAPY, gap=4, minarea=6))

print("=== EXAMPLE LINES (interior) ===")
w = R(792, 900, 110, 298); x0, x1, y0, y1 = w
show("example", rowbands(ra, x0, x1, y0, y1, anymask, lambda p: p * RPT, lambda p: p * RPT, gap=4, minarea=6),
               rowbands(fa, *fw(792, 900, 110, 298), anymask, MAPX, MAPY, gap=4, minarea=6))

print("=== OMEGA LINES (navy, x<888 to skip border) ===")
w = R(478, 888, 313, 532); x0, x1, y0, y1 = w
show("omega", rowbands(ra, x0, x1, y0, y1, navy, lambda p: p * RPT, lambda p: p * RPT, gap=5, minarea=8),
              rowbands(fa, *fw(478, 888, 313, 532), navy, MAPX, MAPY, gap=5, minarea=8))

print("=== INFO LINES (dark, interior) ===")
w = R(52, 199, 240, 334); x0, x1, y0, y1 = w
show("info", rowbands(ra, x0, x1, y0, y1, dark, lambda p: p * RPT, lambda p: p * RPT, gap=5, minarea=6),
             rowbands(fa, *fw(52, 199, 240, 334), dark, MAPX, MAPY, gap=5, minarea=6))

print("=== PAIR LINES (green/orange, interior windows) ===")
pw = [(136, 188, green_t), (208, 258, orange_t), (274, 329, green_t), (374, 428, orange_t), (475, 530, green_t)]
for i, (y0, y1, mk) in enumerate(pw, 1):
    w = R(320, 398, y0, y1); x0, x1, yy0, yy1 = w
    ren = rowbands(ra, x0, x1, yy0, yy1, mk, lambda p: p * RPT, lambda p: p * RPT, gap=6, minarea=10)
    w = fw(320, 398, y0, y1); x0, x1, yy0, yy1 = w
    orig = rowbands(fa, x0, x1, yy0, yy1, mk, MAPX, MAPY, gap=6, minarea=10)
    show(f"pair box {i}", ren, orig)

print("=== EQ INTERNALS ===")
for lab, y0, y1, x0, x1, mk in [("omega", 370, 398, 720, 762, red), ("K", 388, 402, 744, 766, navy),
                                 ("bars", 378, 394, 760, 783, navy), ("fracbar", 380, 392, 780, 870, navy),
                                 ("one", 360, 384, 808, 832, dark), ("10000", 392, 416, 778, 845, dark),
                                 ("2k/d", 386, 406, 835, 868, red)]:
    w = R(x0, x1, y0, y1); xx0, xx1, yy0, yy1 = w
    ren = rowbands(ra, xx0, xx1, yy0, yy1, mk, lambda p: p * RPT, lambda p: p * RPT, gap=4, minarea=3)
    w = fw(x0, x1, y0, y1); xx0, xx1, yy0, yy1 = w
    orig = rowbands(fa, xx0, xx1, yy0, yy1, mk, MAPX, MAPY, gap=4, minarea=3)
    show(lab, ren, orig)

print("=== DX1 (y<536 to skip chrome border) ===")
w = R(404, 445, 514, 536); x0, x1, y0, y1 = w
show("dx1", rowbands(ra, x0, x1, y0, y1, red, lambda p: p * RPT, lambda p: p * RPT, gap=4, minarea=3),
            rowbands(fa, *fw(404, 445, 514, 536), red, MAPX, MAPY, gap=4, minarea=3))

print("=== TITLE ===")
w = R(80, 880, 46, 70); x0, x1, y0, y1 = w
show("title", rowbands(ra, x0, x1, y0, y1, red, lambda p: p * RPT, lambda p: p * RPT, gap=4, minarea=6),
              rowbands(fa, *fw(80, 880, 46, 70), red, MAPX, MAPY, gap=4, minarea=6))
