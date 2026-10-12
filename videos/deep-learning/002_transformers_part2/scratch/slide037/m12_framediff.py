#!/usr/bin/env python3
"""Frame-vs-frame diff: my warped frame vs 001's slide_019.jpg (slide space)."""
from PIL import Image
import json

base = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_019.jpg").convert("RGB")
mine = Image.open("slide037_slide_space.png").convert("RGB")
W, H = base.size
pb, pm = base.load(), mine.load()
TH = 60
diff = [[0]*W for _ in range(H)]
for y in range(H):
    for x in range(W):
        a, b = pb[x, y], pm[x, y]
        if (abs(a[0]-b[0]) + abs(a[1]-b[1]) + abs(a[2]-b[2])) / 3 > TH:
            diff[y][x] = 1
seen = [[False]*W for _ in range(H)]
comps = []
for y in range(H):
    for x in range(W):
        if diff[y][x] and not seen[y][x]:
            stack = [(x, y)]; seen[y][x] = True
            x0=x1=x; y0=y1=y; n=0
            while stack:
                cx, cy = stack.pop(); n += 1
                x0=min(x0,cx); x1=max(x1,cx); y0=min(y0,cy); y1=max(y1,cy)
                for nx, ny in ((cx+1,cy),(cx-1,cy),(cx,cy+1),(cx,cy-1)):
                    if 0<=nx<W and 0<=ny<H and diff[ny][nx] and not seen[ny][nx]:
                        seen[ny][nx]=True; stack.append((nx,ny))
            comps.append({"bbox":[x0,y0,x1,y1],"px":n})
comps.sort(key=lambda c:-c["px"])
print(json.dumps({"total": sum(c["px"] for c in comps), "n": len(comps),
                  "regions": [c for c in comps if c["px"]>=60]}, indent=0))
vis = Image.new("RGB", (W,H), (255,255,255))
vp = vis.load()
for y in range(H):
    for x in range(W):
        if diff[y][x]: vp[x,y]=(255,0,255)
vis.save("diff_frames_vis.png")
