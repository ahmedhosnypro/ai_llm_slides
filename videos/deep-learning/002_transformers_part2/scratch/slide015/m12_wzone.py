from PIL import Image
import numpy as np
im = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_015.jpg').convert('RGB')).astype(int)
par = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_043.jpg').convert('RGB')).astype(int)
def hx(t): return '#%02X%02X%02X' % tuple(t)
print('CHILD zone x560..700 y340..440, 10px grid:')
for y in range(340, 441, 10):
    print(f'  y={y}: ' + ' '.join(hx(im[y,x]) for x in range(560, 701, 10)))
print()
print('PARENT wochips zone model-mapped (child x642..812 y267..434):')
for y in range(340, 441, 20):
    px_par = [int((x-54.3)/0.954) for x in range(560, 701, 20)]
    py_par = int((y+86.1)/0.960)
    print(f'  child y={y} (par y={py_par}): ' + ' '.join(hx(par[py_par, px]) for px in px_par))
