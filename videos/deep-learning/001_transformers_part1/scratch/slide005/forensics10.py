#!/usr/bin/env python3
"""Forensics 10: tri2 absence check, tri4 devmap, block arrow, hatch arrow, caption weight, callout interior."""
import numpy as np
from PIL import Image
from collections import Counter

im = np.asarray(Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_005.jpg").convert("RGB")).astype(int)
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]

def devmap(xa, xb, ya, yb, label, thr=14, step=1):
    print(f"--- {label} (x{xa}-{xb}, y{ya}-{yb}, thr{thr}) ---")
    for y in range(ya, yb, step):
        row = []
        for x in range(xa, xb):
            px = im[y, x]
            d_panel = abs(int(px[0])-233)+abs(int(px[1])-233)+abs(int(px[2])-231)
            d_line = abs(int(px[0])-167)+abs(int(px[1])-175)+abs(int(px[2])-184)
            row.append("X" if min(d_panel, d_line) > thr else ".")
        print(f"{y:3d} " + "".join(row))

# tri2 absence check at low threshold
devsum_low = {}
for xa, xb, ya, yb, lbl in [(246, 306, 330, 465, "gap1 lower tri2")]:
    tot = 0
    for x in range(xa, xb):
        for y in range(ya, yb):
            px = im[y, x]
            d = min(abs(int(px[0])-233)+abs(int(px[1])-233)+abs(int(px[2])-231),
                    abs(int(px[0])-167)+abs(int(px[1])-175)+abs(int(px[2])-184))
            if d > 14:
                tot += 1
    print(f"{lbl}: total dev px thr14 = {tot}")

# tri4 devmap
devmap(679, 738, 190, 265, "gap3 tri4", thr=18)

# block arrow devmap
devmap(246, 310, 300, 330, "block arrow", thr=18)

# hatch arrow: sample three x-windows
devmap(170, 260, 468, 500, "hatch left", thr=18)
devmap(560, 650, 468, 500, "hatch right", thr=18)

# caption: looser blue mask, per-column ink to find bold segment + underline
lbl = (b - r > 25) & (b > 90)
m = lbl[500:530, 150:860]
colsum = m.sum(axis=0)
print("=== caption per-column blue count (x150-860) ===")
xs = [i + 150 for i, v in enumerate(colsum) if v > 0]
print(f"cols with ink: {xs[0]}..{xs[-1]}, n={len(xs)}")
# density profile in 20px buckets
for x0 in range(150, 860, 40):
    seg = colsum[x0-150:x0-110]
    print(f"  x{x0}-{x0+39}: {int(seg.sum())}", end="")
print()
# underline check rows 519-524 loose
for y in range(518, 526):
    rowxs = np.where(m[y-500, :])[0] + 150
    if len(rowxs):
        runs = []
        s = p = rowxs[0]
        for x in rowxs[1:]:
            if x == p + 1: p = x
            else: runs.append((s, p)); s = p = x
        runs.append((s, p))
        print(f"y={y}: n={len(rowxs)} longest run {max(rn[1]-rn[0] for rn in runs)}")

# callout interior + border color
print("callout interior avg (550,120-135):", tuple(round(v,1) for v in im[120:135, 540:560].reshape(-1,3).mean(axis=0)))
print("callout top border rows y111-116 at x550:", [tuple(int(v) for v in im[y,550]) for y in range(110,118)])
print("callout left border x458-464 at y126:", [tuple(int(v) for v in im[126,x]) for x in range(456,466)])

# kernel rect fill modal
patch = im[100:109, 70:135].reshape(-1, 3)
print("kernel rect1 modal:", Counter(tuple(int(v)//8*8 for v in p) for p in patch).most_common(2))
patch = im[132:140, 70:135].reshape(-1, 3)
print("kernel rect3 modal:", Counter(tuple(int(v)//8*8 for v in p) for p in patch).most_common(2))

# tri1 stroke color
print("tri1 stroke sample (upper hyp mid, ~(270,192)):", [tuple(int(v) for v in im[y,x]) for y,x in [(192,268),(193,269),(196,272),(220,290)]])
# seq shaft color
print("seq shaft sample x152-153:", [tuple(int(v) for v in im[y,152]) for y in (200, 300, 400)])
# leader color
print("leader sample (445,137) region:", [tuple(int(v) for v in im[y,x]) for y,x in [(137,445),(138,444),(140,441)]])
# bar edge color
print("bar1 left edge col x413:", [tuple(int(v) for v in im[y,413]) for y in (200,300,400)])
# stack outline col x163
print("stack1 left edge x163:", [tuple(int(v) for v in im[y,163]) for y in (200,300,400)])
