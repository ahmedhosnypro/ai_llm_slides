#!/usr/bin/env python3
"""measure2.py — pass 2: panel borders (right/top), title clean bbox, note box
geometry+colors, grid extents via non-white ink, gridline detection."""
from PIL import Image
import numpy as np

IMG = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_044.jpg"
im = Image.open(IMG).convert("RGB")
a = np.asarray(im).astype(int)
H, W = a.shape[:2]
R, G, B = a[..., 0], a[..., 1], a[..., 2]

def runs(mask_1d, min_len=1):
    idx = np.where(mask_1d)[0]
    if len(idx) == 0:
        return []
    out, s, p = [], idx[0], idx[0]
    for v in idx[1:]:
        if v == p + 1:
            p = v
        else:
            if p - s + 1 >= min_len:
                out.append((s, p))
            s = p = v
    if p - s + 1 >= min_len:
        out.append((s, p))
    return out

# --- panel borders, low threshold ---
redish = (R > 110) & (R - G > 40) & (R - B > 40)
colcnt = redish[:519].sum(axis=0)  # above black bar
print("redish col profile x 50..70:", {x: int(colcnt[x]) for x in range(50, 71)})
print("redish col profile x 875..930:", {x: int(colcnt[x]) for x in range(875, 931)})
rowcnt = redish[:, 60:880].sum(axis=1)
print("redish row profile y 38..55:", {y: int(rowcnt[y]) for y in range(38, 56)})
print("redish row profile y 505..525:", {y: int(rowcnt[y]) for y in range(505, 526)})

# --- clean title bbox: red ink x 62..880, y 48..118 ---
tm = redish.copy()
tm[:, :62] = False; tm[:, 880:] = False; tm[:48] = False; tm[118:] = False
ys, xs = np.where(tm)
print(f"TITLE ink bbox x {xs.min()}..{xs.max()} y {ys.min()}..{ys.max()} (w {xs.max()-xs.min()+1} h {ys.max()-ys.min()+1})")
# per-row red counts to find cap top / baseline
rc = tm.sum(axis=1)
print("title row counts y48..118:", {y: int(rc[y]) for y in range(48, 119) if rc[y] > 0})

# --- note box region: y 388..518, x 60..720: non-white ink ---
nb = a[388:519, 40:740]
nwr = nb[..., 0]; nwg = nb[..., 1]; nwb = nb[..., 2]
nonwhite = (nwr < 240) | (nwg < 240) | (nwb < 240)
ys2, xs2 = np.where(nonwhite)
print(f"NOTEBOX region ink bbox (offsets +40,+388): x {xs2.min()+40}..{xs2.max()+40} y {ys2.min()+388}..{ys2.max()+388}")
# modal non-white colors
q = (nb[nonwhite] // 8) * 8
vals, counts = np.unique(q, axis=0, return_counts=True)
order = np.argsort(-counts)[:8]
print("notebox modal nonwhite colors:", [(tuple(int(c) for c in vals[i]), int(counts[i])) for i in order])

# scan a horizontal line through the note box to find border x positions
for y in [395, 420, 450, 480, 505]:
    row = a[y]
    nz = np.where((row[:, 0] < 240) | (row[:, 1] < 240) | (row[:, 2] < 240))[0]
    nz = nz[(nz > 40) & (nz < 760)]
    if len(nz):
        segs = runs(np.isin(np.arange(960), nz))
        print(f"notebox row {y} ink col runs:", segs[:12])

# scan vertical line through the note box for border y positions
for x in [80, 100, 300, 650]:
    col = a[:, x]
    nz = np.where((col[:, 0] < 240) | (col[:, 1] < 240) | (col[:, 2] < 240))[0]
    nz = nz[(nz > 388) & (nz < 519)]
    if len(nz):
        segs = runs(np.isin(np.arange(540), nz))
        print(f"notebox col {x} ink row runs (y388..519):", segs[:12])

# --- grids: non-white, non-red ink inside inner frame y 130..384 ---
ink = (R < 235) | (G < 235) | (B < 235)
ink[:130] = False; ink[385:] = False; ink[:, :62] = False; ink[:, 880:] = False
# exclude red frame rows/cols already known (77,885,122,386)
icol = ink.sum(axis=0); irow = ink.sum(axis=1)
print("inner ink col runs (>=50):", [(s, e, int(icol[s:e+1].max())) for s, e in runs(icol >= 50)][:30])
print("inner ink row runs (>=50):", [(s, e, int(irow[s:e+1].max())) for s, e in runs(irow >= 50)][:30])
