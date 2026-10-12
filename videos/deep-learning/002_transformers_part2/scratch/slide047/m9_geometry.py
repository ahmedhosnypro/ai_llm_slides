#!/usr/bin/env python3
"""m9_geometry.py — precise geometry of slide_047.jpg + asset probes."""
from PIL import Image
import numpy as np
from collections import Counter

F47 = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_047.jpg'
A = np.asarray(Image.open(F47).convert('RGB')).astype(int)
H, W = A.shape[:2]
R, G, B = A[..., 0], A[..., 1], A[..., 2]
SX, OX, SY = 0.962329, 17.582, 0.955556
fx = lambda sx: OX + SX * sx
sy = lambda fy: fy / SY
sx = lambda fx_: (fx_ - OX) / SX

def hline_rows(x, y0, y1, thresh=430):
    """rows where sum(rgb)<thresh at column x"""
    return [(y, tuple(A[y, x])) for y in range(y0, y1) if A[y, x].sum() < thresh]

def vline_cols(y, x0, x1, thresh=430):
    return [(x, tuple(A[y, x])) for x in range(x0, x1) if A[y, x].sum() < thresh]

print('== A. token row bands: dark rows at col1 center fx=205, fx=282 (col2), fx=838 (col8) ==')
for x in (205, 282, 838):
    rs = hline_rows(x, 45, 520, 470)
    print(f'x={x}:', [(y, c) for y, c in rs])

print()
print('== B. cell vertical borders in the OUTPUT row (y=76, below labels) and X row (y=500) ==')
for y in (76, 500):
    print(f'y={y}:', vline_cols(y, 150, 910, 480))

print()
print('== C. inside-row cell borders: output-of-attention row mid y~391; post-LN mid ~286 ==')
for y in (286, 391):
    print(f'y={y} cols with NOT-tan (sum<560 or b<95):', [(x, tuple(A[y, x])) for x in range(160, 900) if A[y, x].sum() < 560][:60])

print()
print('== D. LN bar edges: orange line rows/cols. Top bar: y=103 line x-extent ==')
for y in (103, 128, 129, 312, 313, 338, 339):
    m = [(x, tuple(A[y, x])) for x in range(120, 905) if (A[y, x][0] > 190 and A[y, x][2] < 110 and A[y, x][1] < 200)]
    if m:
        xs = [x for x, _ in m]
        print(f'y={y}: orange x {min(xs)}..{max(xs)} count={len(m)} sample={m[len(m)//2]}')

print()
print('== E. FFN box: border rows 206/264 x-extent; unit box vertical borders in 232..255 ==')
for y in (206, 207, 263, 264):
    m = [x for x in range(120, 905) if A[y, x].sum() < 500]
    if m: print(f'y={y}: dark x {min(m)}..{max(m)} count={len(m)}')
# unit borders: columns where many rows in 233..255 are darker than unit fill
band = A[234:255, :]
darkcnt = ((band.sum(axis=2)) < 560).sum(axis=0)
print('unit border candidate cols (darkcnt>=12):', [x for x in range(130, 900) if darkcnt[x] >= 12])

print()
print('== F. dash rows + side dashes (green dashed containers) ==')
for y in (96, 97, 164, 165, 166, 302, 303, 304, 377, 378, 379):
    m = [(x, tuple(A[y, x])) for x in range(120, 905) if A[y, x][1] > A[y, x][2] + 20 and A[y, x][0] < 220 and A[y, x].sum() < 600]
    if m:
        xs = [x for x, _ in m]
        print(f'y={y}: greenish x {min(xs)}..{max(xs)} n={len(m)} sample={m[len(m)//2]}')
# side dashes: columns 130..175 and 850..905, rows 100..200: greenish px
for x0, x1, lab in ((125, 180, 'left'), (845, 905, 'right')):
    pts = [(y, x) for y in range(90, 480) for x in range(x0, x1)
           if A[y, x][1] > A[y, x][2] + 20 and A[y, x][0] < 220 and A[y, x].sum() < 600]
    ys = sorted(set(y for y, _ in pts))
    print(f'side dashes {lab} x{x0}-{x1}: y rows {ys[:40]}')

