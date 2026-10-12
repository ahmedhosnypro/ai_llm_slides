#!/usr/bin/env python3
"""Closed-loop self-check for slide 004 (150dpi render vs original frame), rev 2.

Render: 2000x1125 at 150dpi; original frame 960x540 (1px=1pt). Scale: *2.0833 render px per frame px.
Tolerance: 6 render px (~2.9 frame px) on edges, 8 render px on arrow centerline (mid-curve
sampling smear); head tips 2.5. Fixes vs rev 1: box targets = measured box edges (not search
window), fill sampled from a text-free patch, arrow centerline bounded above the head base,
containment run on content masks only (chrome + documented bar overhang excluded).
"""
import numpy as np
from PIL import Image
from collections import Counter

REN = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/qa/slide004/render_1.png"
ORIG = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_004.jpg"
S = 150 / 72.0

def load(p):
    return np.asarray(Image.open(p).convert("RGB")).astype(int)

ren = load(REN)
orig = load(ORIG)
fails, notes = [], []

def check(name, got, want, tol=6.0):
    d = abs(got - want)
    (notes if d <= tol else fails).append(f"{name}: got {got:.1f} want {want:.1f} (d={d:.1f})")

def clusters(idx, gap=6):
    out = []
    if not len(idx):
        return out
    s = p = idx[0]
    for i in idx[1:]:
        if i <= p + gap:
            p = i
        else:
            out.append((s, p)); s = p = i
    out.append((s, p))
    return out

def box_check(img, scale, tag, mask_fn, wx0, wy0, wx1, wy1, tx0, ty0, tx1, ty1, fill_xy):
    r, g, b = img[:, :, 0], img[:, :, 1], img[:, :, 2]
    m = mask_fn(r, g, b)
    x0, y0, x1, y1 = int(wx0 * scale), int(wy0 * scale), int(wx1 * scale), int(wy1 * scale)
    sub = m[y0:y1, x0:x1]
    ys, xs = np.where(sub)
    if not len(ys):
        fails.append(f"{tag}: EMPTY in search window"); return
    rowc = Counter(ys); colc = Counter(xs)
    rows = [y for y, n in rowc.items() if n > (xs.max() - xs.min()) * 0.9]
    cols = [x for x, n in colc.items() if n > (ys.max() - ys.min()) * 0.9]
    gx0, gx1 = cols[0] + x0, cols[-1] + x0
    gy0, gy1 = rows[0] + y0, rows[-1] + y0
    check(f"{tag}.left", gx0, tx0 * scale)
    check(f"{tag}.right", gx1, tx1 * scale)
    check(f"{tag}.top", gy0, ty0 * scale)
    check(f"{tag}.bottom", gy1, ty1 * scale)
    fx, fy = fill_xy
    patch = img[int((fy - 4) * scale):int((fy + 4) * scale), int((fx - 6) * scale):int((fx + 6) * scale)].reshape(-1, 3)
    modal = Counter(map(tuple, patch)).most_common(1)[0][0]
    notes.append(f"{tag}: edges frame ({gx0/scale:.1f},{gy0/scale:.1f})..({gx1/scale:.1f},{gy1/scale:.1f}); fill modal {modal}")

redm = lambda r, g, b: (abs(r - 159) < 35) & (g < 50) & (b < 50)
bluem = lambda r, g, b: (b > 110) & (r < 75) & (g < 75)
greenm = lambda r, g, b: (g > 100) & (g < 210) & (r < 100) & (b < 120) & (g - r > 40) & (g - b > 30)

# window, then TARGET edges, then a text-free fill sample point (frame px)
box_check(ren, S, "redbox", redm, 250, 100, 670, 215, 270, 121, 650, 194, (295, 133))
box_check(ren, S, "bluebox", bluem, 100, 255, 430, 375, 121, 275, 406, 350, (140, 285))
box_check(ren, S, "greenbox", greenm, 470, 255, 795, 375, 492, 275, 770, 350, (510, 285))

# ---- black bar
r, g, b = ren[:, :, 0], ren[:, :, 1], ren[:, :, 2]
black = (r < 60) & (g < 60) & (b < 60)
rows_b = np.where(black.sum(axis=1) > 800)[0]
check("bar.top", rows_b.min(), 519 * S, 5)
rb_ = black[rows_b.min():rows_b.min() + 5]
cols_b = np.where(rb_.sum(axis=0) >= 3)[0]
check("bar.left", cols_b.min(), 38 * S, 5)
check("bar.right", cols_b.max(), (921 + 1) * S, 5)  # built to 922 (x38 + w884); orig ink to 921

# ---- text bands
white = (r > 190) & (g > 190) & (b > 190)
def text_check(tag, fx0, fx1, fy0, fy1, want_base, want_x0, want_x1):
    x0, x1, y0, y1 = int(fx0 * S), int(fx1 * S), int(fy0 * S), int(fy1 * S)
    sub = white[y0:y1, x0:x1]
    ys, xs = np.where(sub)
    if not len(ys):
        fails.append(f"{tag}: NO white ink"); return
    bots = []
    for x in range(xs.min(), xs.max() + 1):
        col = np.where(sub[:, x])[0]
        if len(col):
            bots.append(col.max())
    base = Counter(bots).most_common(1)[0][0] + y0
    check(f"{tag}.baseline", base, want_base * S, 5)
    check(f"{tag}.x0", xs.min() + x0, want_x0 * S)
    check(f"{tag}.x1", xs.max() + x0, want_x1 * S)
    notes.append(f"{tag}: ink y {ys.min()+y0}..{ys.max()+y0} x {xs.min()+x0}..{xs.max()+x0} (render px)")

