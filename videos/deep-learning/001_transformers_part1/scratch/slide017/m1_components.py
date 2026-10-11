#!/usr/bin/env python3
"""Measure slide_017.jpg: fixed flood-fill components for chrome + callouts + diagram shell."""
import numpy as np
from PIL import Image
from collections import deque

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_017.jpg').convert('RGB')
A = np.asarray(im).astype(int)
H, W, _ = A.shape
print(f"size {W}x{H}")

def close(target, tol):
    return np.abs(A - np.array(target)).sum(axis=2) <= tol

def components(mask, min_px=20):
    lab = np.zeros((H, W), dtype=bool)
    comps = []
    ys_all, xs_all = np.nonzero(mask)
    seen = np.zeros((H, W), dtype=bool)
    for (y, x) in zip(ys_all, xs_all):
        if seen[y, x]:
            continue
        q = deque([(y, x)])
        seen[y, x] = True
        pts = []
        while q:
            cy, cx = q.popleft()
            pts.append((cy, cx))
            for dy, dx in ((1,0),(-1,0),(0,1),(0,-1)):
                ny, nx = cy+dy, cx+dx
                if 0 <= ny < H and 0 <= nx < W and mask[ny, nx] and not seen[ny, nx]:
                    seen[ny, nx] = True
                    q.append((ny, nx))
        if len(pts) >= min_px:
            pts = np.array(pts)
            comps.append((len(pts), pts[:,1].min(), pts[:,0].min(), pts[:,1].max(), pts[:,0].max()))
    return comps

def report(name, target, tol, min_px=20, region=None, max_show=40):
    m = close(target, tol)
    if region:
        x0, y0, x1, y1 = region
        mm = np.zeros_like(m)
        mm[y0:y1+1, x0:x1+1] = m[y0:y1+1, x0:x1+1]
        m = mm
    comps = components(m, min_px)
    comps.sort(key=lambda c: (-c[0]))
    print(f"== {name} target{target} tol{tol}: {len(comps)} comps (showing {min(len(comps), max_show)})")
    for n, x0, y0, x1, y1 in comps[:max_show]:
        print(f"   n={n:7d} x{x0}..{x1} y{y0}..{y1}  w={x1-x0+1} h={y1-y0+1}")

# callout boxes (measured avg colors)
report("yellow_callout", (242, 245, 160), 60, 300, region=(0, 60, 580, 540))
report("pink_callout", (244, 179, 245), 60, 300, region=(0, 60, 580, 540))
report("tan_callout3", (212, 196, 178), 40, 300, region=(0, 300, 580, 460))
report("tan_callout4", (212, 196, 178), 40, 300, region=(0, 460, 580, 540))
# title red text
report("title_red", (170, 30, 40), 160, 20, region=(100, 20, 850, 100))
# green frame border (00B050 = 0,176,80)
report("green_frame", (0, 176, 80), 130, 15, region=(560, 60, 960, 540), max_show=10)
# encoder panel fill FBE5D6=(251,229,214)
report("enc_panel", (251, 229, 214), 40, 500, region=(560, 60, 960, 540), max_show=6)
# decoder panel fill D8F0D8=(216,240,216)
report("dec_panel", (216, 240, 216), 40, 500, region=(560, 60, 960, 540), max_show=6)
