#!/usr/bin/env python3
"""m2_panels.py — content panel landmarks on slide_048.jpg.

Main orange encoder panel, right green-bordered inset, thumbnail inset,
the maroon MHSA bar, the two tan LayerNorm bars, the MLP row, token rows,
plus-circles rows, dashed residual outlines. All bboxes in frame px (1px=1pt).
"""
from PIL import Image
import numpy as np

F = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_048.jpg'
A = np.asarray(Image.open(F).convert('RGB')).astype(int)
H, W = A.shape[:2]
R, G, B = A[..., 0], A[..., 1], A[..., 2]
out = []
def p(*a):
    s = ' '.join(str(x) for x in a); out.append(s); print(s)

def bbox(mask):
    ys, xs = np.where(mask)
    if not len(xs):
        return None
    return [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max()), int(mask.sum())]

def spans(bool_1d, min_len=2, gap=1):
    res = []
    i = 0; n = len(bool_1d)
    while i < n:
        if bool_1d[i]:
            j = i
            while j < n and (bool_1d[j] or (gap and bool_1d[j:j+gap].any())):
                j += 1
            if j - i >= min_len:
                res.append((i, j - 1))
            i = j
        else:
            i += 1
    return res

def med_rgb(m):
    ys, xs = np.where(m)
    if not len(xs):
        return None
    return [int(np.median(A[ys, xs][:, i])) for i in range(3)]

p('=== m2_panels: slide_048.jpg ===')
p()

# 1. main orange panel: fill ~FBE3C6
org = (np.abs(A - np.array((0xFB, 0xE3, 0xC6))).max(axis=2) <= 18)
# panel fill rows/cols (require wide runs to skip small orange arrows outside)
p('main panel fill FBE3C6-ish: bbox', bbox(org), 'median fill', med_rgb(org))
oc = (org[:, 200:900]).sum(axis=1)
rows = [y for y in range(H) if oc[y] > 300]
p('  fill rows span (>300 px in x200..900):', (rows[0], rows[-1]) if rows else None, 'count', len(rows))
occ = (org[100:500, :]).sum(axis=0)
cols = [x for x in range(W) if occ[x] > 150]
p('  fill cols span (>150 px in y100..500):', (cols[0], cols[-1]) if cols else None, 'count', len(cols))
# panel border: red-ish frame around the fill — scan row 300 and col 480 near fill edges
p('  row 270 x 110..135:', [(x, tuple(A[270, x])) for x in range(110, 135, 2)])
p('  row 270 x 895..915:', [(x, tuple(A[270, x])) for x in range(895, 915, 2)])
p('  col 480 y 78..95:', [(y, tuple(A[y, 480])) for y in range(78, 95, 2)])
p()

# 2. right inset: white fill + green border
grn = (G > 110) & (G - R > 40) & (G - B > 30)
gc = grn.sum(axis=0); gr = grn.sum(axis=1)
p('green-mask strong cols (cnt>150):', [int(x) for x in range(W) if gc[x] > 150])
p('green-mask strong rows (cnt>150):', [int(y) for y in range(H) if gr[y] > 150])
# inset interior white
wht = (R > 248) & (G > 248) & (B > 248)
p('white px in x620..890,y80..480:', int(wht[80:480, 620:890].sum()))
# sample border color top edge
p('  inset top border samples x=700: y 68..80:', [(y, tuple(A[y, 700])) for y in range(68, 80, 2)])
p('  inset left border samples y=300: x 608..625:', [(x, tuple(A[300, x])) for x in range(608, 625, 2)])
p('  inset right border samples y=300: x 880..895:', [(x, tuple(A[300, x])) for x in range(880, 895, 2)])
p('  inset bottom border samples x=700: y 478..492:', [(y, tuple(A[y, 700])) for y in range(478, 492, 2)])
p()

