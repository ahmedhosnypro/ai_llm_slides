#!/usr/bin/env python3
"""Slide 033 pass 6: region-by-region ink/color scans."""
from PIL import Image
import numpy as np
from collections import Counter, deque

IM = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_033.jpg").convert("RGB")
A = np.asarray(IM).astype(int)
H, W = A.shape[:2]

def comps(m, x0, y0, min_area=5, max_n=2000):
    """components of mask m (already windowed), coords offset by (x0,y0)"""
    h, w = m.shape
    seen = np.zeros((h, w), bool)
    out = []
    idx = np.argwhere(m)
    for (y, x) in idx:
        if seen[y, x]: continue
        q = deque([(y, x)]); seen[y, x] = True
        ys, xs, n = [y], [x], 0
        while q:
            cy, cx = q.popleft(); n += 1
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    ny, nx = cy+dy, cx+dx
                    if 0 <= ny < h and 0 <= nx < w and not seen[ny, nx] and m[ny, nx]:
                        seen[ny, nx] = True; q.append((ny, nx)); ys.append(ny); xs.append(nx)
                if n > max_n: break
            if n > max_n: break
        if n >= min_area:
            out.append((n, x0+min(xs), x0+max(xs), y0+min(ys), y0+max(ys)))
    out.sort(key=lambda b: (b[3], b[1]))
    return out

def show(title, rows):
    print(f"--- {title} ---")
    for n, x0, x1, y0, y1 in rows:
        print(f"  n={n:4d} x {x0:3d}..{x1:3d} y {y0:3d}..{y1:3d} (w={x1-x0+1:3d} h={y1-y0+1:3d})")

def mode(region, k=3):
    x0, y0, x1, y1 = region
    sub = A[y0:y1+1, x0:x1+1].reshape(-1, 3)
    return [(f"#{r:02X}{g:02X}{b:02X}", n) for (r, g, b), n in Counter(map(tuple, sub)).most_common(k)]

def ink(x0, y0, x1, y1, thr=170):
    """any dark/saturated ink mask in window"""
    sub = A[y0:y1+1, x0:x1+1]
    mx = sub.max(axis=2); mn = sub.min(axis=2)
    return (mx < thr) | ((mx - mn) > 60)

R, G, B = A[:,:,0], A[:,:,1], A[:,:,2]

# 1) TITLE band: ink clusters per line + color per cluster
m = ink(0, 40, 959, 104)
rows = comps(m, 0, 40, 8)
print("=== TITLE ink clusters (y40..104) ===")
for n, x0, x1, yy0, yy1 in rows:
    cx0, cy0, cx1, cy1 = x0, yy0-40, x1, yy1-40
    sub = A[cy0:cy1+1, cx0:cx1+1].reshape(-1, 3)
    dark = sub[sub.max(axis=1) < 200]
    c = Counter(map(tuple, dark)).most_common(2)
    cc = ", ".join(f"#{r:02X}{g:02X}{b:02X}" for (r, g, b), _ in c)
    print(f"  n={n:4d} x {x0:3d}..{x1:3d} y {yy0:3d}..{yy1:3d} ink[{cc}]")

# 2) Y2/output region x500..700 y100..200
show("OUTPUT REGION ink (x500..700, y100..200)", comps(ink(500, 100, 700, 200), 500, 100, 5))
print("  output region fills:", mode((620, 120, 660, 140)), mode((540, 125, 560, 145)))

# 3) PILLS: pale-yellow bounds
pill = (R > 240) & (G > 240) & (B > 195) & (B < 245)
show("PILL pale-yellow comps (min 150)", comps(pill, 0, 0, 150))

# 4) pill text colors + bounds (dark ink inside pill band y148..196)
for name, (px0, px1) in {"Similarity": (260, 360), "Probabilities": (420, 530), "WeightedSUM": (590, 710)}.items():
    m2 = ink(px0, 148, px1, 196, 180)
    r2 = comps(m2, px0, 148, 4)
    if r2:
        X0 = min(r[1] for r in r2); X1 = max(r[2] for r in r2)
        Y0 = min(r[3] for r in r2); Y1 = max(r[4] for r in r2)
        sub = A[Y0:Y1+1, X0:X1+1].reshape(-1, 3)
        dk = sub[sub.max(axis=1) < 190]
        print(f"pill {name}: ink x {X0}..{X1} y {Y0}..{Y1} text#{Counter(map(tuple,dk)).most_common(1)[0][0][0]:02X}{Counter(map(tuple,dk)).most_common(1)[0][0][1]:02X}{Counter(map(tuple,dk)).most_common(1)[0][0][2]:02X} nclusters={len(r2)}")

# 5) Weighted-sum column: circles (white+red ring) region x505..665 y205..400
white = (R > 235) & (G > 235) & (B > 235)
show("WHITE comps in x500..680 y205..400", comps(white[205:401, 500:681], 500, 205, 30))
red = (R > 140) & (G < 100) & (B < 100)
show("RED comps in x495..680 y205..400", comps(red[205:401, 495:681], 495, 205, 4))

# 6) Dot Product box: fill bbox + border color + label inks
dp = (np.abs(A - np.array([220, 203, 187])) <= 18).all(axis=2)
show("DOTPRODUCT fill comps", comps(dp[180:420, 240:390], 240, 180, 400))
print("  dp border sample top:", mode((280, 193, 310, 196)), " left:", mode((252, 300, 256, 320)), " right:", mode((344, 300, 349, 320)))
show("DP label ink x258..372 y198..240", comps(ink(258, 198, 372, 240), 258, 198, 4))

# 7) Softmax bar: fill bbox + border
sm = (np.abs(A - np.array([248, 221, 252])) <= 16).all(axis=2)
show("SOFTMAX fill comps", comps(sm[180:420, 440:500], 440, 180, 300))
show("SOFTMAX text ink x450..500 y200..400", comps(ink(450, 200, 500, 400, 165), 450, 200, 3))

# 8) Sigma box: fill bbox
sg = (np.abs(A - np.array([234, 254, 252])) <= 12).all(axis=2)
show("SIGMA fill comps", comps(sg[180:240, 490:700], 490, 180, 200))
show("SIGMA glyph ink x500..700 y185..225", comps(ink(500, 185, 700, 225, 165), 500, 185, 4))
print("  sigma border sample:", mode((520, 194, 560, 197)), mode((520, 216, 560, 220)))

# 9) mini-vector squares: left container rows (precise square colors x60..140)
for i, yy in enumerate([246, 287, 328, 372]):
    print(f"L-row{i+1} y~{yy}: sq1 {mode((66, yy-6, 78, yy+6),2)} sq2 {mode((80, yy-6, 92, yy+6),2)} sq3 {mode((94, yy-6, 106, yy+6),2)} sq4 {mode((108, yy-6, 120, yy+6),2)}")
# white boxes inside left container
show("L-container white boxes x59..139 y227..396", comps(white[227:397, 59:140], 59, 227, 200))
