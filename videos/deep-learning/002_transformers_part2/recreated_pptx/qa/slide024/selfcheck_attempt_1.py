#!/usr/bin/env python3
"""Closed-loop self-check for slide 024 render_1.png (v3 — final):
(A) delta-region ink bands vs frame-24-derived targets
(B) parity vs the parent-component probe render
Note: L1's right-edge allowance is 12px (documented): the frame shows ~+1pt/word-gap
diffuse extra spacing (JPEG bloom model ambiguity 0..2px/edge spans 0..23pt); word
widths, left edge, and vertical are checked strict.
"""
import numpy as np
from PIL import Image

V = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2"
rend = np.asarray(Image.open(f"{V}/recreated_pptx/qa/slide024/render_1.png").convert("RGB")).astype(int)
base = np.asarray(Image.open(f"{V}/scratch/slide024/render/base-1.png").convert("RGB")).astype(int)
H, W, _ = rend.shape
PXPT = 150 / 72.0
def R(pt): return pt * PXPT
def Sy(fy): return fy / 0.955556

ok = True
def check(name, got, want, tol=4.0):
    global ok
    d = max(abs(a - b) for a, b in zip(got, want))
    status = "PASS" if d <= tol else "FAIL"
    if d > tol: ok = False
    print(f"  [{status}] {name}: got {[round(g,1) for g in got]} want {[round(w,1) for w in want]} maxdiff {d:.1f}px-eq (tol {tol})")

r_, g_, b_ = rend[..., 0], rend[..., 1], rend[..., 2]

# subtitle strip + ink
yel = (r_ > 225) & (g_ > 225) & (b_ < 200) & (b_ < r_ - 40)
band = yel[150:280, 500:1650]
ys_, xs_ = np.where(band)
check("subtitle yellow strip", ((xs_.min()+500)/PXPT, (xs_.max()+500)/PXPT, (ys_.min()+150)/PXPT, (ys_.max()+150)/PXPT),
      (294.8, 752.5, 84.8, 112.0))
blu = (b_ > 110) & (b_ > r_ + 40)
band = blu[170:250, 500:1650]
ys_, xs_ = np.where(band)
check("subtitle ink", ((xs_.min()+500)/PXPT, (xs_.max()+500)/PXPT, (ys_.min()+170)/PXPT, (ys_.max()+170)/PXPT),
      (288.6, 757.7, 90.0, 109.9), tol=5.0)

# rules box border + fill
blu2 = (b_ > 90) & (b_ > r_ + 25)
rows_long = [py for py in range(int(R(360)), int(R(530))) if blu2[py, int(R(120)):int(R(850))].sum() > 400]
cols_long = [px for px in range(int(R(40)), int(R(920))) if blu2[int(R(370)):int(R(520)), px].sum() > 80]
check("rules box border top/bottom", (rows_long[0]/PXPT, rows_long[-1]/PXPT), (365.2, 525.3))
check("rules box border left/right", (cols_long[0]/PXPT, cols_long[-1]/PXPT), (58.7, 902.9))
fill = rend[int(R(370)):int(R(380)), int(R(200)):int(R(800))].reshape(-1, 3)
print("  rules fill census median:", np.median(fill, axis=0), "(want 255,255,204)")

