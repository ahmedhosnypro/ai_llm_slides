from PIL import Image
import numpy as np
V='/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction'
f09=np.asarray(Image.open(V+'/unique_slides/slide_009.jpg').convert('RGB')).astype(int)
print('f09 head region (x110..150, y226..246):')
for y in range(226,247):
    line=''
    for x in range(110,151):
        r,g,b=f09[y,x]
        if r>140 and g<100 and b<100: line+='R'
        elif r-g>30 and r-b>30: line+='r'
        elif max(r,g,b)<120: line+='K'
        elif r>200 and g>200 and b>200: line+='.'
        else: line+='o'
    print(f'{y:3d} {line}')
