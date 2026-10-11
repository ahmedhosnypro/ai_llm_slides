#!/usr/bin/env python3
"""m5: X-extents of the inset boxes, arrow line columns, Q/K/V labels,
arrowhead locations; plus panel-interior fill sample."""
from PIL import Image
import numpy as np

V = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1"
im = np.asarray(Image.open(f"{V}/unique_slides/slide_038.jpg").convert("RGB")).astype(int)
R, G, B = im[:, :, 0], im[:, :, 1], im[:, :, 2]
ink = (R < 110) & (G < 110) & (B < 110)

X0, X1 = 760, 935

# box bands (from m4): (top_border_rows, bottom_border_rows, text_rows)
bands = [("MatMul(top)", 137, 155), ("SoftMax", 167, 185), ("Mask(opt.)", 196, 214),
         ("Scale", 225, 243), ("MatMul(bot)", 255, 273)]
for name, yt, yb in bands:
    brow = ink[yt, X0:X1] | ink[yt + 1, X0:X1]
    xs = np.where(brow)[0] + X0
    trow = ink[yt + 6:yb - 5, X0:X1].any(axis=0)
    txs = np.where(trow)[0] + X0
    print(f"{name}: border x[{xs.min()}..{xs.max()}]" if len(xs) else f"{name}: no border",
          f"| text x[{txs.min()}..{txs.max()}]" if len(txs) else "| no text")

# vertical arrow lines: columns with long dark runs below the boxes / between boxes
sub = ink[275:312, X0:X1]  # Q/K/V + arrow zone below bottom MatMul
cols = sub.sum(axis=0)
print("below-box zone cols (y275-311) count>6:", [(x + X0, int(c)) for x, c in enumerate(cols) if c > 6])

# between-box arrow segments (short verticals): scan each gap
gaps = [("A-B", 156, 166), ("B-C", 186, 195), ("C-D", 215, 224), ("D-E", 244, 254), ("above-A", 118, 136)]
for name, y0, y1 in gaps:
    seg = ink[y0:y1, X0:X1]
    cols = seg.sum(axis=0)
    hits = [(x + X0, int(c)) for x, c in enumerate(cols) if c > 3]
    print(f"gap {name} y[{y0},{y1}]:", hits)

# Q/K/V label bboxes below bottom MatMul (y276..300)
lab = ink[276:302, X0:X1]
ys, xs = np.where(lab)
if len(xs):
    # cluster by x-gaps
    order = np.argsort(xs); xs_s = xs[order]; ys_s = ys[order]
    start = 0
    for i in range(1, len(xs_s) + 1):
        if i == len(xs_s) or xs_s[i] - xs_s[i - 1] > 8:
            bx = xs_s[start:i]; by = ys_s[start:i]
            if len(bx) > 4:
                print(f"label cluster: x[{bx.min()+X0}..{bx.max()+X0}] y[{by.min()+276}..{by.max()+276}] n={len(bx)}")
            start = i

# panel interior fill + peach canvas color near the panel
print("panel interior sample (860,200):", tuple(im[200, 860]))
print("panel interior sample (850,300):", tuple(im[300, 850]))
print("left of panel (780,200):", tuple(im[200, 780]))
print("green border core (798,200):", tuple(im[200, 798]), "(913,200):", tuple(im[200, 913]))
print("top border core (860,116):", tuple(im[116, 860]), "bottom (860,311):", tuple(im[311, 860]))

# what's at green row y179 (22px)?
row = np.where(ink[179, X0:X1])[0] + X0
print("ink at y179:", row[:40])

# box border color sample + box fill samples
print("box border px (boxA top,830,137):", tuple(im[137, 830]))
for nm, ytxt in [("A", 146), ("B", 176), ("C", 205), ("D", 234), ("E", 264)]:
    fill = im[ytxt, 820]
    print(f"box {nm} fill sample (820,{ytxt}):", tuple(fill))
