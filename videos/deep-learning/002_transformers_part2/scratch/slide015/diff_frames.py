from PIL import Image, ImageChops
import numpy as np

child = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_015.jpg').convert('RGB')).astype(int)
par   = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_043.jpg').convert('RGB')).astype(int)
d = np.abs(child - par).sum(axis=2)
mask = d > 90  # significant channel-sum difference
print('diff pixels:', mask.sum(), 'of', mask.size)

# connected regions via simple projection profiling on a grid
from scipy import ndimage
lab, n = ndimage.label(mask)
print('regions:', n)
objs = ndimage.find_objects(lab)
sizes = ndimage.sum(mask, lab, range(1, n+1))
order = np.argsort(sizes)[::-1]
for i in order[:25]:
    if sizes[i] < 40: break
    sl = objs[i]
    print(f'region size={int(sizes[i]):6d}  x {sl[1].start:4d}..{sl[1].stop:4d}  y {sl[0].start:4d}..{sl[0].stop:4d}')
