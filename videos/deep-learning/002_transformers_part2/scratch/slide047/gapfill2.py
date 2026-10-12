#!/usr/bin/env python3
"""gapfill2.py — surgical probes resolving gapfill1 conflicts. Read-only on frame;
writes crops + output only into scratch/slide047/."""
from PIL import Image
import numpy as np

F = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_047.jpg'
im = Image.open(F).convert('RGB')
A = np.asarray(im).astype(int)
R, G, B = A[..., 0], A[..., 1], A[..., 2]

out = []
def p(s=''):
    out.append(s); print(s)

# ---- A. disc + plus: crop stage-1 disc1 (205,363) and stage-2 disc1 (205,151) at 10x ----
for lab, cx, cy in (('disc_s2_d1', 205, 151), ('disc_s1_d1', 205, 363)):
    crop = im.crop((cx - 16, cy - 16, cx + 16, cy + 16)).resize((320, 320), Image.NEAREST)
    crop.save(f'/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide047/gapfill_{lab}.png')
p('== A. disc color transects (y=cy, x cx-14..cx+14) ==')
for lab, cx, cy in (('s2d1', 205, 151), ('s1d1', 205, 363)):
    p(f'   {lab} horiz: ' + ' '.join(f'{x}:{tuple(A[cy, x])}' for x in range(cx - 12, cx + 13, 3)))
    p(f'   {lab} vert : ' + ' '.join(f'{y}:{tuple(A[y, cx])}' for y in range(cy - 12, cy + 13, 3)))

# ---- B. internal row labels: where are they? probe y bands x190..230 ----
p('== B. internal row label probe: darkest px per y in x=190..230 (cell1 label zone) ==')
for lab, y0, y1 in (('rowA', 168, 200), ('rowB', 276, 308), ('rowC', 379, 411)):
    best = []
    for y in range(y0, y1):
        seg = A[y, 190:230]
        s = seg.sum(axis=1)
        i = int(s.argmin())
        best.append((y, tuple(seg[i]), int(s[i])))
    best.sort(key=lambda t: t[2])
    p(f'   {lab}: darkest 6: {best[:6]}')

# ---- C. X-row label second glyph: print x ink runs at label band ----
p('== C. X label ink runs y495..508, x195..260 (cell1) ==')
redm = (R > 140) & (R - G > 40)
cols = redm[495:509, 195:260].sum(axis=0)
p('   ' + ' '.join(f'{195+x}:{int(c)}' for x, c in enumerate(cols) if c > 0))
p('   Y label ink runs y60..74, x195..260 (output cell1):')
cols = redm[60:74, 195:260].sum(axis=0)
p('   ' + ' '.join(f'{195+x}:{int(c)}' for x, c in enumerate(cols) if c > 0))

# ---- D. sub-cell segment colors: output cell1 y=66 x170..245; X cell1 y=501 x170..245; rowA cell1 y=180 ----
p('== D. sub-cell segment runs ==')
def segprint(y, x0, x1):
    prev = None; runs2 = []
    for x in range(x0, x1):
        c = tuple((A[y, x] // 24 * 24 + 12).tolist())
        if c != prev:
            runs2.append(f'{x}:{c}'); prev = c
    p('   ' + ' '.join(runs2))
p('   output y=66:'); segprint(66, 168, 246)
p('   X y=501:');     segprint(501, 168, 246)
p('   rowA y=180:');   segprint(180, 168, 246)

# ---- E. block arrows: X->MHA gap. Print classify runs y=485 x180..260 and find all arrow x-groups y477..492 ----
p('== E. block arrow (X->MHA) at y=485 ==')
def cls(px):
    r, g, b = px
    if r > 235 and g > 235 and b > 235: return 'WHT'
    if b > g and b > 150 and r > 150: return 'LAV'
    if b > 110 and r < 110: return 'NAVY'
    if r > 200 and g > 130 and b < 140: return 'TAN'
    if r > 140 and g < 110 and b < 100: return 'RED'
    if sum(px) < 300: return 'DRK'
    return '...'
def runprint(y, x0, x1):
    prev = None; runs2 = []
    for x in range(x0, x1):
        c = cls(A[y, x])
        if c != prev:
            runs2.append(f'{x}:{c}'); prev = c
    p('   ' + ' '.join(runs2))
runprint(485, 180, 260)
p('   navy px col profile y477..492 (cols with >=3 navy):')
navy = (B > 110) & (R < 110) & (B > G + 40)
prof = navy[477:493, 130:910].sum(axis=0)
xs = [130 + i for i, c in enumerate(prof) if c >= 3]
groups = []
for x in xs:
    if groups and x - groups[-1][1] <= 4: groups[-1][1] = x
    else: groups.append([x, x])
p('   ' + str(groups))
p('   MHA->rowC y399..414 dark-purple (plum outline) profile:')
plm = (R > 90) & (R < 175) & (G < 95) & (B > 55) & (B < 140)
prof = plm[399:415, 130:910].sum(axis=0)
xs = [130 + i for i, c in enumerate(prof) if c >= 3]
groups = []
for x in xs:
    if groups and x - groups[-1][1] <= 4: groups[-1][1] = x
    else: groups.append([x, x])
p('   ' + str(groups))
p('   FFN->rowA y189..204 same:')
prof = plm[189:205, 130:910].sum(axis=0)
xs = [130 + i for i, c in enumerate(prof) if c >= 3]
groups = []
for x in xs:
    if groups and x - groups[-1][1] <= 4: groups[-1][1] = x
    else: groups.append([x, x])
p('   ' + str(groups))

# ---- F. olive-green arrows per gap ----
p('== F. olive arrows (G>B+30, 100<G, R<G+60, sum<560) per gap ==')
olv = (G > B + 30) & (G > 100) & (R < G + 60) & ((R + G + B) < 560)
for lab, y0, y1 in (('rowC->disc1', 342, 352), ('disc1->LN1', 330, 342), ('LN1->rowB', 296, 311),
                    ('rowA->disc2', 132, 141), ('disc2->LN2', 120, 132), ('LN2->outrow', 86, 100)):
    prof = olv[y0:y1, 130:910].sum(axis=0)
    xs = [130 + i for i, c in enumerate(prof) if c >= 2]
    groups = []
    for x in xs:
        if groups and x - groups[-1][1] <= 5: groups[-1][1] = x
        else: groups.append([x, x])
    p(f'   {lab}: {len(groups)} groups x{[g[0] for g in groups]}')

# ---- G. title ink darkest ----
p('== G. title ink darkest (y122-419, x85-160) ==')
seg = A[122:420, 85:160].reshape(-1, 3)
s = seg.sum(axis=1)
idx = np.argsort(s)[:60]
p(f'   darkest-60 mean: {seg[idx].mean(axis=0).round(0)}  min: {seg[s.argmin()]}')

# ---- H. red thin arrows: output row -> container (y74..90) census ----
p('== H. red arrows y74..89 census ==')
red2 = (R > 150) & (G < 110) & (B < 90)
prof = red2[74:90, 130:910].sum(axis=0)
xs = [130 + i for i, c in enumerate(prof) if c >= 3]
groups = []
for x in xs:
    if groups and x - groups[-1][1] <= 4: groups[-1][1] = x
    else: groups.append([x, x])
p('   ' + str(groups))

with open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide047/gapfill2_output.txt', 'w') as f:
    f.write('\n'.join(out) + '\n')
print('WROTE gapfill2_output.txt')
