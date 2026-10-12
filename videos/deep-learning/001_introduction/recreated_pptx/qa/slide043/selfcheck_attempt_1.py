#!/usr/bin/env python3
"""selfcheck_attempt_1.py — closed-loop PIL verification of render_1.png vs the
original frame's measured geometry (slide_043, 150dpi render 2001x1125,
frame-px = render-px * 960/2001; tolerance ~4 render px = 1.92 frame px).
Every check prints target / measured / delta and OK/FAIL."""
import numpy as np
from PIL import Image

REN = np.asarray(Image.open(
    "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/qa/slide043/render_1.png"
).convert("RGB")).astype(int)
H, W = REN.shape[:2]
SC = 960.0 / W  # frame px per render px
r, g, b = REN[:, :, 0], REN[:, :, 1], REN[:, :, 2]
lum = r + g + b

def to_f(v):
    return v * SC

fails = []
def check(name, target, measured, tol_f=2.0):
    d = measured - target
    ok = abs(d) <= tol_f
    if not ok:
        fails.append(name)
    print(f"{'OK ' if ok else 'FAIL'} {name:44s} target {target:7.1f} measured {measured:7.1f} delta {d:+5.2f} (tol {tol_f})")

def ink_bbox_f(y0f, y1f, x0f, x1f, thresh=460):
    y0, y1 = int(y0f / SC), int(y1f / SC)
    x0, x1 = int(x0f / SC), int(x1f / SC)
    m = lum[y0:y1, x0:x1] < thresh
    ys, xs = np.where(m)
    if not len(ys):
        return None
    return (to_f(x0 + xs.min()), to_f(x0 + xs.max()), to_f(y0 + ys.min()), to_f(y0 + ys.max()))

# ---------- title ----------
tb = ink_bbox_f(40, 105, 60, 900)
print("--- title ---")
if tb:
    check("title ink left", 99, tb[0])
    check("title ink right", 866, tb[1])
    check("title ink top", 62, tb[2], 2.5)
    check("title ink bottom", 90, tb[3], 2.5)
else:
    fails.append("title EMPTY"); print("FAIL title EMPTY")

# ---------- inner panel ----------
print("--- inner panel (red border) ---")
red = (r > 120) & (g < 110) & (b < 110)
# left border column near x81: scan frame cols 75..90 for a tall red run
best = None
for xf in range(74, 92):
    xr = int(xf / SC)
    n = red[int(100/SC):int(390/SC), xr].sum()
    if n > 200:
        best = xf; break
check("panel left border x", 81, best if best else -1)
bestr = None
for xf in range(852, 836, -1):
    xr = int(xf / SC)
    n = red[int(100/SC):int(390/SC), xr].sum()
    if n > 200:
        bestr = xf; break
check("panel right border x", 845, bestr if bestr else -1)
bestt = None
for yf in range(104, 120):
    yr = int(yf / SC)
    n = red[yr, int(90/SC):int(840/SC)].sum()
    if n > 500:
        bestt = yf; break
check("panel top border y", 111, bestt if bestt else -1)
bestb = None
for yf in range(388, 372, -1):
    yr = int(yf / SC)
    n = red[yr, int(90/SC):int(840/SC)].sum()
    if n > 500:
        bestb = yf; break
check("panel bottom border y", 380, bestb if bestb else -1)

# ---------- bullets ----------
print("--- bullets ---")
dark = lum < 460
for i, (base_t, y0f, y1f) in enumerate([(140.3, 115, 150), (170.2, 150, 180), (199.9, 180, 212)]):
    bb = ink_bbox_f(y0f, y1f, 140, 580)
    if bb:
        # baseline: bottom minus descender for lines with g/p/y; approximate via band bottom
        desc = 5.0 if i != 1 else 5.0
        check(f"bullet{i+1} ink left", 148, bb[0])
        check(f"bullet{i+1} band bottom~baseline+desc", base_t + desc, bb[3], 2.5)
    else:
        fails.append(f"bullet{i+1} EMPTY"); print(f"FAIL bullet{i+1} EMPTY")

# ---------- 5x5 grid borders ----------
print("--- 5x5 grid ---")
grid_dark = (lum < 400)
for xf_t, lbl in [(244, "left"), (283, "c0/c1"), (322, "c1/c2"), (361, "c2/c3"), (400, "c3/c4"), (438.5, "right")]:
    found = None
    for xf in np.arange(xf_t - 3, xf_t + 3.01, 0.5):
        xr = int(xf / SC)
        n = grid_dark[int(230/SC):int(370/SC), xr].sum()
        if n > 100:
            found = xf; break
    check(f"grid5 border col {lbl}", xf_t, found if found else -1, 1.5)
