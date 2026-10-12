from PIL import Image
import numpy as np
f45 = np.asarray(Image.open('videos/deep-learning/002_transformers_part2/unique_slides/slide_045.jpg').convert('RGB')).astype(int)
# top row: slide y 175..192.5 -> frame 167.2..184.0 ; center 175.6
for y in (170, 176, 180):
    print(f'045 frame y={y}:', [tuple(f45[y,x]) for x in range(180, 232, 3)])
# vertical run at x=187 (seg1 center), y 160..190
print('045 frame x=187 y-run:', [(y, tuple(f45[y,187])) for y in range(162, 190, 2)])
