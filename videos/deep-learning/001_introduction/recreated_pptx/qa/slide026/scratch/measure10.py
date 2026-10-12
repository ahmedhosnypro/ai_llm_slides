from PIL import Image
import numpy as np
from collections import Counter
im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_026.jpg').convert('RGB')
a = np.asarray(im).astype(int)
R = a[:,:,0]; G = a[:,:,1]; B = a[:,:,2]
redm  = (R-G>50)&(R-B>50)&(R>120)
bluem = (B-R>40)&(B-G>30)&(B>110)
dkm = (a.sum(axis=2)<330)

# red rule rows 25..58
for y in range(28,60):
    xr = np.where(redm[y])[0]
    if len(xr)>5: print('rule y',y,'x',xr.min(),xr.max(),'n',len(xr))
# what is at x58, rows 45..58?
for y in range(43,60):
    print('x56-62 y',y, a[y,56:63].tolist())
