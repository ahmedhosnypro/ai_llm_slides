from PIL import Image
import numpy as np
from scipy import ndimage
for tag, p in [('CHILD','/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_015.jpg'),
               ('PARENT','/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_043.jpg')]:
    im = np.asarray(Image.open(p).convert('RGB')).astype(int)
    dark = (im.sum(axis=2) < 150)
    lab, n = ndimage.label(dark)
    tags = []
    for i, sl in enumerate(ndimage.find_objects(lab)):
        w_ = sl[1].stop-sl[1].start; h_ = sl[0].stop-sl[0].start
        npx = (lab[sl]==i+1).sum()
        if 24 <= w_ <= 40 and 11 <= h_ <= 20 and npx > 200 and npx/(w_*h_) > 0.6:
            tags.append(((sl[1].start+sl[1].stop)//2, (sl[0].start+sl[0].stop)//2, w_, h_))
    tags.sort()
    print(tag, 'tag centers:', [(c[0],c[1]) for c in tags])
