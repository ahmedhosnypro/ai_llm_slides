#!/usr/bin/env python3
"""Slide 033 frame forensics pass 1: locate major color regions in the original frame.
960x540, 1px = 1pt = 1/72in. Masks use core-color matching (|d|<=tol per channel)."""
from PIL import Image
import sys, json
import numpy as np

IM = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_033.jpg").convert("RGB")
A = np.asarray(IM).astype(int)
H, W = A.shape[:2]

def mask_bboxes(color, tol=28, min_area=40, name=""):
    c = np.array(color)
    m = (np.abs(A - c) <= tol).all(axis=2)
    # connected components via simple flood (scipy may be absent) -> label by rows/cols runs
    from collections import deque
    seen = np.zeros((H, W), bool)
    boxes = []
    idx = np.argwhere(m)
    coords = set(map(tuple, idx))
    for (y0, x0) in idx:
        if seen[y0, x0]:
            continue
        q = deque([(y0, x0)])
        seen[y0, x0] = True
        ys = [y0]; xs = [x0]; n = 0
        while q:
            y, x = q.popleft()
            n += 1
            for dy, dx in ((1,0),(-1,0),(0,1),(0,-1)):
                ny, nx = y+dy, x+dx
                if 0 <= ny < H and 0 <= nx < W and not seen[ny, nx] and (ny, nx) in coords:
                    seen[ny, nx] = True
                    q.append((ny, nx))
                    ys.append(ny); xs.append(nx)
            if n > 60000:
                break
        if n >= min_area:
            boxes.append(dict(name=name, n=n, x0=int(min(xs)), x1=int(max(xs)), y0=int(min(ys)), y1=int(max(ys))))
    boxes.sort(key=lambda b: -b["n"])
    return boxes

def show(boxes, k=14):
    for b in boxes[:k]:
        print(f"  {b['name']:14s} n={b['n']:7d} x {b['x0']:3d}..{b['x1']:3d}  y {b['y0']:3d}..{b['y1']:3d}  (w={b['x1']-b['x0']+1}, h={b['y1']-b['y0']+1})")

targets = [
    ("peachPanel",   (252, 228, 198), 24),   # FCE4C6
    ("greenDashed",  (0, 166, 81),    40),   # 00A651 borders
    ("greenFill",    (234, 246, 234), 10),   # EAF6EA
    ("yellowW",      (255, 255, 0),   40),   # FFFF00
    ("taupeBox",     (179, 170, 164), 16),   # B3AAA4
    ("orchidBar",    (231, 193, 231), 18),   # E7C1E7
    ("sigmaFill",    (204, 228, 247), 14),   # CCE4F7
    ("pillYellow",   (255, 255, 204), 10),   # FFFFCC
    ("red",          (204, 0, 0),     60),   # CC0000 arrows/labels
    ("darkRed",      (139, 0, 0),     45),   # 8B0000 labels
    ("magenta",      (255, 0, 255),   60),   # FF00FF
    ("blueDark",     (0, 51, 102),    45),   # 003366
    ("blueSigmaTx",  (0, 0, 204),     60),   # 0000CC title span
    ("grayPanel",    (233, 233, 231), 8),    # E9E9E7 chrome
]
print("=== region bboxes (top components) ===")
for name, color, tol in targets:
    print(f"[{name}] core={color} tol={tol}")
    show(mask_bboxes(color, tol, name=name))
