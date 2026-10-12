#!/usr/bin/env python3
"""Slide 038 — pre-judge self-check, attempt 1 (150dpi render_1.png, 2000x1125).
1px @150dpi = 1/200 in = 0.36 slide pt. slide_pt * 150/72 = render px."""
import numpy as np
from PIL import Image

R = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide038/render_1.png"
img = np.asarray(Image.open(R).convert("RGB")).astype(int)
H, W = img.shape[:2]
S = 150 / 72.0  # render px per slide pt
px = lambda p: int(round(p * S))
fails, notes = [], []

print(f"render {W}x{H}")
r, g, b = img[:, :, 0], img[:, :, 1], img[:, :, 2]
ink = (r < 205) | (g < 205) | (b < 205)

def band_ink_rows(x0, x1, y0, y1, thresh=2):
    seg = ink[px(y0):px(y1), px(x0):px(x1)]
    prof = seg.sum(axis=1)
    rows = np.where(prof > thresh)[0]
    return (rows.min() + px(y0), rows.max() + px(y0)) if len(rows) else None

def near(c, target, tol):
    return all(abs(int(c[i]) - target[i]) <= tol for i in range(3))

# ---- A. gap band between defbox bottom (246.9) and diagram panel top (260.5):
#        only chrome gray E9E9E7 expected (borders excluded by insetting 2.5pt)
seg = img[px(249.5):px(258), px(60):px(900)]
dark = ((seg[:, :, 0] < 180) | (seg[:, :, 1] < 180) | (seg[:, :, 2] < 180)).sum()
print(f"A defbox/panel gap dark px: {dark}")
if dark > 40: fails.append(f"A: {dark} dark px in defbox-panel gap band")

# ---- B. containment: defbox TEXT ink fully inside the defbox border ----
bb = band_ink_rows(85, 872, 118, 244)
print(f"B defbox-text ink rows (inside borders): {bb}")
if bb and (bb[0] < px(117) - 3 or bb[1] > px(245) + 3):
    fails.append(f"B: defbox text ink outside box: {bb}")
# blue line count inside defbox (5 text lines expected, no wrap)
blue = (b > 130) & (r < 110) & (g < 110)
seg = blue[px(117):px(246), px(85):px(870)]
prof = seg.sum(axis=1)
runs, inr = [], False
for i, v in enumerate(prof):
    if v > 3 and not inr: s = i; inr = True
    elif v <= 3 and inr:
        if i - s >= 4: runs.append((s, i))
        inr = False
print(f"B defbox blue text bands: {len(runs)}")
if len(runs) != 5: fails.append(f"B: defbox shows {len(runs)} text bands (want 5 — wrap?)")

# ---- C. diagram panel: content ink vs panel bounds (48.2..909.6, 260.5..534.8) ----
panel_ink_rows = band_ink_rows(70, 890, 262, 533)
print(f"C panel content ink rows: {panel_ink_rows} (px; panel inner = {px(262)}..{px(533)})")
if panel_ink_rows and (panel_ink_rows[0] < px(262) - 4 or panel_ink_rows[1] > px(533) + 4):
    fails.append(f"C: panel content exceeds panel: {panel_ink_rows}")

# ---- D. container: gray bar + plus row inside container (62.8..903.4, 297.2..377.8) ----
gb = band_ink_rows(160, 890, 301, 374)
print(f"D container content ink rows: {gb} (px; container inner = {px(297.2)}..{px(377.8)})")
if gb and (gb[0] < px(300) or gb[1] > px(375.5)):
    fails.append(f"D: container content exceeds container: {gb}")

# ---- E. color samples ----
def sample(xpt, ypt):
    return tuple(img[px(ypt), px(xpt)])
red = (r > 130) & (g < 110) & (b < 110)
checks = [
    ("navy block", sample(526, 445), (0, 0, 139), 70),
    ("gray bar", sample(500, 322), (217, 217, 217), 30),
    ("cell1 yellow", sample(251.5, 274.5), (255, 255, 0), 70),
    ("cell2 green", sample(264.0, 274.5), (146, 208, 80), 80),
    ("cell3 pink", sample(276.5, 274.5), (255, 153, 153), 70),
    ("cell4 gray", sample(289.0, 274.5), (217, 217, 217), 40),
    ("dot top blue", sample(634.6, 281.0), (0, 0, 204), 90),
    ("dot x green", sample(634.6, 498.6), (0, 176, 80), 90),
    ("plus ring", sample(194.9, 349.6), (192, 0, 0), 90),
    ("caption hl", sample(410, 518.0), (255, 255, 0), 40),
]
# title: count red ink in the title band (robust vs single-pixel gaps)
tseg = red[px(60):px(105), px(150):px(890)]
print(f"E title red ink px: {int(tseg.sum())}")
if tseg.sum() <= 150: fails.append("E: title red ink missing")
for name, c, t, tol in checks:
    ok = near(c, t, tol)
    print(f"E {name}: {c} vs {t} tol {tol} -> {'OK' if ok else 'FAIL'}")
    if not ok: fails.append(f"E: {name} color {c} vs {t}")

