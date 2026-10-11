#!/usr/bin/env python3
"""Measure slide_017.jpg (960x540, 1px=1pt) — color-mask connected components."""
import sys
from PIL import Image
import numpy as np

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_017.jpg').convert('RGB')
A = np.asarray(im).astype(int)
H, W, _ = A.shape

def close(target, tol):
    t = np.array(target)
    d = np.abs(A - t).sum(axis=2)
    return d <= tol

def components(mask, min_px=12):
    """Simple 4-conn flood fill labeling."""
    lab = np.zeros((H, W), dtype=int)
    cur = 0
    comps = []
    from collections import deque
    idx = np.argwhere(mask)
    for (y, x) in idx:
        if lab[y, x]:
            continue
        cur += 1
        q = deque([(y, x)])
        lab[y, x] = cur
        ys, xs = [y], [x]
        n = 0
        while q:
            cy, cx = q.popleft()
            n += 1
            for dy, dx in ((1,0),(-1,0),(0,1),(0,-1)):
                ny, nx = cy+dy, cx+dx
                if 0 <= ny < H and 0 <= nx < W and mask[ny, nx] and not lab[ny, nx]:
                    lab[ny, nx] = cur
                    q.append((ny, nx))
        if n >= min_px:
            ys = np.array(ys); xs = np.array(xs)
            comps.append((n, xs.min(), ys.min(), xs.max(), ys.max()))
    return comps

def report(name, target, tol, min_px=12, region=None):
    m = close(target, tol)
    if region:
        x0, y0, x1, y1 = region
        mm = np.zeros_like(m)
        mm[y0:y1, x0:x1] = m[y0:y1, x0:x1]
        m = mm
    comps = components(m, min_px)
    comps.sort(key=lambda c: (c[2], c[1]))
    print(f"== {name} (target {target} tol {tol}): {len(comps)} comps")
    for n, x0, y0, x1, y1 in comps:
        print(f"   n={n:6d} bbox x{x0}..{x1} y{y0}..{y1}  w={x1-x0+1} h={y1-y0+1}")

# Left-column callouts
report("callout_yellow", (255, 255, 0), 150, 50, region=(0, 60, 600, 540))
report("callout_pink", (249, 168, 240), 120, 50, region=(0, 60, 600, 540))
report("callout_tan", (199, 161, 122), 90, 50, region=(0, 60, 600, 540))
