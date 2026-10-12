#!/usr/bin/env python3
"""slide_032 closed-loop self-check (attempt K): render vs original, all in FRAME px.

Scale: 150dpi render (1 render px = 1/200 in) -> frame px = *72/150.
Targets = PIL-measured ink in unique_slides/slide_032.jpg (960x540, 1px=1pt).
Tolerance ~4 frame px (the pipeline closed-loop standard) unless noted.
"""
import sys
import numpy as np
from PIL import Image

K = sys.argv[1] if len(sys.argv) > 1 else "1"
BASE = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/qa/slide032"
REN = Image.open(f"{BASE}/render_{K}.png").convert("RGB")
ORIG = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_032.jpg").convert("RGB")
print("render size:", REN.size)
S = REN.size[1] / 540.0

A = np.asarray(REN).astype(int)
O = np.asarray(ORIG).astype(int)

def ink_bbox(M, mask, y0, y1, x0, x1):
    sub = mask[y0:y1, x0:x1]
    ys, xs = np.where(sub)
    if len(ys) == 0:
        return None
    return (x0 + xs.min(), x0 + xs.max(), y0 + ys.min(), y0 + ys.max(), int(sub.sum()))

def to_frame(bb):
    if bb is None:
        return None
    return tuple(round(v / S, 1) for v in bb[:4]) + (bb[4],)

checks = []
def chk(name, got, want, tol=4.0):
    if got is None:
        checks.append((name, "MISSING", want, "FAIL"))
        return
    errs = [abs(g - w) for g, w in zip(got[:4], want[:4])]
    ok = all(e <= tol for e in errs)
    wn = tuple(want[:4]) + (want[4],) if len(want) > 4 else tuple(want[:4])
    checks.append((name, tuple(got[:4]) + (got[4],), wn,
                   "PASS" if ok else f"FAIL d={[round(e,1) for e in errs]}"))

# masks on the render
r, g, b = A[:, :, 0], A[:, :, 1], A[:, :, 2]
red_m = (r > 120) & (g < 80) & (b < 80) & (r > g + 60)
blue_m = (b > 100) & (b > r + 40) & (b > g + 30)
blk_m = (r < 80) & (g < 80) & (b < 80)
brown_m = (r > 130) & (r < 220) & (g > 60) & (g < 150) & (b < 90) & (r > g + 40)

# ---- 1. title (red ink, y 60..140 frame) ----
tb_r = ink_bbox(A, red_m, int(60 * S), int(140 * S), 0, A.shape[1])
chk("title ink bbox (x0,x1,y0,y1,n)", to_frame(tb_r), (176, 773, 80, 112), tol=4.0)

# ---- 2. body lines (blue ink) ----
BANDS = [("L1", 95, 286, 149, 170), ("L2", 88, 573, 175, 196), ("L3", 88, 452, 238, 259),
         ("L4", 88, 493, 263, 285), ("L5", 88, 516, 326, 348), ("L6", 88, 274, 352, 374)]
for name, x0, x1, y0, y1 in BANDS:
    bb = ink_bbox(A, blue_m, int((y0 - 14) * S), int((y1 + 14) * S), 0, int(660 * S))
    chk(f"body {name}", to_frame(bb), (x0, x1, y0, y1), tol=4.0)

# line pitch (baselines from band bottoms is unstable; use band tops of L2 vs L1)
# ---- 3. label '2-D Image' ----
lb = ink_bbox(A, red_m, int(215 * S), int(268 * S), int(620 * S), int(900 * S))
chk("label '2-D Image'", to_frame(lb), (692, 807, 229, 250), tol=4.0)

# ---- 4. left box border (blue-gray) ----
bg_m = (b > 140) & (b > r + 15) & (r > 100) & (r < 200) & (g > 100) & (g < 190)
bb2 = ink_bbox(A, bg_m, int(120 * S), int(440 * S), int(60 * S), int(600 * S))
chk("left box border bbox", to_frame(bb2), (77, 591, 139, 422), tol=4.0)

# ---- 5. right box border (red) ----
rb = ink_bbox(A, red_m, int(255 * S), int(515 * S), int(595 * S), int(905 * S))
chk("right box border bbox", to_frame(rb), (612, 890, 271, 501), tol=4.0)

# ---- 6. diagram: plane, filter, arrow ----
pb = ink_bbox(A, brown_m, int(300 * S), int(510 * S), int(620 * S), int(800 * S))
chk("plane bbox (brown)", to_frame(pb), (645, 774, 315, 495), tol=4.0)
fb = ink_bbox(A, blue_m & (np.arange(A.shape[1])[None, :] > int(700 * S)), int(335 * S), int(390 * S), int(700 * S), int(780 * S))
chk("filter bbox (blue)", to_frame(fb), (728, 754, 345, 378), tol=4.0)
# arrow: red ink strictly inside the plane region (not the border columns)
inner = red_m.copy()
inner[: int(305 * S), :] = False; inner[int(435 * S):, :] = False
inner[:, : int(650 * S)] = False; inner[:, int(770 * S):] = False
ab = ink_bbox(A, inner, int(305 * S), int(435 * S), int(650 * S), int(770 * S))
chk("arrow ink inside plane", to_frame(ab), (744, 774, 368, 401), tol=5.0)

# ---- 7. words ----
gw = ink_bbox(A, blk_m, int(265 * S), int(320 * S), int(620 * S), int(900 * S))
chk("'Grayscale' ink bbox", to_frame(gw), (684, 863, 276, 308), tol=4.0)
fw = ink_bbox(A, red_m, int(430 * S), int(470 * S), int(760 * S), int(860 * S))
chk("'Filters' ink bbox", to_frame(fw), (777, 842, 441, 456), tol=4.0)

# ---- 8. black bar ----
bar_rows = [y for y in range(int(505 * S), A.shape[0]) if blk_m[y, int(100 * S):int(880 * S)].sum() > int(600 * S)]
if bar_rows:
    top_fr = bar_rows[0] / S
    ok = abs(top_fr - 519) <= 4
    checks.append(("black bar top (frame y)", round(top_fr, 1), 519, "PASS" if ok else "FAIL"))
else:
    checks.append(("black bar top", None, 519, "MISSING"))

# ---- 9. colors ----
def modal(M, y0, y1, x0, x1, mask=None):
    sub = M[int(y0 * S):int(y1 * S), int(x0 * S):int(x1 * S)]
    if mask is not None:
        sub = sub[mask[int(y0 * S):int(y1 * S), int(x0 * S):int(x1 * S)]]
    if len(sub) == 0:
        return None
    q = (sub // 8 * 8)
    vals, counts = np.unique(q.reshape(-1, 3), axis=0, return_counts=True)
    return tuple(int(v) for v in vals[counts.argmax()])

checks.append(("panel gray modal", modal(A, 120, 135, 200, 400), (233, 233, 231), "info"))
checks.append(("body blue modal (L2 core)", modal(A, 181, 189, 100, 560, blue_m), (0, 0, 128), "info"))
checks.append(("title red modal", modal(A, 85, 100, 200, 750, red_m), (192, 0, 0), "info"))
checks.append(("plane brown modal", modal(A, 430, 470, 660, 700, brown_m), (175, 103, 24), "info"))
checks.append(("filter blue modal", modal(A, 350, 372, 730, 752, blue_m), (13, 153, 187), "info"))
checks.append(("left box fill modal", modal(A, 300, 320, 300, 500), (255, 255, 255), "info"))

print(f"{'check':42s} {'got':28s} {'want':22s} verdict")
for name, got, want, v in checks:
    print(f"{name:42s} {str(got):28s} {str(want):22s} {v}")
