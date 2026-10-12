#!/usr/bin/env python3
"""Forensics round 5: underline run decomposition, bold-stroke check, dot size."""
from PIL import Image
import numpy as np

SRC = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_006.jpg"
a = np.asarray(Image.open(SRC).convert("RGB")).astype(int)
R, G, B = a[..., 0], a[..., 1], a[..., 2]

def runs_of(mask_row, off):
    xs = np.nonzero(mask_row)[0]
    if len(xs) == 0: return []
    runs, s, p = [], xs[0], xs[0]
    for x in xs[1:]:
        if x == p + 1: p = x
        else: runs.append((s + off, p + off)); s = p = x
    runs.append((s + off, p + off))
    return runs

dk = (R < 190) & (G < 190) & (B < 190)
print("-- rows 153..162 contiguous runs (dark<190, x 90..700) --")
for y in range(153, 163):
    rr = runs_of(dk[y, 90:700], 90)
    print(f" row {y}: {[(int(u),int(v)) for u,v in rr if v-u >= 2]}")

# line 2 rows 180..186 runs
print("-- rows 179..187 runs --")
for y in range(179, 188):
    rr = runs_of(dk[y, 90:760], 90)
    print(f" row {y}: {[(int(u),int(v)) for u,v in rr if v-u >= 2]}")

# bold-stroke check: stem widths in bold phrase (x 93..469) vs regular tail (x 469..692), rows 145..155
def stem_stats(x0, x1, y0, y1):
    ws = []
    for y in range(y0, y1):
        for (u, v) in runs_of(dk[y, x0:x1], x0):
            ws.append(v - u + 1)
    ws = np.array(ws)
    return ws.mean() if len(ws) else 0, np.median(ws) if len(ws) else 0, len(ws)

m1 = stem_stats(93, 469, 145, 155)
m2 = stem_stats(469, 700, 145, 155)
print(f"\nline1 runs x<469 (bold?): mean {m1[0]:.1f} med {m1[1]} n={m2 and m1[2]}")
print(f"line1 runs x>=469 (reg?): mean {m2[0]:.1f} med {m2[1]} n={m2[2]}")

# bullet dot 1 exact: rows 198..208, x 172..192
print("\n-- dot 1 pixels (dark<130) --")
d2 = (R < 130) & (G < 130) & (B < 130)
for y in range(197, 209):
    seg = d2[y, 172:195]
    if seg.sum():
        xr = np.nonzero(seg)[0]
        print(f"  row {y}: x {xr.min()+172}..{xr.max()+172} n={int(seg.sum())}")
