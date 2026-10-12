#!/usr/bin/env python3
"""Full region measurement of slide_049.jpg. Band-by-band color census."""
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

def comps_of(mask, minpx=30):
    seen = np.zeros(mask.shape, bool); out = []
    ys, xs = np.where(mask)
    for y0, x0 in zip(ys, xs):
        if seen[y0, x0]: continue
        q = deque([(y0, x0)]); seen[y0, x0] = True
        xmn = xmx = x0; ymn = ymx = y0; n = 0
        while q:
            y, x = q.popleft(); n += 1
            if x < xmn: xmn = x
            if x > xmx: xmx = x
            if y < ymn: ymn = y
            if y > ymx: ymx = y
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    ny, nx = y + dy, x + dx
                    if 0 <= ny < H and 0 <= nx < W and mask[ny, nx] and not seen[ny, nx]:
                        seen[ny, nx] = True; q.append((ny, nx))
        if n >= minpx: out.append((xmn, xmx, ymn, ymx, n))
    return out

def census(x0, x1, y0, y1, name):
    reg = a[y0:y1 + 1, x0:x1 + 1].reshape(-1, 3)
    mean = reg.mean(axis=0)
    med = np.median(reg, axis=0)
    print(f"  {name}: mean rgb ({mean[0]:.0f},{mean[1]:.0f},{mean[2]:.0f}) med ({med[0]:.0f},{med[1]:.0f},{med[2]:.0f})")

# ---------- 1. encoder container (light blue) ----------
# spec C9DFF0-ish; find pixels matching pale blue
paleblue = (abs(r - 201) < 40) & (abs(g - 223) < 40) & (abs(b - 240) < 35) & (b - r > 20)
cc = comps_of(paleblue, 500)
cc.sort(key=lambda c: -c[4])
print("pale-blue components (container):")
for c in cc[:3]:
    print("   ", c, "center", ((c[0]+c[1])/2, (c[2]+c[3])/2))

# ---------- 2. dark blue bars ----------
darkblue = (b > 110) & (b - r > 60) & (b - g > 60) & (r < 110)
cc = comps_of(darkblue, 2000)
cc.sort(key=lambda c: -c[4])
print("dark-blue components (bars/text): top 10")
for c in cc[:10]:
    print("   ", c, "center", ((c[0]+c[1])/2, (c[2]+c[3])/2))

# ---------- 3. dark red bars/arrows ----------
darkred = (r > 110) & (r - g > 55) & (r - b > 55) & (g < 90)
cc = comps_of(darkred, 300)
cc.sort(key=lambda c: (c[2], c[0]))
print("dark-red components (arrows): top 30 by area")
for c in sorted(cc, key=lambda c: -c[4])[:30]:
    print("   ", c, "center", ((c[0]+c[1])/2, (c[2]+c[3])/2))
