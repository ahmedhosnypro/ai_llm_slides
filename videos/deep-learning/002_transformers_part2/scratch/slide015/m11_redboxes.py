from PIL import Image
import numpy as np
from scipy import ndimage
im = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_015.jpg').convert('RGB')).astype(int)
# tight bright-red mask (CC0000-like), excluding panel border rows/cols
m = (im[:,:,0]>165) & (im[:,:,1]<90) & (im[:,:,2]<90)
m[:50,:] = False; m[510:,:] = False; m[:, :75] = False; m[:, 900:] = False
lab, n = ndimage.label(m)
print('tight-red components >80px:')
for i, sl in enumerate(ndimage.find_objects(lab)):
    npx = (lab[sl]==i+1).sum()
    if npx >= 80:
        print(f'  x {sl[1].start:4d}..{sl[1].stop:4d}  y {sl[0].start:4d}..{sl[0].stop:4d}  n={npx}')
