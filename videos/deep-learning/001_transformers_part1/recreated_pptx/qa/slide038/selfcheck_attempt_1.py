#!/usr/bin/env python3
"""selfcheck_attempt_1 for slide 038 (150dpi render 2001x1125; frame px * 2000/960).
Checks:
 1. inheritance diff vs parent's certified render qa/slide037/render_1.png —
    confined to badge zone / inset zone / scaling-box zone (delta inventory)
 2. house chrome (shared_patterns/house_chrome_check.py runs separately)
 3. scaling box landed at the child frame's measured position (+8px frame)
 4. inset panel containment: boxes + arrows inside the green panel; panel inside
    the house frame; inset ink vs the frame's measured geometry
"""
from PIL import Image
import numpy as np

V = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1"
S = 2000 / 960.0  # 150dpi px per frame px

mine = np.asarray(Image.open(f"{V}/recreated_pptx/qa/slide038/render_1.png").convert("RGB")).astype(int)
par = np.asarray(Image.open(f"{V}/recreated_pptx/qa/slide037/render_1.png").convert("RGB")).astype(int)
orig = np.asarray(Image.open(f"{V}/unique_slides/slide_038.jpg").convert("RGB")).astype(int)
print("render shapes:", mine.shape, par.shape)

# ---- 1. inheritance diff ---------------------------------------------------------
h = min(mine.shape[0], par.shape[0]); w = min(mine.shape[1], par.shape[1])
d = np.abs(mine[:h, :w] - par[:h, :w]).sum(axis=2)
mask = d > 60
ys, xs = np.where(mask)
print(f"[1] diff pixels vs certified parent: {len(xs)}")
if len(xs):
    print(f"    bbox x[{xs.min()}..{xs.max()}] y[{ys.min()}..{ys.max()}]")
# allowed zones (150dpi coords) = delta inventory:
zones = {
    "badge":        (875 * S, 920 * S, 50 * S, 95 * S),
    "inset":        (780 * S, 925 * S, 95 * S, 325 * S),
    "scaling_box":  (360 * S, 425 * S, 160 * S, 430 * S),
}
outside = np.zeros_like(mask)
mz = np.zeros_like(mask)
for name, (x0, x1, y0, y1) in zones.items():
    x0, x1, y0, y1 = int(x0), int(x1), int(y0), int(y1)
    mz[y0:y1, x0:x1] = True
outside = mask & ~mz
n_out = int(outside.sum())
print(f"[1] diff pixels OUTSIDE delta zones: {n_out}")
if n_out:
    yo, xo = np.where(outside)
    print(f"    outside bbox x[{xo.min()}..{xo.max()}] y[{yo.min()}..{yo.max()}]")
    # coarse grid of outside clusters
    cell = 20
    from collections import Counter
    cc = Counter((int(x // cell) * cell, int(y // cell) * cell) for x, y in zip(xo, yo))
    for (gx, gy), c in sorted(cc.items(), key=lambda kv: -kv[1])[:12]:
        print(f"      cell x{gx} y{gy}: {c}")

# ---- 2. scaling box position in MY render vs MY frame ----------------------------
def yellow_run(img, x150, y0=300, y1=950):
    R, G, B = img[:, :, 0], img[:, :, 1], img[:, :, 2]
    yel = (R > 215) & (G > 200) & (B < 170) & (R - B > 60)
    col = np.where(yel[y0:y1, x150])[0] + y0
    return (col.min(), col.max()) if len(col) else None

x150 = int(395 * S)
r38 = yellow_run(mine, x150)
o38 = yellow_run(orig, 395)
print(f"[3] scaling yellow run my-render x~{x150}: {r38}  (frame x395 orig: {o38})")
if r38 and o38:
    exp = (round(o38[0] * S), round(o38[1] * S))
    print(f"    expected ~{exp}, delta render-vs-expected: {r38[0]-exp[0]}, {r38[1]-exp[1]} (150dpi px, tol 6)")
# fraction bar must stay at the parent position: red bar row ~206*S
R, G, B = mine[:, :, 0], mine[:, :, 1], mine[:, :, 2]
red = (R > 130) & (R - G > 60) & (R - B > 50)
barband = red[int(200 * S):int(212 * S), int(416 * S):int(452 * S)]
ys2, xs2 = np.where(barband)
print(f"[3] fraction bar ink rows (y200-212 band): {sorted(set((ys2 + int(200*S)).tolist()))[:6]}... expected ~{int(206*S)}")

# ---- 4. inset geometry in MY render vs MY frame ----------------------------------
def green_bbox(img, x0f, x1f, y0f, y1f):
    R, G, B = img[:, :, 0], img[:, :, 1], img[:, :, 2]
    g = (G > R + 25) & (G > B + 15) & (G > 80) & (G < 200) & (R < 150)
    m = np.zeros(g.shape, bool)
    m[int(y0f * S):int(y1f * S), int(x0f * S):int(x1f * S)] = g[int(y0f * S):int(y1f * S), int(x0f * S):int(x1f * S)]
    ys3, xs3 = np.where(m)
    return (xs3.min(), xs3.max(), ys3.min(), ys3.max()) if len(xs3) else None

gb_r = green_bbox(mine, 760, 935, 85, 340)
gb_o = green_bbox(orig, 760, 935, 85, 340)
print(f"[4] panel green bbox render: {gb_r}")
print(f"    panel green bbox frame : {gb_o} -> expected ~({gb_o[0]*S:.0f},{gb_o[1]*S:.0f},{gb_o[2]*S:.0f},{gb_o[3]*S:.0f})")

# containment: all inset ink inside the panel (+2px border tolerance) and inside house frame
Rr, Gr, Br = mine[:, :, 0], mine[:, :, 1], mine[:, :, 2]
ink = (Rr < 140) & (Gr < 140) & (Br < 140)
px0, px1 = int(797 * S), int(915 * S)
py0, py1 = int(114 * S), int(314 * S)
zone = np.zeros(ink.shape, bool)
zone[py0 - 6:py1 + 8, px0 - 8:px1 + 10] = True
zin = ink & zone
zys, zxs = np.where(zin)
print(f"[4] inset ink bbox in render: x[{zxs.min()}..{zxs.max()}] y[{zys.min()}..{zys.max()}] (panel {px0}..{px1} x {py0}..{py1})")
print(f"    ink inside panel bounds+tol: x ok={zxs.min() >= px0 - 8 and zxs.max() <= px1 + 10}, y ok={zys.min() >= py0 - 6 and zys.max() <= py1 + 8}")
# house frame containment for the whole delta: right edge of ink vs house border ~x918*S
house_r = int(918 * S)
print(f"[4] max ink x in inset zone vs house panel border x~{house_r}: {zxs.max()} (must be < {house_r})")

# box band rows in my render vs frame (borders = wide dark rows inside panel)
rows = zin.sum(axis=1)
wide = [y for y in range(py0 - 6, py1 + 8) if rows[y] > 100]
print(f"[4] wide-ink rows (box borders) render: {wide}")
exp_bands = [(136, 156), (166, 185), (196, 214), (225, 243), (255, 273)]
print(f"    expected bands*S: {[(round(a*S), round(b*S)) for a, b in exp_bands]}")
