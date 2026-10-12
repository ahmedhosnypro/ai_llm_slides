#!/usr/bin/env python3
"""m14_ink_fonts_census.py — consolidated ink census, font-metric evidence, and
color verdicts for slide_047.jpg. All frame px; slide-pt conversions use the
m13c fit: slide_x=(fx-17.582)/0.962329, slide_y=fy/0.955556.
"""
from PIL import Image
import numpy as np
from collections import Counter

F = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_047.jpg'
A = np.asarray(Image.open(F).convert('RGB')).astype(int)
R, G, B = A[..., 0], A[..., 1], A[..., 2]
SX, OX, SY = 0.962329, 17.582, 0.955556
sx = lambda fx: (fx - OX) / SX
sy = lambda fy: fy / SY
def spts(fx, fy): return f'slide ({sx(fx):.1f},{sy(fy):.1f})'

def edge_rows(y0, y1, xs, lo=110, hi=225):
    """rows where >=2/3 of sample cols are gray-outline (max-min<45, lo<mean<hi)"""
    out = []
    for y in range(y0, y1):
        hits = 0
        for x in xs:
            px = A[y, x]
            mx, mn = int(px.max()), int(px.min())
            if mx - mn < 45 and lo < px.mean() < hi:
                hits += 1
        if hits >= len(xs) * 2 / 3:
            out.append(y)
    return out

COLS = [195, 270, 345, 420, 495, 570, 760, 835]   # strip-center sample cols
print('== A. token-row cell outline rows (top/bottom edges), per row ==')
for lab, y0, y1 in (('OUTPUT', 48, 82), ('post-FFN', 166, 200), ('post-LN', 272, 304),
                    ('out-attn', 378, 410), ('X', 486, 518)):
    er = edge_rows(y0, y1, COLS)
    if er:
        runs = []
        s = p = er[0]
        for y in er[1:]:
            if y - p <= 1: p = y
            else: runs.append((s, p)); s = p = y
        runs.append((s, p))
        print(f'{lab}: edge runs {runs}')

print('\n== B. LN bars: edge rows + x extent ==')
for lab, y0, y1, etop, ebot in (('LN1', 96, 136, 101, 130), ('LN2', 306, 346, 312, 341)):
    print(f'{lab}: edge rows (measured) top {etop}..{etop+2} bottom {ebot-2}..{ebot}  h={ebot-etop+1}px={(ebot-etop+1)/SY:.1f}pt')
    ymid = etop + 1
    m = [(x, tuple(A[ymid, x])) for x in range(130, 900)
         if A[ymid, x][0] > 150 and A[ymid, x][1] < 175 and A[ymid, x][2] < 110]
    xs = [x for x, _ in m]
    print(f'   bar x extent (at edge y={ymid}): {min(xs)}..{max(xs)}  -> slide x {sx(min(xs)):.1f}..{sx(max(xs)):.1f}')
    fillreg = A[etop+3:ebot-2, 175:230].reshape(-1, 3)
    print(f'   fill sample (left of text) median: {np.median(fillreg, axis=0)}')
    t0, t1 = etop + 3, ebot - 2
    rows = [(y, int(((A[y, 240:860].sum(axis=1)) < 480).sum())) for y in range(t0, t1 + 1)]
    band = [y for y, n in rows if n > 30]
    if band:
        print(f'   text rows n>30: {band[0]}..{band[-1]} (cap h={band[-1]-band[0]+1}px = {(band[-1]-band[0]+1)/SY:.1f}pt)')
    # two-tone: reddish (Layer) vs brown (Normalization) darkest px
    txt = A[band[0]:band[-1]+1, 240:860].reshape(-1, 3)
    reddish = txt[(txt[:, 0] - txt[:, 1] > 70) & (txt[:, 0] > 120)]
    brown = txt[(txt[:, 0] - txt[:, 1] > 15) & (txt[:, 0] - txt[:, 1] <= 60) & (txt[:, 0] < 150)]
    print(f'   "Layer" reddish darkest mean: {reddish.mean(axis=0).round(0) if len(reddish) else None} n={len(reddish)}')
    print(f'   "Normalization" brown darkest mean: {brown.mean(axis=0).round(0) if len(brown) else None} n={len(brown)}')
    xs2 = [x for x in range(240, 860) if ((A[band[0]:band[-1]+1, x].sum(axis=1)) < 480).sum() > 1]
    print(f'   text ink x extent: {min(xs2)}..{max(xs2)} (cx {np.mean([min(xs2), max(xs2)]):.0f})')

