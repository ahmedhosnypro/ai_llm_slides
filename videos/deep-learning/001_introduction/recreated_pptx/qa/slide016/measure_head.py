from PIL import Image
import numpy as np
V='/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction'
f16=np.asarray(Image.open(V+'/unique_slides/slide_016.jpg').convert('RGB')).astype(int)
# dump the head region x110..150 y226..244 as compact chars
print('f16 head region (x110..150, y226..244): R value map, .=none')
for y in range(226,245):
    line=''
    for x in range(110,151):
        r,g,b=f16[y,x]
        if r>140 and g<100 and b<100: line+='R'
        elif r-g>30 and r-b>30: line+='r'
        elif r>200 and g>200 and b>200: line+='.'
        elif max(r,g,b)<120: line+='K'
        else: line+='o'
    print(f'{y:3d} {line}')
print()
print('f16 box1 left-top corner region (x140..160, y200..215):')
for y in range(200,216):
    line=''
    for x in range(140,161):
        r,g,b=f16[y,x]
        if r>140 and g<100 and b<100: line+='R'
        elif r-g>30 and r-b>30: line+='r'
        elif max(r,g,b)<120: line+='K'
        elif r>200 and g>200 and b>200: line+='.'
        else: line+='o'
    print(f'{y:3d} {line}')
