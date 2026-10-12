from PIL import Image
import numpy as np
from collections import Counter
im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_026.jpg').convert('RGB')
a = np.asarray(im).astype(int)
# rows 40..48 sample at x=300,500,700 and column extents
for y in range(40,50):
    print('y',y, 'x300',a[y,300].tolist(),'x500',a[y,500].tolist(),'x700',a[y,700].tolist(),'x905',a[y,905].tolist())
# red mask row profile rows 38..50
R = a[:,:,0]; G = a[:,:,1]; B = a[:,:,2]
redm  = (R-G>50)&(R-B>50)&(R>120)
for y in range(36,52):
    xr = np.where(redm[y])[0]
    print('red y',y,'n',len(xr), (xr.min(),xr.max()) if len(xr) else '')
# gray panel edges precise: cols 36..50 and 914..926 at y=300
print('left edge y300:', [(x, a[300,x].tolist()) for x in range(36,52)])
print('right edge y300:', [(x, a[300,x].tolist()) for x in range(912,926)])
print('top edge x500:', [(y, a[y,500].tolist()) for y in range(40,52)])
print('bottom edge x500:', [(y, a[y,500].tolist()) for y in range(512,540)])
