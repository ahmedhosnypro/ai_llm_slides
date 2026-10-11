#!/usr/bin/env python3
"""Pass 5b: blue callout precise; blue curve trace; bottom-right region map."""
from PIL import Image
import numpy as np
from scipy import ndimage

B = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_009.jpg"
bi = np.asarray(Image.open(B).convert("RGB"), dtype=np.int16)
R, G, Bl = bi[:,:,0], bi[:,:,1], bi[:,:,2]

print("== BLUE CALLOUT precise ==")
fill = (np.abs(R-204) < 20) & (np.abs(G-228) < 20) & (np.abs(Bl-247) < 20)
lab, n = ndimage.label(fill, structure=np.ones((3,3)))
if n:
    sizes = ndimage.sum(fill, lab, range(1, n+1))
    big = int(np.argmax(sizes)) + 1
    ys, xs = np.where(lab == big)
    print(f"  fill largest comp: x{xs.min()}..{xs.max()+1} y{ys.min()}..{ys.max()+1} (w{xs.max()-xs.min()+1} h{ys.max()-ys.min()+1})")
darkblue = (Bl > 110) & (Bl - R > 80) & (Bl - G > 70)
win = darkblue[120:205, 100:450]
rows = win.sum(axis=1)
print("  darkblue row bands y120..205 (count>4):")
s = None
for i, v in enumerate(rows):
    if v >= 4 and s is None: s = i
    elif v < 4 and s is not None:
        print(f"    y{s+120}..{i+120} (peak {int(rows[s:i].max())})"); s = None
cols = win.sum(axis=0)
print("  darkblue col bands x100..450 (count>4):")
s = None
for i, v in enumerate(cols):
    if v >= 4 and s is None: s = i
    elif v < 4 and s is not None:
        print(f"    x{s+100}..{i+100} (peak {int(cols[s:i].max())})"); s = None

print("== LEADER-REGION red px positions (slide9, y330..402 x470..558) ==")
redink = (R > 120) & (G < 90) & (Bl < 90)
ys, xs = np.where(redink[330:402, 470:558])
if len(ys):
    print(f"  n={len(ys)} bbox x{xs.min()+470}..{xs.max()+471} y{ys.min()+330}..{ys.max()+331}")
    for yy in range(330, 402, 8):
        row = np.where(redink[yy, 470:558])[0]
        if len(row):
            print(f"    y{yy}: x {row.min()+470}..{row.max()+470} (n={len(row)})")

print("== BLUE CURVE trace ==")
curve = (Bl - R > 60) & (Bl - G > 40) & (Bl > 90)
ys, xs = np.where(curve[150:345, 415:515])
print(f"  blue curve px in window: {len(ys)}")
for yy in range(150, 345, 10):
    row = np.where(curve[yy, 415:515])[0]
    if len(row):
        print(f"    y{yy}: x {row.min()+415}..{row.max()+415} (n={len(row)})")

print("== BOTTOM-RIGHT REGION MAP (x480..935, y280..515) ==")
# row color modes to understand the panel
for y0 in range(280, 515, 15):
    reg = bi[y0:y0+15, 480:935].reshape(-1, 3)
    vals, counts = np.unique(reg, axis=0, return_counts=True)
    top = [(tuple(int(v) for v in t), int(c)) for t, c in sorted(zip(vals, counts), key=lambda z: -z[1])[:3]]
    print(f"  y{y0:3d}..{y0+14}: {top}")
