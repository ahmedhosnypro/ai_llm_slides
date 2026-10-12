#!/usr/bin/env python3
"""Refined chrome landmark measurement for slide_049.jpg."""
from PIL import Image
import numpy as np

F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_049.jpg"
im = Image.open(F).convert("RGB")
a = np.asarray(im).astype(int)
H, W = a.shape[:2]
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]

# wider red mask (JPEG-darkened border core ~(114,41,48))
red = (r > 90) & (r - g > 45) & (r - b > 45)
colcount = red.sum(axis=0)
rowcount = red.sum(axis=1)

def clusters(vals, gap=3):
    out = []; cur = [vals[0]]
    for v in vals[1:]:
        if v - cur[-1] <= gap: cur.append(v)
        else: out.append(cur); cur = [v]
    out.append(cur); return out

tall = np.where(colcount > 150)[0]
cl = clusters(tall) if len(tall) else []
print("tall red col clusters:", [(c[0], c[-1], int(colcount[c].max())) for c in cl][:14])
wide = np.where(rowcount > 250)[0]
rw = clusters(wide) if len(wide) else []
print("wide red row clusters:", [(c[0], c[-1], int(rowcount[c].max())) for c in rw][:14])

# yellow mask clusters (badge + any pastel-yellow slots)
yellow = (r > 200) & (g > 200) & (b < 195) & (abs(r - g) < 45) & (r - b > 15)
ys, xs = np.where(yellow)
lab = np.zeros((H, W), bool)
from collections import deque
seen = np.zeros((H, W), bool)
comps = []
ys_idx = np.where(yellow)
for y0, x0 in zip(ys_idx[0][::7], ys_idx[1][::7]):
    if seen[y0, x0]: continue
    q = deque([(y0, x0)]); seen[y0, x0] = True
    xmn = xmx = x0; ymn = ymx = y0; n = 0
    while q:
        y, x = q.popleft(); n += 1
        xmn = min(xmn, x); xmx = max(xmx, x); ymn = min(ymn, y); ymx = max(ymy := ymx, y) if False else max(ymx, y)
        for dy, dx in ((1,0),(-1,0),(0,1),(0,-1)):
            ny, nx = y+dy, x+dx
            if 0 <= ny < H and 0 <= nx < W and yellow[ny, nx] and not seen[ny, nx]:
                seen[ny, nx] = True; q.append((ny, nx))
    if n > 40:
        comps.append((xmn, xmx, ymn, ymx, n))
comps.sort(key=lambda c: -c[4])
print("yellow components (x0,x1,y0,y1,npx) top 8:")
for c in comps[:8]:
    print("   ", c, "center", ((c[0]+c[1])/2, (c[2]+c[3])/2))
