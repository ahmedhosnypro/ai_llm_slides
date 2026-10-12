from PIL import Image
import numpy as np
im = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_015.jpg').convert('RGB')).astype(int)
par = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_043.jpg').convert('RGB')).astype(int)

def hexc(t): return '#%02X%02X%02X' % tuple(t)

print('CHILD left-interior grid (x 105..245, y 205..355) — 8 cols x 6 rows')
for y in range(205, 356, 30):
    row = []
    for x in range(105, 246, 20):
        row.append(hexc(im[y, x]))
    print(f'  y={y}: ' + ' '.join(row))

print('PARENT same logical area (x 65..205, y 303..453)')
for y in range(303, 454, 30):
    row = []
    for x in range(65, 206, 20):
        row.append(hexc(par[y, x]))
    print(f'  y={y}: ' + ' '.join(row))

print('CHILD right-interior grid (x 400..620, y 205..355)')
for y in range(205, 356, 30):
    row = []
    for x in range(400, 621, 20):
        row.append(hexc(im[y, x]))
    print(f'  y={y}: ' + ' '.join(row))

print('PARENT right-interior grid (x 360..580, y 303..453)')
for y in range(303, 454, 30):
    row = []
    for x in range(360, 581, 20):
        row.append(hexc(par[y, x]))
    print(f'  y={y}: ' + ' '.join(row))
