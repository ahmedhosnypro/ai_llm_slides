#!/usr/bin/env python3
"""Third pass: fine structure of word row, left column, red arrows, chip cells."""
import numpy as np
from PIL import Image
from collections import Counter

F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_049.jpg"
im = Image.open(F).convert("RGB")
a = np.asarray(im).astype(int)
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]

def cls(p):
    R, G, B = p
    if R > 240 and G > 240 and B > 240: return "."
    if R - G > 22 and R - B > 22 and R > 140: return "R"       # red/pink ink
    if B - R > 22 and B - G > 18: return "B"                   # blue
    if G - R > 22 and G - B > 22: return "G"                   # green
    if R > 190 and G > 160 and B < 200 and R - B > 28: return "T"  # tan/yellow
    if abs(R-G) < 20 and abs(G-B) < 20 and R < 215: return "k"  # dark/gray
    return "?"

# ---- word row: per-row class histogram, x 150..900, y 466..518
print("== word row band per-row classes x150..900 ==")
for y in range(466, 519):
    row = a[y, 150:900]
    cnt = Counter(cls(tuple(p)) for p in row)
    s = "".join(f"{k}:{v} " for k, v in sorted(cnt.items()))
    print(f"  y={y} {s}")

# ---- word box vertical border positions at y=495 (mid box): class runs
print("== y=495 class runs x150..900 ==")
y = 495
runs = []
cur = None; start = 150
for x in range(150, 900):
    c = cls(tuple(a[y, x]))
    if c != cur:
        if cur is not None: runs.append((cur, start, x-1))
        cur = c; start = x
runs.append((cur, start, 899))
print("  ", [(c, s, e) for c, s, e in runs if c != "." or (e-s) > 4])

# ---- chip0 X top strip (y 375..381) per column
print("== X chip0 top strip y375..381 per-column mode ==")
for x in range(168, 248):
    col = a[375:382, x]
    cc = Counter(map(tuple, col)).most_common(1)[0][0]
    print(f"  x={x} {cc} {cls(cc)}")

# ---- Y chip0 top strip (y 82..88)
print("== Y chip0 top strip y82..88 per-column mode ==")
for x in range(168, 248):
    col = a[82:89, x]
    cc = Counter(map(tuple, col)).most_common(1)[0][0]
    print(f"  x={x} {cc} {cls(cc)}")

# ---- red arrows gap 2->1: looser red map, x 160..880 y 264..286 (downsampled x2)
print("== gap 2-1 red map (R=loose red) ==")
loose_red = (r - g > 18) & (r - b > 18) & (r > 140)
for y in range(264, 287):
    row = loose_red[y, 160:880]
    xs = np.where(row)[0]
    if len(xs):
        # cluster starts
        cl = []
        prev = -10; 
        for xx in xs:
            if xx - prev > 3: cl.append([xx+160, xx+160])
            else: cl[-1][1] = xx+160
            prev = xx
        print(f"  y={y} n={len(xs)} clusters={cl[:14]}")
    else:
        print(f"  y={y} -")
print("== gap 1-0 red map ==")
for y in range(309, 333):
    row = loose_red[y, 160:880]
    xs = np.where(row)[0]
    if len(xs):
        cl = []
        prev = -10
        for xx in xs:
            if xx - prev > 3: cl.append([xx+160, xx+160])
            else: cl[-1][1] = xx+160
            prev = xx
        print(f"  y={y} n={len(xs)} clusters={cl[:14]}")
    else:
        print(f"  y={y} -")
print("red arrow color sample:", Counter(map(tuple, a[270:280, 352:358].reshape(-1,3))).most_common(3))
print("red arrow color sample2:", Counter(map(tuple, a[270:280, 424:430].reshape(-1,3))).most_common(3))

# ---- left column boxes: horizontal red RUNS (contiguous >=30px)
print("== left column contiguous red runs (len>=25) ==")
red = (r - g > 30) & (r - b > 30) & (r > 130)
for y in range(60, 520):
    row = red[y, 55:165]
    xs = np.where(row)[0]
    if len(xs) == 0: continue
    runs = []
    prev = -10; start = None
    for xx in xs:
        if xx - prev > 2:
            if start is not None: runs.append((start+55, prev+55))
            start = xx
        prev = xx
    runs.append((start+55, prev+55))
    long_runs = [rr for rr in runs if rr[1]-rr[0] >= 25]
    if long_runs:
        print(f"  y={y} runs={long_runs}")

# ---- vertical red cols in left column (contiguous >=15)
print("== left column vertical red runs (len>=15) ==")
for x in range(55, 165):
    col = red[60:520, x]
    ys = np.where(col)[0]
    if len(ys) == 0: continue
    runs = []
    prev = -10; start = None
    for yy in ys:
        if yy - prev > 2:
            if start is not None: runs.append((start+60, prev+60))
            start = yy
        prev = yy
    runs.append((start+60, prev+60))
    long_runs = [rr for rr in runs if rr[1]-rr[0] >= 15]
    if long_runs:
        print(f"  x={x} runs={long_runs}")

# ---- ellipsis dots: Y row (blue) and X row (green) exact positions
print("== Y row blue dots x560..760 y84..106 ==")
blue = (b - r > 30) & (b - g > 25) & (b > 100)
sub = blue[84:106, 560:760]
lab_n = sub.sum()
ys, xs = np.where(sub)
if len(xs):
    print("   x clusters:", sorted(set((xs//4*4+560).tolist())))

# ---- container border: exact bbox via dark blue line detection
print("== container border rows/cols ==")
dblue = (b - r > 60) & (b - g > 55) & (r < 90)
for y in range(120, 375):
    row = dblue[y, 150:900]
    if row.mean() > 0.5: print(f"  hline y={y}")
for x in range(150, 900):
    col = dblue[125:365, x]
    if col.mean() > 0.5: print(f"  vline x={x}")

# ---- word box borders via loose red in word band
print("== word band loose-red hruns x160..890 ==")
for y in range(468, 519):
    row = loose_red[y, 160:890]
    xs = np.where(row)[0]
    if len(xs) > 300:
        print(f"  y={y} n={len(xs)} (near-full row)")
print("== word band loose-red vcols ==")
for x in range(160, 890):
    col = loose_red[468:519, x]
    if col.mean() > 0.5:
        print(f"  vline x={x}")
