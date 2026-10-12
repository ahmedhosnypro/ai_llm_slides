#!/usr/bin/env python3
"""measure3.py — pass 3: per-grid geometry (gridlines, cells, fills, numerals),
bullet-line segment runs, operators, note-box border/text lines, mystery band."""
from PIL import Image
import numpy as np

IMG = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_044.jpg"
im = Image.open(IMG).convert("RGB")
a = np.asarray(im).astype(int)
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

def modal(region, n=6):
    q = (region.reshape(-1, 3) // 8) * 8
    vals, counts = np.unique(q, axis=0, return_counts=True)
    order = np.argsort(-counts)[:n]
    return [(tuple(int(c) for c in vals[i]), int(counts[i])) for i in order]

GRIDS = {"g77": (101, 377), "f33": (440, 526), "o55": (622, 819)}
for name, (x0, x1) in GRIDS.items():
    sub = a[160:390, x0:x1 + 1]
    ink = (sub[..., 0] < 235) | (sub[..., 1] < 235) | (sub[..., 2] < 235)
    r = ink.sum(axis=1)
    rr = runs(r >= 3)
    print(f"{name}: x {x0}..{x1} row runs:", [(s + 160, e + 160) for s, e in rr])
    # gridlines = dark rows/cols
    dark = (sub[..., 0] < 120) & (sub[..., 1] < 120) & (sub[..., 2] < 120)
    dc = dark.sum(axis=0); dr = dark.sum(axis=1)
    print(f"{name} dark col runs (>=60% of height):",
          [(s + x0, e + x0) for s, e in runs(dc >= 0.6 * dark.shape[0])])
    print(f"{name} dark row runs (>=60% of width):",
          [(s + 160, e + 160) for s, e in runs(dr >= 0.6 * dark.shape[1])])

# per-cell modal fills for each grid (using 7x7 as example first) — full cell maps
def cell_map(name, x0, x1, y0, y1, n, m):
    print(f"--- {name} cells ({n}x{m}) x{x0}..{x1} y{y0}..{y1} ---")
    cw = (x1 - x0 + 1) / n
    ch = (y1 - y0 + 1) / m
    for r in range(m):
        row = []
        for c in range(n):
            cx0 = int(x0 + c * cw + cw * 0.25); cx1 = int(x0 + (c + 1) * cw - cw * 0.25)
            cy0 = int(y0 + r * ch + ch * 0.25); cy1 = int(y0 + (r + 1) * ch - ch * 0.25)
            reg = a[cy0:cy1 + 1, cx0:cx1 + 1]
            mm = modal(reg, 3)
            # classify: cyan / green / yellow / other
            top = mm[0][0]
            row.append(top)
        print(f"  row {r+1}: " + " | ".join(str(t) for t in row))

# 7x7: x 101..377, y? — row extent from its own run; use band y 173..382 provisionally
cell_map("7x7 provisional", 101, 377, 173, 382, 7, 7)

# mystery band x 672..759 y 389..515
print("mystery band x672..759 y389..515 modal:", modal(a[389:516, 672:760]))
print("mystery band sample rows:")
for y in [400, 430, 460, 490]:
    print(f"  row {y}:", [tuple(a[y, x]) for x in [660, 675, 700, 730, 755, 765]])

# bullet line: ink runs at y 136..153
band = a[130:158, 62:880]
ink = (band[..., 0] < 200) | (band[..., 1] < 200) | (band[..., 2] < 200)
colc = ink.sum(axis=0)
print("bullet ink col runs (>=2):", [(s + 62, e + 62) for s, e in runs(colc >= 2, min_len=2)][:40])
# orange bullet pixels
orange = (R > 180) & (G > 100) & (G < 190) & (B < 120)
om = orange[130:158, :].sum(axis=0)
print("orange col runs y130..158:", [(s, e) for s, e in runs(om >= 1)])

# operators * and =: ink in gaps
for label, (gx0, gx1) in [("star gap", (380, 438)), ("eq gap", (528, 620))]:
    band2 = a[160:390, gx0:gx1]
    ink2 = (band2[..., 0] < 150) & (band2[..., 1] < 150) & (band2[..., 2] < 150)
    ys, xs = np.where(ink2)
    if len(xs):
        print(f"{label}: ink x {xs.min()+gx0}..{xs.max()+gx0} y {ys.min()+160}..{ys.max()+160}")

# note box: exact border — scan row y=460 (mid) for the border strokes left/right
for y in [400, 450, 500]:
    row = a[y]
    # look for periwinkle-ish: B > R, moderate darkness
    idx = [x for x in range(60, 700) if row[x][2] - row[x][0] > 10 and row[x][2] > 150 and row[x][0] < 230]
    print(f"notebox border-ish cols at y{y}:", idx[:10], "...", idx[-10:] if len(idx) > 10 else "")
# note text line bboxes: navy ink (dark blue) in y 395..510, x 85..660
navy = (B > 80) & (B - R > 40) & (R < 120)
nm = navy.copy(); nm[:396] = False; nm[510:] = False; nm[:, :85] = False; nm[:, 660:] = False
nrow = nm.sum(axis=1)
print("note text row runs (>=3):", [(s, e) for s, e in runs(nrow >= 3)])
ncol = nm.sum(axis=0)
print("note text col extent:", runs(ncol >= 1)[:3], runs(ncol >= 1)[-3:] if len(runs(ncol >= 1)) else "")
