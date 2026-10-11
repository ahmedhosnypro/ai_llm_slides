#!/usr/bin/env python3
"""Measure slide_007.jpg delta elements + verify inherited title position vs 006."""
from PIL import Image
import numpy as np

BASE = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides"
a = np.asarray(Image.open(f"{BASE}/slide_006.jpg").convert("RGB")).astype(int)
b = np.asarray(Image.open(f"{BASE}/slide_007.jpg").convert("RGB")).astype(int)

def ink_rows(img, x0, x1, y0, y1, thr=400):
    """rows containing dark ink in window"""
    win = img[y0:y1, x0:x1].sum(axis=2)
    dark = win < thr
    return [(y0 + i, int(dark[i].sum())) for i in range(dark.shape[0]) if dark[i].sum() > 0]

def ink_bbox(img, x0, x1, y0, y1, thr=400):
    win = img[y0:y1, x0:x1].sum(axis=2)
    dark = win < thr
    ys, xs = np.nonzero(dark)
    if not len(ys):
        return None
    return (x0 + xs.min(), y0 + ys.min(), x0 + xs.max(), y0 + ys.max())

print("=== TITLE LINE 1 (x 260..700, y 40..95) ===")
bb6 = ink_bbox(a, 260, 700, 40, 95)
bb7 = ink_bbox(b, 260, 700, 40, 95)
print("006 title bbox:", bb6)
print("007 title bbox:", bb7)

print("\n=== BADGE NUMERAL (x 870..920, y 48..95) ===")
print("006:", ink_bbox(a, 870, 920, 48, 95, thr=350))
print("007:", ink_bbox(b, 870, 920, 48, 95, thr=350))

print("\n=== SUBTITLE '(Challenges)' in 007 (x 260..700, y 86..125) ===")
bb = ink_bbox(b, 260, 700, 86, 125, thr=420)
print("007 subtitle bbox:", bb)
# color sample at ink center
if bb:
    cx, cy = (bb[0] + bb[2]) // 2, (bb[1] + bb[3]) // 2
    # darkest pixel color in window
    win = b[bb[1]:bb[3] + 1, bb[0]:bb[2] + 1]
    lum = win.sum(axis=2)
    iy, ix = np.unravel_index(np.argmin(lum), lum.shape)
    print("darkest px color (007):", win[iy, ix])
    # 006 same window should be empty
    print("006 same window ink bbox:", ink_bbox(a, 260, 700, 86, 125, thr=420))

print("\n=== row ink counts, title region, x260..700 ===")
r6 = ink_rows(a, 260, 700, 40, 125)
r7 = ink_rows(b, 260, 700, 40, 125)
def bands(rows):
    out = []
    cur = None
    for y, c in rows:
        if cur and y - cur[1] <= 2:
            cur[1] = y; cur[2] += c
        else:
            if cur: out.append(tuple(cur))
            cur = [y, y, c]
    if cur: out.append(tuple(cur))
    return out
print("006 bands (y0,y1,px):", bands(r6))
print("007 bands (y0,y1,px):", bands(r7))
