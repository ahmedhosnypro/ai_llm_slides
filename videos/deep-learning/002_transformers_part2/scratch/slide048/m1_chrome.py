#!/usr/bin/env python3
"""m1_chrome.py — chrome landmarks of slide_048.jpg (960x540, 1px = 1pt).

Measures the playlist house-chrome elements ON THIS FRAME (read-only):
  - white canvas bounds, gray panel E9E9E7 bounds, red C00000 border strokes
  - badge disc geometry (reusing badge_audit detection constants), occlusion state
  - the unexpected black bottom band (spec-vs-frame item)
Writes m1_output.txt (this dir). READ-ONLY on the frame; writes only here.
"""
from PIL import Image
import numpy as np

VID = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2'
F = f'{VID}/unique_slides/slide_048.jpg'
im = Image.open(F).convert('RGB')
A = np.asarray(im).astype(int)
H, W = A.shape[:2]
R, G, B = A[..., 0], A[..., 1], A[..., 2]
out = []
def p(*a):
    s = ' '.join(str(x) for x in a)
    out.append(s); print(s)

def mask(c, tol=12):
    return (np.abs(A - np.array(c)).max(axis=2) <= tol)

def spans(bool_1d, min_len=1):
    out_ = []
    i = 0; n = len(bool_1d)
    while i < n:
        if bool_1d[i]:
            j = i
            while j < n and bool_1d[j]:
                j += 1
            if j - i >= min_len:
                out_.append((i, j - 1))
            i = j
        else:
            i += 1
    return out_

p('=== m1_chrome: slide_048.jpg ===', f'{W}x{H}')
p()

# --- 1. white canvas ---
wht = (R > 245) & (G > 245) & (B > 245)
p('white px total:', int(wht.sum()))
# canvas corners
p('corner px (0,0):', A[0, 0], '(959,0):', A[0, 959], '(0,539):', A[539, 0], '(959,539):', A[539, 959])
p()

# --- 2. gray panel E9E9E7 ---
g = mask((0xE9, 0xE9, 0xE7), 10)
gcols, grows = g.sum(axis=0), g.sum(axis=1)
xs = np.where(gcols > H * 0.3)[0]
ys = np.where(grows > W * 0.3)[0]
p('panel gray col span:', (int(xs.min()), int(xs.max())) if len(xs) else None,
  ' row span:', (int(ys.min()), int(ys.max())) if len(ys) else None)
p('gray px total:', int(g.sum()))
# gray visible rows profile (where is gray actually visible around content?)
grows_vis = g.sum(axis=1)
vis_rows = [y for y in range(H) if grows_vis[y] > 50]
p('rows with >50 gray px:', (vis_rows[0], vis_rows[-1]) if vis_rows else None,
  ' count:', len(vis_rows))
gcols_vis = g.sum(axis=0)
vis_cols = [x for x in range(W) if gcols_vis[x] > 50]
p('cols with >50 gray px:', (vis_cols[0], vis_cols[-1]) if vis_cols else None,
  ' count:', len(vis_cols))
p()

# --- 3. red border C00000 ---
r = mask((0xC0, 0x00, 0x00), 60)
rcol, rrow = r.sum(axis=0), r.sum(axis=1)
strong_cols = [int(x) for x in range(W) if rcol[x] > 200]
strong_rows = [int(y) for y in range(H) if rrow[y] > 300]
p('red strong cols (cnt>200):', strong_cols)
p('red strong rows (cnt>300):', strong_rows)
# sample border colors
p('border sample colors: (42,300):', A[300, 42], '(43,300):', A[300, 43],
  '(300,44):', A[300, 44], '(918,300):', A[300, 918], '(45,500):', A[45, 500])
p()

# --- 4. black bottom band ---
blk = (R < 40) & (G < 40) & (B < 40)
bcols, brows = blk.sum(axis=0), blk.sum(axis=1)
band_rows = [y for y in range(H) if brows[y] > 200]
band_cols = [x for x in range(W) if bcols[x] > 15]
p('black band rows (cnt>200):', (band_rows[0], band_rows[-1]) if band_rows else None)
p('black band cols (cnt>15):', (band_cols[0], band_cols[-1]) if band_cols else None)
p('black px total:', int(blk.sum()))
if band_rows:
    y0 = band_rows[0]
    row = A[y0 + 2]
    p(f'sample row {y0+2}: x=20:', row[20], 'x=30:', row[30], 'x=40:', row[40],
      'x=500:', row[500], 'x=940:', row[940], 'x=955:', row[955])
p()

# --- 5. badge disc (audit method: pale-yellow threshold in chrome corner) ---
corner = np.zeros((H, W), bool)
corner[:170, 830:] = True
yel = (R > 215) & (G > 205) & (B < 215) & (R - B > 35) & (G - B > 35) & corner
ys_, xs_ = np.where(yel)
if len(xs_):
    bx0, bx1, by0, by1 = xs_.min(), xs_.max(), ys_.min(), ys_.max()
    p('badge yellow bbox:', [int(bx0), int(by0), int(bx1), int(by1)],
      ' yellow px:', int(yel.sum()))
    cx, cy = float(xs_.mean()), float(ys_.mean())
    p('badge yellow centroid:', (round(cx, 1), round(cy, 1)))
    p('disc fill RGB (median of yellow px):', [int(np.median(A[ys_, xs_][:, i])) for i in range(3)])
# purple ring 6A5ACD
pur = mask((0x6A, 0x5A, 0xCD), 45) & corner
if pur.sum():
    pys, pxs = np.where(pur)
    p('purple ring bbox:', [int(pxs.min()), int(pys.min()), int(pxs.max()), int(pys.max())],
      ' ring px:', int(pur.sum()))
else:
    p('purple ring: none found in corner')
# occlusion check: green box edge at badge columns
p('occlusion: rows y=70..76 at x=876..881 (should turn green at y=72):')
for y in range(70, 77):
    p(' y=%d:' % y, ' '.join(str(tuple(A[y, x])) for x in range(876, 882, 3)))
p()

# --- 6. chrome-vs-frame mapping summary (numbers for MEASUREMENTS.md) ---
p('HOUSE CHROME LAW (recreation-binding): canvas FFFFFF; panel E9E9E7 x42..918 y45..540;')
p('  red C00000 border panel L/R/T; badge circle d~36 center (893,71) fill FDFD96 ring 6A5ACD numeral 333333 Arial 18pt bold.')
p('  (Recreation uses the LAW values regardless of this frame; this file records the FRAME.)')

with open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide048/m1_output.txt', 'w') as f:
    f.write('\n'.join(out) + '\n')
