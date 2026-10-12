#!/usr/bin/env python3
# measure1.py — slide_012.jpg frame measurements (960x540, 1px=1pt)
# Mapping: slide_x=(fx-17.628)/0.961232, slide_y=fy/0.955556
from PIL import Image
import numpy as np

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_012.jpg').convert('RGB')
a = np.asarray(im).astype(int)
H, W = a.shape[:2]
print("size", W, H)

def ink_mask(sub, thr=200):
    # "ink" = strongly non-background (dark or saturated)
    r, g, b = sub[..., 0], sub[..., 1], sub[..., 2]
    mx = np.maximum(np.maximum(r, g), b)
    mn = np.minimum(np.minimum(r, g), b)
    return (mx - mn > 60) | (mx < thr - 60)

def row_ink_spans(y0, y1, x0, x1, thr=200):
    m = ink_mask(a[y0:y1, x0:x1], thr)
    cols = m.any(axis=0)
    spans = []
    s = None
    for i, v in enumerate(cols):
        if v and s is None: s = i
        if not v and s is not None:
            spans.append((x0 + s, x0 + i - 1)); s = None
    if s is not None: spans.append((x0 + s, x0 + len(cols) - 1))
    return spans

def band_ink_rows(x0, x1, y0, y1, thr=200):
    m = ink_mask(a[y0:y1, x0:x1], thr)
    rows = m.any(axis=1)
    spans = []
    s = None
    for i, v in enumerate(rows):
        if v and s is None: s = i
        if not v and s is not None:
            spans.append((y0 + s, y0 + i - 1)); s = None
    if s is not None: spans.append((y0 + s, y0 + len(rows) - 1))
    return spans

def color_at(fx, fy, n=3):
    patch = a[fy - n:fy + n + 1, fx - n:fx + n + 1].reshape(-1, 3)
    med = np.median(patch, axis=0)
    return tuple(int(v) for v in med)

def mode_color(x0, y0, x1, y1):
    sub = a[y0:y1, x0:x1].reshape(-1, 3)
    q = (sub // 8) * 8
    uniq, cnt = np.unique(q, axis=0, return_counts=True)
    k = int(cnt.argmax())
    return tuple(int(v) for v in uniq[k]), int(cnt[k])

print("\n--- TITLE band (fy 55..95) ---")
for s in band_ink_rows(20, 940, 55, 100):
    print("row-span fy", s)
r = band_ink_rows(20, 940, 55, 100)
if r:
    y0, y1 = r[0]
    sp = row_ink_spans(30, 930, y0, y1)
    print("title ink fx spans:", sp[0][0] if sp else None, "..", sp[-1][1] if sp else None, "nspans", len(sp))
    print("title color:", mode_color(100, y0, 800, y1))

print("\n--- SUBTITLE band (fy 95..130) ---")
r = band_ink_rows(20, 940, 95, 135)
for s in r: print("row-span fy", s)
if r:
    y0, y1 = r[0]
    sp = row_ink_spans(30, 930, y0, y1)
    if sp: print("subtitle ink fx:", sp[0][0], "..", sp[-1][1])
    print("subtitle color:", mode_color(100, y0, 800, y1))

print("\n--- full-column profile x=0..960: which rows have ink outside letterbox ---")
# coarse map of content bands
rows = ink_mask(a[:, 20:940], 200).sum(axis=1)
for y in range(0, H, 10):
    seg = rows[y:y+10].max()
    if seg > 5:
        print(f"fy {y:3d}-{y+9:3d}: maxink {seg:4d}")