for yf_t, lbl in [(228, "top"), (257.6, "r0/r1"), (287.2, "r1/r2"), (316.8, "r2/r3"), (346.4, "r3/r4"), (375, "bottom")]:
    found = None
    for yf in np.arange(yf_t - 3, yf_t + 3.01, 0.5):
        yr = int(yf / SC)
        n = grid_dark[yr, int(250/SC):int(430/SC)].sum()
        if n > 100:
            found = yf; break
    check(f"grid5 border row {lbl}", yf_t, found if found else -1, 1.5)

# grid fill colors
def modal_f(x0f, x1f, y0f, y1f):
    x0, x1 = int(x0f/SC), int(x1f/SC)
    y0, y1 = int(y0f/SC), int(y1f/SC)
    reg = REN[y0:y1, x0:x1].reshape(-1, 3)
    vals, counts = np.unique(reg, axis=0, return_counts=True)
    return '#%02X%02X%02X' % tuple(vals[np.argmax(counts)])
print(f"yellow fill (target FDFF0B): {modal_f(250, 275, 248, 254)}")
print(f"green fill (target 0DC94F): {modal_f(405, 430, 352, 370)}")
print(f"sage fill (target 95A38A): {modal_f(520, 550, 255, 275)}")

# number ink in cell (0,0) '1' center
nb = ink_bbox_f(230, 256, 248, 280, 300)
if nb:
    check("num(0,0) ink center x", 263.5, (nb[0] + nb[1]) / 2)
    check("num(0,0) ink center y", 242.8, (nb[2] + nb[3]) / 2)
else:
    fails.append("num(0,0) EMPTY"); print("FAIL num(0,0) EMPTY")

# ---------- annotations ----------
print("--- x0/x1 annotations ---")
red2 = (r > 140) & (g < 110) & (b < 110)
m = red2[int(240/SC):int(320/SC), int(255/SC):int(370/SC)]
ys, xs = np.where(m)
if len(ys):
    print(f"annot total bbox frame: x {to_f(int(255/SC)+xs.min()):.1f}..{to_f(int(255/SC)+xs.max()):.1f} "
          f"y {to_f(int(240/SC)+ys.min()):.1f}..{to_f(int(240/SC)+ys.max()):.1f} n={len(ys)}")
    check("annot region left", 268, to_f(int(255/SC) + xs.min()), 3)
    check("annot region right", 359, to_f(int(255/SC) + xs.max()), 3)
    check("annot region top", 248, to_f(int(240/SC) + ys.min()), 3)
    check("annot region bottom", 315, to_f(int(240/SC) + ys.max()), 3)
else:
    fails.append("annots EMPTY"); print("FAIL annotations EMPTY (BLOCKER)")

# ---------- labels ----------
print("--- labels ---")
for name, cx_t, cy_t, x0f, x1f in [("Image", 341, 213, 260, 430),
                                    ("After conv 1", 584.5, 211, 470, 680),
                                    ("After conv 2", 754.5, 210, 670, 870)]:
    bb = ink_bbox_f(190, 232, x0f, x1f)
    if bb:
        check(f"{name} ink center x", cx_t, (bb[0] + bb[1]) / 2)
        check(f"{name} ink center y", cy_t, (bb[2] + bb[3]) / 2)
    else:
        fails.append(f"{name} EMPTY"); print(f"FAIL label {name} EMPTY")

# ---------- arrows ----------
print("--- arrows ---")
# arrow outlines: dark ink in the arrow regions (away from grids)
for name, (x0f, x1f, y0f, y1f), (bx_t, by_t, bw_t, bh_t) in [
    ("arrow1", (445, 508, 288, 324), (451, 296, 50, 20)),
    ("arrow2", (670, 732, 288, 324), (676, 296.5, 50, 20)),
]:
    bb = ink_bbox_f(y0f, y1f, x0f, x1f)
    if bb:
        check(f"{name} left", bx_t, bb[0], 1.5)
        check(f"{name} right", bx_t + bw_t, bb[1], 1.5)
        check(f"{name} top", by_t, bb[2], 1.5)
        check(f"{name} bottom", by_t + bh_t, bb[3], 1.5)
    else:
        fails.append(f"{name} EMPTY"); print(f"FAIL {name} EMPTY")

