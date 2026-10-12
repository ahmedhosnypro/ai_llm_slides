#!/usr/bin/env python3
"""gapfill1.py — resume-gap fills (read-only on slide_047.jpg): items m14's crash left
unprinted + spot-verifications of vision/PIL conflicts. Writes only to scratch/slide047/."""
from PIL import Image
import numpy as np
from collections import Counter

F = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_047.jpg'
A = np.asarray(Image.open(F).convert('RGB')).astype(int)
R, G, B = A[..., 0], A[..., 1], A[..., 2]
SY = 0.955556
SX, OX = 0.962329, 17.582          # m13b slide-047 fit
SXg, OXg = 0.961232, 17.628        # deck-given mapping (task ground truth)
sx = lambda fx: (fx - OXg) / SXg   # deck pt via deck-given mapping
sy = lambda fy: fy / SY

out = []
def p(s=''):
    out.append(s); print(s)

# ---- 1. vertical title cap height, UNCONTAMINATED (y 122..419 only; Block In/Out excluded) ----
red = (R > 130) & (R - G > 45) & (R - B > 40)
sub = red[122:420, 60:160]
ys, xs = np.where(sub)
p('== 1. title cap (y122-419 only) ==')
p(f'   x extent {60+xs.min()}..{60+xs.max()} (cap h={xs.max()-xs.min()+1}px = {(xs.max()-xs.min()+1)/SY:.1f}pt)')
colprof = sub.sum(axis=0)
cols = [60 + i for i, c in enumerate(colprof) if c > 0]
p(f'   ink cols: {cols[0]}..{cols[-1]}, dense(>=3): {[c for c in cols if colprof[c-60] >= 3][0]}..{[c for c in cols if colprof[c-60] >= 3][-1]}')
inkpx = A[122:420, 60:160][sub]
p(f'   ink color mean {inkpx.mean(axis=0).round(0)}')

