#!/usr/bin/env python3
"""Systematic diagram-zone measurement for slide_016.jpg: every distinct fill
(q8, count>=250) gets a component map, printed with bbox + area + core mode color."""
import numpy as np
from PIL import Image
from collections import deque

IM = np.asarray(Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_016.jpg").convert("RGB")).astype(int)
H, W = IM.shape[:2]
X0, Y0, X1, Y1 = 560, 95, 925, 540   # diagram zone incl. green frame margin
zone = IM[Y0:Y1, X0:X1]
q = (zone // 8) * 8
flat = q.reshape(-1, 3)
colors, counts = np.unique(flat, axis=0, return_counts=True)
order = np.argsort(-counts)

def components(mask, min_area=100):
    lbl = np.zeros(mask.shape, dtype=bool)
    comps = []
    ys, xs = np.where(mask)
    coords = set(zip(ys.tolist(), xs.tolist()))
    seen = set()
    for start in coords:
        if start in seen:
            continue
        qq = deque([start]); seen.add(start); pix = []
        while qq:
            y, x = qq.popleft(); pix.append((y, x))
            for dy, dx in ((1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)):
                n = (y+dy, x+dx)
                if n in coords and n not in seen:
                    seen.add(n); qq.append(n)
        if len(pix) >= min_area:
            py = np.array([p[0] for p in pix]); px_ = np.array([p[1] for p in pix])
            comps.append((X0+px_.min(), Y0+py.min(), X0+px_.max(), Y0+py.max(), len(pix)))
    return comps

print("-- diagram-zone fills (q8 count>=250, comp min_area 100, top 6 comps each) --")
seen_colors = 0
for i in order:
    c = colors[i]; n = counts[i]
    if n < 250: break
    r8, g8, b8 = int(c[0]), int(c[1]), int(c[2])
    # skip near-white/gray panel/canvas
    if abs(r8-g8) < 16 and abs(g8-b8) < 16 and r8 > 200: continue
    mask = (q[:,:,0]==r8)&(q[:,:,1]==g8)&(q[:,:,2]==b8)
    comps = components(mask, 100)
    if not comps: continue
    seen_colors += 1
    print(f"\ncolor ({r8},{g8},{b8}) = #{r8:02X}{g8:02X}{b8:02X}  zone_n={n}")
    comps.sort(key=lambda t: -t[4])
    for x0, y0, x1, y1, a in comps[:6]:
        print(f"   x{x0}-{x1} y{y0}-{y1} (w{x1-x0+1} h{y1-y0+1}) n={a}")
print(f"\n{seen_colors} distinct non-neutral fills")