print('\n== C. MHA bar: edges, fill, white-text cap ==')
for y in range(412, 425):
    px = A[y, 500]
    if px[0] < 170 and px[1] < 110: print(f'   top edge first plum y={y} {tuple(px)}'); break
for y in range(476, 460, -1):
    px = A[y, 500]
    if px[0] < 170 and px[1] < 110: print(f'   bottom edge last plum y={y} {tuple(px)}'); break
fillreg = A[440:452, 200:240].reshape(-1, 3)
print(f'   bar fill median: {np.median(fillreg, axis=0)}')
# NOTE (m14 probe): text is white JPEG-blurred on plum — max px sum ~622, so the
# "white ink" detector must use sum>560 (not 700); measured stems peak ~ (239,180,150).
wt = [(y, int(((A[y, 300:760].sum(axis=1)) > 560).sum())) for y in range(424, 468)]
band = [y for y, n in wt if n > 20]
print(f'   white text rows n>30: {band[0]}..{band[-1]} (cap h={band[-1]-band[0]+1}px = {(band[-1]-band[0]+1)/SY:.1f}pt)')
xs = [x for x in range(280, 780) if (A[band[0]:band[-1]+1, x].sum(axis=1) > 560).sum() > 2]
print(f'   text ink x extent: {min(xs)}..{max(xs)} (cx {np.mean([min(xs),max(xs)]):.0f})')
bright = A[band[0]:band[-1]+1, min(xs):max(xs)+1].reshape(-1, 3)
bright = bright[bright.sum(axis=1) > 560]
print(f'   text stem brightest mean: {bright.mean(axis=0).round(0) if len(bright) else None} (white blurred on plum)')
print(f'   text ink x extent: {min(xs)}..{max(xs)} (cx {np.mean([min(xs),max(xs)]):.0f})')

print('\n== D. FFN box: borders, fill, header, tiles ==')
# side borders: dark cols over y 210..258
cnt = ((A[210:259].sum(axis=2)) < 500).sum(axis=0)
borders = [x for x in range(140, 900) if cnt[x] > 30]
print(f'   side border cols (>30 dark rows): {borders}')
# top/bottom border rows
cnt2 = ((A[:, 300:700].sum(axis=2)) < 500).sum(axis=1)
tb = [y for y in range(198, 272) if cnt2[y] > 200]
print(f'   top/bottom border rows (>200 dark cols): {tb}')
if len(borders) >= 2 and len(tb) >= 2:
    print(f'   box: x {borders[0]}..{borders[-1]} y {tb[0]}..{tb[-1]} -> slide x {sx(borders[0]):.1f}..{sx(borders[-1]):.1f} y {sy(tb[0]):.1f}..{sy(tb[-1]):.1f}')
    bc = tuple(A[tb[0]+1, borders[0]])  # border color sample
    print(f'   border color sample: {bc}')
# interior fill between tiles (x 240..262, y 226..238)
ireg = A[228:238, 244:262].reshape(-1, 3)
print(f'   interior fill median: {np.median(ireg, axis=0)}')
# tile 1: left/right border cols in x 160..245, rows 232..258
tcnt = ((A[232:259, 160:250].sum(axis=2)) < 520).sum(axis=0)
tcols = [160 + i for i, c in enumerate(tcnt) if c > 12]
print(f'   tile1 border cols: {tcols}')
treg = A[236:246, 200:230].reshape(-1, 3)
print(f'   tile1 fill median (200..230,236..246): {np.median(treg, axis=0)}')
# dots: green row + pink row in tile 1 (x 190..225)
for lab, y0, y1, mask in (
    ('green', 236, 248, lambda s: (s[..., 1] > 120) & (s[..., 1] - s[..., 0] > 30) & (s[..., 1] - s[..., 2] > 30)),
    ('pink ', 248, 260, lambda s: (s[..., 0] > 200) & (s[..., 2] > 120) & (s[..., 0] - s[..., 1] > 40)),
):
    sub = A[y0:y1, 190:226]
    m = mask(sub)
    ys, xs = np.where(m)
    if len(xs):
        cols = sorted(set(xs.tolist()))
        groups = []
        for x in cols:
            if groups and x - groups[-1][-1] <= 1: groups[-1].append(x)
            else: groups.append([x])
        print(f'   tile1 {lab} dots: {len(groups)} clusters x={[(g[0]+190, g[-1]+190) for g in groups]} cy~{y0+int(ys.mean())}')
        px = sub[m]
        print(f'      {lab} color mean: {px.mean(axis=0).round(0)}')

