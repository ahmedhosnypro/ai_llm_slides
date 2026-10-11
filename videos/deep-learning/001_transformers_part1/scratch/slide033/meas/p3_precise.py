#!/usr/bin/env python3
"""Slide 033 pass 3: precise (unquantized) mode colors + per-family bboxes."""
from PIL import Image
import numpy as np
from collections import Counter, deque

IM = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_033.jpg").convert("RGB")
A = np.asarray(IM).astype(int)
H, W = A.shape[:2]

def mode_precise(region, k=4):
    x0, y0, x1, y1 = region
    sub = A[y0:y1+1, x0:x1+1].reshape(-1, 3)
    c = Counter(map(tuple, sub))
    return [(f"#{r:02X}{g:02X}{b:02X}", n) for (r, g, b), n in c.most_common(k)]

def mask_boxes(color, tol, min_area, label, k=16, region=None):
    c = np.array(color)
    if region:
        rx0, ry0, rx1, ry1 = region
    else:
        rx0, ry0, rx1, ry1 = 0, 0, W - 1, H - 1
    sub = A[ry0:ry1+1, rx0:rx1+1]
    m = (np.abs(sub - c) <= tol).all(axis=2)
    idx = np.argwhere(m)
    if len(idx) == 0:
        print(f"[{label}] NONE"); return
    seen = np.zeros(m.shape, bool)
    boxes = []
    for (yy, xx) in idx:
        if seen[yy, xx]: continue
        q = deque([(yy, xx)]); seen[yy, xx] = True
        ys, xs, n = [yy], [xx], 0
        while q:
            y, x = q.popleft(); n += 1
            for dy, dx in ((1,0),(-1,0),(0,1),(0,-1)):
                ny, nx = y+dy, x+dx
                if 0 <= ny < m.shape[0] and 0 <= nx < m.shape[1] and not seen[ny, nx] and m[ny, nx]:
                    seen[ny, nx] = True; q.append((ny, nx)); ys.append(ny); xs.append(nx)
            if n > 80000: break
        if n >= min_area:
            boxes.append((n, rx0+min(xs), rx0+max(xs), ry0+min(ys), ry0+max(ys)))
    boxes.sort(key=lambda b: -b[0])
    print(f"[{label}] core #{color[0]:02X}{color[1]:02X}{color[2]:02X} tol={tol}")
    for n, x0, x1, y0, y1 in boxes[:k]:
        print(f"   n={n:6d}  x {x0:3d}..{x1:3d}  y {y0:3d}..{y1:3d}  (w={x1-x0+1}, h={y1-y0+1})")

print("=== precise color modes ===")
probes = {
    "peach panel a": (300, 440, 340, 470),
    "peach panel top": (600, 115, 660, 135),
    "W_k box a": (155, 250, 185, 278),
    "W_k box b": (155, 292, 185, 318),
    "dotprod": (270, 360, 300, 390),
    "softmax": (465, 255, 480, 295),
    "sigma": (560, 202, 630, 213),
    "container L": (60, 300, 64, 320),
    "container R": (766, 300, 770, 320),
    "sentence": (310, 478, 330, 490),
    "legend": (750, 476, 780, 486),
    "pill S": (285, 168, 320, 178),
    "pill P": (450, 168, 490, 178),
    "pill WS": (620, 160, 660, 178),
    "gray panel": (930, 300, 950, 400),
    "canvas": (10, 300, 30, 400),
    "mini sq1 L": (69, 242, 76, 251),
    "mini sq2 L": (81, 242, 92, 251),
    "mini sq3 L": (95, 242, 106, 251),
}
for nm, r in probes.items():
    print(f"{nm:16s} {r}: {mode_precise(r)}")

print("\n=== family scans ===")
mask_boxes((255, 255, 102), 30, 300, "W-boxes(yellow)")     # W boxes
mask_boxes((0, 58, 0), 90, 60, "dark-green borders")         # 00A651 is (0,166,81); dashed border cores maybe darker
mask_boxes((0, 166, 81), 70, 25, "green-ink", 20)
mask_boxes((139, 0, 0), 50, 40, "darkred-ink", 22)
mask_boxes((204, 0, 0), 55, 40, "red-ink", 22)
mask_boxes((2, 0, 171), 60, 12, "blue-dots", 12)
mask_boxes((255, 0, 255), 80, 20, "magenta", 10)
mask_boxes((0, 0, 204), 60, 12, "blue-ink", 12)
mask_boxes((0, 128, 0), 45, 12, "green-label-ink", 10)
