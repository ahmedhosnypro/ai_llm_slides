#!/usr/bin/env python3
"""Measure slide_049.jpg bands 2: tokens, arrows, bars, word row, left column."""
from PIL import Image
import numpy as np
from collections import deque

F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_049.jpg"
im = Image.open(F).convert("RGB")
a = np.asarray(im).astype(int)
H, W = a.shape[:2]
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]

def clusters(vals, gap=3):
    if not len(vals): return []
    out = []; cur = [vals[0]]
    for v in vals[1:]:
        if v - cur[-1] <= gap: cur.append(v)
        else: out.append(cur); cur = [v]
    out.append(cur); return out

def comps_of(mask, minpx=30, region=None):
    m = mask
    if region is not None:
        x0, x1, y0, y1 = region
        mm = np.zeros_like(mask); mm[y0:y1+1, x0:x1+1] = mask[y0:y1+1, x0:x1+1]; m = mm
    seen = np.zeros(mask.shape, bool); out = []
    ys, xs = np.where(m)
    for y0_, x0_ in zip(ys, xs):
        if seen[y0_, x0_]: continue
        q = deque([(y0_, x0_)]); seen[y0_, x0_] = True
        xmn = xmx = x0_; ymn = ymx = y0_; n = 0
        while q:
            y, x = q.popleft(); n += 1
            if x < xmn: xmn = x
            if x > xmx: xmx = x
            if y < ymn: ymn = y
            if y > ymx: ymx = y
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    ny, nx = y + dy, x + dx
                    if 0 <= ny < H and 0 <= nx < W and m[ny, nx] and not seen[ny, nx]:
                        seen[ny, nx] = True; q.append((ny, nx))
        if n >= minpx: out.append((xmn, xmx, ymn, ymx, n))
    return sorted(out, key=lambda c: (c[2], c[0]))

def census(x0, x1, y0, y1, name):
    reg = a[y0:y1+1, x0:x1+1].reshape(-1, 3)
    mean = reg.mean(axis=0); med = np.median(reg, axis=0)
    print(f"  {name}: mean ({mean[0]:.0f},{mean[1]:.0f},{mean[2]:.0f}) med ({med[0]:.0f},{med[1]:.0f},{med[2]:.0f})")

print("== green arrows (band y 100..128, x 150..900) ==")
green = (g > 120) & (g - r > 40) & (g - b > 40)
for c in comps_of(green, 40, (150, 900, 100, 128)):
    print("   ", c, "cx %.1f" % ((c[0]+c[1])/2))
print("== gray arrows (band y 460..480) ==")
gray = (abs(r-g) < 14) & (abs(g-b) < 14) & (r > 130) & (r < 205)
for c in comps_of(gray, 25, (150, 900, 458, 482)):
    print("   ", c, "cx %.1f" % ((c[0]+c[1])/2))
print("== medium-blue arrows (band y 396..414) ==")
mblue = (b > 130) & (b - r > 45) & (b - g > 30) & (g < 140) & (r < 140)
for c in comps_of(mblue, 25, (150, 900, 394, 416)):
    print("   ", c, "cx %.1f" % ((c[0]+c[1])/2))
print("== red arrows between bars: band y 160..237 x 150..900 ==")
dred = (r > 100) & (r - g > 45) & (r - b > 45) & (g < 95)
for c in comps_of(dred, 20, (150, 900, 160, 237)):
    print("   ", c, "cx %.1f" % ((c[0]+c[1])/2))
print("== red arrows band y 267..283 ==")
for c in comps_of(dred, 20, (150, 900, 267, 283)):
    print("   ", c, "cx %.1f" % ((c[0]+c[1])/2))
print("== red arrows band y 312..329 ==")
for c in comps_of(dred, 20, (150, 900, 312, 329)):
    print("   ", c, "cx %.1f" % ((c[0]+c[1])/2))
print("== blue dots between Block2/M (band y 162..236, dark blue, small) ==")
dblue = (b > 110) & (b - r > 60) & (b - g > 60) & (r < 110)
dc = comps_of(dblue, 8, (150, 900, 163, 235))
# group by column
cols = {}
for c in dc:
    cx = (c[0]+c[1])/2
    key = round(cx/2)*2
    cols.setdefault(key, []).append(c)
print("   n comps:", len(dc))
for k in sorted(cols):
    ys = sorted((c[2]+c[3])/2 for c in cols[k])
    print("    col cx~%d: %d dots y %s" % (k, len(cols[k]), ["%.0f" % y for y in ys]))
