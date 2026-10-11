#!/usr/bin/env python3
"""Measure slide_006 original frame geometry via color masks (960x540, 1px=1pt, in=px/72)."""
import json
from PIL import Image
import numpy as np

IMG = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_006.jpg"
im = Image.open(IMG).convert("RGB")
W, H = im.size
a = np.asarray(im).astype(int)
print(f"size: {W}x{H}")

def mask(hexcolor, tol):
    r, g, b = int(hexcolor[0:2], 16), int(hexcolor[2:4], 16), int(hexcolor[4:6], 16)
    d = np.abs(a[:, :, 0] - r) + np.abs(a[:, :, 1] - g) + np.abs(a[:, :, 2] - b)
    return d <= tol

def components(m, min_px=30):
    """Simple connected components via flood fill (4-neighborhood), returns bboxes (x0,y0,x1,y1,area)."""
    from collections import deque
    visited = np.zeros_like(m, dtype=bool)
    out = []
    ys, xs = np.where(m)
    coords = set(zip(ys.tolist(), xs.tolist()))
    seen = set()
    for start in coords:
        if start in seen:
            continue
        q = deque([start]); seen.add(start)
        x0 = x1 = start[1]; y0 = y1 = start[0]; n = 0
        while q:
            y, x = q.popleft(); n += 1
            x0 = min(x0, x); x1 = max(x1, x); y0 = min(y0, y); y1 = max(y1, y)
            for dy, dx in ((1,0),(-1,0),(0,1),(0,-1)):
                p = (y+dy, x+dx)
                if p in coords and p not in seen:
                    seen.add(p); q.append(p)
        if n >= min_px:
            out.append({"bbox": [x0, y0, x1, y1], "area": n})
    out.sort(key=lambda c: -c["area"])
    return out

def report(name, hexc, tol=60, min_px=30, top=12):
    m = mask(hexc, tol)
    n = int(m.sum())
    print(f"\n== {name} #{hexc} tol={tol}: {n} px ==")
    if n == 0:
        return []
    comps = components(m, min_px)
    for c in comps[:top]:
        x0, y0, x1, y1 = c["bbox"]
        print(f"  bbox px=({x0},{y0})-({x1},{y1})  w={x1-x0+1} h={y1-y0+1} area={c['area']}  "
              f"in=({x0/72:.2f},{y0/72:.2f})-({(x1+1)/72:.2f},{(y1+1)/72:.2f}) w={(x1-x0+1)/72:.2f} h={(y1-y0+1)/72:.2f}")
    return comps

# Containers
report("decoder-yellow", "F2F25C", tol=90, min_px=500)
report("encoder-peach", "FAC090", tol=70, min_px=500)
# Decoder bars
report("green-bars", "9CE05C", tol=80, min_px=100)
report("orange-bars", "F7C683", tol=70, min_px=100)
# Encoder bars
report("pink-bars", "F2A396", tol=70, min_px=100)
report("tan-bars", "E6C49C", tol=70, min_px=100)
# Callout + reds
report("callout-pink", "FFC0CB", tol=70, min_px=200)
report("red-C00000", "C00000", tol=90, min_px=8, top=20)
report("red-FF0000", "FF0000", tol=90, min_px=8, top=20)
# Title red
report("title-E0301E", "E0301E", tol=80, min_px=20, top=15)

# sample some rows/cols for structure understanding
print("\n-- row samples (unique colors along rows) --")
for y in (60, 80, 120, 160, 200, 250, 300, 350, 400, 450, 500):
    row = a[y]
    # print color runs
    runs = []
    prev = None; start = 0
    for x in range(W):
        c = tuple(row[x])
        if prev is None:
            prev, start = c, x
        elif abs(c[0]-prev[0])+abs(c[1]-prev[1])+abs(c[2]-prev[2]) > 60:
            if x - start > 8:
                runs.append(f"{start}-{x-1}:{'#%02x%02x%02x' % prev}")
            prev, start = c, x
    if W - start > 8:
        runs.append(f"{start}-{W-1}:{'#%02x%02x%02x' % prev}")
    print(f" y={y}: " + " | ".join(runs[:14]))
