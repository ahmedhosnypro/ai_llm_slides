from PIL import Image
import numpy as np
V='/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction'
f16=np.asarray(Image.open(V+'/unique_slides/slide_016.jpg').convert('RGB')).astype(int)
f09=np.asarray(Image.open(V+'/unique_slides/slide_009.jpg').convert('RGB')).astype(int)

def trace(img,label,y0,y1,x0,x1):
    print(f'--- {label} red-ish trace (r-g>35 and r-b>35) ---')
    for y in range(y0,y1):
        row=img[y,x0:x1]
        m=((row[:,0]-row[:,1])>35)&((row[:,0]-row[:,2])>35)
        xs=np.where(m)[0]
        if len(xs)>0: print(f'  y={y}: x {x0+xs.min()}..{x0+xs.max()} n={len(xs)}')
trace(f16,'f16',180,248,70,250)
trace(f09,'f09',180,248,70,250)