# 3. thumbnail inset (bottom-left): white + green border around x58..155,y415..490
p('thumb region row 450 x 50..160:', [(x, tuple(A[450, x])) for x in range(50, 160, 8)])
p('thumb region col 100 y 405..500:', [(y, tuple(A[y, 100])) for y in range(405, 500, 6)])
# green border of thumb
tg = grn[400:500, 40:170]
p('thumb green px:', int(tg.sum()))
p()

# 4. maroon MHSA bar ~7E2D5B
mar = (np.abs(A - np.array((0x7E, 0x2D, 0x5B))).max(axis=2) <= 30)
mr = mar.sum(axis=1)
mrows = [y for y in range(H) if mr[y] > 300]
p('maroon bar rows (>300 px):', (mrows[0], mrows[-1]) if mrows else None)
mcols = mar[mrows[0]:mrows[-1]+1].sum(axis=0) if mrows else []
mc = [x for x in range(W) if mcols[x] > 10]
p('maroon bar cols span:', (mc[0], mc[-1]) if mc else None)
p('maroon median fill:', med_rgb(mar))
p()

# 5. tan LayerNorm bars ~D9B779
tan = (np.abs(A - np.array((0xD9, 0xB7, 0x79))).max(axis=2) <= 25)
tr = tan[:, 150:600].sum(axis=1)
trows = spans(tr > 200)
p('tan bar row bands (x150..600, cnt>200):', trows)
for (y0, y1) in trows:
    seg = tan[y0:y1+1]
    tcs = seg.sum(axis=0)
    tcols = [x for x in range(W) if tcs[x] > (y1 - y0) * 0.5]
    p(f'  band y{y0}..{y1}: cols {tcols[0]}..{tcols[-1]}' if tcols else f'  band y{y0}..{y1}: no cols')
p('tan median fill:', med_rgb(tan))
p()

# 6. MLP row: pink boxes ~FF9FC5 with purple border ~9B2D86
pnk = (np.abs(A - np.array((0xFF, 0x9F, 0xC5))).max(axis=2) <= 30)
pr = pnk.sum(axis=1)
prows = [y for y in range(H) if pr[y] > 150]
p('pink MLP row rows (>150):', (prows[0], prows[-1]) if prows else None)
pc = pnk[prows[0]:prows[-1]+1].sum(axis=0) if prows else []
pcols = spans(pc > 3, min_len=10)
p('pink box col runs (min 10px):', pcols)
p('pink count:', int(pnk.sum()), 'median fill:', med_rgb(pnk))
# green neuron dots inside boxes
grn2 = (G > 120) & (G - R > 50) & (G - B > 50)
p('green dot px in MLP band:', int(grn2[prows[0]:prows[-1]+1, 140:620].sum()) if prows else 0)
p()

# 7. plus circles: red CC0000 discs in two rows
red = (R > 170) & (G < 80) & (B < 80)
p('red rows cnt>60:', spans(red.sum(axis=1) > 60))
# find circular red blobs rows (exclude bar rows) — probe specific bands later in m3
p()

# 8. token rows: colored small boxes at bottom (~y 495..515) and between layers
blue_tok = (np.abs(A - np.array((0x2E, 0x75, 0xB6))).max(axis=2) <= 35)
yel_tok = (np.abs(A - np.array((0xFF, 0xE1, 0x35))).max(axis=2) <= 40)
p('blue token px rows:', spans(blue_tok.sum(axis=1) > 20))
p('yellow token px rows:', spans(yel_tok.sum(axis=1) > 20))
p()

# 9. dashed residual outlines: orange E87722-ish dashed rounded rects
dash = (np.abs(A - np.array((0xE8, 0x77, 0x22))).max(axis=2) <= 40)
dr = dash.sum(axis=1)
p('orange-dash rows cnt>40:', spans(dr > 40, min_len=3))
p('orange-dash total px:', int(dash.sum()))

with open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide048/m2_output.txt', 'w') as f:
    f.write('\n'.join(out) + '\n')
