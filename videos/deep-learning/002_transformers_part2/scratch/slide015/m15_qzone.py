from PIL import Image
import numpy as np
im = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_015.jpg').convert('RGB')).astype(int)
def hx(t): return '#%02X%02X%02X' % tuple(t)
print('QUERY zone fine grid x250..355, y332..392 (2px steps -> 5px shown):')
print('      ' + ' '.join(f'{x:4d}' for x in range(250, 356, 5)))
for y in range(332, 393, 3):
    print(f'y={y:3d}: ' + ' '.join(hx(im[y,x]) for x in range(250, 356, 5)))
