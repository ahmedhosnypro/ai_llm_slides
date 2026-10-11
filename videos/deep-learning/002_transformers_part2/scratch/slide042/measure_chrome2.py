#!/usr/bin/env python3
"""Chrome landmark fit v2 for slide_042.jpg (960x540).
Fits frame->slide mapping from the four chrome border landmarks
(panel left/right/top/bottom red strokes) using relaxed red threshold."""
from PIL import Image
import numpy as np

F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_042.jpg"
im = Image.open(F).convert("RGB")
W, H = im.size
a = np.asarray(im).astype(int)
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]

red = (r > 130) & (r - g > 60) & (r - b > 60)
colcount = red.sum(axis=0)
rowcount = red.sum(axis=1)
print("columns with red count > 150:", [x for x in range(W) if colcount[x] > 150])
print("rows with red count > 300:", [y for y in range(H) if rowcount[y] > 300])

# vertical border columns: look at x<100 and x>820, red frac over y 150..450 (content band)
band = red[150:450, :]
colfrac = band.mean(axis=0)
lcols = [x for x in range(0, 150) if colfrac[x] > 0.4]
rcols = [x for x in range(W - 150, W) if colfrac[x] > 0.4]
print("left border cols (frac>0.4 in y150..450):", lcols)
print("right border cols:", rcols)

# horizontal: top border row over x 200..800; bottom stroke near y 515..540
mid = red[:, 200:800]
rowfrac = mid.mean(axis=1)
trows = [y for y in range(0, 150) if rowfrac[y] > 0.4]
brows = [y for y in range(480, H) if rowfrac[y] > 0.4]
print("top border rows (frac>0.4, x200..800):", trows)
print("bottom stroke rows (frac>0.4):", brows)
print("rowfrac 505..540:", [(y, round(rowfrac[y], 3)) for y in range(505, H)])

# letterbox: find black rows
black = (r < 60) & (g < 60) & (b < 60)
blkfrac = black[:, 100:800].mean(axis=1)
print("black rows frac>0.8:", [y for y in range(H) if blkfrac[y] > 0.8][:5], "...",
      [y for y in range(H) if blkfrac[y] > 0.8][-5:])

# Fit mapping: slide-space chrome = panel x 42..918 (border strokes at 42 and 918),
# top border row 45, bottom stroke rows 538-539 (bottom edge 539.5).
# frame landmarks: L, R, T, B (centers of detected strokes).
# Fit sx, ax: frame_x = ax + sx * slide_x  (2 pts); sy, ay: frame_y = ay + sy * slide_y (2 pts)