text_check("parent.txt", 280, 645, 130, 190, 167, 312, 606)
text_check("blue.L1", 130, 400, 280, 313, 306, 195, 330)
text_check("blue.L2", 130, 400, 313, 350, 335, 160, 366)
text_check("green.L1", 500, 765, 280, 313, 306, 563, 698)
text_check("green.L2", 500, 765, 313, 350, 335, 515, 747)

# ---- arrow centerline: point-to-ink distance. Original centerline points (per-row AND
# per-column extraction, covering both the steep and the near-horizontal sections) must lie
# within 4 frame px of the RENDER's stroke ink.
arrm_ren = (r > 100) & (r < 200) & (g < 75) & (b < 80)
ro, go, bo = orig[:, :, 0], orig[:, :, 1], orig[:, :, 2]
arrm_org = (ro > 100) & (go < 70) & (bo < 75)
ren_ink_yx = np.where(arrm_ren)
ren_ink = np.stack([ren_ink_yx[0] / S, ren_ink_yx[1] / S], axis=1)  # frame px coords

def centerline_pts(mask, side, x_lo=100, x_hi=880, y_lo=197, y_hi=262):
    pts = {}
    for y in range(y_lo, y_hi):
        xs = np.where(mask[y, x_lo:x_hi])[0] + x_lo
        if not len(xs):
            continue
        cl = clusters(xs, gap=8)
        c = cl[0] if side == "L" else cl[-1]
        if c[1] - c[0] <= 6:
            pts[(y, (c[0] + c[1]) / 2.0)] = None
    for x in range(x_lo, x_hi):
        ys = np.where(mask[y_lo:y_hi, x])[0] + y_lo
        if not len(ys):
            continue
        cl = clusters(ys, gap=8)
        c = cl[0] if side == "L" else cl[-1]
        if c[1] - c[0] <= 6:
            pts[((c[0] + c[1]) / 2.0, x)] = None
    return np.array(sorted(pts))

from scipy.spatial import cKDTree
tree = cKDTree(ren_ink)
for tag, side in [("arrowL", "L"), ("arrowR", "R")]:
    pts = centerline_pts(arrm_org, side)
    d, _ = tree.query(pts)
    mean, mx = d.mean(), d.max()
    (notes if mx <= 4.0 else fails).append(
        f"{tag}: orig centerline -> render ink dist max {mx:.2f} frame px (mean {mean:.2f}, n={len(pts)})")

# ---- arrowheads
for tag, fx0, fx1 in [("headL", 255, 276), ("headR", 620, 640)]:
    x0, x1, y0, y1 = int(fx0 * S), int(fx1 * S), int(256 * S), int(274.9 * S)
    sub = arrm_ren[y0:y1, x0:x1]
    ys, xs = np.where(sub)
    if not len(ys):
        fails.append(f"{tag}: NO head ink")
    else:
        check(f"{tag}.tip_y", (ys.max() + y0) / S, 274.5, 2.5)
        notes.append(f"{tag}: ink y {(ys.min()+y0)/S:.1f}..{(ys.max()+y0)/S:.1f} x {(xs.min()+x0)/S:.1f}..{(xs.max()+x0)/S:.1f} (frame px)")

# ---- containment: COLORED content ink (boxes+bar+arrows+heads) inside the panel interior,
# excluding chrome stroke bands and the documented bar overhang (x 36..924 frame).
content = arrm_ren | black
allowed = np.zeros_like(content)
allowed[int(47 * S):int(537 * S), int(44 * S):int(917 * S)] = True
allowed[int(41 * S):int(50 * S), :] = True        # chrome top border band
allowed[:, int(38 * S):int(47 * S)] = True        # chrome left border band
allowed[:, int(913 * S):int(923 * S)] = True      # chrome right border band
allowed[int(534 * S):, :] = True                  # chrome bottom stroke band
allowed[int(518 * S):int(539 * S), int(36 * S):int(924 * S)] = True  # bar overhang
stray = content & ~allowed
stray_rows = np.where(stray.sum(axis=1) > 6)[0]
stray_cols = np.where(stray.sum(axis=0) > 6)[0]
if len(stray_rows) or len(stray_cols):
    fails.append(f"containment: stray content rows {stray_rows[:5]} cols {stray_cols[:5]}")
else:
    notes.append(f"containment: colored content inside panel ({int(stray.sum())} scattered halo px)")

print("=== PASS lines ===")
for n in notes:
    print("  ok:", n)
print("=== FAILS ===" if fails else "=== NO FAILS ===")
for f in fails:
    print("  FAIL:", f)
raise SystemExit(1 if fails else 0)
