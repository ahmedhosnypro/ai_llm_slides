import numpy as np
from PIL import Image
ren=np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/qa/slide026/render_1.png').convert('RGB')).astype(int)
S=ren.shape[1]/960.0
dk=(ren.sum(axis=2)<560)
def art(x0f,x1f,y0f,y1f,label,step=3):
    x0,x1,y0,y1=[int(v*S) for v in (x0f,x1f,y0f,y1f)]
    print(f'--- {label} (frame {x0f}..{x1f}, {y0f}..{y1f}) ---')
    for y in range(y0,y1,step):
        print(f'{y:5d} '+''.join('#' if dk[y,x:x+step].any() else '.' for x in range(x0,x1,step)))
art(95,390,185,255,'render c201 region')
