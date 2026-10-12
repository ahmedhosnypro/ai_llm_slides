#!/usr/bin/env python3
"""Measure slide_026 frame: chrome landmarks + major color blocks (960x540, 1px=1pt)."""
from PIL import Image
import sys
from collections import deque

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_026.jpg').convert('RGB')
W, H = im.size
px = im.load()

def near(c, target, tol):
    return all(abs(c[i] - target[i]) <= tol for i in range(3))

# ---- 1. chrome landmarks: scan for red border rows/cols ----
RED = (192, 0, 0)
red_cols = []
for x in range(W):
    cnt = sum(1 for y in range(H) if near(px[x, y], RED, 60))
    if cnt > 100:
        red_cols.append(x)
red_rows = []
for y in range(H):
    cnt = sum(1 for x in range(W) if near(px[x, y], RED, 60))
    if cnt > 300:
        red_rows.append(y)
print("red cols (>100 px):", red_cols[:20], "..." if len(red_cols) > 20 else "")
print("red rows (>300 px):", red_rows)

# ---- 2. color census ----
targets = {
    'blue00A9E0': (0, 169, 224),
    'grayBFBFBF': (191, 191, 191),
    'lgreenDFEECD': (223, 238, 205),
    'green92D050': (146, 208, 80),
    'orangeF79646': (247, 150, 70),
    'green00B050': (0, 176, 80),
    'yellowFFFF00': (255, 255, 0),
    'darkred800000': (128, 0, 0),
    'white': (255, 255, 255),
    'black': (0, 0, 0),
}
print("\n--- color counts (tol 30) ---")
for name, t in targets.items():
    cnt = sum(1 for x in range(0, W, 2) for y in range(0, H, 2) if near(px[x, y], t, 30))
    print(f"{name}: {cnt*4}")

# ---- 3. connected components for key fills ----
def components(target, tol, min_size=150):
    mask = [[False] * W for _ in range(H)]
    for y in range(H):
        for x in range(W):
            if near(px[x, y], target, tol):
                mask[y][x] = True
    seen = [[False] * W for _ in range(H)]
    comps = []
    for y0 in range(H):
        for x0 in range(W):
            if mask[y0][x0] and not seen[y0][x0]:
                q = deque([(x0, y0)])
                seen[y0][x0] = True
                minx = maxx = x0; miny = maxy = y0; n = 0
                while q:
                    x, y = q.popleft()
                    n += 1
                    if x < minx: minx = x
                    if x > maxx: maxx = x
                    if y < miny: miny = y
                    if y > maxy: maxy = y
                    for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
                        nx, ny = x+dx, y+dy
                        if 0 <= nx < W and 0 <= ny < H and mask[ny][nx] and not seen[ny][nx]:
                            seen[ny][nx] = True
                            q.append((nx, ny))
                if n >= min_size:
                    fill_frac = n / max(1, (maxx-minx+1) * (maxy-miny+1))
                    comps.append((n, minx, miny, maxx, maxy, fill_frac))
    comps.sort(reverse=True)
    return comps

for name in ['blue00A9E0', 'grayBFBFBF', 'lgreenDFEECD', 'orangeF79646', 'green00B050', 'yellowFFFF00']:
    print(f"\n--- components {name} (n, x0,y0,x1,y1, fillfrac) ---")
    for c in components(targets[name], 40)[:14]:
        print(c)