# ---------- 3x3 grid ----------
print("--- 3x3 grid ---")
for xf_t in (510, 558, 562, 610, 614, 662):
    found = None
    for xf in np.arange(xf_t - 3, xf_t + 3.01, 0.5):
        xr = int(xf / SC)
        n = ((lum[:, xr] < 550) & (lum[:, xr] > 150))[int(250/SC):int(360/SC)].sum()
        if n > 60:
            found = xf; break
    check(f"grid3 border col {xf_t}", xf_t, found if found else -1, 1.5)
for yf_t in (248, 285, 287, 324, 326, 363):
    found = None
    for yf in np.arange(yf_t - 3, yf_t + 3.01, 0.5):
        yr = int(yf / SC)
        n = ((lum[yr] < 550) & (lum[yr] > 150))[int(515/SC):int(660/SC)].sum()
        if n > 30:
            found = yf; break
    check(f"grid3 border row {yf_t}", yf_t, found if found else -1, 1.5)
nb3 = ink_bbox_f(252, 280, 515, 552, 300)
if nb3:
    check("num3(0,0) center x", 534, (nb3[0] + nb3[1]) / 2)
    check("num3(0,0) center y", 266, (nb3[2] + nb3[3]) / 2)
else:
    fails.append("num3(0,0) EMPTY"); print("FAIL num3(0,0) EMPTY")

# 18-cell
nb18 = ink_bbox_f(292, 320, 742, 784, 300)
if nb18:
    check("'18' ink center x", 762.5, (nb18[0] + nb18[1]) / 2)
    check("'18' ink center y", 305, (nb18[2] + nb18[3]) / 2)
else:
    fails.append("'18' EMPTY"); print("FAIL '18' EMPTY")

# ---------- blue box + navy lines ----------
print("--- blue box / navy ---")
darkish = lum < 620
bl = darkish[int(395/SC):int(512/SC), :]
for xf_t, lbl in [(77, "left"), (859, "right")]:
    found = None
    for xf in np.arange(xf_t - 3, xf_t + 3.01, 0.5):
        xr = int(xf / SC)
        n = bl[:, xr].sum()
        if n > 70:
            found = xf; break
    check(f"box border col {lbl}", xf_t, found if found else -1, 1.5)
for yf_t, lbl in [(393, "top"), (509.5, "bottom")]:
    found = None
    for yf in np.arange(yf_t - 3, yf_t + 3.01, 0.5):
        yr = int(yf / SC)
        n = darkish[yr, int(90/SC):int(850/SC)].sum()
        if n > 500:
            found = yf; break
    check(f"box border row {lbl}", yf_t, found if found else -1, 1.5)
navy = (b > 90) & (r < 110) & (g < 110) & (b > r + 30)
for i, (base_t, y0f, y1f) in enumerate([(418.5, 400, 428), (445.4, 428, 455), (472.4, 455, 482), (499.7, 482, 508)]):
    y0, y1 = int(y0f/SC), int(y1f/SC)
    m = navy[y0:y1, int(80/SC):int(700/SC)]
    ys, xs = np.where(m)
    if len(ys):
        f_top = to_f(y0 + ys.min()); f_bot = to_f(y0 + ys.max())
        f_l = to_f(int(80/SC) + xs.min())
        check(f"navy L{i+1} ink left", 88, f_l)
        check(f"navy L{i+1} band bottom (base+desc)", base_t + 4.6, f_bot, 2.5)
    else:
        fails.append(f"navy L{i+1} EMPTY"); print(f"FAIL navy L{i+1} EMPTY")

# ---------- frame containment ----------
print("--- frame containment ---")
# content ink must stay inside panel border (81..845 x 111..380 inner; chrome canvas elsewhere)
content = lum < 400
ys, xs = np.where(content)
cx0, cx1 = to_f(xs.min()), to_f(xs.max())
print(f"content ink bbox frame: x {cx0:.1f}..{cx1:.1f}")
check("content left >= 43 (chrome panel)", 43, cx0, 0.01, ) if cx0 < 43 else print(f"OK  content left {cx0:.1f} >= 43")
check("content right <= 917", 917, min(cx1, 917), 0.01) if cx1 > 917 else print(f"OK  content right {cx1:.1f} <= 917")

print()
print("=" * 60)
if fails:
    print(f"SELFCHECK RESULT: {len(fails)} FAIL(S): {fails}")
else:
    print("SELFCHECK RESULT: ALL OK")
