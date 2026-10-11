#!/usr/bin/env python3
"""Measure color regions in slide_037.jpg (960x540, 1px=1pt)."""
import numpy as np
from PIL import Image
import sys

IMG = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_037.jpg"
im = Image.open(IMG).convert("RGB")
W, H = im.size
a = np.asarray(im).astype(int)
print(f"size {W}x{H}")

def close(target, tol):
    t = np.array(target)
    return (np.abs(a - t).max(axis=2) <= tol)

def components(mask, min_px=25):
    """simple connected components via flood fill (scipy absent?)"""
    try:
        from scipy import ndimage
        lab, n = ndimage.label(mask)
        out = []
        for i in range(1, n + 1):
            ys, xs = np.where(lab == i)
            if len(ys) < min_px:
                continue
            out.append((xs.min(), ys.min(), xs.max(), ys.max(), len(ys)))
        return out
    except ImportError:
        # BFS fallback
        out = []
        visited = np.zeros(mask.shape, dtype=bool)
        idx = np.argwhere(mask)
        for (y, x) in idx:
            if visited[y, x]:
                continue
            stack = [(y, x)]
            visited[y, x] = True
            ys = [y]; xs = [x]
            while stack:
                cy, cx = stack.pop()
                for dy in (-1, 0, 1):
                    for dx in (-1, 0, 1):
                        ny, nx = cy + dy, cx + dx
                        if 0 <= ny < H and 0 <= nx < W and mask[ny, nx] and not visited[ny, nx]:
                            visited[ny, nx] = True
                            stack.append((ny, nx))
                            ys.append(ny); xs.append(nx)
            if len(ys) >= min_px:
                out.append((min(xs), min(ys), max(xs), max(ys), len(ys)))
        return out

REGIONS = {
    "peach FCE3D0": ((0xFC, 0xE3, 0xD0), 14),
    "tan D2A870": ((0xD2, 0xA8, 0x70), 20),
    "yellow FFFF00": ((0xFF, 0xFF, 0x00), 40),
    "pill FFEE58": ((0xFF, 0xEE, 0x58), 12),
    "purple CC99FF": ((0xCC, 0x99, 0xFF), 20),
    "lightblue BDD7EE": ((0xBD, 0xD7, 0xEE), 20),
    "green EAF5E4": ((0xEA, 0xF5, 0xE4), 8),
    "medgreen 92D050": ((0x92, 0xD0, 0x50), 30),
    "green 00B050": ((0x00, 0xB0, 0x50), 30),
    "pink FF66CC": ((0xFF, 0x66, 0xCC), 40),
    "mint D9F2D9": ((0xD9, 0xF2, 0xD9), 10),
    "gray BFBFBF": ((0xBF, 0xBF, 0xBF), 20),
    "white FFFFFF": ((0xFF, 0xFF, 0xFF), 8),
    "red FF0000": ((0xFF, 0x00, 0x00), 60),
    "blue 0000CC": ((0x00, 0x00, 0xCC), 20),
    "darkred 943634": ((0x94, 0x36, 0x34), 30),
    "blue text 0033CC": ((0x00, 0x33, 0xCC), 30),
    "orange FF8000": ((0xFF, 0x80, 0x00), 25),
    "dark 464646": ((0x46, 0x46, 0x46), 20),
}

sel = sys.argv[1:] if len(sys.argv) > 1 else None
for name, (rgb, tol) in REGIONS.items():
    if sel and not any(s in name for s in sel):
        continue
    mask = close(rgb, tol)
    total = int(mask.sum())
    comps = sorted(components(mask, 20), key=lambda c: -c[4])[:12]
    print(f"\n== {name}: total {total}")
    for (x0, y0, x1, y1, n) in comps:
        print(f"   bbox x[{x0},{x1}] y[{y0},{y1}]  w={x1-x0+1} h={y1-y0+1} n={n}")
