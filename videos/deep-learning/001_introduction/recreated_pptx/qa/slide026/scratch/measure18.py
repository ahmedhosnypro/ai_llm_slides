from PIL import Image
import numpy as np
im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_026.jpg').convert('RGB')
a = np.asarray(im).astype(int)
dk = (a.sum(axis=2)<560)
def art(y0,y1,x0,x1,label):
    print(f'--- {label} ---')
    tens = '    ' + ''.join(str((x0+i)//10%10) if (x0+i)%10==0 else ' ' for i in range(x1-x0+1))
    print(tens)
    for y in range(y0,y1):
        print(f'{y:4d} ' + ''.join('#' if dk[y,x] else '.' for x in range(x0,x1+1)))
art(458,494,556,700,'eq8 first part: w_ji^new = w_ji^old')
