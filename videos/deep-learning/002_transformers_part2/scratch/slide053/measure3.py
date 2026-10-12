#!/usr/bin/env python3
"""Measure ALL content ink regions of slide_053.jpg, zone by zone, per color mask.
Outputs frame-px bboxes; mapping to slide pts:
  slide_x = (frame_x - 18.45)/0.95991 ; slide_y = (frame_y + 0.29)/0.95600
"""
from PIL import Image
import numpy as np

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_053.jpg').convert('RGB')
a = np.asarray(im).astype(int)
H, W, _ = a.shape
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]

def sxy(fx, fy):
    sx = (np.asarray(fx) - 18.45) / 0.95991
    sy = (np.asarray(fy) + 0.29) / 0.95600
    return sx, sy

masks = {
    'red':   (r - (g + b) / 2 > 55),
    'blue':  (b - (r + g) / 2 > 55),
    'green': (g > r + 6) & (g > b + 6) & (g > 195) & (r > 150),
    'mauve': (r > 140) & (r < 230) & (g > 90) & (g < 190) & (b > 90) & (b < 190) & (r > g + 15) & (r > b + 15),
    'yellow': (r > 228) & (g > 228) & (b > 150) & (b < 220),
    'dark':  (r < 100) & (g < 100) & (b < 100),
}

def bbox(mask, x0, y0, x1, y1, label):
    z = np.zeros_like(mask); z[y0:y1, x0:x1] = True
    m = mask & z
    ys, xs = np.where(m)
    if len(xs) == 0:
        print(f'{label}: EMPTY')
        return None
    bx0, bx1, by0, by1 = xs.min(), xs.max(), ys.min(), ys.max()
    sx0, sx1 = sxy(bx0, bx1); sy0, sy1 = sxy(by0, by1)
    print(f'{label}: frame x {bx0}..{bx1} y {by0}..{by1}  n={len(xs)}  -> slide x {sx0:.1f}..{sx1:.1f} y {sy0:.1f}..{sy1:.1f}')
    return (bx0, bx1, by0, by1)

print('=== TITLE L1 (red, top band) ===')
bbox(masks['red'], 200, 52, 760, 92, 'L1 red ink')
print('=== SUBTITLE L2 (red+blue, band y 92..135) ===')
bbox(masks['red'], 200, 92, 760, 135, 'L2 red ink')
bbox(masks['blue'], 200, 92, 760, 135, 'L2 blue ink')
print('=== SOFTMAX LABEL (red, top-right) ===')
bbox(masks['red'], 700, 92, 930, 135, 'Softmax label')
print('=== EQUATION BOX ZONE (dark/black border + ink, top-right y 110..200) ===')
bbox(masks['dark'], 700, 110, 930, 210, 'eq box dark ink')
print('=== DIAGRAM CONTAINER (blue border, center) ===')
bbox(masks['blue'], 300, 100, 740, 420, 'container blue')
print('=== ROW CHIPS (green, left of matrix) ===')
bbox(masks['green'], 320, 130, 460, 420, 'row chips green zone')
print('=== COLUMN TAGS (green, above matrix) ===')
bbox(masks['green'], 440, 110, 740, 220, 'col tags green zone')
print('=== MATRIX ZONE (red border) ===')
bbox(masks['red'], 430, 180, 720, 420, 'matrix red border')
print('=== MATRIX GREEN FILL ===')
bbox(masks['green'], 440, 180, 720, 420, 'matrix green fill')
print('=== MATRIX MAUVE FILL ===')
bbox(masks['mauve'], 440, 180, 720, 420, 'matrix mauve fill')
print('=== MATRIX YELLOW CHIPS ===')
bbox(masks['yellow'], 440, 180, 720, 420, 'matrix chips')
print('=== ARROW (blue, left of container) ===')
bbox(masks['blue'], 280, 240, 360, 340, 'arrow blue')
print('=== STATEMENT BOX (blue border + text, bottom band y 405..465) ===')
bbox(masks['blue'], 40, 405, 920, 465, 'statement box blue')
print('=== EXPLANATORY LINES (band y 460..510) ===')
bbox(masks['red'], 40, 460, 920, 510, 'expl red ink')
bbox(masks['dark'], 40, 460, 920, 510, 'expl dark ink')
print('=== color samples ===')
print('title red core:', a[70, 350], a[70, 400])
print('subtitle blue core:', a[108, 500], a[110, 520])
print('container blue border:', a[115, 520])
print('green chip fill:', a[160, 380])
print('mauve fill:', a[220, 660], a[230, 670])
print('green fill lower tri:', a[350, 480])
print('yellow chip fill:', a[250, 500])
