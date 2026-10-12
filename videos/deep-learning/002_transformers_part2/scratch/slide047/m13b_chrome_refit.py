#!/usr/bin/env python3
"""m13b_chrome_refit.py — chrome landmark re-fit, take 2 (clean zones + blur-aware
detectors). The chrome border is a thin C00000 1pt line JPEG-blurred to 2-3 px of
pink/dark-red; the content (orange container x~128..896) also has red-orange
borders, so landmark zones avoid all content:
  T: y 28..52, x 250..750   (above everything; only chrome + white)
  L: x 44..70,  y 200..280  (left of container x128, right of canvas white; title
                             ink starts x~72 so keep x<70)
  R: x 898..930, y 200..280 (right of container right edge ~x897)
  B: y 505..530, x 250..750 (above video strip; below X row ~y510? X row ends ~510
                             -> use x where no X-label ink: dots zone x600..700)
"""
from PIL import Image
import numpy as np
import math

F = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_047.jpg'
A = np.asarray(Image.open(F).convert('RGB')).astype(int)
H, W = A.shape[:2]
R, G, B = A[..., 0], A[..., 1], A[..., 2]

# blur-aware chrome-red: pinkish OR dark-red, clearly non-white non-gray non-tan
def chrome_red(sub):
    r, g, b = sub[..., 0], sub[..., 1], sub[..., 2]
    pinkish = (r > 165) & (r - g > 18) & (r - b > 18) & (g < 220)
    darkred = (r > 85) & (r - g > 30) & (r - b > 25) & (g < 120)
    return pinkish | darkred

# T
ts = [(y, int(chrome_red(A[y:y+1, 250:750]).sum())) for y in range(28, 53)]
print('T candidates:', [(y, c) for y, c in ts if c > 100])
T_row = max(ts, key=lambda t: t[1])[0]
# L
ls = [(x, int(chrome_red(A[200:280, x:x+1]).sum())) for x in range(44, 71)]
print('L candidates:', [(x, c) for x, c in ls if c > 10])
L_col = max(ls, key=lambda t: t[1])[0]
# R
rs = [(x, int(chrome_red(A[200:280, x:x+1]).sum())) for x in range(898, 931)]
print('R candidates:', [(x, c) for x, c in rs if c > 10])
R_col = max(rs, key=lambda t: t[1])[0]
# B (use dot zone x600..700 — X-row dots are green, no red ink there)
bs = [(y, int(chrome_red(A[y:y+1, 600:700]).sum())) for y in range(505, 531)]
print('B candidates:', [(y, c) for y, c in bs if c > 20])
B_row = max(bs, key=lambda t: t[1])[0]

# print raw pixel columns for verification
print('\nverify L col profile x=54..62 at y=240:', [(x, tuple(A[240, x])) for x in range(54, 63)])
print('verify R col profile x=896..908 at y=240:', [(x, tuple(A[240, x])) for x in range(896, 909)])
print('verify T row profile y=40..48 at x=500:', [(y, tuple(A[y, 500])) for y in range(40, 49)])
print('verify B row profile y=512..520 at x=650:', [(y, tuple(A[y, 650])) for y in range(512, 521)])

# badge (yellow disc) + ring color at horizontal extremes
yel = (R > 225) & (G > 215) & (B < 190) & (R - B > 50)
sub = yel[40:110, 840:935]
ys, xs = np.where(sub)
bx0, bx1, by0, by1 = 840 + xs.min(), 840 + xs.max(), 40 + ys.min(), 40 + ys.max()
cx, cy = (bx0 + bx1) / 2, (by0 + by1) / 2
d = (bx1 - bx0 + by1 - by0) / 2 + 1
print(f'\nbadge fill bbox x {bx0}..{bx1} y {by0}..{by1} center ({cx},{cy}) d~{d:.1f}')
print('ring samples left/right at cy:', [(dx, tuple(A[int(cy), int(cx + dx)])) for dx in range(-int(d/2)-3, -int(d/2)+4)] + [(dx, tuple(A[int(cy), int(cx + dx)])) for dx in range(int(d/2)-3, int(d/2)+4)])
# numeral ink
dk = (A[by0:by1+1, bx0:bx1+1].sum(axis=2) < 330)
ys2, xs2 = np.where(dk)
print(f'numeral ink bbox: x {bx0+xs2.min()}..{bx0+xs2.max()} y {by0+ys2.min()}..{by0+ys2.max()} (h={ys2.max()-ys2.min()+1})')

# FIT
SX = (R_col - L_col) / (918 - 42)
OX = L_col - SX * 42
SY = T_row / 45.0
print(f'\n== FIT ==  L={L_col} R={R_col} T={T_row} B={B_row}')
print(f'SX={SX:.6f}  OX={OX:.3f}  SY(T-fit)={SY:.6f}')
print(f'B check: B_row/SY = {B_row/SY:.2f} (expect ~540)')
for name, (SXp, OXp, SYp) in {
    'deck-given (0.961232,17.628,.955556)': (0.961232, 17.628, 0.955556),
    '045-certif (0.962329,17.582,.955556)': (0.962329, 17.582, 0.955556),
    'this-fit': (SX, OX, SY),
}.items():
    print(f'{name}: errL {OXp+SXp*42-L_col:+.2f} errR {OXp+SXp*918-R_col:+.2f} errT {SYp*45-T_row:+.2f} errB {SYp*540-B_row:+.2f}')

sx = lambda fx: (fx - OX) / SX
sy = lambda fy: fy / SY
print('\nbadge in slide pts (this fit): cx %.1f cy %.1f d %.1f' % (sx(cx), sy(cy), d / SX))
print('L->%.1f R->%.1f T->%.1f B->%.1f (slide pts)' % (sx(L_col), sx(R_col), sy(T_row), sy(B_row)))
