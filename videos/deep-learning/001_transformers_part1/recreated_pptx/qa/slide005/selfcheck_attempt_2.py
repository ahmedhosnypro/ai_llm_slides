#!/usr/bin/env python3
"""Self-check attempt 2 (corrected units): render vs frame, all in frame px.
frame_x = win_x0_frame + idx * S, S = 960/2000."""
import numpy as np
from PIL import Image
from collections import Counter
import math

REN = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/qa/slide005/render_2.png"
im = np.asarray(Image.open(REN).convert("RGB")).astype(int)
H, W = im.shape[:2]
S = 960.0 / 2000.0
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]
fails = []

def W2R(v): return int(v / S)  # frame px -> render px

# ---------- title (excluding chrome border rows: render y98+) ----------
red = (r > 140) & (g < 110) & (b < 110)
m = red[100:200, W2R(150):W2R(850)]
ys, xs = np.where(m)
tx0, tx1 = 150 + xs.min() * S, 150 + xs.max() * S
ty0, ty1 = 50 + ys.min() * S, 50 + ys.max() * S
print(f"title: x {tx0:.1f}-{tx1:.1f} (tgt 261-653) y {ty0:.1f}-{ty1:.1f} (tgt 59-76)")
if abs(tx0 - 261) > 10 or abs(tx1 - 653) > 10: fails.append(f"title x {tx0:.0f}-{tx1:.0f}")
if abs(ty0 - 59) > 3: fails.append(f"title cap top {ty0:.1f} vs 59")

# ---------- headers ----------
for nm, xa, xb, txa, txb in [("WV", 165, 245, 179, 223), ("FM1", 300, 400, 323, 384), ("FM2", 450, 545, 466, 531), ("FM3", 590, 690, 605, 669), ("FM4", 730, 825, 747, 811)]:
    m = red[W2R(140):W2R(178), W2R(xa):W2R(xb)]
    ys, xs = np.where(m)
    if not len(xs):
        fails.append(f"header {nm}: no ink"); continue
    x0, x1 = xa + xs.min() * S, xa + xs.max() * S
    y0 = 140 + ys.min() * S
    print(f"header {nm}: x {x0:.1f}-{x1:.1f} (tgt {txa}-{txb}) top {y0:.1f} (tgt 149)")
    if abs((x0 + x1) / 2 - (txa + txb) / 2) > 6: fails.append(f"header {nm} center")
    if abs(y0 - 149) > 3: fails.append(f"header {nm} top {y0:.1f}")

# ---------- grid ----------
def outline_mask(xa, xb, ya, yb):
    win = im[W2R(ya):W2R(yb), W2R(xa):W2R(xb)]
    rr, gg, bb = win[:, :, 0], win[:, :, 1], win[:, :, 2]
    return (abs(rr - 167) < 45) & (abs(gg - 175) < 45) & (abs(bb - 184) < 45)
om = outline_mask(165, 242, 170, 470)
rows = np.where(om.sum(axis=1) > (W2R(242) - W2R(165)) * 0.55)[0]
gy0, gy1 = 170 + rows.min() * S, 170 + rows.max() * S
print(f"grid: top {gy0:.1f} (tgt 178.5) bottom {gy1:.1f} (tgt 462.5) lines {len(rows)} (tgt 19)")
if abs(gy0 - 178.5) > 4 or abs(gy1 - 462.5) > 4: fails.append(f"grid y {gy0:.0f}-{gy1:.0f}")
if len(rows) < 17: fails.append(f"grid lines {len(rows)}")

# ---------- fills (banner-crossed cells whitelisted) ----------
TOP, PITCH, NCELL = 178.5, (462.5 - 178.5) / 18, 18
PALR = {"FFFFCC": (255, 255, 204), "FFCC99": (255, 204, 153), "99FFFF": (153, 255, 255),
        "FFCCFF": (255, 204, 255), "CCFFCC": (204, 255, 204)}
EXPECT = {"WV": (163, 244, "FFFFCC", [1, 2, 3]), "FM1": (308, 390, "FFCC99", [3, 14, 15, 16]),
          "FM2": (456, 537, "99FFFF", [9, 10, 11, 15]), "FM3": (598, 679, "FFCCFF", [3, 4, 5, 10]),
          "FM4": (737, 818, "CCFFCC", [4, 14])}
