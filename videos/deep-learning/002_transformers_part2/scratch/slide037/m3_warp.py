#!/usr/bin/env python3
"""Warp slide_037.jpg (0.958-scale capture) into true slide space 960x540 (1px=1pt)
using the four-chrome-landmark affine fit:
  frame_x = 17.101 + 0.962329 * slide_x
  frame_y = -0.224 + 0.960526 * slide_y
"""
from PIL import Image

SRC = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_037.jpg"
A = 17.101; SX = 0.962329
B = -0.224; SY = 0.960526

img = Image.open(SRC).convert("RGB")
# inverse map: for each slide-space pixel, sample the frame (bilinear)
out = Image.new("RGB", (960, 540), (255, 255, 255))
sp = img.load()
op = out.load()
for sy in range(540):
    fy = B + SY * sy
    y0 = int(fy // 1); fyf = fy - y0
    for sx in range(960):
        fx = A + SX * sx
        x0 = int(fx // 1); fxf = fx - x0
        if 0 <= x0 < 959 and 0 <= y0 < 539:
            p00 = sp[x0, y0]; p10 = sp[x0+1, y0]; p01 = sp[x0, y0+1]; p11 = sp[x0+1, y0+1]
            op[sx, sy] = tuple(int(p00[c]*(1-fxf)*(1-fyf) + p10[c]*fxf*(1-fyf) + p01[c]*(1-fxf)*fyf + p11[c]*fxf*fyf) for c in range(3))
        elif 0 <= x0 < 960 and 0 <= y0 < 540:
            op[sx, sy] = sp[x0, y0]
out.save("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide037/slide037_slide_space.png")
print("wrote slide037_slide_space.png")