print('\n== E. plus discs (both units): centers, diameter, fill ==')
def discs(y0, y1):
    m = (R[y0:y1] > 140) & (G[y0:y1] < 115) & (B[y0:y1] < 95)
    colc = m.sum(axis=0)
    out = []
    x = 140
    while x < 900:
        if colc[x] > 6:
            x2 = x
            while x2 < 900 and colc[x2] > 2: x2 += 1
            seg = m[:, x:x2]
            ys = np.where(seg.any(axis=1))[0]
            cy = y0 + (ys.min() + ys.max()) / 2
            cxp = (x + x2 - 1) / 2
            d = max(x2 - x, ys.max() - ys.min() + 1)
            c = A[int(cy)-2:int(cy)+3, int(cxp)-2:int(cxp)+3].reshape(-1, 3)
            # exclude the white plus (bright px)
            dark = c[c.sum(axis=1) < 480]
            fill = dark.mean(axis=0).round(0) if len(dark) else c.mean(axis=0).round(0)
            out.append((int(cxp), round(cy, 1), int(d), tuple(fill)))
            x = x2
        x += 1
    return out
for lab, y0, y1 in (('unit-1', 136, 164), ('unit-2', 348, 376)):
    dd = discs(y0, y1)
    print(f'   {lab}: {len(dd)} discs')
    for cxp, cy, d, fill in dd:
        print(f'      cx={cxp} cy={cy} d={d} fill={fill} -> slide cy {sy(cy):.1f}')

print('\n== F. ellipsis dots per row: color + count at x 615..665 ==')
for lab, cy in (('output', 67), ('post-FFN', 181), ('post-LN', 289), ('out-attn', 391), ('X', 501)):
    reg = A[cy-5:cy+6, 610:670]
    m = reg.sum(axis=2) < 620
    ys, xs = np.where(m)
    if len(xs):
        cols = sorted(set((610 + x) for x in xs.tolist()))
        groups = []
        for x in cols:
            if groups and x - groups[-1][-1] <= 2: groups[-1].append(x)
            else: groups.append([x])
        px = reg[m]
        dk = px[px.sum(axis=1) < px.sum(axis=1).min() + 120]
        print(f'   {lab}: {len(groups)} dot clusters at x={[g[0] for g in groups]} color(dark)={dk.mean(axis=0).round(0)}')

print('\n== G. red output arrows + green arrows + house arrows census ==')
redm = (R > 140) & (G < 105) & (B < 95)
for y0, y1, lab in ((56, 86, 'red arrows output zone'), (470, 486, 'MHA->X red?')):
    colc = redm[y0:y1].sum(axis=0)
    xs = [x for x in range(140, 900) if colc[x] >= 3]
    groups = []
    for x in xs:
        if groups and x - groups[-1][1] <= 3: groups[-1][1] = x
        else: groups.append([x, x])
    print(f'   {lab}: {len(groups)} clusters {[g[0] for g in groups]}')
greenm = (G > 120) & (G - R > 30) & (G - B > 30)
for y0, y1, lab in ((128, 146, 'green Y->plus unit1'), (236, 256, 'green rowA->FFN?'), (340, 360, 'green Y->plus unit2'), (296, 312, 'green LN1->rowB')):
    colc = greenm[y0:y1].sum(axis=0)
    xs = [x for x in range(140, 900) if colc[x] >= 2]
    groups = []
    for x in xs:
        if groups and x - groups[-1][1] <= 3: groups[-1][1] = x
        else: groups.append([x, x])
    print(f'   {lab} y{y0}-{y1}: {len(groups)} clusters')
lav = (R > 185) & (B > 195) & (B > G + 8)
for y0, y1, lab in ((190, 206, 'house arrows FFN-gap-up'), (266, 280, 'house arrows FFN-gap-down'), (402, 418, 'zone1'), (468, 486, 'zone2')):
    colc = lav[y0:y1].sum(axis=0)
    xs = [x for x in range(140, 900) if colc[x] >= 2]
    groups = []
    for x in xs:
        if groups and x - groups[-1][1] <= 4: groups[-1][1] = x
        else: groups.append([x, x])
    groups = [g for g in groups if g[1] - g[0] >= 3]
    print(f'   {lab}: {len(groups)} clusters widths {[g[1]-g[0]+1 for g in groups]}')

