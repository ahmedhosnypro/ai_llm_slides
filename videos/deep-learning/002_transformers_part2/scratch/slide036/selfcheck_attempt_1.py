#!/usr/bin/env python3
"""Pre-judge self-check attempt 1 for slide 036 (17 §2-§8; equations/tables N/A).
Render: qa/slide036/render_2.png (2000x1125 @150dpi; render_px = pt * 150/72).
Banks printed numbers as the QA record."""
import numpy as np
from PIL import Image

R = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide036/render_2.png"
im = np.asarray(Image.open(R).convert("RGB")).astype(int)
H, W = im.shape[:2]
print(f"render {W}x{H}")
S = 150 / 72.0  # pt -> render px
FX = lambda fx: (fx - 18.628) / 0.961231
FY = lambda fy: fy / 0.955556
PX = lambda fx: FX(fx) * S  # frame x -> render px
PY = lambda fy: FY(fy) * S
fails = []

r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]
red = (r > 130) & (g < 110) & (b < 110)
blue = (b > 120) & (r < 110) & (g < 110)
navy = (b > 120) & (b < 200) & (r < 70) & (g < 70)
yel = (r > 220) & (g > 220) & (b < 140)

def ink_bbox(mask, x0, y0, x1, y1, tag, expect, tol=10):
    sub = mask[int(y0):int(y1), int(x0):int(x1)]
    ys, xs = np.where(sub)
    if len(ys) == 0:
        fails.append(f"{tag}: NO ink in region")
        return None
    bx0, bx1, by0, by1 = xs.min() + x0, xs.max() + x0, ys.min() + y0, ys.max() + y0
    ok = all(abs(v - e) <= tol * (1 if i % 2 == 0 else 1) for v, e, i in
             [(bx0, expect[0], 0), (bx1, expect[1], 1), (by0, expect[2], 2), (by1, expect[3], 3)])
    print(f"{tag}: ink x {bx0}..{bx1} y {by0}..{by1} expect x {expect[0]:.0f}..{expect[1]:.0f} y {expect[2]:.0f}..{expect[3]:.0f} {'OK' if ok else 'OFF'}")
    if not ok:
        fails.append(f"{tag}: ink bbox off (got {bx0},{bx1},{by0},{by1} expect {expect})")
    return (bx0, bx1, by0, by1)

# ---- 2. title ink ----
ink_bbox(red, 500, 140, 1650, 240, "title", (PX(306), PX(712), PY(76), PY(99)), tol=14)

# ---- info panel border + fill ----
px0, px1, py0, py1 = PX(95), PX(862), PY(110), PY(334)
sub = blue[int(py0) - 8:int(py1) + 8, int(px0) - 8:int(px1) + 8]
ys, xs = np.where(sub)
print(f"info panel blue border bbox: x {xs.min()+px0-8}..{xs.max()+px0-8} y {ys.min()+py0-8}..{ys.max()+py0-8} (expect {px0:.0f}..{px1:.0f}, {py0:.0f}..{py1:.0f})")
if abs(xs.min() + px0 - 8 - px0) > 8 or abs(xs.max() + px0 - 8 - px1) > 8 or abs(ys.min() + py0 - 8 - py0) > 8 or abs(ys.max() + py0 - 8 - py1) > 8:
    fails.append("info panel border bbox off")
cream = (r > 245) & (g > 245) & (b > 195) & (b < 240)
cfrac = cream[int(py0) + 10:int(py1) - 10, int(px0) + 30:int(px1) - 30].mean()
print(f"info panel cream fill fraction: {cfrac:.2f} (expect >0.8)")
if cfrac < 0.8: fails.append("info panel fill not cream")

# ---- info text lines: band + left edge (tolerance 8 render px) ----
lines = [(119, 105), (137, 181), (156, 182), (196, 105), (215, 182), (256, 105), (274, 146), (293, 227), (312, 144)]
for cap, lx in lines:
    y0, y1 = PY(cap) - 4, PY(cap) + 26
    x0 = PX(lx) - 20
    sub = blue[int(y0):int(y1), int(x0):int(px1)]
    ys, xs = np.where(sub)
    if len(ys) == 0:
        fails.append(f"panel line cap{cap}: no ink")
        continue
    l_ink = xs.min() + x0
    okl = abs(l_ink - PX(lx)) <= 9
    okb = ys.min() + y0 >= PY(cap) - 9 and ys.max() + y0 <= PY(cap) + 28
    print(f"line cap{cap} x{lx}: ink left {l_ink} (expect {PX(lx):.0f}+-9) band y {ys.min()+y0}..{ys.max()+y0} {'OK' if okl and okb else 'OFF'}")
    if not okl: fails.append(f"panel line cap{cap}: left edge off")
    if not okb: fails.append(f"panel line cap{cap}: band off")