BANNER_CELLS = {("FM3", 18), ("FM4", 15), ("FM4", 16), ("FM4", 17)}
for nm, (x0, x1, hexc, cells) in EXPECT.items():
    tgt = PALR[hexc]
    bad = []
    for ci in range(1, NCELL + 1):
        if (nm, ci) in BANNER_CELLS:
            continue
        y0 = W2R(TOP + PITCH * (ci - 1)) + 5
        y1 = W2R(TOP + PITCH * ci) - 5
        patch = im[y0:y1, W2R(x0) + 8:W2R(x1) - 8].reshape(-1, 3)
        mode = Counter(tuple(int(v) // 16 * 16 for v in p) for p in patch).most_common(1)[0][0]
        if ci in cells:
            if sum(abs(mode[k] - tgt[k]) for k in range(3)) > 60:
                bad.append(f"cell{ci}={mode} want {hexc}")
        else:
            if sum(abs(mode[k] - 233) for k in range(3)) > 45:
                bad.append(f"cell{ci}={mode} want panel")
    if bad: fails.append(f"{nm} fills: " + "; ".join(bad[:4]))
print("fills: checked (banner cells whitelisted)")

# ---------- bars ----------
graybar = (abs(r - 216) < 14) & (abs(g - 216) < 14) & (abs(b - 216) < 14)
for lbl, xf in [("bar1", 421), ("bar2", 569), ("bar3", 711), ("bar4", 841)]:
    col = graybar[W2R(170):W2R(468), W2R(xf) - 2:W2R(xf) + 3].sum(axis=1)
    rows_ = np.where(col > 2)[0]
    y0, y1 = 170 + rows_.min() * S, 170 + rows_.max() * S
    print(f"{lbl}: y {y0:.1f}-{y1:.1f} (tgt 178-461)")
    if abs(y0 - 178) > 5 or abs(y1 - 461) > 5: fails.append(f"{lbl} y {y0:.0f}-{y1:.0f}")
blue = (b > 120) & (r < 110) & (g < 110)
m = blue[W2R(260):W2R(380), W2R(405):W2R(440)]
ys, xs = np.where(m)
bt0, bt1 = 260 + ys.min() * S, 260 + ys.max() * S
print(f"bar1 text: y {bt0:.1f}-{bt1:.1f} (tgt 273-363)")
if abs((bt0 + bt1) / 2 - 318) > 8 or abs((bt1 - bt0) - 90) > 12: fails.append(f"bar1 text y {bt0:.0f}-{bt1:.0f}")

# ---------- triangles (edges + apex ink) ----------
lr = (r - g > 35) & (r - b > 35) & (r > 140)
for lbl, xf, ya, yb, ax, ay in [("tri1", 252, 180, 225, 306, 218), ("tri3", 545, 305, 351, 596, 328), ("tri4", 687, 212, 256, 737, 233)]:
    seg = lr[W2R(ya) - 3:W2R(yb) + 3, W2R(xf) - 3:W2R(xf) + 4]
    n_edge = (seg).sum()
    apex = lr[W2R(ay) - 4:W2R(ay) + 5, W2R(ax) - 6:W2R(ax) + 3].sum()
    print(f"{lbl}: edge px {n_edge}, apex px {apex}")
    if n_edge < 60: fails.append(f"{lbl} edge weak {n_edge}")
    if apex < 3: fails.append(f"{lbl} apex missing")

# ---------- block arrow ----------
m = lr[W2R(295):W2R(335), W2R(245):W2R(315)]
ys, xs = np.where(m)
bx0, bx1, by0, by1 = 245 + xs.min() * S, 245 + xs.max() * S, 295 + ys.min() * S, 295 + ys.max() * S
print(f"block arrow: x {bx0:.1f}-{bx1:.1f} (tgt 253-305) y {by0:.1f}-{by1:.1f} (tgt 303.5-325.5)")
if abs(bx0 - 253) > 5 or abs(bx1 - 305) > 7 or abs(by0 - 303.5) > 5 or abs(by1 - 325.5) > 5:
    fails.append(f"block arrow {bx0:.0f}-{bx1:.0f},{by0:.0f}-{by1:.0f}")

# ---------- seq arrow ----------
m = lr[W2R(170):W2R(470), W2R(146):W2R(160)]
ys, xs = np.where(m)
sy0, sy1 = 170 + ys.min() * S, 170 + ys.max() * S
print(f"seq shaft+head: x {146 + xs.min() * S:.1f}-{146 + xs.max() * S:.1f} y {sy0:.1f}-{sy1:.1f} (tgt 178-459)")
if abs(sy0 - 178) > 5 or abs(sy1 - 459) > 5: fails.append(f"seq y {sy0:.0f}-{sy1:.0f}")

# ---------- kernel ----------
sal = (r > 225) & (g > 110) & (g < 200) & (b > 110) & (b < 200)
m = sal[W2R(90):W2R(150), W2R(50):W2R(150)]
ys, xs = np.where(m)
print(f"kernel rects: x {50 + xs.min() * S:.1f}-{50 + xs.max() * S:.1f} (tgt 60-143) y {90 + ys.min() * S:.1f}-{90 + ys.max() * S:.1f} (tgt 98-142)")
m = red[W2R(148):W2R(185), W2R(50):W2R(150)]
ys, xs = np.where(m)
ky0 = 148 + ys.min() * S
print(f"kernel label: x {50 + xs.min() * S:.1f}-{50 + xs.max() * S:.1f} (tgt 59-142) top {ky0:.1f} (tgt 155)")
if abs(ky0 - 155) > 3: fails.append(f"kernel label top {ky0:.1f}")

# ---------- callout ----------
grn = (g - r > 25) & (g - b > 25) & (g > 110)
m = grn[W2R(100):W2R(160), W2R(395):W2R(680)]
ys, xs = np.where(m)
cx0, cx1, cy0, cy1 = 395 + xs.min() * S, 395 + xs.max() * S, 100 + ys.min() * S, 100 + ys.max() * S
print(f"callout: x {cx0:.1f}-{cx1:.1f} (tgt 403leader-653) y {cy0:.1f}-{cy1:.1f} (tgt 113-151)")
if abs(cy0 - 113) > 4 or abs(cy1 - 151) > 5 or abs(cx1 - 653) > 5: fails.append(f"callout {cx0:.0f}-{cx1:.0f},{cy0:.0f}-{cy1:.0f}")

# ---------- hatch ----------
redl = (r > 150) & (g < 160) & (b < 160) & (r - g > 40)
m = redl[W2R(468):W2R(500), W2R(180):W2R(812)]
ys, xs = np.where(m)
if len(xs) < 500:
    fails.append(f"hatch body weak: {len(xs)}px")
else:
    print(f"hatch body: {len(xs)} red px, x {180 + xs.min() * S:.1f}-{180 + xs.max() * S:.1f} y {468 + ys.min() * S:.1f}-{468 + ys.max() * S:.1f}")
m2 = redl[W2R(468):W2R(500), W2R(780):W2R(818)]
print(f"hatch head: {m2.sum()} red px (tgt >100)")
if m2.sum() < 100: fails.append("hatch head missing")
# white body present between stripes?
m3 = ((r > 245) & (g > 245) & (b > 245))[W2R(478):W2R(490), W2R(200):W2R(700)]
print(f"hatch white body: {m3.sum()} px (tgt >3000)")
if m3.sum() < 3000: fails.append("hatch white body missing")

# ---------- banner ----------
yel = (r > 225) & (g > 225) & (b < 190)
m = yel[W2R(330):W2R(520), W2R(540):W2R(940)]
ys, xs = np.where(m)
bx0, bx1, by0, by1 = 540 + xs.min() * S, 540 + xs.max() * S, 330 + ys.min() * S, 330 + ys.max() * S
print(f"banner yellow AABB: x {bx0:.1f}-{bx1:.1f} (tgt 572-918) y {by0:.1f}-{by1:.1f} (tgt 341-509)")
if abs(bx0 - 572) > 10 or abs(bx1 - 918) > 10 or abs(by0 - 341) > 10 or abs(by1 - 509) > 10:
    fails.append(f"banner AABB {bx0:.0f}-{bx1:.0f},{by0:.0f}-{by1:.0f}")
mb = blue[W2R(330):W2R(520), W2R(540):W2R(940)]
ysb, xsb = np.where(mb)
if len(xsb) < 100:
    fails.append("banner text missing")
else:
    print(f"banner text: {len(xsb)} blue px, x {540 + xsb.min() * S:.1f}-{540 + xsb.max() * S:.1f} (tgt 564-909)")

# ---------- caption + underline ----------
m = blue[W2R(498):W2R(530), W2R(150):W2R(860)]
ys, xs = np.where(m)
cx0, cx1, cy0, cy1 = 150 + xs.min() * S, 150 + xs.max() * S, 498 + ys.min() * S, 498 + ys.max() * S
print(f"caption: x {cx0:.1f}-{cx1:.1f} (tgt 181-808) y {cy0:.1f}-{cy1:.1f} (tgt 506-521)")
if abs(cx0 - 181) > 12 or abs(cx1 - 808) > 12: fails.append(f"caption x {cx0:.0f}-{cx1:.0f}")
if abs(cy0 - 506) > 4: fails.append(f"caption top {cy0:.1f}")
# underline: long blue runs 2-5px below the text baseline (frame y518-522)
ul = 0
for yy in range(W2R(517), W2R(523)):
    rowxs = np.where(blue[yy, W2R(150):W2R(860)])[0]
    if len(rowxs):
        runs_, s_, p_ = [], rowxs[0], rowxs[0]
        for x in rowxs[1:]:
            if x == p_ + 1: p_ = x
            else: runs_.append(p_ - s_); s_ = p_ = x
        runs_.append(p_ - s_)
        ul = max(ul, max(runs_) * S)
print(f"caption underline longest run: {ul:.1f}px (tgt ~250)")
if ul < 120: fails.append(f"underline weak {ul:.0f}px")

# ---------- containment (border AA excluded by 3px inset) ----------
margin = np.ones((H, W), bool)
margin[W2R(48):, W2R(45):W2R(915)] = False
ink = ((r < 200) | (g < 200) | (b < 200)) & margin
ys, xs = np.where(ink)
print(f"stray ink outside panel: {len(xs)} px")
if len(xs) > 200:
    fails.append(f"ink outside panel {len(xs)}px x{150 + 0}-{0}")

print()
if fails:
    print("SELF-CHECK 2: FAIL")
    for f in fails: print("  -", f)
else:
    print("SELF-CHECK 2: ALL PASS")
