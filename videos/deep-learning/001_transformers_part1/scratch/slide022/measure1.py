#!/usr/bin/env python3
"""PIL measurement of the original frame slide_022.jpg (960x540, 1px=1pt).
Detects color regions + ink bands to derive exact geometry for the build."""
import sys
from PIL import Image
import numpy as np

FR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_022.jpg"
im = Image.open(FR).convert("RGB")
a = np.asarray(im).astype(int)
H, W, _ = a.shape
print(f"frame {W}x{H}")

def mask_near(hexcol, tol):
    r, g, b = int(hexcol[0:2], 16), int(hexcol[2:4], 16), int(hexcol[4:6], 16)
    d = np.abs(a[:, :, 0] - r) + np.abs(a[:, :, 1] - g) + np.abs(a[:, :, 2] - b)
    return d <= tol

def regions(m, min_px=30, name=""):
    """connected-ish bounding boxes via row/col projection clustering"""
    ys, xs = np.where(m)
    if len(xs) < min_px:
        print(f"{name}: NO PIXELS ({len(xs)})")
        return []
    # cluster by connected components on a coarse grid using scipy-free flood
    from collections import deque
    visited = np.zeros_like(m, dtype=bool)
    boxes = []
    ys, xs = np.where(m)
    coords = set(zip(ys.tolist(), xs.tolist()))
    seen = set()
    for start in list(coords):
        if start in seen:
            continue
        q = deque([start])
        seen.add(start)
        miny = maxy = start[0]; minx = maxx = start[1]
        n = 0
        while q:
            y, x = q.popleft(); n += 1
            if y < miny: miny = y
            if y > maxy: maxy = y
            if x < minx: minx = x
            if x > maxx: maxx = x
            for dy in (-2, -1, 0, 1, 2):
                for dx in (-2, -1, 0, 1, 2):
                    p = (y + dy, x + dx)
                    if p in coords and p not in seen:
                        seen.add(p); q.append(p)
        if n >= min_px:
            boxes.append((minx, miny, maxx, maxy, n))
    boxes.sort(key=lambda b: (b[1], b[0]))
    print(f"{name}: {len(boxes)} regions (x,y,x2,y2,npx) [pt = px]:")
    for b in boxes[:40]:
        print(f"   x{b[0]}..{b[2]}  y{b[1]}..{b[3]}  n={b[4]}  -> in: x {b[0]/72:.3f}..{b[2]/72:.3f} y {b[1]/72:.3f}..{b[3]/72:.3f}")
    return boxes

print("\n=== BLUE panel borders (#0000CC) ===")
regions(mask_near("0000CC", 150), 60, "blue")
print("\n=== DARK RED container borders (#8B0000) ===")
regions(mask_near("8B0000", 110), 60, "dkred")
print("\n=== ORANGE border (#E8940A) ===")
regions(mask_near("E8940A", 110), 60, "orange")
print("\n=== PEACH fill (#F5C99B) ===")
regions(mask_near("F5C99B", 60), 200, "peach")
print("\n=== GREEN border (#008000) ===")
regions(mask_near("008000", 110), 60, "green")
print("\n=== YELLOW tags (#FFFF99) — bottom area only y>380 ===")
m = mask_near("FFFF99", 60)
m[:380, :] = False
regions(m, 200, "yellow")
