from PIL import Image
import numpy as np
im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_026.jpg').convert('RGB')
a = np.asarray(im).astype(int)
dk = (a.sum(axis=2)<560)
print('rows 280..292, x460..570:')
for y in range(280,293):
    print(f'{y:4d} ' + ''.join('#' if dk[y,x] else '.' for x in range(460,571)))
