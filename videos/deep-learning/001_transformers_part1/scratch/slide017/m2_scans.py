#!/usr/bin/env python3
"""Scanline color runs for slide_017.jpg — identify panel/node boundaries."""
import numpy as np
from PIL import Image

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_017.jpg').convert('RGB')
A = np.asarray(im).astype(int)

def runs_along_row(y, x0=0, x1=960, tol=28):
    out = []
    start = x0
    cur = A[y, x0]
    for x in range(x0+1, x1):
        if np.abs(A[y, x] - cur).sum() > tol:
            out.append((start, x-1, tuple(int(v) for v in cur)))
            start = x
            cur = A[y, x]
        else:
            # running average update
            cur = (cur*3 + A[y, x]) // 4
    out.append((start, x1-1, tuple(int(v) for v in cur)))
    return out

def show_row(y, x0=0, x1=960, minlen=3):
    print(f"--- row y={y} ---")
    for s, e, c in runs_along_row(y, x0, x1):
        if e - s + 1 >= minlen:
            print(f"   x{s:3d}..{e:3d} ({e-s+1:3d}px) rgb{c}")

def runs_along_col(x, y0=0, y1=540, tol=28):
    out = []
    start = y0
    cur = A[y0, x]
    for y in range(y0+1, y1):
        if np.abs(A[y, x] - cur).sum() > tol:
            out.append((start, y-1, tuple(int(v) for v in cur)))
            start = y
            cur = A[y, x]
        else:
            cur = (cur*3 + A[y, x]) // 4
    out.append((start, y1-1, tuple(int(v) for v in cur)))
    return out

def show_col(x, y0=0, y1=540, minlen=3):
    print(f"--- col x={x} ---")
    for s, e, c in runs_along_col(x, y0, y1):
        if e - s + 1 >= minlen:
            print(f"   y{s:3d}..{e:3d} ({e-s+1:3d}px) rgb{c}")

# through encoder panel middle (x=655) full height
show_col(655)
