#!/usr/bin/env python3
"""Read-only corroboration scan for the attempt-3 re-judge claims (slide 008 restoration).

Claim 1 (BLOCKER): red connector segments softmax->(x) nodes and vertical toward Sigma
                   exist in the ORIGINAL frame but are absent from the recreation.
Claim 3 (MAJOR):   the red block arrow under X2 reaches/crosses "the bottom red
                   house-frame line (~y 7.35in)" in the recreation.
Claim 2 (MAJOR):   recreation's multiply circles are ~2-3x larger than the original's.

Pure PIL/numpy, reads only the two images; prints measurements. Writes nothing.
"""
import numpy as np
from PIL import Image

VID = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2"
render = np.asarray(Image.open(f"{VID}/recreated_pptx/qa/slide008/render_2.png").convert("RGB")).astype(int)
frame = np.asarray(Image.open(f"{VID}/unique_slides/slide_008.jpg").convert("RGB")).astype(int)
print(f"render {render.shape[1]}x{render.shape[0]}  frame {frame.shape[1]}x{frame.shape[0]}")

def redmask(a):
    R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    return (R >= 140) & (G <= 120) & (B <= 120) & ((R - np.maximum(G, B)) >= 50)

def components(mask, min_px=8):
    """BFS label connected red components; return list of (x0,y0,x1,y1,npx)."""
    h, w = mask.shape
    seen = np.zeros_like(mask, dtype=bool)
    comps = []
    ys, xs = np.nonzero(mask)
    coords = set(zip(ys.tolist(), xs.tolist()))
    for start in list(coords):
        if seen[start]:
            continue
        stack = [start]
        seen[start] = True
        pix = []
        while stack:
            y, x = stack.pop()
            pix.append((y, x))
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    ny, nx = y + dy, x + dx
                    if 0 <= ny < h and 0 <= nx < w and mask[ny, nx] and not seen[ny, nx]:
                        seen[ny, nx] = True
                        stack.append((ny, nx))
        if len(pix) >= min_px:
            py = [p[0] for p in pix]; px = [p[1] for p in pix]
            comps.append((min(px), min(py), max(px), max(py), len(pix)))
    return comps

# frame->render mapping (certified fit from build/slide_008.js header):
#   frame_x = 17.628 + 0.961232*slide_x ; frame_y = 0.955556*slide_y
# render px = slide px * (W/960, H/540) at 150dpi
FW, FH = frame.shape[1], frame.shape[0]
RW, RH = render.shape[1], render.shape[0]
SX, SY = FW / 960.0, FH / 540.0  # if frame is not exactly 960x540

def f2r(fx, fy):
    sx = (fx / SX - 17.628) / 0.961232
    sy = (fy / SY) / 0.955556
    return sx * RW / 960.0, sy * RH / 540.0

mr = redmask(render)
mf = redmask(frame)
print(f"red px: render {mr.sum()}  frame {mf.sum()}")

# ---------- Claim 3: bottom region of the render ----------
print("\n=== CLAIM 3: render bottom region (rows 1040..end) ===")
for y in range(1040, RH):
    cnt = int(mr[y, 100:1900].sum())
    if cnt:
        xs = np.nonzero(mr[y, 100:1900])[0] + 100
        print(f"row {y} ({y/150:.3f}in): red px={cnt} x-span {xs.min()}..{xs.max()}")
print("(rows with no output have zero red px in x 100..1900)")

# red horizontal lines anywhere near bottom (frame chrome?)
print("\nrender rows 1000..end with >400 red px (candidate lines):")
for y in range(1000, RH):
    cnt = int(mr[y].sum())
    if cnt > 400:
        print(f"  row {y}: {cnt}")

# ---------- Claims 1 & 2: red components in the multiply/softmax band ----------
print("\n=== CLAIMS 1+2: red components (>=30 px), render space ===")
print("-- render components (x0,y0,x1,y1,npx,w,h):")
cr = sorted(components(mr, 30), key=lambda c: (c[1], c[0]))
for c in cr:
    x0, y0, x1, y1, n = c
    print(f"   ({x0},{y0})-({x1},{y1}) npx={n} w={x1-x0+1} h={y1-y0+1}")
print("-- frame components mapped into render coords:")
cf = sorted(components(mf, 12), key=lambda c: (c[1], c[0]))
for x0, y0, x1, y1, n in cf:
    rx0, ry0 = f2r(x0, y0); rx1, ry1 = f2r(x1, y1)
    print(f"   frame({x0},{y0})-({x1},{y1}) npx={n} -> render ({rx0:.0f},{ry0:.0f})-({rx1:.0f},{ry1:.0f}) w={rx1-rx0:.0f} h={ry1-ry0:.0f}")
