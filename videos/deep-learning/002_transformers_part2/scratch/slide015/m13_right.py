from PIL import Image
import numpy as np
im = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_015.jpg').convert('RGB')).astype(int)
def hx(t): return '#%02X%02X%02X' % tuple(t)
print('CHILD right zone x580..680, y215..425 (fine grid):')
print('      ' + ' '.join(f'{x:4d}' for x in range(580, 681, 10)))
for y in range(215, 426, 10):
    print(f'y={y}: ' + ' '.join(hx(im[y,x]) for x in range(580, 681, 10)))