# ---- diagram panel border ----
d = (PX(65), PX(892), PY(348), PY(511))
sub = red[int(d[2]) - 8:int(d[3]) + 8, int(d[0]) - 8:int(d[1]) + 8]
ys, xs = np.where(sub)
print(f"diagram red border bbox: x {xs.min()+d[0]-8}..{xs.max()+d[0]-8} y {ys.min()+d[2]-8}..{ys.max()+d[2]-8} (expect {d[0]:.0f}..{d[1]:.0f}, {d[2]:.0f}..{d[3]:.0f})")
if abs(xs.min() + d[0] - 8 - d[0]) > 8 or abs(xs.max() + d[0] - 8 - d[1]) > 8 or abs(ys.min() + d[2] - 8 - d[2]) > 8 or abs(ys.max() + d[2] - 8 - d[3]) > 8:
    fails.append("diagram panel border bbox off")

# ---- banner ----
bnd = (PX(165), PX(884), PY(394), PY(444))
sub = navy[int(bnd[2]) - 6:int(bnd[3]) + 6, int(bnd[0]) - 6:int(bnd[1]) + 6]
ys, xs = np.where(sub)
print(f"banner navy bbox: x {xs.min()+bnd[0]-6}..{xs.max()+bnd[0]-6} y {ys.min()+bnd[2]-6}..{ys.max()+bnd[2]-6} (expect {bnd[0]:.0f}..{bnd[1]:.0f}, {bnd[2]:.0f}..{bnd[3]:.0f})")
if abs(xs.min() + bnd[0] - 6 - bnd[0]) > 8 or abs(xs.max() + bnd[0] - 6 - bnd[1]) > 8 or abs(ys.min() + bnd[2] - 6 - bnd[2]) > 8 or abs(ys.max() + bnd[2] - 6 - bnd[3]) > 8:
    fails.append("banner bbox off")
white = (r > 220) & (g > 220) & (b > 220)
wt = white[int(bnd[2]) + 6:int(bnd[3]) - 6, int(bnd[0]) + 6:int(bnd[1]) - 6]
print(f"banner white-text px: {int(wt.sum())} (expect >200)")
if wt.sum() < 200: fails.append("banner text missing")

# ---- strips: 8 units per band, yellow+green+pink ink; labels red ink ----
units = [(176, 236), (249, 309), (322, 382), (395, 455), (468, 528), (541, 601), (731, 791), (803, 863)]
for tag, (s0, s1, lcy) in (("Y", (360, 376, 368)), ("X", (463, 479, 471))):
    for i, (ux0, ux1) in enumerate(units):
        x0, x1 = PX(ux0), PX(ux1)
        y0, y1 = PY(s0), PY(s1)
        cell = im[int(y0):int(y1), int(x0):int(x1)]
        sat = (np.max(cell, axis=2) - np.min(cell, axis=2)) > 18
        if sat.mean() < 0.3:
            fails.append(f"{tag} unit{i}: slots missing (tint frac {sat.mean():.2f})")
        lab = red[int(y0) - 4:int(y1) + 6, int(x0):int(x1)]
        if lab.sum() < 12:
            fails.append(f"{tag} unit{i} label: red ink missing ({int(lab.sum())}px)")
print("strips: 16 units checked for slot tint + label ink")

# ---- dots ----
for cx in (628.5, 647, 665, 683, 698):
    for cy, msk, tag in ((368, blue, "Ydot"), (470.5, None, "Xdot")):
        if msk is None:
            msk = (g > 150) & (r < 150) & (b < 150)
        sub = msk[int(PY(cy) - 12):int(PY(cy) + 12), int(PX(cx) - 12):int(PX(cx) + 12)]
        if sub.sum() < 8:
            fails.append(f"{tag}@{cx}: missing ({int(sub.sum())}px)")
