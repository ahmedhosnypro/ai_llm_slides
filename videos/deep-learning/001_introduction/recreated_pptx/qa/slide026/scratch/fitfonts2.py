from PIL import Image
import numpy as np
im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_026.jpg').convert('RGB')
a = np.asarray(im).astype(int)
R=a[:,:,0]; G=a[:,:,1]; B=a[:,:,2]
redm  = (R-G>50)&(R-B>50)&(R>120)
bluem = (B-R>40)&(B-G>30)&(B>110)
def profile(mask,y0,y1,x0,x1,label):
    m = mask[y0:y1,x0:x1]
    print(label, 'row-density (row: count):')
    for i,c in enumerate(m.sum(axis=1)):
        if c>0: print(f'  {y0+i}: {c}')
profile(redm,55,84,90,830,'title1 (excl U/ghost)')
profile(bluem,84,118,100,870,'title2 (excl G start)')
