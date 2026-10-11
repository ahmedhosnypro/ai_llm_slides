#!/usr/bin/env python3
"""Precision pass m07: VKQ circles, yellow highlight, red dashes, exact box bounds."""
import numpy as np
from PIL import Image
from collections import deque

IM = np.asarray(Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_016.jpg").convert("RGB")).astype(int)
H, W = IM.shape[:2]
r, g, b = IM[:,:,0], IM[:,:,1], IM[:,:,2]

def comps(mask, min_area=25):
    coords = set(zip(*np.where(mask)))
    seen, out = set(), []
    for start in coords:
        if start in seen: continue
        qq = deque([start]); seen.add(start); pix = []
        while qq:
            y, x = qq.popleft(); pix.append((y, x))
            for dy in (-1,0,1):
                for dx in (-1,0,1):
                    n = (y+dy, x+dx)
                    if n in coords and n not in seen:
                        seen.add(n); qq.append(n)
        if len(pix) >= min_area:
            py = np.array([p[0] for p in pix]); px = np.array([p[1] for p in pix])
            out.append((int(px.min()), int(py.min()), int(px.max()), int(py.max()), len(pix)))
    return out

def show(name, cs):
    print(f"\n-- {name} --")
    for x0, y0, x1, y1, n in sorted(cs, key=lambda t: (t[1], t[0])):
        print(f"   x{x0}-{x1} y{y0}-{y1} (w{x1-x0+1} h{y1-y0+1}) n={n}")

# 1. blue circles (V/K): dark blue cores
blue = (b > r + 40) & (b > g + 40) & (b > 110) & (r < 140)
show("BLUE (V/K circles)", comps(blue, 25))
# 2. strong red (Q circles, arrows, dashes)
red = (r > 150) & (g < 90) & (b < 90)
show("RED (all)", comps(red, 20))
# 3. strong yellow (highlight + callout4)
yel = (r > 235) & (g > 235) & (b < 130)
show("YELLOW strong", comps(yel, 30))
# 4. olive decoder container
olive = (abs(r-181) < 22) & (abs(g-184) < 22) & (abs(b-141) < 22)
show("OLIVE B5B88D", comps(olive, 60))
# 5. tan container
tan = (abs(r-205) < 16) & (abs(g-170) < 16) & (abs(b-134) < 18)
show("TAN CCA884", comps(tan, 80))
# 6. dark-green masked box? (72,120,84)
dg = (abs(r-72) < 25) & (abs(g-120) < 25) & (abs(b-84) < 25)
show("DARKGREEN 487854", comps(dg, 40))
# 7. light-green fill C5F6D9 (dec lower container)
lg = (abs(r-197) < 10) & (abs(g-246) < 9) & (abs(b-217) < 9)
show("LTGREEN C5F6D9", comps(lg, 60))
# 8. red arrow at enc bottom + dec top (thick) — from RED list above
# 9. panel green CEFFE1 vs lower C5F6D9 done.
# 10. white-ish box in enc embed region
wh = (r > 244) & (g > 244) & (b > 240) & (abs(r-g) < 8)
show("WHITE-ish", comps(wh & (np.arange(W)[None,:] > 560) & (np.arange(W)[None,:] < 920) & (np.arange(H)[:,None] > 100) & (np.arange(H)[:,None] < 525), 80))
# 11. maroon/brown fills
br = (abs(r-176) < 25) & (abs(g-128) < 25) & (abs(b-88) < 25)
show("BROWN B08058", comps(br, 50))
