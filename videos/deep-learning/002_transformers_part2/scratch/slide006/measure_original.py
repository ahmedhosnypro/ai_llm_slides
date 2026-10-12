#!/usr/bin/env python3
"""Measure slide_006.jpg chrome landmarks + content ink (frame px, 1px=1pt at frame scale)."""
from PIL import Image
import numpy as np, json, sys

p = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_006.jpg"
im = Image.open(p).convert("RGB")
W, H = im.size
a = np.asarray(im).astype(int)
R, G, B = a[:,:,0], a[:,:,1], a[:,:,2]
print(f"frame size: {W}x{H}")

# --- chrome red border strokes (C00000-ish): R high, G/B low
red = (R > 120) & (G < 90) & (B < 90)
# panel border: exclude badge region (badge ~x>850,y<110) for border scans
red_border = red.copy()
red_border[:115, 845:] = False

# vertical strokes: columns with many red px
colsum = red_border.sum(axis=0)
rowsum = red_border.sum(axis=1)
cand_cols = [x for x in range(W) if colsum[x] > 200]
cand_rows = [y for y in range(H) if rowsum[y] > 200]
print("red border candidate cols:", cand_cols[:10], "...", cand_cols[-10:] if len(cand_cols) > 10 else "")
print("red border candidate rows:", cand_rows[:10], "...", cand_rows[-10:] if len(cand_rows) > 10 else "")

# stroke center estimates: weighted centroid near each cluster
def centroid(vals, weights):
    vals = np.array(vals); weights = np.array(weights, dtype=float)
    return float((vals * weights).sum() / weights.sum())

def stroke_center(idxs, prof):
    grp = []
    groups = []
    for i in idxs:
        if grp and i == grp[-1] + 1:
            grp.append(i)
        else:
            if grp: groups.append(grp)
            grp = [i]
    if grp: groups.append(grp)
    out = []
    for g in groups:
        wsum = sum(prof[i] for i in g)
        c = sum(i * prof[i] for i in g) / wsum
        out.append((round(c, 2), g[0], g[-1], wsum))
    return out

print("\n-- vertical border strokes (center, first, last, mass) --")
print(stroke_center(cand_cols, colsum))
print("-- horizontal border strokes --")
print(stroke_center(cand_rows, rowsum))

# --- badge: yellow fill
yel = (R > 225) & (G > 225) & (B < 190)
ys, xs = np.where(yel)
if len(xs):
    print("\nbadge yellow bbox: x %d..%d (cx %.1f), y %d..%d (cy %.1f), n=%d" %
          (xs.min(), xs.max(), xs.mean(), ys.min(), ys.max(), ys.mean(), len(xs)))
    # purple ring pixels
    pur = (np.abs(R - 106) < 60) & (np.abs(G - 90) < 60) & (np.abs(B - 205) < 70) & (B > R) & (B > G)
    pys, pxs = np.where(pur)
    if len(pxs) > 50:
        print("purple ring bbox: x %d..%d (cx %.1f), y %d..%d (cy %.1f), n=%d" %
              (pxs.min(), pxs.max(), pxs.mean(), pys.min(), pys.max(), pys.mean(), len(pxs)))

# --- black bottom strip rows
dark = (R < 60) & (G < 60) & (B < 60)
drow = dark.sum(axis=1)
strip = [y for y in range(H) if drow[y] > 500]
print("\nblack strip rows:", (strip[0], strip[-1]) if strip else None)

# --- title ink: red-ish inside panel, excluding border rows/cols and badge
ink = red.copy()
y0, y1 = 60, 200
ink[:y0, :] = False; ink[y1:, :] = False
ink[:, :70] = False; ink[:, 890:] = False
tys, txs = np.where(ink)
print("\nTITLE red ink bbox: x %d..%d (cx %.1f, w %d), y %d..%d (cy %.1f), n=%d" %
      (txs.min(), txs.max(), txs.mean(), txs.max()-txs.min()+1,
       tys.min(), tys.max(), tys.mean(), len(tys)))
# core color census of title ink
core = a[tys, txs]
from collections import Counter
c = Counter(map(tuple, core))
print("title ink top colors:", c.most_common(8))

# --- agenda lines: blue ink (1414B8-family)
blue = (B > 130) & (R < 110) & (G < 110)
brow = blue.sum(axis=1)
lines = []
inl = False
for y in range(H):
    if brow[y] >= 3 and not inl:
        inl = True; start = y
    elif brow[y] < 3 and inl:
        inl = False; lines.append((start, y - 1))
if inl: lines.append((start, H - 1))
# merge gaps < 4
merged = []
for ln in lines:
    if merged and ln[0] - merged[-1][1] <= 4:
        merged[-1] = (merged[-1][0], ln[1])
    else:
        merged.append(list(ln))
print("\nBLUE line bands (y0,y1,height):")
for (y0b, y1b) in merged:
    band = blue[y0b:y1b+1, :]
    bys, bxs = np.where(band)
    if len(bxs) < 20: continue
    print("  y %d..%d h=%d | x %d..%d (w %d, cx %.1f) npx=%d" %
          (y0b, y1b, y1b - y0b + 1, bxs.min(), bxs.max(), bxs.max()-bxs.min()+1, bxs.mean(), len(bxs)))

# --- background samples
print("\nbg samples: panel(200,300)=%s (480,450)=%s outside(20,270)=%s (940,270)=%s" %
      (tuple(a[300,200]), tuple(a[450,480]), tuple(a[270,20]), tuple(a[270,940])))
# --- bottom strip color + extent
if strip:
    y = (strip[0] + strip[-1]) // 2
    row = a[y]
    print("strip row %d samples x=100..900: %s" % (y, [tuple(row[x]) for x in (50, 100, 300, 480, 700, 900, 930)]))
    # find strip horizontal extent
    dcols = [x for x in range(W) if dark[y, x]]
    print("strip dark cols at y=%d: %d..%d" % (y, dcols[0], dcols[-1]) if dcols else "none")
