from PIL import Image
import numpy as np
im = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_015.jpg').convert('RGB')).astype(int)
def hx(t): return '#%02X%02X%02X' % tuple(t)
print('TOP STRIPS zone x395..640, y62..175:')
print('      ' + ' '.join(f'{x:4d}' for x in range(395, 641, 15)))
for y in range(62, 176, 4):
    print(f'y={y:3d}: ' + ' '.join(hx(im[y,x]) for x in range(395, 641, 15)))
