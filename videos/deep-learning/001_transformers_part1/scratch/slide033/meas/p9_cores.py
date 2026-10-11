#!/usr/bin/env python3
"""Slide 033 pass 9: cores, circles vertical, X2 box map, W-box vertical, connectors."""
from PIL import Image
import numpy as np
from collections import Counter

IM = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_033.jpg").convert("RGB")
A = np.asarray(IM).astype(int)
R, G, B = A[:,:,0], A[:,:,1], A[:,:,2]

def core(name, x0, y0, x1, y1, thr=110):
    sub = A[y0:y1+1, x0:x1+1].reshape(-1, 3)
    dk = sub[sub.max(axis=1) < thr]
    if len(dk) == 0:
        print(f"{name}: none <{thr}"); return
    c = Counter(map(tuple, dk)).most_common(3)
    print(f"{name}: {[(f'#{r:02X}{g:02X}{b:02X}', n) for (r, g, b), n in c]} n={len(dk)}")

def cmap(name, x0, x1, y0, y1, step=1):
    print(f"--- {name} (x{x0}..{x1}, y{y0}..{y1}) step{step} ---")
    for yy in range(y0, y1+1, step):
        row = ""
        for xx in range(x0, x1+1, step):
            r, g, b = A[yy, xx]
            mx, mn = max(r, g, b), min(r, g, b)
            if mx < 110: ch = "K"                      # dark ink
            elif r - g > 45 and r - b > 30: ch = "R"   # red
            elif g - r > 25 and g - b > 10: ch = "G"   # green
            elif b - r > 40: ch = "B"                  # blue
            elif r > 195 and b > 150 and g < 175 and r - g > 40: ch = "P"  # pink
            elif r > 215 and g > 215 and b < 170: ch = "Y"  # yellow
            elif mx - mn > 30: ch = "?"                # other saturated
            else: ch = "."                             # pale/peach
            row += ch
        print(f"{yy:3d} {row}")

# circles: vertical red profile at ring centers
sred = (R - G > 40) & (R - B > 28) & (R > 150)
for cx, cy in [(532, 246), (563, 288), (592, 328), (622, 372)]:
    col = sred[cy-25:cy+26, cx-1:cx+2].any(axis=1)
    ys = [cy-25+i for i, v in enumerate(col) if v]
    row = sred[cy-1:cy+2, cx-25:cx+26].any(axis=0)
    xs = [cx-25+i for i, v in enumerate(row) if v]
    print(f"circle@({cx},{cy}): vert y {ys[0] if ys else '-'}..{ys[-1] if ys else '-'}  horiz x {xs[0] if xs else '-'}..{xs[-1] if xs else '-'}")

# W_k box 1 vertical extent at x175 (yellow)
colY = ((R > 215) & (G > 215) & (B < 175))[:, 173:178].any(axis=1)
ys = [i for i in range(225, 270) if colY[i]]
print("W_k box1 yellow rows at x173..177:", ys[:3], "...", ys[-3:] if len(ys) > 3 else "")
colY2 = ((R > 215) & (G > 215) & (B < 175))[:, 720:725].any(axis=1)
ys2 = [i for i in range(225, 270) if colY2[i]]
print("W_v box1 yellow rows at x720..724:", ys2[:3], "...", ys2[-3:] if len(ys2) > 3 else "")

# horizontal sensitive-red at arrow rows: segments
for yy in [246, 287, 328, 372, 491, 466]:
    m = sred[yy, :]
    segs = []
    x = 40
    while x < 930:
        if m[x]:
            x2 = x
            while x2 < 930 and (m[x2] or (x2+3 < 930 and m[x2:x2+4].any())):
                x2 += 1
            segs.append((x, x2-1)); x = x2
        else:
            x += 1
    print(f"red segs y={yy}: {segs}")

# connectors: green-ish mask (loose)
gconn = (G - R > 22) & (G - B > 12) & (G > 95) & (R < 160)
print("connector green segs:")
for yy in [400, 420, 440, 460, 470, 480, 488, 491, 494, 500]:
    m = gconn[yy, :]
    segs = []
    x = 40
    while x < 930:
        if m[x]:
            x2 = x
            while x2 < 930 and m[x2:x2+8].any():
                x2 += 1
            if x2 - x >= 1: segs.append((x, x2-1))
            x = x2
        else:
            x += 1
    print(f"  y={yy}: {segs}")
for xx in [99, 803]:
    col = gconn[380:500, xx-1:xx+2].any(axis=1)
    ys = [380+i for i, v in enumerate(col) if v]
    print(f"  vertical x={xx}: y {ys[0] if ys else '-'}..{ys[-1] if ys else '-'}")

# X2 pink box map
cmap("X2 box", 258, 340, 468, 510, 2)
# output Y widget map
cmap("output widget", 544, 624, 114, 158, 2)
# q2 label + vector map
cmap("q2", 276, 345, 404, 428, 1)

# core colors
core("title blue '('", 488, 58, 495, 77, 140)
core("title blue mid", 616, 60, 662, 73, 120)
core("title black 'M' x395", 395, 58, 406, 73, 120)
core("DP 'Dot'", 270, 198, 322, 228, 120)
core("DP 'K2q'", 344, 196, 370, 214, 120)
core("Soft max", 466, 262, 482, 336, 130)
core("Sigma glyph", 576, 197, 590, 215, 120)
core("W box text r1", 158, 233, 195, 260, 130)
core("caption 'd: Embedding'", 765, 512, 880, 530, 120)
core("pill S text", 260, 166, 340, 186, 170)
core("pill P text", 438, 166, 506, 186, 170)
core("pill W text", 600, 164, 684, 182, 170)
core("K label r1", 234, 226, 252, 244, 120)
core("V label r2", 636, 270, 660, 292, 120)
core("X container r1", 90, 238, 108, 255, 140)
core("Y glyph", 574, 122, 592, 144, 140)
core("Y '2' subscript", 577, 143, 590, 156, 150)
core("legend red '1^d' L", 774, 476, 798, 500, 150)
core("legend W black", 804, 480, 822, 496, 120)
core("legend right red", 838, 478, 866, 502, 150)
core("legend d*d", 798, 500, 828, 514, 150)
core("legend eq '='", 826, 478, 844, 502, 150)
core("X2 X glyph", 288, 484, 312, 503, 130)
core("q glyph", 278, 410, 300, 428, 130)
core("dot1", 326, 242, 335, 251, 130)
core("blockarrow", 266, 511, 287, 528, 150)
core("Wq box text", 280, 435, 315, 458, 140)
core("legend mini-v cells", 736, 478, 776, 496, 200)
core("sent cell1 yellow", 192, 488, 202, 500, 220)
core("container cell1", 66, 240, 79, 252, 220)
