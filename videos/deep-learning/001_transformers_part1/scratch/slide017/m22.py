#!/usr/bin/env python3
"""Exact V/K/Q circle positions + leader lines + panel labels + white box geometry."""
import numpy as np
from PIL import Image
from collections import deque

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_017.jpg').convert('RGB')
A = np.asarray(im).astype(int)
H, W, _ = A.shape

def comps(test, x0, x1, y0, y1, min_px=8):
    seen = np.zeros((H, W), dtype=bool)
    out = []
    for y in range(y0, y1+1):
        for x in range(x0, x1+1):
            if seen[y, x] or not test(*A[y, x]):
                continue
            q = deque([(y, x)]); seen[y, x] = True; pts = []
            while q:
                cy, cx = q.popleft(); pts.append((cy, cx))
                for dy, dx in ((1,0),(-1,0),(0,1),(0,-1)):
                    ny, nx = cy+dy, cx+dx
                    if y0 <= ny <= y1 and x0 <= nx <= x1 and not seen[ny, nx] and test(*A[ny, nx]):
                        seen[ny, nx] = True; q.append((ny, nx))
            if len(pts) >= min_px:
                ys = [p[0] for p in pts]; xs = [p[1] for p in pts]
                out.append((len(pts), min(xs), min(ys), max(xs), max(ys)))
    return out

blue = lambda r, g, b: b > 120 and b-r > 45 and b-g > 25
red = lambda r, g, b: r > 150 and g < 110 and b < 110 and r-g > 55

print("ENCODER circles band (y388..412):")
for n, x0, y0, x1, y1 in comps(blue, 630, 730, 388, 412) + comps(red, 630, 730, 388, 412):
    print(f"   n={n} x{x0}..{x1} y{y0}..{y1} c=({(x0+x1)/2},{(y0+y1)/2}) d={x1-x0+1}")
print("DECODER masked circles band (y305..326):")
for n, x0, y0, x1, y1 in comps(blue, 740, 840, 305, 326) + comps(red, 740, 840, 305, 326):
    print(f"   n={n} x{x0}..{x1} y{y0}..{y1} c=({(x0+x1)/2},{(y0+y1)/2}) d={x1-x0+1}")
print("DECODER cross circles band (y382..400):")
for n, x0, y0, x1, y1 in comps(blue, 740, 840, 382, 400) + comps(red, 740, 840, 382, 400):
    print(f"   n={n} x{x0}..{x1} y{y0}..{y1} c=({(x0+x1)/2},{(y0+y1)/2}) d={x1-x0+1}")

# leader lines in the left margin (x520..578): faint gray on gray panel
print("leader lines x516..576:")
dark = lambda r, g, b: (r+g+b)/3 < 224 and max(r,g,b)-min(r,g,b) < 30
for y in range(100, 531):
    xs = [x for x in range(516, 577) if dark(*A[y, x])]
    if len(xs) >= 2:
        print(f"   y{y:3d}: x{min(xs)}..{max(xs)} n={len(xs)}")

# Encoder / Decoder labels (red italic / green italic)
print("Encoder label red text:")
for n, x0, y0, x1, y1 in comps(lambda r,g,b: r > 130 and g < 120 and b < 120 and r-g > 40, 578, 660, 108, 135):
    print(f"   n={n} x{x0}..{x1} y{y0}..{y1}")
print("Decoder label green text:")
for n, x0, y0, x1, y1 in comps(lambda r,g,b: g > 100 and g-r > 30 and g-b > 30, 820, 900, 108, 140):
    print(f"   n={n} x{x0}..{x1} y{y0}..{y1}")

# white boxes (Linear/Softmax) — white fill on pale green panel
white = lambda r, g, b: r > 242 and g > 242 and b > 242
print("white boxes decoder top (x745..840, y145..200):")
for n, x0, y0, x1, y1 in comps(white, 745, 840, 145, 200, 40):
    print(f"   n={n} x{x0}..{x1} y{y0}..{y1} w={x1-x0+1} h={y1-y0+1}")
