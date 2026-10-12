#!/usr/bin/env python3
"""selfcheck_attempt_1.py (v2) — closed-loop verification of render_1.png (2001x1125,
150dpi) against the frame-measured geometry. Tolerance ~4px @150dpi (= ~2 frame px).
v2: word-level bullet grouping, blue-classifier note borders, numeral ink checks,
corrected title baseline expectation (original ink bottom = 100 incl comma descender)."""
from PIL import Image
import numpy as np

R = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/qa/slide044/render_1.png"
im = Image.open(R).convert("RGB")
a = np.asarray(im).astype(int)
H, W = a.shape[:2]
S = W / 960.0
print(f"render {W}x{H} scale {S:.4f}")

ok_all = True
def check(name, got, want, tol, unit="fpx"):
    global ok_all
    if isinstance(got, (tuple, list)):
        d = max(abs(g - w) for g, w in zip(got, want))
    else:
        d = abs(got - want)
    ok = d <= tol
    ok_all &= ok
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}: got {got} want {want} (max dev {d:.1f} {unit}, tol {tol})")

def runs(mask_1d, min_len=1):
    idx = np.where(mask_1d)[0]
    if len(idx) == 0:
        return []
    out, s, p = [], idx[0], idx[0]
    for v in idx[1:]:
        if v == p + 1:
            p = v
        else:
            if p - s + 1 >= min_len:
                out.append((s, p))
            s = p = v
    if p - s + 1 >= min_len:
        out.append((s, p))
    return out

Rc, Gc, Bc = a[..., 0], a[..., 1], a[..., 2]

# ---- 1) title ----
redm = (Rc > 140) & (Gc < 110) & (Bc < 110)
tm = redm.copy()
tm[:int(55 * S)] = False
tm[int(112 * S):] = False
tm[:, :int(70 * S)] = False
tm[:, int(880 * S):] = False
ys, xs = np.where(tm)
print("TITLE (original ink x211..751 y68..100):")
check("ink bbox", (xs.min() / S, xs.max() / S, ys.min() / S, ys.max() / S), (211, 751, 68, 100), 4)
check("ink center x", (xs.min() + xs.max()) / 2 / S, 481, 4)

# ---- 2) inner content frame (red strokes near x77/x885, excluding panel chrome) ----
print("FRAME (stroke centers 77/885/122/386):")
fm = redm.copy()
fm[:int(110 * S)] = False
fm[int(420 * S):] = False
colc = fm.sum(axis=0)
vr = [(s, e) for s, e in runs(colc >= int(150 * S), min_len=1) if 60 * S < (s + e) / 2 < 900 * S]
rowc = fm.sum(axis=1)
hr = [(s, e) for s, e in runs(rowc >= int(500 * S), min_len=1) if 100 * S < (s + e) / 2 < 420 * S]
check("left stroke center", (vr[0][0] + vr[0][1]) / 2 / S, 77, 4)
check("right stroke center", (vr[-1][0] + vr[-1][1]) / 2 / S, 885, 4)
check("top stroke center", (hr[0][0] + hr[0][1]) / 2 / S, 122, 4)
check("bottom stroke center", (hr[-1][0] + hr[-1][1]) / 2 / S, 386, 4)

# ---- 3) grids ----
print("GRID 7x7 (ink 101..378 x 173..383):")
sub = a[int(165 * S):int(380 * S), int(85 * S):int(390 * S)]
ink = (sub[..., 0] < 200) | (sub[..., 1] < 200) | (sub[..., 2] < 200)
ys, xs = np.where(ink)
check("g77 ink bbox", (xs.min() / S + 85, xs.max() / S + 85, ys.min() / S + 165, ys.max() / S + 165),
      (101, 378, 173, 383), 4)
for label, (sx, sy), want in [("ring fill r1c1", (120, 188), (14, 191, 233)),
                              ("interior fill r4c4", (260, 297), (14, 202, 82))]:
    px_ = a[int(sy * S) - 2:int(sy * S) + 3, int(sx * S) - 2:int(sx * S) + 3].reshape(-1, 3)
    check(label, tuple(int(v) for v in np.median(px_, axis=0)), want, 45)

def digitbox(x0, x1, y0, y1):
    sub = a[int(y0 * S):int(y1 * S), int(x0 * S):int(x1 * S)]
    ink = (sub[..., 0] < 120) & (sub[..., 1] < 120) & (sub[..., 2] < 120)
    ys, xs = np.where(ink)
    if len(xs) == 0:
        return None
    return (xs.min() / S + x0, xs.max() / S + x0, ys.min() / S + y0, ys.max() / S + y0)

print("NUMERALS (measured digit ink from the frame):")
check("g77 r1c1 '0'", digitbox(104, 138, 175, 201), (115, 126, 182, 193), 4)
check("g77 r2c2 '1'", digitbox(143, 178, 205, 231), (156, 165, 213, 224), 4)
check("f33 r1c1 '0'", digitbox(442, 468, 249, 268), (450, 458, 253, 262), 4)
check("o55 r1c1 '1'", digitbox(624, 659, 205, 231), (638, 647, 213, 224), 4)
check("o55 r5c4 '3'", digitbox(742, 778, 325, 351), (753, 764, 331, 344), 4)

