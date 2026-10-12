#!/usr/bin/env python3
"""measure8_cores.py — core color censuses for strokes/text + remaining vector strips."""
import numpy as np
from PIL import Image
from collections import Counter

FR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_034.jpg"
img = np.asarray(Image.open(FR).convert("RGB")).astype(int)
r, g, b = img[..., 0], img[..., 1], img[..., 2]
S = r + g + b

def core(y0, y1, x0, x1, name, thr=430, topn=6):
    win = img[y0:y1, x0:x1].reshape(-1, 3)
    m = win.sum(axis=1) < thr
    if m.sum() == 0:
        print(f"{name}: none < {thr}"); return
    q = (win[m] // 20) * 20
    c = Counter(map(tuple, q))
    tot = m.sum()
    print(f"{name}: n={tot}", [(f"({rr},{gg},{bb})", n) for (rr, gg, bb), n in c.most_common(topn)])

print("== DASH/STROKE CORES ==")
core(135, 139, 180, 880, "token container top dash")
core(173, 177, 180, 880, "token container bottom dash")
core(289, 292, 180, 880, "vector container top dash")
core(327, 330, 180, 880, "vector container bottom dash")
core(143, 147, 180, 880, "token box top borders")
core(163, 167, 180, 880, "token box bottom borders")
core(299, 303, 180, 880, "vector box top borders")
core(318, 322, 180, 880, "vector box bottom borders")

print("\n== TEXT CORES ==")
core(146, 164, 195, 230, "token box1 text '0'")
core(146, 164, 770, 800, "token box7 text 'N-2'")
core(303, 319, 195, 285, "vector box1 text 'Vector_P0'")
core(303, 319, 810, 870, "vector box8 text 'Vector_PN-1'")
core(58, 100, 270, 480, "title red '[2] Position'")
core(58, 100, 480, 700, "title blue 'Embedding'")
core(100, 120, 330, 660, "subtitle red")
core(140, 170, 60, 170, "left label1 blue")
core(180, 200, 60, 260, "left label2 blue")
core(218, 250, 60, 170, "left label3 red 'Positional Embedding'")
core(255, 275, 60, 260, "left label4 blue")
core(224, 248, 170, 890, "purple bar text")
core(408, 460, 230, 820, "summary red lines")
core(380, 500, 230, 820, "summary black lines")
core(358, 368, 220, 830, "summary box top border")

print("\n== VECTOR STRIPS x=560..880 (y288..352) ==")
for x in [560, 660, 700, 800, 860, 880]:
    print(f"-- x={x}: ", end="")
    for y in [290, 294, 298, 300, 306, 310, 314, 320, 324, 328, 332, 340, 343]:
        p = img[y, x]
        print(f"y{y}:({p[0]},{p[1]},{p[2]})", end=" ")
    print()

print("\n== TOKEN ROW x=560..880 ==")
for x in [560, 640, 660, 700, 760, 800, 840, 870]:
    print(f"-- x={x}: ", end="")
    for y in [136, 140, 144, 150, 155, 160, 165, 170, 174]:
        p = img[y, x]
        print(f"y{y}:({p[0]},{p[1]},{p[2]})", end=" ")
    print()

print("\n== BOX EDGE COLUMNS: token row, count over y144..165, cols>=16 ==")
dark = S < 470
prof = dark[144:166, 160:900].sum(axis=0)
cols = np.where(prof >= 16)[0] + 160
groups = []
for c in cols:
    if groups and c - groups[-1][-1] <= 2: groups[-1].append(c)
    else: groups.append([c])
print("token borders:", [(gp[0], gp[-1]) for gp in groups])

print("\n== BOX EDGE COLUMNS: vector row, darkish count over y300..321 ==")
darkv = S < 560
prof = darkv[300:322, 160:900].sum(axis=0)
cols = np.where(prof >= 14)[0] + 160
groups = []
for c in cols:
    if groups and c - groups[-1][-1] <= 2: groups[-1].append(c)
    else: groups.append([c])
print("vector borders:", [(gp[0], gp[-1]) for gp in groups])
