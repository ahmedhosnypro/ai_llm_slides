#!/usr/bin/env python3
# m13_resume.py — finer region forensics for 002:51 judge-1 findings (original only).
# Connected color-class blobs in frame-px regions, + render_4 comparison.
import sys
from collections import deque
from PIL import Image

ROOT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2"
orig = Image.open(f"{ROOT}/unique_slides/slide_051.jpg").convert("RGB")
r4 = Image.open(f"{ROOT}/recreated_pptx/qa/slide051/render_4.png").convert("RGB")
SX = lambda fx: (fx - 18.128) / 0.961235
SY = lambda fy: (fy + 0.045) / 0.956566
K = 150.0 / 72.0

def classify(r, g, b):
    if b > 100 and r < 90 and g < 90: return "navy"
    if g > 140 and g > r + 30 and g > b + 20: return "green"
    if r > 150 and g > 110 and b < 110 and r > b + 60: return "tan"
    if r > 130 and g < 90 and b < 90: return "red"
    if r < 90 and g < 90 and b < 90: return "dark"
    return None

def blobs(img, x0, y0, x1, y1, to_frame, min_px=6):
    """connected components over classified pixels; to_frame maps img px -> frame px"""
    W, H = x1 - x0, y1 - y0
    grid = [[None] * W for _ in range(H)]
    for j in range(H):
        for i in range(W):
            fx, fy = to_frame(x0 + i, y0 + j)
            r, g, b = img.getpixel((min(max(int(fx), 0), img.size[0] - 1), min(max(int(fy), 0), img.size[1] - 1)))
            grid[j][i] = classify(r, g, b)
    seen = [[False] * W for _ in range(H)]
    out = []
    for j in range(H):
        for i in range(W):
            if grid[j][i] and not seen[j][i]:
                c = grid[j][i]
                q = deque([(i, j)])
                seen[j][i] = True
                pts = []
                while q:
                    x, y = q.popleft()
                    pts.append((x, y))
                    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)):
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < W and 0 <= ny < H and not seen[ny][nx] and grid[ny][nx] == c:
                            seen[ny][nx] = True
                            q.append((nx, ny))
                if len(pts) >= min_px:
                    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
                    cx, cy = sum(xs) / len(xs), sum(ys) / len(ys)
                    fx0, fy0 = to_frame(x0 + min(xs), y0 + min(ys))
                    fx1, fy1 = to_frame(x0 + max(xs), y0 + max(ys))
                    out.append((c, len(pts), round(fx0), round(fy0), round(fx1), round(fy1),
                                round(to_frame(x0 + cx, y0 + cy)[0]), round(to_frame(x0 + cy * 0 + cx * 0 + (x0 + cx), y0 + cy)[1])))
    return sorted(out, key=lambda t: (t[1], ), reverse=True)

def orig2frame(x, y): return x, y
def r4_2frame(x, y): return x / K * 0.961235 + 18.128, y / K * 0.956566 - 0.045

for (name, x0, y0, x1, y1) in [
    ("A decoder-Nx", 770, 285, 895, 350),
    ("B decoder-PE", 770, 390, 895, 445),
    ("C encoder-PE", 130, 385, 215, 440),
    ("E enc-norm-box1", 205, 260, 285, 282),
]:
    print(f"=== {name} ORIGINAL (class, npx, fx0,fy0,fx1,fy1, ~center):")
    for t in blobs(orig, x0, y0, x1, y1, orig2frame)[:14]:
        print("   ", t)
    print(f"=== {name} RENDER_4:")
    for t in blobs(r4, int(SX(x0) * K), int(SY(y0) * K), int(SX(x1) * K), int(SY(y1) * K), r4_2frame)[:14]:
        print("   ", t)

# direct color samples in the decoder right-edge band (original), grid 5px
print("=== A grid samples ORIGINAL (x: 790..890 step 10, y: 290..345 step 5):")
hdr = "      " + "".join(f"x{x:<14}" for x in range(790, 891, 10))
print(hdr)
for y in range(290, 346, 5):
    row = f"y{y}: "
    for x in range(790, 891, 10):
        r, g, b = orig.getpixel((x, y))
        row += f"({r:3},{g:3},{b:3}) "
    print(row)
