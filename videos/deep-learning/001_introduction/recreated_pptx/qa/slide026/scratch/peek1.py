import numpy as np
from PIL import Image
ren=np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/qa/slide026/render_1.png').convert('RGB')).astype(int)
S=ren.shape[1]/960.0
# dark ink count per region (frame coords)
def dark(x0,y0,x1,y1):
    sub=ren[int(y0*S):int(y1*S), int(x0*S):int(x1*S)]
    return int((sub.sum(axis=2)<400).sum())
print('tan1 whole:', dark(80,127,647,298))
print('eq1 line1 zone:', dark(100,125,300,175))
print('yellow whole:', dark(83,307,761,368))
print('tan2 whole:', dark(80,376,841,500))
# ASCII of eq1 line1 zone at render scale (step 4)
dk=(ren.sum(axis=2)<400)
x0,x1,y0,y1=int(100*S),int(320*S),int(125*S),int(180*S)
tens='    '+''.join(str((x0+i)//10%10) if (x0+i)%40==0 else ' ' for i in range(0,x1-x0,4))
print(tens)
for y in range(y0,y1,3):
    print(f'{y:5d} '+''.join('#' if dk[y,x:x+4].any() else '.' for x in range(x0,x1,4)))
