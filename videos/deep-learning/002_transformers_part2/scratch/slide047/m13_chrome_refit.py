#!/usr/bin/env python3
"""m13_chrome_refit.py — re-fit the deck mapping (chrome landmarks) on THIS frame
(slide_047.jpg, 960x540, 1px=1pt on the reference deck).

Task-given prior mappings to check against:
  deck-002 generic : slide_x = (fx - 17.628)/0.961232 , slide_y = fy/0.955556
  certified 045 fit: SX=0.962329 OX=17.582, SY=0.955556 OY=0 (chrome L58/R901/T43/B516)

Chrome model (playlist law, shared_patterns/house_chrome.js):
  white canvas; gray E9E9E7 panel x 42..918 pt, y 45..540 pt; thin C00000 border on
  panel left/right/top (bottom stroke at slide bottom); badge disc center (893,71) d36.
Landmarks on a frame: L = left border col, R = right border col, T = top border row,
B = bottom border row (half-visible above the video strip here).

Outputs: landmark px, fitted SX/OX/SY, residuals vs both prior mappings, badge
geometry, video-strip top row.
"""
from PIL import Image
import numpy as np

F = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_047.jpg'
A = np.asarray(Image.open(F).convert('RGB')).astype(int)
H, W = A.shape[:2]
R, G, B = A[..., 0], A[..., 1], A[..., 2]

def red_ink(sub):
    r, g, b = sub[..., 0], sub[..., 1], sub[..., 2]
    return (r > 120) & (r - g > 45) & (r - b > 40) & (g < 150)

# --- T: top border row, scan x 200..800 (clean zone between badge/boxes) ---
scores = []
for y in range(28, 62):
    m = red_ink(A[y:y+1, 200:800])
    scores.append((y, int(m.sum())))
T_row, T_cnt = max(scores, key=lambda t: t[1])
print('top border candidates (y,cnt) top5:', sorted(scores, key=lambda t: -t[1])[:5])
print('T =', T_row, 'cnt', T_cnt)

# --- L / R: border columns, scan y 110..300 (clean of title ink? title starts x~72) ---
# left: x 40..75 ; right: x 880..930
ls = [(x, int(red_ink(A[110:300, x:x+1]).sum())) for x in range(40, 76)]
rs = [(x, int(red_ink(A[110:300, x:x+1]).sum())) for x in range(880, 931)]
print('left border candidates (x,cnt) top5:', sorted(ls, key=lambda t: -t[1])[:5])
print('right border candidates (x,cnt) top5:', sorted(rs, key=lambda t: -t[1])[:5])
L_col = max(ls, key=lambda t: t[1])[0]
R_col = max(rs, key=lambda t: t[1])[0]

# --- B: bottom border row (above video strip), scan y 505..530, x 200..800 ---
bs = [(y, int(red_ink(A[y:y+1, 200:800]).sum())) for y in range(500, 532)]
print('bottom border candidates (y,cnt) top5:', sorted(bs, key=lambda t: -t[1])[:5])
B_row = max(bs, key=lambda t: t[1])[0]

# --- video strip top: first row from bottom up where mean luma < 40 ---
strip = None
for y in range(H - 1, 480, -1):
    if A[y, 200:800].mean() > 60:
        strip = y + 1
        break
print('video strip top row =', strip)

# --- badge: yellow disc ---
yel = (R > 225) & (G > 215) & (B < 190) & (R - B > 50)
sub = yel[40:110, 840:930]
ys, xs = np.where(sub)
bx0, bx1, by0, by1 = 840 + xs.min(), 840 + xs.max(), 40 + ys.min(), 40 + ys.max()
print(f'badge yellow bbox: x {bx0}..{bx1} y {by0}..{by1}  center=({(bx0+bx1)/2},{(by0+by1)/2}) d~{(bx1-bx0+by1-by0)/2+1}')
# numeral ink inside badge
dk = (A[by0:by1+1, bx0:bx1+1].sum(axis=2) < 330)
ys2, xs2 = np.where(dk)
print(f'badge numeral ink bbox: x {bx0+xs2.min()}..{bx0+xs2.max()} y {by0+ys2.min()}..{by0+ys2.max()}')
# badge ring color (just outside fill, on the circle) — sample ring pixels
ring_pts = []
for ang in range(0, 360, 30):
    import math
    a = math.radians(ang)
    cx, cy = (bx0 + bx1) / 2, (by0 + by1) / 2
    rad = (bx1 - bx0) / 2 + 2
    x, y = int(cx + rad * math.cos(a)), int(cy + rad * math.sin(a))
    if 0 <= x < W and 0 <= y < H:
        ring_pts.append(tuple(A[y, x]))
print('badge ring samples (12 dirs, r=d/2+2):', ring_pts)

# --- FIT ---
# model: fx = OX + SX * sx ; landmark sx values (house chrome): L->42, R->918, T->45, B->540
SX_lr = (R_col - L_col) / (918 - 42)
OX_lr = L_col - SX_lr * 42
SY_t = T_row / 45.0
SY_b = B_row / 540.0
print('\n== FIT on THIS frame ==')
print(f'L={L_col} R={R_col} T={T_row} B={B_row}')
print(f'SX={SX_lr:.6f} OX={OX_lr:.3f}   (from L/R)')
print(f'SY from T: {SY_t:.6f}   SY from B: {SY_b:.6f}   (deck uses OY=0)')
# residuals of both prior mappings on the landmarks
for name, (SXp, OXp, SYp) in {
    'deck-given  (0.961232,17.628,0.955556)': (0.961232, 17.628, 0.955556),
    '045-certif  (0.962329,17.582,0.955556)': (0.962329, 17.582, 0.955556),
    'this-frame fit': (SX_lr, OX_lr, (SY_t + SY_b) / 2),
}.items():
    eL = OXp + SXp * 42 - L_col
    eR = OXp + SXp * 918 - R_col
    eT = SYp * 45 - T_row
    eB = SYp * 540 - B_row
    print(f'{name}: err L {eL:+.2f}px  R {eR:+.2f}px  T {eT:+.2f}px  B {eB:+.2f}px')

# cross-check: known family x positions (slide pts from 45/46 T.cols via 038) -> frame px
# 038 cols (slide pts, from components/slide_038.js via 045 T.cols) — printed by 045 build:
# we do not have them here numerically; instead check the ROW/cell borders found in m9/m11:
print('\nlandmark -> slide-pt conversions (this-frame fit):')
sx = lambda fx: (fx - OX_lr) / SX_lr
sy = lambda fy: fy / ((SY_t + SY_b) / 2)
for lab, fx in (('L', L_col), ('R', R_col)):
    print(f'  {lab} fx={fx} -> slide_x {sx(fx):.1f}')
for lab, fy in (('T', T_row), ('B', B_row)):
    print(f'  {lab} fy={fy} -> slide_y {sy(fy):.1f}')
