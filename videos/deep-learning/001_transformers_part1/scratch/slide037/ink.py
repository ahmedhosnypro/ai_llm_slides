#!/usr/bin/env python3
"""Cluster saturated ink colors (red / blue / dark / green) into component bboxes."""
import numpy as np
from PIL import Image
import sys

IMG = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_037.jpg"
im = Image.open(IMG).convert("RGB")
a = np.asarray(im).astype(int)
H, W, _ = a.shape

try:
    from scipy import ndimage
    HAVE_SCIPY = True
except ImportError:
    HAVE_SCIPY = False

def cluster(mask, min_px=8):
    if HAVE_SCIPY:
        lab, n = ndimage.label(mask, structure=np.ones((3, 3)))
        out = []
        for i in range(1, n + 1):
            ys, xs = np.where(lab == i)
            if len(ys) < min_px:
                continue
            out.append((int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max()), len(ys)))
        return out
    # BFS fallback
    out = []
    visited = np.zeros(mask.shape, dtype=bool)
    for (y, x) in np.argwhere(mask):
        if visited[y, x]:
            continue
        stack = [(y, x)]
        visited[y, x] = True
        ys, xs = [y], [x]
        while stack:
            cy, cx = stack.pop()
            for dy in (-2, -1, 0, 1, 2):
                for dx in (-2, -1, 0, 1, 2):
                    ny, nx = cy + dy, cx + dx
                    if 0 <= ny < H and 0 <= nx < W and mask[ny, nx] and not visited[ny, nx]:
                        visited[ny, nx] = True
                        stack.append((ny, nx))
                        ys.append(ny); xs.append(nx)
        if len(ys) >= min_px:
            out.append((min(xs), min(ys), max(xs), max(ys), len(ys)))
    return out

R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]

masks = {
    "RED": (R > 150) & (G < 95) & (B < 95),
    "RED2": (R > 100) & (R - G > 55) & (R - B > 55),
    "BLUE": (B > 130) & (R < 110) & (G < 110),
    "DARK": (R < 95) & (G < 95) & (B < 95),
    "GREEN": (G > 120) & (R < 110) & (B < 130) & (G - R > 40),
}
sel = sys.argv[1:] if len(sys.argv) > 1 else None
args = [v for v in sys.argv[1:] if not v.isalpha()]
x0, y0, x1, y1 = (int(v) for v in args[:4]) if len(args) >= 4 else (0, 0, W, H)

for name, m in masks.items():
    if sel and name not in sel:
        continue
    mm = np.zeros_like(m)
    mm[y0:y1, x0:x1] = m[y0:y1, x0:x1]
    comps = sorted(cluster(mm, 10), key=lambda c: (c[1], c[0]))
    print(f"\n== {name} ({int(mm.sum())} px) in x[{x0},{x1}] y[{y0},{y1}] — {len(comps)} comps")
    for (cx0, cy0, cx1, cy1, n) in comps[:80]:
        print(f"   x[{cx0:3d},{cx1:3d}] y[{cy0:3d},{cy1:3d}] w={cx1-cx0+1:3d} h={cy1-cy0+1:3d} n={n}")
