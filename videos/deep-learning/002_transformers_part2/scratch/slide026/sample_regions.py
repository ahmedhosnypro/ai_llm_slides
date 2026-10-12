#!/usr/bin/env python3
"""Targeted sampling of slide_026 frame regions."""
from PIL import Image

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_026.jpg').convert('RGB')
W, H = im.size
px = im.load()

def s(name, x, y):
    print(f"{name} ({x},{y}): {px[x, y]}")

print("=== fills ===")
s('blue box', 300, 245)
s('blue box2', 240, 300)
s('subblock1', 290, 270)
s('subblock2', 290, 320)
s('subblock3', 290, 370)
s('host box', 403, 300)
s('host box2', 405, 350)
s('tida container', 500, 210)
s('tida container2', 440, 430)
s('encoder conn', 655, 300)
s('encoder conn2', 657, 350)
s('right panel inside', 710, 220)
s('right panel inside2', 750, 430)
s('diff box', 760, 260)
s('diff box2', 780, 250)
s('dual adc', 490, 260)
s('power supplies', 500, 435)
s('24v box', 425, 437)
s('motor body', 790, 350)
s('sincos enc box', 760, 462)
s('white box 16bit', 480, 230)
print("=== TIDA container fill scan x=430..600 y=200 ===")
for x in range(430, 601, 20):
    print(x, px[x, 200])
print("=== TIDA dashed border scan y=190..215 x=500 (top edge?) ===")
for y in range(188, 216):
    print(y, px[500, y])
