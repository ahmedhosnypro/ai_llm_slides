#!/usr/bin/env python3
"""Diff base_960.png (imported 001:19 composition) vs slide037_slide_space.png.
Reports connected diff regions (threshold-gated) with bboxes."""
from PIL import Image
import json, sys

base = Image.open("base_960.png").convert("RGB")
mine = Image.open("slide037_slide_space.png").convert("RGB")
W, H = base.size
pb, pm = base.load(), mine.load()

TH = 60  # per-channel mean distance threshold
diff = [[0]*W for _ in range(H)]
for y in range(H):
    for x in range(W):
        a, b = pb[x, y], pm[x, y]
        d = (abs(a[0]-b[0]) + abs(a[1]-b[1]) + abs(a[2]-b[2])) / 3
        if d > TH:
            diff[y][x] = 1

# connected components (4-neighborhood, iterative)
seen = [[False]*W for _ in range(H)]
comps = []
for y in range(H):
    for x in range(W):
        if diff[y][x] and not seen[y][x]:
            stack = [(x, y)]
            seen[y][x] = True
            x0=x1=x; y0=y1=y; n=0
            while stack:
                cx, cy = stack.pop()
                n += 1
                if cx<x0: x0=cx
                if cx>x1: x1=cx
                if cy<y0: y0=cy
                if cy>y1: y1=cy
                for nx, ny in ((cx+1,cy),(cx-1,cy),(cx,cy+1),(cx,cy-1)):
                    if 0<=nx<W and 0<=ny<H and diff[ny][nx] and not seen[ny][nx]:
                        seen[ny][nx]=True
                        stack.append((nx,ny))
            comps.append({"bbox":[x0,y0,x1,y1],"px":n})
comps.sort(key=lambda c:-c["px"])
big = [c for c in comps if c["px"] >= 40]
small = [c for c in comps if 15 <= c["px"] < 40]
print(json.dumps({"total_diff_px": sum(c["px"] for c in comps),
                  "n_comps": len(comps),
                  "big_regions": big, "small_regions": small}, indent=0))
# also save a diff visualization
vis = Image.new("RGB", (W, H), (255,255,255))
vp = vis.load()
for y in range(H):
    for x in range(W):
        if diff[y][x]:
            vp[x,y] = (255,0,255)
vis.save("diff_vis.png")