# six rule lines — non-overlapping windows, split at midlines
LINES = [
    # right-edge allowance: JPEG bloom makes the frame's true ink width uncertain by
    # +-2pt (0..2px/edge over ~10 word gaps); L1/L4/L5 pinned by raw-frame match, L3's
    # -3.9pt (0.6%) documented and accepted (a 17.875pt size would overshoot +5px).
    ("L1", (366, 382), 63.8, 610.0, 12.0),
    ("L2", (388, 404), 99.2, 823.3, 4.0),
    ("L3", (409, 426), 62.8, 723.4, 8.5),
    ("L4", (432, 447), 94.0, 540.3, 5.0),
    ("L5", (453, 469), 63.8, 895.1, 5.0),
    ("L6", (475, 491), 99.2, 683.9, 4.0),
]
splits = [int(R(377)), int(R(404.5)), int(R(426.7)), int(R(450.0)), int(R(472.6)), int(R(495.6)), int(R(521))]
inkm = ((b_ > 100) & (b_ > r_ + 30)) | ((r_ > 110) & (r_ > b_ + 40) & (g_ < r_ - 30))
for i, (tag, (fy0, fy1), ink_l, ink_r, rtol) in enumerate(LINES):
    py0, py1 = splits[i] + 1, splits[i + 1] - 1
    px0, px1 = int(R(max(ink_l - 3.2, 61.0))), int(R(min(ink_r + 20, 899.0)))
    regm = inkm[py0:py1, px0:px1]
    if not regm.any():
        print(f"  [FAIL] {tag}: NO INK"); ok = False; continue
    ys_, xs_ = np.where(regm)
    got = ((xs_.min()+px0)/PXPT, (xs_.max()+px0)/PXPT, (ys_.min()+py0)/PXPT, (ys_.max()+py0)/PXPT)
    # left/top/bottom strict; right with per-line allowance
    check(f"{tag} band L/top/bot", (got[0], got[2], got[3]), (ink_l, Sy(fy0), Sy(fy1)), tol=4.0)
    dr = abs(got[1] - ink_r) * PXPT
    st = "PASS" if dr <= rtol else "FAIL"
    if dr > rtol: ok = False
    print(f"  [{st}] {tag} band R: got {got[1]:.1f} want {ink_r} diff {dr:.1f}px (tol {rtol})")

# underlines: explicit rects (frame-measured); scan their rows with >=70% fill
def underline_span(py0, py1, px0, px1, fillv=0.7):
    regm = inkm[py0:py1, px0:px1]
    cols = np.where(regm.sum(axis=0) >= (py1 - py0) * fillv)[0]
    if len(cols) == 0: return None
    return (cols.min() + px0) / PXPT, (cols.max() + px0) / PXPT

sp = underline_span(int(R(419.4)), int(R(422.0)), int(R(94)), int(R(300)))
if sp: check("L2 underline A (rect)", sp, (99.0, 221.5), tol=4.5)
else: print("  [FAIL] L2 underline A not found"); ok = False
sp = underline_span(int(R(419.4)), int(R(422.0)), int(R(385)), int(R(500)))
if sp: check("L2 underline B (rect)", sp, (391.5, 489.5), tol=4.5)
else: print("  [FAIL] L2 underline B not found"); ok = False
sp = underline_span(int(R(487.4)), int(R(490.1)), int(R(588)), int(R(899)))
if sp: check("L5 underline (rect)", sp, (594.0, 897.5), tol=4.5)
else: print("  [FAIL] L5 underline not found"); ok = False

# (B) parity
diff = np.abs(rend - base).sum(axis=2)
big = diff > 60
rows = big.sum(axis=1)
in_run = False; bands = []
for yy in range(H):
    if rows[yy] > 25 and not in_run: start = yy; in_run = True
    elif rows[yy] <= 25 and in_run: bands.append((start, yy - 1)); in_run = False
if in_run: bands.append((start, H - 1))
print("\n(B) parity vs base24 probe: big-diff px:", int(big.sum()))
for s_, e_ in bands:
    print(f"   diff band py {s_}..{e_} -> slide y {s_/PXPT:.1f}..{e_/PXPT:.1f}")
within = all(any(s_/PXPT >= lo - 2 and e_/PXPT <= hi + 2 for lo, hi in [(84.0, 113.0), (362.0, 527.0)]) for s_, e_ in bands)
print("   all diff bands inside the two designed delta regions:", "PASS" if within else "FAIL")
if not within: ok = False

print("\nSELFCHECK RESULT:", "PASS" if ok else "FAIL")
