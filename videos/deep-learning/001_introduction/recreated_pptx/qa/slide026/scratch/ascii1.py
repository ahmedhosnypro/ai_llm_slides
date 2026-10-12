from PIL import Image
import numpy as np
im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_026.jpg').convert('RGB')
a = np.asarray(im).astype(int)
dk = (a.sum(axis=2)<400)
def art(y0,y1,x0,x1,step=2):
    print(f'--- rows {y0}..{y1} cols {x0}..{x1} (col step {step}) ---')
    hdr = '    ' + ''.join(str((x0+i*step)//100%10) for i in range((x1-x0)//step+1))
    hdr2 = '    ' + ''.join(str((x0+i*step)//10%10) for i in range((x1-x0)//step+1))
    print(hdr); print(hdr2)
    for y in range(y0,y1):
        row = dk[y, x0:x1+1]
        s = ''.join('#' if row[i:i+step].any() else '.' for i in range(0, x1-x0+1, step))
        print(f'{y:4d} {s}')
art(248,296,100,310,2)
