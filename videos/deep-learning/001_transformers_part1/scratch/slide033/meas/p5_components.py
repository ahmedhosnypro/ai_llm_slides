#!/usr/bin/env python3
"""Slide 033 pass 5: thin-ink component extraction (red lines, green dashes, labels)."""
from PIL import Image
import numpy as np
from collections import deque

IM = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_033.jpg").convert("RGB")
A = np.asarray(IM).astype(int)
H, W = A.shape[:2]
R, G, B = A[:,:,0], A[:,:,1], A[:,:,2]

def components(m, min_area=6, max_n=400):
    seen = np.zeros((H, W), bool)
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
                    if 0 <= ny < H and 0 <= nx < W and not seen[ny, nx] and m[ny, nx]:
                        seen[ny, nx] = True; q.append((ny, nx)); ys.append(ny); xs.append(nx)
                if n > max_n: break
            if n > max_n: break
        if min_area <= n <= max_n:
            out.append((n, min(xs), max(xs), min(ys), max(ys)))
    out.sort(key=lambda b: (b[3], b[1]))
    return out

red = (R > 140) & (G < 100) & (B < 100)
dred = (R > 90) & (R < 200) & (G < 70) & (B < 70)
green = (G > 110) & (G - R > 40) & (G - B > 25) & (R < 130)

print("=== RED components (lines/arrowheads/circle) ===")
for n, x0, x1, y0, y1 in components(red, 6, 500):
    kind = "dot" if n < 40 and (x1-x0) < 8 and (y1-y0) < 8 else ("line" if max(x1-x0, y1-y0) > 12 else "blob")
    print(f"  n={n:4d} x {x0:3d}..{x1:3d} y {y0:3d}..{y1:3d} (w={x1-x0+1:3d} h={y1-y0+1:3d}) {kind}")
print("=== DARKRED components (labels K,V,q, pill text, box labels) ===")
for n, x0, x1, y0, y1 in components(dred, 6, 500):
    print(f"  n={n:4d} x {x0:3d}..{x1:3d} y {y0:3d}..{y1:3d} (w={x1-x0+1:3d} h={y1-y0+1:3d})")
print("=== GREEN components (dashed borders, arrows, labels) ===")
for n, x0, x1, y0, y1 in components(green, 4, 500):
    print(f"  n={n:4d} x {x0:3d}..{x1:3d} y {y0:3d}..{y1:3d} (w={x1-x0+1:3d} h={y1-y0+1:3d})")
