#!/usr/bin/env python3
"""Self-check attempt 1: closed-loop render vs frame measurements (all in frame px).
Render 2000x1125 @150dpi -> frame px scale 960/2000 = 0.48."""
import numpy as np
from PIL import Image
from collections import Counter

REN = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/qa/slide005/render_1.png"
im = np.asarray(Image.open(REN).convert("RGB")).astype(int)
H, W = im.shape[:2]
print(f"render {W}x{H}")
S = 960 / 2000.0  # render px -> frame px
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]

def fx(v): return round(v * S, 1)

fails, notes = [], []

# ---------- title ----------
red = (r > 140) & (g < 110) & (b < 110)
m = red[80:260, 300:1700]  # y40-130 frame, x150-850
ys, xs = np.where(m)
tx0, tx1, ty0, ty1 = fx(xs.min() + 300), fx(xs.max() + 300), fx(ys.min() + 80), fx(ys.max() + 80)
print(f"title: x {tx0}-{tx1} (target 261-653)  y {ty0}-{ty1} (target 59-76)")
if abs(tx0 - 261) > 8 or abs(tx1 - 653) > 8: fails.append(f"title x {tx0}-{tx1} vs 261-653")
if abs(ty0 - 59) > 4: fails.append(f"title cap top {ty0} vs 59")
if abs(ty1 - 76) > 4: fails.append(f"title bottom {ty1} vs 76")

# ---------- headers ----------
redl = red[280:380, :]  # frame y140-190
for nm, xa, xb, txa, txb in [("WV", 300, 560, 179, 223), ("FM1", 600, 830, 323, 384), ("FM2", 900, 1120, 466, 531), ("FM3", 1180, 1420, 605, 669), ("FM4", 1480, 1720, 747, 811)]:
    mm = redl[:, xa:xb]
    ys, xs = np.where(mm)
    if not len(xs):
        fails.append(f"header {nm}: no ink"); continue
    x0, x1 = fx(xs.min() + xa), fx(xs.max() + xa)
    y0, y1 = fx(ys.min() + 280), fx(ys.max() + 280)
    print(f"header {nm}: x {x0}-{x1} (tgt {txa}-{txb})  y {y0}-{y1} (tgt 149-174)")
    if abs((x0 + x1) / 2 - (txa + txb) / 2) > 6: fails.append(f"header {nm} center {(x0+x1)/2} vs {(txa+txb)/2}")
    if abs(y0 - 149) > 4: fails.append(f"header {nm} top {y0} vs 149")

# ---------- stack grid ----------
# top/bottom boundary lines: rows with many gray-blue px in a stack window
def gridrows(xa_f, xb_f):
    xa, xb = int(xa_f / S), int(xb_f / S)
    win = im[300:1000, xa:xb]
    rr, gg, bb = win[:, :, 0], win[:, :, 1], win[:, :, 2]
    outline = (abs(rr - 167) < 45) & (abs(gg - 175) < 45) & (abs(bb - 184) < 45)
    rows = np.where(outline.sum(axis=1) > (xb - xa) * 0.55)[0] + 300
    return rows
rows = gridrows(163, 244)
if len(rows):
    print(f"stack grid: top {fx(rows.min())} (tgt 178.5) bottom {fx(rows.max())} (tgt 462.5), n_lines {len(rows)} (tgt 19)")
    if abs(fx(rows.min()) - 178.5) > 4: fails.append(f"grid top {fx(rows.min())}")
    if abs(fx(rows.max()) - 462.5) > 4: fails.append(f"grid bottom {fx(rows.max())}")
    if len(rows) < 17: fails.append(f"grid lines {len(rows)} < 17")
else:
    fails.append("no grid rows found")

# stack edges (vertical outline columns) at mid-height
rowy = int(320 / S)
for lbl, xf in [("WV.L", 163), ("WV.R", 244), ("FM1.L", 308), ("FM2.L", 456), ("FM3.L", 598), ("FM4.L", 737), ("FM4.R", 818)]:
    x = int(xf / S)
    seg = im[350:900, x - 3:x + 4]
    rr, gg, bb = seg[:, :, 0], seg[:, :, 1], seg[:, :, 2]
    outline = (abs(rr - 167) < 50) & (abs(gg - 175) < 50) & (abs(bb - 184) < 50)
    cols = np.where(outline.sum(axis=0) > 100)[0]
    got = fx(x - 3 + cols[0]) if len(cols) else None
    print(f"edge {lbl}: x {got} (tgt {xf})")
    if got is None or abs(got - xf) > 4: fails.append(f"edge {lbl} {got} vs {xf}")