print('\n== H. container (tan panel) borders + fill ==')
for lab, prof in (('left x120..135 @y250', [(x, tuple(A[250, x])) for x in range(120, 136)]),
                  ('right x888..902 @y250', [(x, tuple(A[250, x])) for x in range(888, 903)]),
                  ('top y84..92 @x500', [(y, tuple(A[y, 500])) for y in range(84, 93)]),
                  ('bottom y474..482 @x300', [(y, tuple(A[y, 300])) for y in range(474, 483)])):
    print(f'   {lab}: {prof}')
freg = A[300:310, 430:470].reshape(-1, 3)
print(f'   container fill median (300..310,430..470): {np.median(freg, axis=0)}')

print('\n== I. vertical title metrics ==')
tm = (R > 90) & (R - G > 35) & (R - B > 30) & (G < 130)
sub = tm[95:515, 70:150]
colcnt = sub.sum(axis=0)
xs = [70 + i for i, n in enumerate(colcnt) if n > 3]
print(f'   glyph cap extent x {min(xs)}..{max(xs)} (cap h={max(xs)-min(xs)+1}px = {(max(xs)-min(xs)+1)/SX:.1f}pt wide)')
rowcnt = sub.sum(axis=1)
bands = []
inb = False
for i, n in enumerate(rowcnt):
    if n > 2 and not inb: st = 95 + i; inb = True
    elif n <= 2 and inb: bands.append((st, 95 + i - 1)); inb = False
if inb: bands.append((st, 514))
bands = [b for b in bands if b[1] - b[0] >= 2]
print(f'   letter bands (y): {bands}')
starts = [b[0] for b in bands]
pitch = np.diff(starts)
print(f'   letter pitch (cap-top deltas): {list(pitch)} mean={np.mean(pitch):.1f}px = {np.mean(pitch)/SY:.1f}pt')
ink = A[95:515, 70:150][tm]
print(f'   title ink color mean: {ink.mean(axis=0).round(0)}')

print('\n== J. Block Output / Input boxes + text metrics ==')
redm2 = (R > 130) & (R - G > 50) & (R - B > 45) & (G < 110)
for lab, y0, y1 in (('BlockOutput', 46, 96), ('BlockInput', 470, 520)):
    sub = redm2[y0:y1, 48:190]
    ys, xs = np.where(sub)
    if len(xs):
        bx0, bx1, by0, by1 = 48 + xs.min(), 48 + xs.max(), y0 + ys.min(), y0 + ys.max()
        print(f'   {lab} red-ink bbox: x {bx0}..{bx1} y {by0}..{by1} -> slide x {sx(bx0):.1f}..{sx(bx1):.1f} y {sy(by0):.1f}..{sy(by1):.1f}')
        # text-only cap: rows with moderate counts (borders are 1-2 rows at extremes)
        rows = [(y, int(redm2[y, bx0:bx1+1].sum())) for y in range(by0, by1 + 1)]
        inner = [y for y, n in rows if 3 <= n <= 60]
        print(f'      text-ish rows: {inner[0]}..{inner[-1]} (cap h={inner[-1]-inner[0]+1}px)')

print('\n== K. badge numeral (clean) ==')
sub = A[60:84, 864:896]
dk = sub.sum(axis=2) < 300
ys, xs = np.where(dk)
if len(ys):
    print(f'   numeral ink bbox: x {864+xs.min()}..{864+xs.max()} y {60+ys.min()}..{60+ys.max()} '
          f'(cap h={ys.max()-ys.min()+1}px = {(ys.max()-ys.min()+1)/SY:.1f}pt) color={sub[dk].mean(axis=0).round(0)}')

print('\n== L. strip cell segments (output row col1, y=70) + X row (y=499) ==')
for y in (70, 499):
    print(f'   y={y}:', [(x, tuple(A[y, x])) for x in range(180, 236, 4)])

print('\n== M. video strip + cursor check ==')
print('   strip top: y=517 dark (56,0,0)-> y518 black; strip spans to y=539')
print('   cursor: m1 noted none on 47? check white-bright cluster near LN bar 220..260,96..110:')
reg = A[96:112, 215:265]
wm = (reg[..., 0] > 245) & (reg[..., 1] > 245) & (reg[..., 2] > 245)
print('   white px count in that window:', int(wm.sum()))