print("dots: 5 blue + 5 green checked")

# ---- arrows: blue-outline ink columns in both bands ----
for tag, (a0, a1) in (("upper", (378, 395)), ("lower", (445, 461))):
    sub = blue[int(PY(a0)):int(PY(a1)), int(PX(150)):int(PX(890))]
    cols = np.where(sub.sum(axis=0) > 2)[0]
    if len(cols) == 0:
        fails.append(f"{tag} arrows: no ink")
        continue
    runs, s_, p_ = [], cols[0], cols[0]
    for x in cols[1:]:
        if x <= p_ + 6: p_ = x
        else: runs.append((s_, p_)); s_ = p_ = x
    runs.append((s_, p_))
    print(f"{tag} arrows: {len(runs)} column groups (expect 8): {[int(a + PX(150)) for a, b in runs]}")
    if len(runs) != 8: fails.append(f"{tag} arrows: {len(runs)} groups vs 8")

# ---- gutters ----
ink_bbox(blue, int(PX(60)), int(PY(355)), int(PX(175)), int(PY(395)), "gutter-up(blue)", (PX(74), PX(157), PY(361), PY(392)), tol=12)
ink_bbox(red, int(PX(60)), int(PY(440)), int(PX(175)), int(PY(482)), "gutter-dn(red)", (PX(72), PX(153), PY(446), PY(479)), tol=12)

# ---- caption ----
ink_bbox(yel, int(PX(280)), int(PY(484)), int(PX(585)), int(PY(506)), "caption-highlight", (PX(292), PX(573), PY(488), PY(501)), tol=10)
dark = (np.max(im, axis=2) < 150)
ink_bbox(dark, int(PX(285)), int(PY(486)), int(PX(580)), int(PY(504)), "caption-text", (PX(294), PX(570), PY(489), PY(502)), tol=14)

# ---- containment: content ink inside chrome frame ----
# chrome inner area: x 87.5..1914.6, y 93.75..1125 (panel bounds at 150dpi)
cx0, cx1, cy0 = 87.5, 1914.6, 93.75
content = (red | blue | navy | yel)[:, :]
ys, xs = np.where(content)
if xs.min() < cx0 - 3 or xs.max() > cx1 + 3 or ys.min() < cy0 - 3:
    fails.append(f"content escapes chrome: x {xs.min()}..{xs.max()} y {ys.min()}..{ys.max()}")
else:
    print(f"containment vs chrome: ink x {xs.min()}..{xs.max()} y {ys.min()}..{ys.max()} inside ({cx0:.0f}..{cx1:.0f}, {cy0:.0f}..) OK")
# diagram content inside diagram panel
din = (blue | navy | (r > 220) & (g > 220) & (b < 210) & (b > 140))  # blue+navy+pastel
sub = din[int(d[2]) + 4:int(d[3]) - 3, int(d[0]) + 4:int(d[1]) - 3]
ys, xs = np.where(sub)
print(f"diagram interior ink extent: x {xs.min()+d[0]+4}..{xs.max()+d[0]+4} y {ys.min()+d[2]+4}..{ys.max()+d[2]+4} (panel interior {d[0]+4:.0f}..{d[1]-4:.0f}, {d[2]+4:.0f}..{d[3]-4:.0f})")
if xs.min() < 2 or ys.min() < 2:
    fails.append("diagram ink touches panel border")

# ---- 7. wrap check: no ink outside the expected bands ----
# blue ink rows between panel lines (gaps): lines cap tops at FY rows; gaps at
# frame rows 168..195, 229..255, 305..311 must be ink-free (x 100..860)
for (g0, g1, tag) in ((170, 194, "gap1"), (230, 254, "gap2"), (306, 310, "gap3")):
    sub = blue[int(PY(g0)):int(PY(g1)), int(PX(100)):int(PX(855))]
    if sub.sum() > 30:
        fails.append(f"panel {tag}: unexpected blue ink ({int(sub.sum())}px)")
print("wrap gaps checked")

print()
if fails:
    print("SELF-CHECK FAILURES:")
    for f in fails: print("  -", f)
    raise SystemExit(1)
print("SELF-CHECK: ALL PASS")