# ---------- per-cell fills on render ----------
TOP, PITCH, NCELL = 178.5, (462.5 - 178.5) / 18, 18
def cellclass(x0, x1, ci):
    y0 = int((TOP + PITCH * ci) / S) + 5
    y1 = int((TOP + PITCH * (ci + 1)) / S) - 5
    x0i, x1i = int(x0 / S) + 8, int(x1 / S) - 8
    patch = im[y0:y1, x0i:x1i].reshape(-1, 3)
    cnt = Counter(tuple(int(v) // 16 * 16 for v in p) for p in patch)
    return cnt.most_common(1)[0][0]
EXPECT = {
    "WV": (163, 244, "FFFFCC", [1, 2, 3]),
    "FM1": (308, 390, "FFCC99", [3, 14, 15, 16]),
    "FM2": (456, 537, "99FFFF", [9, 10, 11, 15]),
    "FM3": (598, 679, "FFCCFF", [3, 4, 5, 10]),
    "FM4": (737, 818, "CCFFCC", [4, 14]),
}
PALR = {"FFFFCC": (255, 255, 204), "FFCC99": (255, 204, 153), "99FFFF": (153, 255, 255),
        "FFCCFF": (255, 204, 255), "CCFFCC": (204, 255, 204), "E9E9E7": (233, 233, 231)}
for nm, (x0, x1, hexc, cells) in EXPECT.items():
    tgt = PALR[hexc]
    bad = []
    for ci in range(1, NCELL + 1):
        mode = cellclass(x0, x1, ci - 1)
        d = sum(abs(mode[k] - tgt[k]) for k in range(3))
        if ci in cells and d > 60: bad.append(f"cell{ci}={mode} should be {hexc}")
        if ci not in cells and sum(abs(mode[k] - 233) for k in range(3)) > 45: bad.append(f"cell{ci}={mode} should be panel")
    if bad:
        fails.append(f"{nm} fills: " + "; ".join(bad[:4]))
    else:
        print(f"fills {nm}: OK ({hexc} at {cells})")

# ---------- bars ----------
graybar = (abs(r - 216) < 14) & (abs(g - 216) < 14) & (abs(b - 216) < 14)
for lbl, xf in [("bar1", 421), ("bar2", 569), ("bar3", 711), ("bar4", 841)]:
    x = int(xf / S)
    col = graybar[:, x - 2:x + 3].sum(axis=1)
    rows_ = np.where(col > 2)[0]
    if not len(rows_):
        fails.append(f"{lbl}: no gray"); continue
    y0, y1 = fx(rows_.min()), fx(rows_.max())
    # x extent at mid-height
    rowm = graybar[int(320 / S), :]
    xs = np.where(rowm)[0]
    x0 = fx(xs.min()) if len(xs) else None
    print(f"{lbl}: y {y0}-{y1} (tgt 178-461)")
    if abs(y0 - 178) > 5 or abs(y1 - 461) > 5: fails.append(f"{lbl} y {y0}-{y1}")
# bar text (blue) in bar1
blue = (b > 120) & (r < 110) & (g < 110)
m = blue[520:900, int(400 / S):int(445 / S)]
ys, xs = np.where(m)
if len(xs):
    print(f"bar1 text: y {fx(ys.min()+520)}-{fx(ys.max()+520)} (tgt 273-363)")
    if abs(fx((ys.min() + ys.max()) / 2 + 520) - 318) > 8: fails.append("bar1 text center off")
else:
    fails.append("bar1 text missing")

# ---------- triangles ----------
lr = (r - g > 35) & (r - b > 35) & (r > 140)
for lbl, xf, ya, yb in [("tri1.edge", 252, 180, 225), ("tri3.edge", 545, 305, 351), ("tri4.edge", 687, 212, 256)]:
    x = int(xf / S)
    seg = lr[int(ya / S) - 4:int(yb / S) + 4, x - 4:x + 5]
    ys, xs = np.where(seg)
    if len(ys) < 10:
        fails.append(f"{lbl}: weak ({len(ys)}px)")
    else:
        print(f"{lbl}: {len(ys)}px OK")

# ---------- block arrow ----------
m = lr[int(290 / S):int(340 / S), int(240 / S):int(320 / S)]
ys, xs = np.where(m)
if len(xs):
    print(f"block arrow: x {fx(xs.min()+240)}-{fx(xs.max()+240)} (tgt 253-305) y {fx(ys.min()+290)}-{fx(ys.max()+290)} (tgt 303.5-325.5)")
    if abs(fx(xs.min() + 240) - 253) > 5 or abs(fx(xs.max() + 240) - 305) > 6: fails.append("block arrow x")
else:
    fails.append("block arrow missing")

# ---------- seq arrow + label ----------
m = lr[int(170 / S):int(470 / S), int(140 / S):int(165 / S)]
ys, xs = np.where(m)
if len(xs):
    print(f"seq arrow zone: x {fx(xs.min()+140)}-{fx(xs.max()+140)} y {fx(ys.min()+170)}-{fx(ys.max()+170)} (tgt 178-459)")
else:
    fails.append("seq arrow missing")
redl = red
m = redl[int(250 / S):int(420 / S), int(120 / S):int(160 / S)]
ys, xs = np.where(m)
if len(xs):
    print(f"seq label: center ({fx((xs.min()+xs.max())/2+120)}, {fx((ys.min()+ys.max())/2+250)}) (tgt 141.5,330.5)")
else:
    fails.append("seq label missing")

# ---------- kernel ----------
sal = (r > 225) & (g > 110) & (g < 200) & (b > 110) & (b < 200)
m = sal[int(90 / S):int(150 / S), int(50 / S):int(150 / S)]
ys, xs = np.where(m)
if len(xs):
    print(f"kernel rects: x {fx(xs.min()+50)}-{fx(xs.max()+50)} (tgt 60-143) y {fx(ys.min()+90)}-{fx(ys.max()+90)} (tgt 98-142)")
else:
    fails.append("kernel rects missing")
m = redl[int(145 / S):int(185 / S), int(50 / S):int(150 / S)]
ys, xs = np.where(m)
if len(xs):
    print(f"kernel label: x {fx(xs.min()+50)}-{fx(xs.max()+50)} (tgt 59-142) y {fx(ys.min()+145)}-{fx(ys.max()+145)} (tgt 155-178)")
    if abs(fx(ys.min() + 145) - 155) > 4: fails.append(f"kernel label top {fx(ys.min()+145)}")
else:
    fails.append("kernel label missing")

# ---------- callout ----------
grn = (g - r > 25) & (g - b > 25) & (g > 110)
m = grn[int(100 / S):int(160 / S), int(420 / S):int(680 / S)]
ys, xs = np.where(m)
if len(xs):
    print(f"callout green: x {fx(xs.min()+420)}-{fx(xs.max()+420)} (tgt 460-653) y {fx(ys.min()+100)}-{fx(ys.max()+100)} (tgt 113-139)")
else:
    fails.append("callout missing")

# ---------- hatch arrow ----------
redl2 = (r > 170) & (g < 140) & (b < 140)
m = redl2[int(640 / S):int(710 / S), int(150 / S):int(850 / S)]
ys, xs = np.where(m)
if len(xs):
    print(f"hatch arrow: x {fx(xs.min()+150)}-{fx(xs.max()+150)} (tgt 176-815) y {fx(ys.min()+640)}-{fx(ys.max()+640)} (tgt 470-496)")
else:
    fails.append("hatch arrow missing")

# ---------- banner ----------
yel = (r > 225) & (g > 225) & (b < 190)
m = yel[int(320 / S):int(520 / S), int(540 / S):int(940 / S)]
ys, xs = np.where(m)
if len(xs):
    bx0, bx1, by0, by1 = fx(xs.min() + 540), fx(xs.max() + 540), fx(ys.min() + 320), fx(ys.max() + 320)
    print(f"banner yellow: x {bx0}-{bx1} (tgt 572-918) y {by0}-{by1} (tgt 341-509)")
    ang = np.degrees(np.arctan2((by1 - by0), (bx1 - bx0)))
    # top-edge slope: per-column min y
    colmin = {}
    for x in range(xs.min(), xs.max(), 20):
        col = np.where(m[:, x])[0]
        if len(col):
            colmin[x + 540] = col.min() + 320
    kx = sorted(colmin)
    if len(kx) > 2:
        import math
        slope = (colmin[kx[-1]] - colmin[kx[0]]) / (kx[-1] - kx[0])
        print(f"banner top-edge slope: {math.degrees(math.atan(slope)):.1f} deg (tgt ~-21)")
else:
    fails.append("banner missing")

# ---------- caption ----------
m = blue[int(495 / S):int(530 / S), int(150 / S):int(860 / S)]
ys, xs = np.where(m)
if len(xs):
    print(f"caption: x {fx(xs.min()+150)}-{fx(xs.max()+150)} (tgt 181-808) y {fx(ys.min()+495)}-{fx(ys.max()+495)} (tgt 506-521)")
    if abs(fx(ys.min() + 495) - 506) > 4: fails.append(f"caption top {fx(ys.min()+495)}")
else:
    fails.append("caption missing")

# ---------- frame containment: no ink outside panel (white margin clean) ----------
# panel: x42-918 frame px -> render x87.5-1912.5, y45->93.75 to bottom
margin_mask = np.ones((H, W), bool)
margin_mask[int(45 * 2.0833):, int(42 * 2.0833):int(918 * 2.0833)] = False
ink = ((r < 200) | (g < 200) | (b < 200)) & margin_mask
ys, xs = np.where(ink)
if len(xs) > 50:
    fails.append(f"ink outside panel: {len(xs)}px at x{fx(xs.min())}-{fx(xs.max())} y{fx(ys.min())}-{fx(ys.max())}")
else:
    print(f"containment: {len(xs)} stray px outside panel (ok if <50)")

print()
if fails:
    print("SELF-CHECK: FAIL")
    for f in fails:
        print("  -", f)
else:
    print("SELF-CHECK: ALL PASS")
