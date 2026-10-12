#!/usr/bin/env python3
"""Slide 043: cube stacks structure (color runs along scanlines) + arrows."""
from PIL import Image
import numpy as np

F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_043.jpg"
im = Image.open(F).convert("RGB")
a = np.asarray(im).astype(int)

def name(px):
    r, g, b = int(px[0]), int(px[1]), int(px[2])
    if r > 180 and g < 80 and b > 180: return "magenta"
    if r > 180 and 60 <= g < 160 and b < 90: return "orange"
    if r > 180 and 140 <= g < 200 and b < 120: return "salmon"
    if g > 150 and r < 120 and b < 120: return "green"
    if r > 180 and g > 180 and b < 120: return "yellow"
    if 100 < r < 190 and 120 < g < 200 and b > 170: return "bluegray"
    if r < 90 and g < 90 and b < 130: return "dark"
    if abs(r - g) < 25 and abs(g - b) < 25 and r > 190: return "white/gray"
    if r > 180 and g < 90 and b < 90: return "red"
    if r < 110 and g < 110 and b < 150: return "darknavy"
    return f"({r},{g},{b})"

def runs_row(y, x0, x1, minlen=2):
    out, cur, start = [], None, x0
    for x in range(x0, x1):
        n = name(a[y, x])
        if n != cur:
            if cur is not None and x - start >= minlen: out.append((start, x - 1, cur))
            elif cur is not None: out.append((start, x - 1, cur + "?"))
            cur, start = n, x
    out.append((start, x1 - 1, cur))
    return out

def runs_col(x, y0, y1, minlen=2):
    out, cur, start = [], None, y0
    for y in range(y0, y1):
        n = name(a[y, x])
        if n != cur:
            if cur is not None and y - start >= minlen: out.append((start, y - 1, cur))
            elif cur is not None: out.append((start, y - 1, cur + "?"))
            cur, start = n, y
    out.append((start, y1 - 1, cur))
    return out

print("=== LEFT STACK ===")
print("row y=300 (fronts):", runs_row(300, 75, 345))
print("row y=200 (upper fronts/tops):", runs_row(200, 75, 345))
print("row y=140 (tops):", runs_row(140, 75, 345))
print("row y=110 (tops):", runs_row(110, 75, 345))
print("row y=95 (tops back):", runs_row(95, 75, 345))
print("col x=140 (front col):", runs_col(140, 85, 345))
print("col x=280 (mid slice):", runs_col(280, 85, 345))
print("col x=320 (orange slice):", runs_col(320, 85, 345))

print("=== RIGHT STACK ===")
print("row y=300 (fronts):", runs_row(300, 630, 905))
print("row y=200 (fronts):", runs_row(200, 630, 905))
print("row y=140 (tops/slices):", runs_row(140, 630, 905))
print("row y=110 (tops):", runs_row(110, 630, 905))
print("row y=95 (tops back):", runs_row(95, 630, 905))
print("col x=700 (front col):", runs_col(700, 75, 360))
print("col x=840 (rear slices):", runs_col(840, 75, 360))
print("col x=880 (bluegray):", runs_col(880, 75, 360))

print("=== ARROWS (red mask) ===")
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
redm = (r > 140) & (r - g > 50) & (r - b > 50) & (g < b + 35)
# vertical arrow: window x 630..680, y 130..360
ys, xs = np.where(redm[130:370, 630:690])
print("vert-arrow window bbox: x", xs.min() + 630, "..", xs.max() + 630, " y", ys.min() + 130, "..", ys.max() + 130)
# per-column count to find shaft x
from collections import Counter
cc = Counter(xs + 630)
print("vert-arrow top columns:", cc.most_common(6))
# horizontal arrow: window x 600..830, y 450..510
ys, xs = np.where(redm[450:515, 600:840])
print("horiz-arrow window bbox: x", xs.min() + 600, "..", xs.max() + 600, " y", ys.min() + 450, "..", ys.max() + 450)
rr = Counter(ys + 450)
print("horiz-arrow top rows:", rr.most_common(6))
# diagonal arrow: window x 760..910, y 380..510
ys, xs = np.where(redm[380:515, 760:915])
print("diag-arrow window bbox: x", xs.min() + 760, "..", xs.max() + 760, " y", ys.min() + 380, "..", ys.max() + 380)