print("GRID 3x3 / 5x5:")
sub = a[int(240 * S):int(320 * S), int(425 * S):int(540 * S)]
ink = (sub[..., 0] < 200) | (sub[..., 1] < 200) | (sub[..., 2] < 200)
ys, xs = np.where(ink)
check("f33 ink bbox", (xs.min() / S + 425, xs.max() / S + 425, ys.min() / S + 240, ys.max() / S + 240), (440, 527, 247, 313), 4)
sub = a[int(196 * S):int(360 * S), int(605 * S):int(840 * S)]
ink = (sub[..., 0] < 200) | (sub[..., 1] < 200) | (sub[..., 2] < 200)
ys, xs = np.where(ink)
check("o55 ink bbox", (xs.min() / S + 605, xs.max() / S + 605, ys.min() / S + 196, ys.max() / S + 196), (622, 820, 203, 354), 4)

# ---- 4) operators ----
print("OPERATORS:")
for label, (x0, x1, y0, y1), want in [
    ("'*' ink", (395, 425, 265, 295), (407, 413, 278, 284)),
    ("'=' ink", (535, 570, 265, 295), (546, 559, 276, 281)),
]:
    sub = a[int(y0 * S):int(y1 * S), int(x0 * S):int(x1 * S)]
    ink = (sub[..., 0] < 130) & (sub[..., 1] < 130) & (sub[..., 2] < 130)
    ys, xs = np.where(ink)
    check(label, (xs.min() / S + x0, xs.max() / S + x0, ys.min() / S + y0, ys.max() / S + y0), want, 4)

# ---- 5) bullet: word-level groups + math bands + word baselines ----
print("BULLET (word-level):")
def wordbox(x0, x1, y0=130, y1=162):
    sub = a[int(y0 * S):int(y1 * S), int(x0 * S):int(x1 * S)]
    ink = (sub[..., 0] < 200) | (sub[..., 1] < 200) | (sub[..., 2] < 200)
    ys, xs = np.where(ink)
    if len(xs) == 0:
        return None
    return (xs.min() / S + x0, xs.max() / S + x0, ys.min() / S + y0, ys.max() / S + y0)

WORDS = [("ring", 106, 130, (111, 125, 141, 150)), ("For", 132, 170, (136, 166, 137, 150)),
         ("s=1,", 170, 238, (173, 234, 137, 152)), ("surround", 240, 335, (243, 331, 141, 150)),
         ("the", 336, 375, (340, 371, 141, 150)), ("image", 377, 440, (380, 437, 141, 153)),
         ("with", 442, 490, (445, 487, 141, 150)), ("htok", 492, 598, (496, 592, 136, 157)),
         ("and", 602, 646, (607, 642, 136, 150)), ("wtok", 648, 762, (651, 756, 136, 156)),
         ("layers", 763, 824, (766, 821, 140, 153)), ("of", 826, 850, (828, 847, 141, 150)),
         ("zero", 852, 870, (855, 866, 137, 150))]
for name, x0, x1, want in WORDS:
    got = wordbox(x0, x1)
    if got is None:
        print(f"  [FAIL] {name}: NO INK")
        ok_all = False
    else:
        check(name, got, want, 5)

# ---- 6) note box ----
print("NOTEBOX:")
blue = (Bc - Rc > 12) & (Bc > 140) & (Bc < 230) & (Rc < 210)
bm = blue.copy()
bm[:int(386 * S)] = False
bm[int(518 * S):] = False
bm[:, :int(60 * S)] = False
bm[:, int(700 * S):] = False
colc = bm.sum(axis=0)
vr = [(s, e) for s, e in runs(colc >= int(40 * S), min_len=1)]
check("left border center", (vr[0][0] + vr[0][1]) / 2 / S, 77, 4)
check("right border center", (vr[-1][0] + vr[-1][1]) / 2 / S, 672.5, 4)
rowc = bm.sum(axis=1)
hr = [(s, e) for s, e in runs(rowc >= int(300 * S), min_len=1)]
check("top border center", (hr[0][0] + hr[0][1]) / 2 / S, 393, 4)
check("bottom border center", (hr[-1][0] + hr[-1][1]) / 2 / S, 509, 4)

navy = (Bc - Rc > 30) & (Rc < 150)
nm = navy.copy()
nm[:int(396 * S)] = False
nm[int(512 * S):] = False
nm[:, :int(80 * S)] = False
nm[:, int(665 * S):] = False
nrow = nm.sum(axis=1)
lr = runs(nrow >= 3, min_len=2)
EXPECT_LINES = [(406, 423), (432, 450), (459, 477), (486, 504)]
if len(lr) != 4:
    print(f"  [FAIL] line band count {len(lr)} != 4")
    ok_all = False
else:
    for (g, e) in zip(lr, EXPECT_LINES):
        check("line band", (g[0] / S, g[1] / S), e, 4)
for label, (x0, x1), base_want in [("L1 baseline", (86, 200), 418.5), ("L2 baseline", (86, 640), 445.5)]:
    sub = a[int(400 * S):int(510 * S), int(x0 * S):int(x1 * S)]
    nv = (sub[..., 2] - sub[..., 0] > 30) & (sub[..., 0] < 150)
    ys, xs = np.where(nv)
    rows = np.unique(ys)
    # baseline = bottom of x-height glyphs: use the bottom of the row-histogram's main band
    print(f"  {label}: ink rows {ys.min()/S+400:.1f}..{ys.max()/S+400:.1f}")

print("CONTAINMENT:")
z = a[int(130 * S):int(380 * S), int(60 * S):int(76 * S)]
zi = (z[..., 0] < 200) | (z[..., 1] < 200) | (z[..., 2] < 200)
print(f"  [{'PASS' if zi.sum() == 0 else 'WARN'}] left gutter (x60..76, y130..380) stray ink px: {zi.sum()}")

print("SELFCHECK RESULT:", "ALL PASS" if ok_all else "HAS FAILURES")
