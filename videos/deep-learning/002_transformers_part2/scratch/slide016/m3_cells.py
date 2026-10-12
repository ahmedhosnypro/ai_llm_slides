#!/usr/bin/env python3
# m3_cells.py — slide 016 matrix cells (3 x 4x4) + output cells (3 x 5x4):
# per-cell bbox, fill, text-core color, border color. Frame px.
from PIL import Image
import numpy as np
from scipy import ndimage

im = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_016.jpg").convert("RGB")
a = np.asarray(im).astype(int)
H, W = a.shape[:2]
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]

def cc(mask, minpx=4):
    lab, n = ndimage.label(mask, structure=np.ones((3, 3)))
    comps = []
    for sl in ndimage.find_objects(lab):
        ys, xs = sl
        npx = int(mask[sl].sum())
        if npx >= minpx:
            comps.append((xs.start, ys.start, xs.stop - 1, ys.stop - 1, xs.stop - xs.start, ys.stop - ys.start, npx))
    return sorted(comps, key=lambda c: (c[1], c[0]))

def med(x0, y0, x1, y1):
    p = a[y0:y1 + 1, x0:x1 + 1].reshape(-1, 3)
    m = np.median(p, axis=0).astype(int)
    return "#%02X%02X%02X" % (m[0], m[1], m[2])

CONTAINERS = [("Head1", 311, 459), ("Head2", 476, 624), ("Head3", 636, 781)]
CFILL = {"Head1": (214, 255, 230), "Head2": (248, 230, 208), "Head3": (213, 213, 251)}

print("=== MATRIX CONTAINERS (measured edges) ===")
for nm, cx0, cx1 in CONTAINERS:
    f = np.array(CFILL[nm])
    d = np.abs(a[:, cx0 - 6:cx1 + 7] - f).max(axis=2)
    m = d <= 12
    cs = [c for c in cc(m, 4000)]
    if cs:
        c = max(cs, key=lambda c: c[6])
        print(f"{nm}: fill-comp fx {c[0]}..{c[2]} fy {c[1]}..{c[3]} (w{c[4]} h{c[5]}) fill {med(c[0]+8, c[1]+8, c[0]+14, c[1]+14)}")

print("=== MATRIX CELLS: 3 containers x 16 cells ===")
for nm, cx0, cx1 in CONTAINERS:
    f = np.array(CFILL[nm])
    sub = a[128:312, cx0 - 2:cx1 + 3]
    d = np.abs(sub - f).max(axis=2)
    m = d > 30
    cs = [c for c in cc(m, 80) if 18 <= c[4] <= 42 and 14 <= c[5] <= 34]
    # merge fragments: cluster by grid proximity (round to 25px bins)
    cells = {}
    for c in cs:
        key = ((c[0] - cx0) // 34, (c[1] - 128) // 33)
        cells.setdefault(key, []).append(c)
    merged = []
    for k, group in cells.items():
        x0 = min(g[0] for g in group); y0 = min(g[1] for g in group)
        x1 = max(g[2] for g in group); y1 = max(g[3] for g in group)
        merged.append((x0 + cx0 - 2, y0 + 128, x1 + cx0 - 2, y1 + 128, len(group)))
    merged = [c for c in merged if (c[2] - c[0]) >= 18 and (c[3] - c[1]) >= 14]
    merged.sort(key=lambda c: (c[1], c[0]))
    print(f"--- {nm}: {len(merged)} cells (grid-merged)")
    for (x0, y0, x1, y1, nfrag) in merged:
        fill = med(x0 + 2, y0 + 2, x0 + 6, y0 + 6)
        cxm, cym = (x0 + x1) // 2, (y0 + y1) // 2
        tp = a[max(y0+2,0):y1-1, max(x0+2,0):x1-1].reshape(-1, 3)
        dark = tp[tp.sum(axis=1) < tp.sum(axis=1).min() + 150]
        tcol = "#%02X%02X%02X" % tuple(np.median(dark, axis=0).astype(int)) if len(dark) else "n/a"
        bord = med(x0, (y0 + y1) // 2, x0 + 1, (y0 + y1) // 2)
        print(f"    cell ({x0},{y0})..({x1},{y1}) w{x1-x0+1} h{y1-y0+1} fill {fill} text {tcol} borderL {bord} frag{nfrag}")

print("=== OUTPUT CELLS: text-anchored (y_j glyph comps), 3 groups x 5 rows ===")
reg = np.zeros((H, W), bool)
reg[330:484, 298:782] = True
tm = reg & (R + G + B < 560) & (R - (G + B) / 2 > 25)
tcs = cc(tm, 6)
print(f"dark-red text comps: {len(tcs)}")
# cluster into grid: fx groups (3), fy rows (5)
gx = {}
for c in tcs:
    key = 0 if c[0] < 470 else (1 if c[0] < 640 else 2)
    gx.setdefault(key, []).append(c)
for g in sorted(gx):
    cs = gx[g]
    rows = {}
    for c in cs:
        rows.setdefault(round((c[1] + c[3]) / 2 / 29), []).append(c)
    print(f"--- group {g+1}: {len(cs)} text comps in {len(rows)} row-bands")
    gxs = [c[0] for c in cs]
    print(f"    fx span {min(gxs)}..{max(c[2] for c in cs)}")
    for rk in sorted(rows):
        rcs = rows[rk]
        y0 = min(c[1] for c in rcs); y1 = max(c[3] for c in rcs)
        cols = sorted(set(round((c[0]) / 38) for c in rcs))
        print(f"    row~fy {y0}..{y1}: {len(rcs)} comps")
# per-cell fill: derive cell boxes from text rows/cols then sample around text
print("=== OUTPUT CELL GRID (fit from text anchors) ===")
for g in sorted(gx):
    cs = gx[g]
    ys = sorted(set(round((c[1] + c[3]) / 2 / 29) for c in cs))
    xs = sorted(set(round(c[0] / 38) for c in cs))
    print(f"group {g+1}: row centers fy ~{[round((k*29)) for k in ys]}")
    for rk in ys:
        rcs = [c for c in cs if round((c[1] + c[3]) / 2 / 29) == rk]
        y0 = min(c[1] for c in rcs) - 5; y1 = max(c[3] for c in rcs) + 5
        fills = []
        for c in sorted(rcs, key=lambda c: c[0]):
            # sample fill just left of glyph and just right
            lx = max(c[0] - 4, 300)
            rx = min(c[2] + 4, 780)
            fills.append(med(lx, (c[1] + c[3]) // 2, lx + 2, (c[1] + c[3]) // 2))
            fills.append(med(rx, (c[1] + c[3]) // 2, rx + 2, (c[1] + c[3]) // 2))
        print(f"    row fy {y0}..{y1}: cell-fill samples {fills[:8]}")