print()
print('== G. plus discs: centers/diameters (scan red-disc mask per unit band) ==')
def discs(y0, y1):
    m = (R[y0:y1] > 150) & (G[y0:y1] < 110) & (B[y0:y1] < 80)
    cols = m.sum(axis=0)
    out = []
    x = 130
    while x < 900:
        if cols[x] > 6:
            x2 = x
            while x2 < 900 and cols[x2] > 2: x2 += 1
            seg = slice(x, x2)
            ys = np.where(m[:, seg].any(axis=1))[0]
            out.append((x, x2, y0 + int(ys.min()), y0 + int(ys.max())))
            x = x2
        x += 1
    return out
print('top unit discs:', discs(138, 162))
print('bottom unit discs:', discs(350, 374))

print()
print('== H. red arrows above container (y 60..88) + green/red arrows between bands ==')
m = (R > 150) & (G < 110) & (B < 90)
for y0, y1, lab in ((58, 86, 'red arrows zone'), (90, 103, 'in-container red'), (155, 173, 'row->plus'), (380, 400, 'below out-row'), (469, 486, 'MHA->X')):
    cols = m[y0:y1].sum(axis=0)
    xs = [x for x in range(130, 900) if cols[x] >= 3]
    groups = []
    for x in xs:
        if groups and x - groups[-1][1] <= 3: groups[-1][1] = x
        else: groups.append([x, x])
    print(f'{lab} y{y0}-{y1}: {len(groups)} clusters', groups[:12])

print()
print('== I. block arrows: lavender-outline px (b>g, b>200, r>190) per gap band ==')
lav = (R > 185) & (B > 195) & (B > G + 8)
for y0, y1, lab in ((401, 420, 'zone1 (outrow->MHA)'), (467, 487, 'zone2 (MHA->X)'), (188, 207, 'FFN gap up'), (264, 280, 'FFN gap down')):
    cols = lav[y0:y1].sum(axis=0)
    xs = [x for x in range(130, 900) if cols[x] >= 2]
    groups = []
    for x in xs:
        if groups and x - groups[-1][1] <= 4: groups[-1][1] = x
        else: groups.append([x, x])
    print(f'{lab}: {len(groups)} clusters', groups[:12])

print()
print('== J. left boxes + vertical title + badge ==')
# Block Output box: find red border rect in x 50..180, y 40..110
red = (R > 140) & (G < 90) & (B < 90)
sub = red[40:115, 45:185]
ys, xs = np.where(sub)
print('Block Output red-ink bbox: x', 45 + xs.min(), 45 + xs.max(), 'y', 40 + ys.min(), 40 + ys.max())
sub = red[470:520, 45:185]
ys, xs = np.where(sub)
print('Block Input red-ink bbox: x', 45 + xs.min(), 45 + xs.max(), 'y', 470 + ys.min(), 470 + ys.max())
# vertical title: red ink in x 80..130, y 90..500
sub = red[90:500, 80:135]
ys, xs = np.where(sub)
print('vertical title red-ink bbox: x', 80 + xs.min(), 80 + xs.max(), 'y', 90 + ys.min(), 90 + ys.max())
# badge: yellow disc
yel = (R > 230) & (G > 230) & (B < 200)
sub = yel[30:110, 850:930]
ys, xs = np.where(sub)
print('badge yellow bbox: x', 850 + xs.min(), 850 + xs.max(), 'y', 30 + ys.min(), 30 + ys.max())

print()
print('== K. asset colors ==')
for p in ('s038_blkarrow.png', 's038_orangearrow.png'):
    im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/build/assets/' + p).convert('RGBA')
    arr = np.asarray(im)
    op = arr[..., 3] > 128
    px = arr[op][:, :3]
    print(p, im.size, 'opaque px:', len(px), 'mean:', px.mean(axis=0).round(0) if len(px) else None,
          'top:', Counter(map(tuple, (px // 32 * 32 + 16))).most_common(4))

print()
print('== L. FFN unit fill + interior dots: unit 1 interior census ==')
reg = A[238:250, 200:228].reshape(-1, 3)
print('unit1 interior (238:250,200:228):', Counter(map(tuple, (reg // 16 * 16 + 8))).most_common(6))
reg = A[232:256, 130:905:2].reshape(-1, 3)
print('FFN band all:', Counter(map(tuple, (reg // 16 * 16 + 8))).most_common(8))
