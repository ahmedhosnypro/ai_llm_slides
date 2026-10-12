#!/usr/bin/env python3
"""Part 3: zoom on the multiply-ring chain (read-only)."""
import numpy as np
from PIL import Image

VID = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2"
render = np.asarray(Image.open(f"{VID}/recreated_pptx/qa/slide008/render_2.png").convert("RGB")).astype(int)
frame = np.asarray(Image.open(f"{VID}/unique_slides/slide_008.jpg").convert("RGB")).astype(int)

def redmask(a):
    R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    return (R >= 140) & (G <= 120) & (B <= 120) & ((R - np.maximum(G, B)) >= 50)

mr, mf = redmask(render), redmask(frame)
RW, RH = render.shape[1], render.shape[0]
FH, FW = mf.shape

def components(mask, min_px=8):
    h, w = mask.shape
    seen = np.zeros_like(mask, dtype=bool)
    comps = []
    ys, xs = np.nonzero(mask)
    for start in zip(ys.tolist(), xs.tolist()):
        if seen[start]:
            continue
        stack = [start]; seen[start] = True; pix = []
        while stack:
            y, x = stack.pop(); pix.append((y, x))
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    ny, nx = y + dy, x + dx
                    if 0 <= ny < h and 0 <= nx < w and mask[ny, nx] and not seen[ny, nx]:
                        seen[ny, nx] = True; stack.append((ny, nx))
        if len(pix) >= min_px:
            py = [p[0] for p in pix]; px = [p[1] for p in pix]
            comps.append((min(px), min(py), max(px), max(py), len(pix)))
    return comps

print("=== FULL frame red components (frame 960-space coords) ===")
for x0, y0, x1, y1, n in sorted(components(mf, 6), key=lambda c: (c[1], c[0])):
    print(f"  frame({x0},{y0})-({x1},{y1}) npx={n} w={x1-x0+1} h={y1-y0+1}")

# High-res aligned maps of the ring-chain band: render x 980..1480, y 380..880
X0, X1, Y0, Y1 = 980, 1480, 380, 880
W, H = 100, 50
cw, ch = (X1 - X0) / W, (Y1 - Y0) / H
gr = np.zeros((H, W), dtype=int); gf = np.zeros((H, W), dtype=int)
ys, xs = np.nonzero(mr)
for yy, xx in zip(ys.tolist(), xs.tolist()):
    if X0 <= xx < X1 and Y0 <= yy < Y1:
        gr[int((yy - Y0) / ch), int((xx - X0) / cw)] += 1
fys, fxs = np.nonzero(mf)
sx = ((fxs - 17.628) / 0.961232) * (RW / 960.0)
sy = (fys / 0.955556) * (RH / 540.0)
for yy, xx in zip(sy.tolist(), sx.tolist()):
    if X0 <= xx < X1 and Y0 <= yy < Y1:
        gf[int((yy - Y0) / ch), int((xx - X0) / cw)] += 1

def sym(n):
    return " " if n == 0 else ("." if n < 5 else ("+" if n < 20 else ("*" if n < 60 else "#")))

print(f"\n=== Ring-chain zoom: render x {X0}..{X1}, y {Y0}..{Y1} (LEFT=render, RIGHT=frame mapped) ===")
print("      " + "".join(str((X0 + int(i * cw)) // 100 % 10) for i in range(0, W, 5)))
for i in range(H):
    print(f"y{Y0 + int(i * ch):4d} {''.join(sym(n) for n in gr[i])} | {''.join(sym(n) for n in gf[i])}")
