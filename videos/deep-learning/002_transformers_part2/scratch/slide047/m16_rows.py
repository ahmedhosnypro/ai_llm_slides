#!/usr/bin/env python3
"""m16_rows.py — per-row cell structure via 2pt-binned median color profiles,
sampled at label-free offsets (row_top+2 and row_bottom-2), + row edge detection."""
import numpy as np
from PIL import Image

F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_047.jpg"
A = np.asarray(Image.open(F).convert("RGB")).astype(int)
SX, OX, SY = 0.962329, 17.582, 0.955556
sx = lambda x: (x - OX) / SX
hx = lambda c: "#%02X%02X%02X" % tuple(int(round(v)) for v in c)

ROWS = {"output": (54, 80), "A": (172, 198), "B": (280, 307), "C": (382, 409), "X": (490, 515)}
for name, (y0, y1) in ROWS.items():
    print(f"== {name} rows {y0}..{y1} ==")
    for tag, yy in [("top+2", y0 + 2), ("bot-2", y1 - 3)]:
        line = A[yy]
        # cell-edge candidates: local darkness dips (borders) along x 175..905
        prof = []
        for x0 in range(178, 900, 4):
            c = np.median(A[yy - 1:yy + 2, x0:x0 + 4].reshape(-1, 3), axis=0)
            prof.append((x0, hx(c)))
        # print compact: only transitions (color changes vs prev)
        outl = []
        prev = None
        for x0, h in prof:
            if prev is None or h != prev:
                outl.append(f"{sx(x0):.0f}:{h}")
                prev = h
        print(f"  {tag} y={yy} transitions(slide_x:hex):", " ".join(outl))
    # label ink bbox: dark red px in row band, x 185..215 (col1)
    reg = A[y0:y1, 185:216]
    m = reg.sum(axis=2) < 430
    ys, xs = np.nonzero(m)
    if len(ys):
        print(f"  col1 label ink: y {y0+ys.min()}..{y0+ys.max()} x {185+xs.min()}..{185+xs.max()} -> slide y {sy_ := (y0+ys.min())/SY:.1f}..{(y0+ys.max())/SY:.1f} x {sx(185+xs.min()):.1f}..{sx(185+xs.max()):.1f} color {hx(np.median(reg[m],axis=0))}")
