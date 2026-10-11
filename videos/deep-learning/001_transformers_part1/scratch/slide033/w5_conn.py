#!/usr/bin/env python3
"""Slide 033 pass W5: connector topology + V-line continuation + fine details."""
from PIL import Image
import numpy as np

IM = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_033.jpg').convert('RGB')
A = np.asarray(IM).astype(int)
R, G, B = A[:, :, 0], A[:, :, 1], A[:, :, 2]
g = (G - R > 14) & (G - B > 4) & (G > 90) & (R < 190)

def gsegs(y, x0, x1):
    row = g[y]
    out = []
    x = x0
    while x < x1:
        if row[x]:
            x2 = x
            while x2 < x1 and (row[x2] or (x2 + 6 < x1 and row[x2:x2 + 7].any())):
                x2 += 1
            out.append((x, x2 - 1))
            x = x2
        else:
            x += 1
    return out

print("== green rows 455..475: segs in x60..920 ==")
for y in range(455, 476):
    s = gsegs(y, 60, 920)
    if s:
        print(f"  y={y}: {s}")

print("\n== green cols x88..112: vertical runs y390..480 ==")
for x in range(88, 113, 2):
    col = g[390:480, x]
    ys = np.where(col)[0]
    if len(ys):
        print(f"  x={x}: y {ys.min()+390}..{ys.max()+390} n={len(ys)}")

print("\n== green cols x795..815: vertical runs y390..480 ==")
for x in range(795, 816, 2):
    col = g[390:480, x]
    ys = np.where(col)[0]
    if len(ys):
        print(f"  x={x}: y {ys.min()+390}..{ys.max()+390} n={len(ys)}")

# V-line continuation: soft red pixels y240..254, x550..700
sred = (R - G > 18) & (R - B > 10) & (R > 150)
print("\n== soft-red pixels y238..256, x550..700 (V line continuation?) ==")
for y in range(238, 257):
    xs = np.where(sred[y, 550:700])[0]
    if len(xs):
        print(f"  y={y}: x {550+xs.min()}..{550+xs.max()} n={len(xs)} (runs: {np.split(xs, np.where(np.diff(xs) > 3)[0]+1).__len__()})")

# same for rows 2-4 right of circles
for (y0, y1, x0) in [(278, 296, 585), (318, 338, 612), (362, 382, 642)]:
    print(f"== soft-red y{y0}..{y1}, x{x0}..700 ==")
    for y in range(y0, y1 + 1):
        xs = np.where(sred[y, x0:700])[0]
        if len(xs):
            print(f"  y={y}: x {x0+xs.min()}..{x0+xs.max()} n={len(xs)}")

# incoming arrowheads: orange at W_k box left edge (x145..162) rows
orange = (R > 130) & (R - B > 60) & (G - B > 20) & (G < 160) & (R - G > 25)
print("\n== orange pixels x144..164 at row bands ==")
for (a, b) in [(238, 256), (278, 296), (318, 338), (362, 382)]:
    sub = orange[a:b + 1, 144:165]
    ys, xs = np.nonzero(sub)
    if len(ys):
        print(f"  band y{a}..{b}: x {144+xs.min()}..{144+xs.max()} y {a+ys.min()}..{a+ys.max()} n={len(ys)}")
    else:
        print(f"  band y{a}..{b}: none")

# W_q -> X2 arrow: red pixels x290..310, y462..476
print("\n== red x288..312, y460..478 ==")
red = (R - G > 40) & (R - B > 28) & (R > 130)
for y in range(460, 479):
    xs = np.where(red[y, 288:313])[0]
    if len(xs):
        print(f"  y={y}: x {288+xs.min()}..{288+xs.max()} n={len(xs)}")

# softmax bar border color + sigma border + DP border precise
print("\n== border core colors ==")
def core(name, x0, y0, x1, y1, thr=200):
    sub = A[y0:y1 + 1, x0:x1 + 1].reshape(-1, 3)
    dk = sub[sub.max(axis=1) < thr]
    if len(dk) == 0:
        print(f"{name}: none"); return
    from collections import Counter
    c = Counter(map(tuple, dk)).most_common(3)
    print(f"{name}: {[(f'#{r:02X}{g:02X}{b:02X}', n) for (r, g, b), n in c]} n={len(dk)}")

core("softmax bar top border", 460, 192, 486, 197)
core("softmax bar left border", 452, 250, 458, 350)
core("sigma box border top", 520, 192, 640, 197)
core("DP box left border", 250, 250, 258, 350)
core("DP box top border", 270, 190, 330, 195)
core("peach panel top border", 300, 104, 800, 110, 210)
core("legend border top", 740, 464, 890, 470)
core("Y2 widget border", 548, 119, 616, 124)
core("sentence container border top", 200, 471, 480, 478)
core("L container border top", 60, 222, 136, 229)
core("W_k box1 top border", 152, 231, 196, 237)
core("pill S border", 268, 158, 340, 166, 215)
core("title line1 left edge x", 210, 56, 230, 78, 150)
