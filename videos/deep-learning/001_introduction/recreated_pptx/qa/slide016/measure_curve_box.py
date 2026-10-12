from PIL import Image
import numpy as np
from collections import Counter
V='/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction'
f16=np.asarray(Image.open(V+'/unique_slides/slide_016.jpg').convert('RGB')).astype(int)
f09=np.asarray(Image.open(V+'/unique_slides/slide_009.jpg').convert('RGB')).astype(int)

# 1) curve1 trace: red pixels x70..250 y182..245, per-row col range
def trace(img,label):
    print(f'--- {label} curve1 red trace (y: xmin..xmax) ---')
    for y in range(180,246):
        row=img[y,70:250]
        m=(row[:,0]>140)&(row[:,1]<95)&(row[:,2]<95)
        xs=np.where(m)[0]
        if len(xs)>0: print(f'  y={y}: x {70+xs.min()}..{70+xs.max()} n={len(xs)}')
trace(f16,'f16')
print()
trace(f09,'f09')
