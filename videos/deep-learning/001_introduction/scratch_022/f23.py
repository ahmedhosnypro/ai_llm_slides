from PIL import Image
import numpy as np
im = np.asarray(Image.open('unique_slides/slide_022.jpg').convert('RGB')).astype(int)
r, g, b = im[:,:,0], im[:,:,1], im[:,:,2]
lum = (r+g+b)/3
def ascii1(x0,y0,x1,y1,label,thr):
    print(f'== {label} x{x0}..{x1} y{y0}..{y1} thr={thr} ==')
    print('     ' + ''.join(str((x//100)%10) if x%50<10 else ' ' for x in range(x0,x1)))
    print('     ' + ''.join(str((x//10)%10) if x%10==0 else ' ' for x in range(x0,x1)))
    for y in range(y0,y1):
        row=''
        for x in range(x0,x1):
            L=lum[y,x]; ch=' '
            if L<thr: ch='.'
            row+=ch
        print(f'{y:4d} {row}')
ascii1(306,352,408,506,'FAN LINES (any sub-bg)',238)