# ---- F. vertical structure bands (raw render px; 1pt = 2.0833px) ----
navy = (b > 100) & (r < 80) & (g < 80) & (b - r > 50)
seg = navy[700:1050, px(200):px(850)]
prof = seg.sum(axis=1)
rows = np.where(prof > 400)[0]
if len(rows):
    print(f"F navy band px rows {rows.min()+700}..{rows.max()+700} (expect ~{px(419.6)}..{px(470.9)})")
    if abs(rows.min() + 700 - px(419.6)) > 8 or abs(rows.max() + 700 - px(470.9)) > 8:
        fails.append(f"F: navy band {rows.min()+700}..{rows.max()+700} vs {px(419.6)}..{px(470.9)}")
else:
    fails.append("F: navy block not found")
gray = (abs(r - g) < 7) & (abs(g - b) < 7) & (r > 208) & (r < 226)
seg = gray[600:760, px(300):px(700)]
prof = seg.sum(axis=1)
rows = np.where(prof > 250)[0]
if len(rows):
    print(f"F gray bar px rows {rows.min()+600}..{rows.max()+600} (expect ~{px(309.8)}..{px(334.9)})")
    if abs(rows.min() + 600 - px(309.8)) > 8 or abs(rows.max() + 600 - px(334.9)) > 8:
        fails.append(f"F: gray band {rows.min()+600}..{rows.max()+600}")
else:
    fails.append("F: gray bar not found")

# ---- G. plus-row red clusters at the 8 column centers ----
seg = red[px(350):px(364), px(150):px(890)]
prof = seg.sum(axis=0)
runs, inr = [], False
for i, v in enumerate(prof):
    if v > 2 and not inr: s = i; inr = True
    elif v <= 2 and inr:
        if i - s >= 5: runs.append(((s + px(150)) / S, (i + px(150)) / S))
        inr = False
centers = [round((a + c) / 2, 1) for a, c in runs]
print(f"G plus-circle clusters: {len(runs)} centers {centers}")
print(f"  expected centers: {T.cols if False else [194.9, 270.3, 346.3, 422.8, 499.8, 574.1, 771.8, 848.8]}")
if len(runs) != 8: fails.append(f"G: found {len(runs)} plus circles (want 8)")
exp = [194.9, 270.3, 346.3, 422.8, 499.8, 574.1, 771.8, 848.8]
if len(centers) == 8:
    for c, e in zip(centers, exp):
        if abs(c - e) > 4: fails.append(f"G: plus center {c} vs {e}")

# ---- H. arrow presence: red arrowheads between top bars and gray bar; green; navy ----
seg = red[px(291):px(309), px(150):px(890)]
n_red_arrows = len([1 for i in range(0, seg.shape[1]) if seg[:, i].sum() > 1])
print(f"H red-arrow ink columns in band: {n_red_arrows}")
if n_red_arrows < 8: fails.append(f"H: red arrows missing ({n_red_arrows} cols)")
green = (g > 120) & (g - r > 40) & (g - b > 40)
seg = green[px(337):px(349), px(150):px(890)]
n_green = int((seg.sum(axis=0) > 1).sum())
print(f"H green-arrow ink columns in band: {n_green}")
if n_green < 8: fails.append(f"H: green arrows missing ({n_green})")
seg = navy[px(366):px(382), px(150):px(890)]
n_navy = int((seg.sum(axis=0) > 1).sum())
print(f"H navy-arrow ink columns in band: {n_navy}")
if n_navy < 8: fails.append(f"H: navy arrows missing ({n_navy})")
# block arrows (navy outlines) above navy block and below it
seg = navy[px(401):px(418), px(150):px(890)]
n_blk = int((seg.sum(axis=0) > 1).sum())
print(f"H block-arrow (mid) ink cols: {n_blk}")
if n_blk < 16: fails.append(f"H: block arrows above navy missing ({n_blk})")
orange = (r > 140) & (g > 50) & (g < 190) & (b < 120) & (r - b > 70)
seg = orange[px(410):px(490), px(120):px(220)]
n_or = int((seg.sum(axis=0) > 0).sum())
print(f"H orange col1 curve ink cols: {n_or}")
if n_or < 5: fails.append(f"H: orange curves missing ({n_or})")

# ---- I. caption text present (red ink inside highlight band) ----
seg = red[px(517):px(531), px(265):px(556)]
print(f"I caption red px: {seg.sum()}")
if seg.sum() < 200: fails.append("I: caption text missing/thin")

# ---- J. title position ----
seg = red[px(60):px(105), px(150):px(890)]
prof = seg.sum(axis=1)
rows = np.where(prof > 3)[0]
cols = np.where(seg.sum(axis=0) > 0)[0]
if len(rows):
    t0, t1 = (rows.min() + px(60)) / S, (rows.max() + px(60)) / S
    c0, c1 = (cols.min() + px(150)) / S, (cols.max() + px(150)) / S
    print(f"J title ink y {t0:.1f}..{t1:.1f} x {c0:.1f}..{c1:.1f} (target y 74.3..94.2 x 232.4..788.9)")
    if abs((c0 + c1) / 2 - 510.2) > 6: fails.append(f"J: title cx {(c0+c1)/2:.1f} vs 510.2")
    if abs(t0 - 74.3) > 5: fails.append(f"J: title cap top {t0:.1f} vs 74.3")
else:
    fails.append("J: title not found")

print()
if fails:
    print("SELF-CHECK: FAIL")
    for f in fails: print("  -", f)
    raise SystemExit(1)
print("SELF-CHECK: PASS (all bands/colors/structures within tolerance)")