# ---- 2. plus-sign color inside disc (stage-1 disc 1: cx~205, cy~363; stage-2: cx~205, cy~151) ----
p('== 2. plus-sign color ==')
for lab, cx, cy in (('stage2 disc1', 205, 151), ('stage1 disc1', 205, 363), ('stage1 disc5', 498, 363)):
    box = A[cy - 8:cy + 8, cx - 8:cx + 8].reshape(-1, 3)
    white = int(((box > 225).all(axis=1)).sum())
    redd = int(((box[:, 0] > 150) & (box[:, 1] < 110) & (box[:, 2] < 90)).sum())
    cc = Counter(map(tuple, (box // 24 * 24 + 12))).most_common(4)
    p(f'   {lab} 16x16: white={white} red={redd} top={cc}')

# ---- 3. LN bars: border x-extent (tight dark-orange mask on border rows) ----
p('== 3. LN bar border x-extent ==')
for lab, rows in (('LN-top(y101-130)', (102, 103, 104, 128, 129)), ('LN-bottom(y312-341)', (313, 314, 339, 340))):
    for y in rows:
        m = (R[y] > 150) & (R[y] < 230) & (G[y] < 150) & (B[y] < 90)
        xs2 = np.where(m[120:905])[0]
        if len(xs2):
            p(f'   {lab} y={y}: x {120+xs2.min()}..{120+xs2.max()} n={len(xs2)}')
# fill extent at mid-bar y=115 / y=325: tan-fill run
for y in (115, 325):
    tanm = (abs(R[y] - 235) < 20) & (abs(G[y] - 176) < 22) & (abs(B[y] - 118) < 26)
    xs3 = np.where(tanm[120:905])[0]
    p(f'   bar fill tan y={y}: x {120+xs3.min()}..{120+xs3.max()} n={len(xs3)}')

# ---- 4. FFN tile 1 dot census (tile1 x~163..241, y 232..258) ----
p('== 4. FFN tile1 dots ==')
t = A[232:258, 160:245]
grn = (t[..., 1] > t[..., 2] + 40) & (t[..., 1] > 130) & (t[..., 0] < 190)
pnk = (t[..., 0] > 200) & (t[..., 2] > 110) & (t[..., 0] - t[..., 1] > 40)
def blob_cols(mask, minc=1):
    cols = mask.sum(axis=0); groups = []; i = 0
    while i < len(cols):
        if cols[i] >= minc:
            j = i
            while j < len(cols) and cols[j] >= minc - 0: j += 1
            groups.append((i, j - 1)); i = j
        else: i += 1
    return groups
gb = blob_cols(grn); pb = blob_cols(pnk)
p(f'   green col-groups: {gb}  -> {len(gb)} dots')
p(f'   pink  col-groups: {pb}  -> {len(pb)} dots')
grows = np.where(grn.sum(axis=1) > 0)[0]; prows = np.where(pnk.sum(axis=1) > 0)[0]
p(f'   green rows y {232+grows.min()}..{232+grows.max()}' if len(grows) else '   green none')
p(f'   pink  rows y {232+prows.min()}..{232+prows.max()}' if len(prows) else '   pink none')

# ---- 5. full cell census: label-ink x-clusters per row (red-ish ink in label band) ----
p('== 5. label-ink x-clusters (cell centers) per row ==')
def clusters(mask1d, gap=6):
    xs4 = np.where(mask1d)[0]; gs = []
    for x in xs4:
        if gs and x - gs[-1][1] <= gap: gs[-1][1] = x
        else: gs.append([x, x])
    return gs
rows = [('output', 60, 73), ('rowA', 174, 187), ('rowB', 282, 295), ('rowC', 385, 398), ('X', 495, 508)]
for lab, y0, y1 in rows:
    ink = (R[y0:y1, 130:910] > 140) & (R[y0:y1, 130:910] - G[y0:y1, 130:910] > 40)
    prof = ink.sum(axis=0)
    gs = clusters(prof > 0, gap=8)
    cs = [round((130 + a + 130 + b) / 2, 1) for a, b in gs]
    p(f'   {lab}: {len(gs)} ink-groups, centers {cs}')
    if len(gs) > 2:
        d = np.diff(cs); p(f'      center deltas: {[round(x,1) for x in d]}')

# ---- 6. cell side borders: gray-line columns in output row (y 58..74, off-label x runs) ----
p('== 6. output-row cell borders (y=72, just above bottom edge 74) ==')
y = 72
row = A[y, 130:910]
borderish = (abs(row[:, 0] - row[:, 1]) < 25) & (row.sum(axis=1) < 660) & (row.sum(axis=1) > 380)
gs = clusters(borderish, gap=3)
p(f'   y=72 border-ish col groups: {[ (130+a, 130+b) for a,b in gs ]}')
y = 500
row = A[y, 130:910]
borderish = (abs(row[:, 0] - row[:, 1]) < 25) & (row.sum(axis=1) < 660) & (row.sum(axis=1) > 380)
gs = clusters(borderish, gap=3)
p(f'   y=500 border-ish col groups: {[ (130+a, 130+b) for a,b in gs ]}')

# ---- 7. ellipsis dots per row: full x window 590..760 ----
p('== 7. ellipsis dots x590-760 per row ==')
for lab, y0, y1 in rows:
    seg = A[y0:y1, 590:760]
    dk = seg.sum(axis=2)
    dark = dk < 480
    gs = clusters(dark.sum(axis=0) > 0, gap=4)
    p(f'   {lab}: {len(gs)} dark groups at x {[590+a for a,b in gs]}')

# ---- 8. block arrows in the three light gaps (presence census) ----
p('== 8. block-arrow presence per gap (outline-dark px columns) ==')
gaps = [('X->MHA', 474, 496), ('MHA->rowC', 399, 414), ('rowB->FFN', 297, 304), ('FFN->rowA', 189, 204)]
for lab, y0, y1 in gaps:
    seg = A[y0:y1, 130:910]
    dark = (seg.sum(axis=2) < 420)
    prof = dark.sum(axis=0)
    gs = clusters(prof >= 2, gap=6)
    p(f'   {lab} y{y0}-{y1}: {len(gs)} dark col-clusters x{[130+a for a,b in gs]}')

# ---- 9. green inter-stage arrows (rowC->discs, discs->LN1, LN1->rowB, etc.) census ----
p('== 9. green arrow columns per stage gap ==')
grn2 = (G > R + 30) & (G > B + 40) & (G > 120)
for lab, y0, y1 in (('rowC->disc1', 340, 352), ('disc1->LN1', 332, 346), ('LN1->rowB', 296, 311),
                    ('rowA->disc2', 130, 141), ('disc2->LN2', 122, 136), ('LN2->out', 86, 100)):
    prof = grn2[y0:y1, 130:910].sum(axis=0)
    gs = clusters(prof >= 2, gap=6)
    p(f'   {lab} y{y0}-{y1}: {len(gs)} green clusters x{[130+a for a,b in gs]}')

# ---- 10. deck-pt conversions of key landmarks (deck-given mapping) ----
p('== 10. key landmarks in deck pt (deck-given mapping) ==')
for lab, fx, fy in (('container L', 126, None), ('container R', 899, None), ('container T', None, 89),
                    ('container B', None, 477), ('MHA top', None, 415), ('MHA bottom', None, 471),
                    ('FFN top', None, 205), ('FFN bottom', None, 265), ('out row top', None, 58),
                    ('out row bot', None, 74), ('X top', None, 493), ('X bot', None, 509),
                    ('LN2 top', None, 101), ('LN2 bot', None, 130), ('LN1 top', None, 312), ('LN1 bot', None, 341)):
    if fx is not None:
        p(f'   {lab}: fx={fx} -> slide_x {sx(fx):.1f}pt')
    else:
        p(f'   {lab}: fy={fy} -> slide_y {sy(fy):.1f}pt')

with open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide047/gapfill1_output.txt', 'w') as f:
    f.write('\n'.join(out) + '\n')
print('WROTE gapfill1_output.txt')
