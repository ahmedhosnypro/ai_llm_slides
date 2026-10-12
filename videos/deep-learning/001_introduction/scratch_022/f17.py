from PIL import Image
import numpy as np
im = np.asarray(Image.open('unique_slides/slide_022.jpg').convert('RGB')).astype(int)
r, g, b = im[:,:,0], im[:,:,1], im[:,:,2]
lum = (r+g+b)/3
def ascii2(x0,y0,x1,y1,label,sx=2,sy=2):
    w=(x1-x0)//sx; h=(y1-y0)//sy
    print(f'== {label} x{x0}..{x1} y{y0}..{y1} cell {sx}x{sy} ==')
    print('     ' + ''.join(str(((x0+i*sx)//100)%10) if ((x0+i*sx)%40)<sx else ' ' for i in range(w)))
    print('     ' + ''.join(str(((x0+i*sx)//10)%10) if ((x0+i*sx)%40)<sx else ' ' for i in range(w)))
    for j in range(h):
        row=''
        for i in range(w):
            R=r[y0+j*sy:y0+(j+1)*sy, x0+i*sx:x0+(i+1)*sx].mean()
            G=g[y0+j*sy:y0+(j+1)*sy, x0+i*sx:x0+(i+1)*sx].mean()
            B=b[y0+j*sy:y0+(j+1)*sy, x0+i*sx:x0+(i+1)*sx].mean()
            L=(R+G+B)/3; ch=' '
            if L<110: ch='#'
            elif R-G>40 and R-B>30: ch='R'
            elif B-R>35: ch='B'
            elif B-R>15: ch='b'
            elif R-G>18: ch='r'
            elif R>200 and G>170 and B>170 and R-B>10 and G-B>5: ch='p'
            elif L<200: ch='+'
            elif L<225: ch='-'
            row+=ch
        mark = f'{y0+j*sy:4d} ' if (j*sy)%20<sy else '     '
        print(mark+row)
ascii2(232,352,612,508,'DIAGRAM BOX',2,2)
