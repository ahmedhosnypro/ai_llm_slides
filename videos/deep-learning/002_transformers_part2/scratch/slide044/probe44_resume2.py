#!/usr/bin/env python3
import numpy as np
from PIL import Image
from collections import Counter

F = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_044.jpg").convert("RGB")
a = np.asarray(F).astype(int)

def census(x0, x1, y0, y1, name, k=5):
    reg = a[y0:y1, x0:x1].reshape(-1, 3)
    q = Counter(map(tuple, reg))
    print(f"{name} ({x0},{y0})-({x1},{y1}):", " | ".join(f"{c}:{n}" for c, n in q.most_common(k)))

# LEFT front face actual colors (build claims x66..197 y232..421 solid F07060)
census(80, 180, 260, 300, "LEFT front upper")
census(80, 180, 360, 400, "LEFT front lower")
census(70, 100, 230, 250, "LEFT front top-left corner")
census(150, 195, 400, 418, "LEFT front bottom-right")
# LEFT cube top bands (build: bluegray y187..199, yellow-dark 200..218, orange-dark 221..236)
census(140, 240, 190, 198, "LEFT band1 bluegray")
census(140, 240, 203, 216, "LEFT band2 yellow-dark")
census(140, 240, 224, 234, "LEFT band3 orange-dark")
# LEFT side strips (build: green 201..216, orange 219..236, yellow 238..254, bluegray 256..270, y238..410)
census(202, 215, 300, 380, "LEFT strip green?")
census(220, 235, 300, 380, "LEFT strip orange?")
census(240, 253, 300, 380, "LEFT strip yellow?")
census(257, 269, 300, 380, "LEFT strip bluegray?")
# GN right part (build: salmon 337..410)
census(345, 405, 240, 280, "GN right part")
census(345, 405, 290, 325, "GN right part lower")
# GN front magenta
census(285, 330, 240, 280, "GN magenta front")
# IN salmon column (build 549..575) + right face 578..588
census(550, 574, 240, 280, "IN salmon col")
census(578, 587, 240, 280, "IN right face")
# header lines: row profiles of blue ink, x50..280
blu = (a[:,:,2] > 120) & (a[:,:,2] - a[:,:,0] > 40) & (a[:,:,2] - a[:,:,1] > 30)
print("--- header blue row profile x50..280, y85..170 ---")
for yy in range(85, 172, 3):
    n = int(blu[yy, 50:280].sum())
    print(f"  y{yy}: {n}", end=("" if yy % 15 else "\n"))
print()
ysH, xsH = np.where(blu[85:170, 50:280]); ysH += 85; xsH += 50
rows = {}
for x, y in zip(xsH, ysH): rows.setdefault(y, []).append(x)
for y in sorted(rows):
    xs = rows[y]
    print(f"  hdr y{y}: x {min(xs)}..{max(xs)} n={len(xs)}")
# title tail: what's the ink at x750..850 y55..82?
census(755, 850, 55, 82, "title tail region", 6)
redish = (a[:,:,0] > 120) & ((a[:,:,0] - a[:,:,1]) > 35) & ((a[:,:,0] - a[:,:,2]) > 25)
ysT, xsT = np.where(redish[40:90, 100:900]); ysT += 40; xsT += 100
print("loose-red title bbox: x", xsT.min(), xsT.max(), " y", ysT.min(), ysT.max())
# RT channels arrow: red rows y330..345 x660..800
print("--- RT channels arrow rows (red, x660..800) ---")
for yy in range(328, 348):
    row = np.where(redish[yy, 660:800])[0] + 660
    if len(row): print(f"  y{yy}: x {row.min()}..{row.max()} n={len(row)}")
# FV arrow shaft: red rows x650..670
print("--- FV shaft cols (red, y140..360, x648..672) ---")
redish2 = (a[:,:,0] > 130) & ((a[:,:,0] - a[:,:,1]) > 40) & ((a[:,:,0] - a[:,:,2]) > 30)
col = np.where(redish2[100:370, 648:672])
ysF = col[0] + 100; xsF = col[1] + 648
if len(xsF):
    import collections
    cc = collections.Counter(xsF)
    print("  red col histogram:", dict(sorted(cc.items())))
    print("  red y extent:", ysF.min(), ysF.max())
