#!/usr/bin/env python3
"""slide_032 closed-loop self-check (attempt K): render vs original, all in FRAME px.

Attempt-2 version: measurement windows fixed (chrome excluded from title scan; plane
scan excludes the arrow-tail zone; 'Filters' word scanned in its own y-window; body
lines measured in tight per-line windows).
"""
import sys
import numpy as np
from PIL import Image

K = sys.argv[1] if len(sys.argv) > 1 else "2"
BASE = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/qa/slide032"
REN = Image.open(f"{BASE}/render_{K}.png").convert("RGB")
print("render size:", REN.size)
S = REN.size[1] / 540.0
A = np.asarray(REN).astype(int)

r, g, b = A[:, :, 0], A[:, :, 1], A[:, :, 2]
red_m = (r > 120) & (g < 80) & (b < 80) & (r > g + 60)
blue_m = (b > 100) & (b > r + 40) & (b > g + 30)
blk_m = (r < 80) & (g < 80) & (b < 80)
brown_m = (r > 130) & (r < 220) & (g > 60) & (g < 150) & (b < 90) & (r > g + 40)

def bbox(mask, y0, y1, x0, x1):
    sub = mask[int(y0 * S):int(y1 * S), int(x0 * S):int(x1 * S)]
    ys, xs = np.where(sub)
    if len(ys) == 0:
        return None
    return (round(x0 + xs.min() / S, 1), round(x0 + xs.max() / S, 1),
            round(y0 + ys.min() / S, 1), round(y0 + ys.max() / S, 1), int(sub.sum()))

checks = []
def chk(name, got, want, tol=4.0):
    if got is None:
        checks.append((name, "MISSING", want, "FAIL"))
        return
    errs = [abs(gv - wv) for gv, wv in zip(got[:4], want[:4])]
    ok = all(e <= tol for e in errs)
    checks.append((name, got[:4], tuple(want[:4]), "PASS" if ok else f"FAIL d={[round(e,1) for e in errs]}"))

# title (chrome excluded: x 100..860, y 65..135)
chk("title ink bbox", bbox(red_m, 65, 135, 100, 860), (176, 773, 80, 112))
# body lines: tight per-line windows (y target +-6, x 60..660)
BANDS = [("L1", 95, 286, 149, 170), ("L2", 88, 573, 175, 196), ("L3", 88, 452, 238, 259),
         ("L4", 88, 493, 263, 285), ("L5", 88, 516, 326, 348), ("L6", 88, 274, 352, 374)]
for name, x0, x1, y0, y1 in BANDS:
    got = bbox(blue_m, y0 - 6, y1 + 6, 60, 660)
    chk(f"body {name}", got, (x0, x1, y0, y1))
# label
chk("label '2-D Image'", bbox(red_m, 215, 268, 620, 900), (692, 807, 229, 250))
# left/right box borders
bg_m = (b > 140) & (b > r + 15) & (r > 100) & (r < 200) & (g > 100) & (g < 190)
chk("left box border bbox", bbox(bg_m, 120, 440, 60, 600), (77, 591, 139, 422))
chk("right box border bbox", bbox(red_m, 255, 515, 595, 905), (612, 890, 271, 501))
# plane: exclude arrow tail zone (x>770 & y>420)
pm = brown_m.copy()
pm[int(420 * S):, int(770 * S):] = False
chk("plane bbox (arrow excl.)", bbox(pm, 300, 510, 620, 800), (645, 774, 315, 495))
# filter
chk("filter bbox", bbox(blue_m, 335, 390, 700, 780), (728, 754, 345, 378))
# arrow inside plane (red, x 650..770, y 360..410)
chk("arrow ink in plane", bbox(red_m, 360, 410, 650, 770), (744, 774, 368, 401), tol=5)
# words
chk("'Grayscale' ink bbox", bbox(blk_m, 265, 320, 620, 900), (684, 863, 276, 308))
chk("'Filters' ink bbox (y438+)", bbox(red_m, 438, 465, 760, 860), (777, 842, 441, 456))
# black bar
bar_rows = [y for y in range(int(505 * S), A.shape[0]) if blk_m[y, int(100 * S):int(880 * S)].sum() > int(600 * S)]
top_fr = bar_rows[0] / S if bar_rows else None
checks.append(("black bar top", round(top_fr, 1) if top_fr else None, 519,
               "PASS" if top_fr and abs(top_fr - 519) <= 4 else "FAIL"))

# colors (modal of quantized pixels)
def modal(y0, y1, x0, x1, mask=None):
    sl = (slice(int(y0 * S), int(y1 * S)), slice(int(x0 * S), int(x1 * S)))
    sub = A[sl]
    if mask is not None:
        sub = sub[mask[sl]]
    if len(sub) == 0:
        return None
    q = sub // 8 * 8
    vals, counts = np.unique(q.reshape(-1, 3), axis=0, return_counts=True)
    return tuple(int(v) for v in vals[counts.argmax()])

checks.append(("panel gray modal", modal(120, 135, 200, 400), (233, 233, 231), "info"))
checks.append(("body blue modal (L2)", modal(181, 189, 100, 560, blue_m), (0, 0, 128), "info"))
checks.append(("title red modal", modal(85, 100, 200, 750, red_m), (192, 0, 0), "info"))
checks.append(("plane brown modal", modal(430, 470, 660, 700, brown_m), (175, 103, 24), "info"))
checks.append(("filter blue modal", modal(350, 372, 730, 752, blue_m), (13, 153, 187), "info"))
checks.append(("left box fill modal", modal(300, 320, 300, 500), (255, 255, 255), "info"))

print(f"{'check':36s} {'got':26s} {'want':20s} verdict")
fails = 0
for name, got, want, v in checks:
    print(f"{name:36s} {str(got):26s} {str(want):20s} {v}")
    if v.startswith("FAIL") or v == "MISSING":
        fails += 1
print(f"\n{fails} hard failures")
