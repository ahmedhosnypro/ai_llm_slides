from PIL import Image
import numpy as np
im = np.asarray(Image.open('unique_slides/slide_022.jpg').convert('RGB')).astype(int)
r, g, b = im[:,:,0], im[:,:,1], im[:,:,2]
lum = (r+g+b)/3
def ascii1(x0,y0,x1,y1,label):
    print(f'== {label} x{x0}..{x1} y{y0}..{y1} ==')
    print('     ' + ''.join(str((x//100)%10) if x%50<10 else ' ' for x in range(x0,x1)))
    print('     ' + ''.join(str((x//10)%10) if x%10==0 else ' ' for x in range(x0,x1)))
    for y in range(y0,y1):
        row=''
        for x in range(x0,x1):
            R,G,B = r[y,x], g[y,x], b[y,x]
            L=(R+G+B)/3; ch=' '
            if L<110: ch='#'
            elif R-G>40 and R-B>30: ch='R'
            elif B-R>35: ch='B'
            elif R-G>18: ch='r'
            elif B-R>15: ch='b'
            elif L<190: ch='+'
            elif L<215: ch='-'
            row+=ch
        print(f'{y:4d} {row}')
ascii1(196,100,280,240,'AUG: red arrow + right vector')
