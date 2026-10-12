#!/usr/bin/env python3
"""Stage 4: panel interior — row bands, highlight fills (nearest-ref classification), outlines."""
import numpy as np
from PIL import Image

im = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_040.jpg')).astype(int)
r, g, b = im[:,:,0], im[:,:,1], im[:,:,2]

REFS = {
    'lavender':  (153,153,204),   # spec 9999CC
    'pink':      (255,156,156),   # spec FF9C9C
    'lightblue': (166,208,242),   # spec A6D0F2
    'green':     (144,238,144),   # spec 90EE90
    'orange':    (255,166,77),    # spec FFA64D
}
def class_mask(name, tol=42):
    rr, gg, bb = REFS[name]
    return (np.abs(r-rr)<tol) & (np.abs(g-gg)<tol) & (np.abs(b-bb)<tol)

def bbox_of(m, x0=0, x1=None, y0=0, y1=None):
    mm = np.zeros_like(m); mm[y0:y1, x0:x1] = m[y0:y1, x0:x1]
    ys, xs = np.where(mm)
    if len(xs)==0: return None
    return (int(xs.min()), int(xs.max()), int(ys.min()), int(ys.max()), int(mm.sum()))

# panel interior frame coords: x 147..551, y 206..496
PX0, PX1, PY0, PY1 = 148, 551, 206, 496
lum = (r+g+b)/3
dark = lum < 130

# --- row profile of dark ink in panel -> text/equation bands
prof = dark[PY0:PY1, PX0:PX1].sum(axis=1)
bands, in_b = [], False
for i, v in enumerate(prof):
    y = PY0 + i
    if v > 1 and not in_b: s, in_b = y, True
    elif v <= 1 and in_b:
        bands.append((s, y-1)); in_b = False
if in_b: bands.append((s, PY1-1))
print('dark-ink bands in panel (frame y):')
for (a, bb) in bands:
    ys, xs = np.where(dark[a:bb+1, PX0:PX1])
    print(f'  y {a}..{bb}  x {xs.min()+PX0}..{xs.max()+PX0}')

# --- highlight fills: bboxes per band region
print()
for name in REFS:
    m = class_mask(name)
    mm = np.zeros_like(m); mm[PY0:PY1, PX0:PX1] = m[PY0:PY1, PX0:PX1]
    ys, xs = np.where(mm)
    if len(xs)==0:
        print(f'{name}: none in panel'); continue
    # cluster by connected row-bands
    rowshas = np.where(mm.any(axis=1))[0]
    groups = []
    s = rowshas[0]; prev = rowshas[0]
    for y in rowshas[1:]:
        if y - prev > 4: groups.append((s, prev)); s = y
        prev = y
    groups.append((s, prev))
    print(f'{name}: {len(groups)} band(s)')
    for (a, bb) in groups:
        sub = mm[a:bb+1]
        xs2 = np.where(sub.any(axis=0))[0]
        # x-gaps -> separate rects on same band
        gaps = np.where(np.diff(xs2) > 6)[0]
        segs = []
        start = xs2[0]
        for gi in gaps:
            segs.append((start, xs2[gi])); start = xs2[gi+1]
        segs.append((start, xs2[-1]))
        for (xa, xb) in segs:
            cnt = int(sub[:, xa:xb+1].sum())
            # mean color of fill pixels
            sel = m[a:bb+1, xa:xb+1]
            mr = r[a:bb+1, xa:xb+1][sel].mean(); mg = g[a:bb+1, xa:xb+1][sel].mean(); mb = b[a:bb+1, xa:xb+1][sel].mean()
            print(f'   rect frame x {xa}..{xb} y {a}..{bb} n={cnt} meanRGB=({mr:.0f},{mg:.0f},{mb:.0f})')
