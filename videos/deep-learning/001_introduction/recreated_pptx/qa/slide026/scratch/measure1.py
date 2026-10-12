from PIL import Image
import numpy as np
im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_026.jpg').convert('RGB')
a = np.asarray(im).astype(int)
H, W = a.shape[:2]
print('size', W, H)
# corner + canvas samples
for (x,y) in [(5,5),(10,10),(950,5),(5,270),(479,5),(200,300),(480,500)]:
    print('px',x,y,a[y,x])
# row profile: for each row, count of non-white-ish and distinct colors
def rowinfo(y):
    row = a[y]
    nonwhite = np.abs(row - 255).sum(axis=1) > 90
    return nonwhite.sum()
# scan for the red rule near top
for y in range(0, 60):
    row = a[y]
    red = (row[:,0]>120)&(row[:,1]<90)&(row[:,2]<90)
    if red.sum() > 50:
        xs = np.where(red)[0]
        print('red rule row', y, 'count', red.sum(), 'x', xs.min(), xs.max(), 'color', a[y, (xs.min()+xs.max())//2])
