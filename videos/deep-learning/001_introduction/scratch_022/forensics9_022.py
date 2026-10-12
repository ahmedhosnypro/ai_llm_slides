from PIL import Image
import numpy as np
im = np.asarray(Image.open('unique_slides/slide_022.jpg').convert('RGB')).astype(int)
r, g, b = im[:,:,0], im[:,:,1], im[:,:,2]
lum = (r+g+b)/3

def ascii_map(x0,y0,x1,y1,label,sx=3,sy=3):
    h = (y1-y0)//sy; w = (x1-x0)//sx
    print(f'== {label} x{x0}..{x1} y{y0}..{y1} (cell {sx}x{sy}) ==')
    hdr = '     ' + ''.join(str(((x0+i*sx)//100)%10) if ((x0+i*sx)%50<sx) else ' ' for i in range(w))
    hdr2= '     ' + ''.join(str(((x0+i*sx)//10)%10) if ((x0+i*sx)%50<sx) else ' ' for i in range(w))
    print(hdr); print(hdr2)
    for j in range(h):
        row=''
        for i in range(w):
            sub_r = r[y0+j*sy:y0+(j+1)*sy, x0+i*sx:x0+(i+1)*sx]
            sub_g = g[y0+j*sy:y0+(j+1)*sy, x0+i*sx:x0+(i+1)*sx]
            sub_b = b[y0+j*sy:y0+(j+1)*sy, x0+i*sx:x0+(i+1)*sx]
            rl,gl,bl = sub_r.mean(), sub_g.mean(), sub_b.mean()
            L = (rl+gl+bl)/3
            ch=' '
            if L<110: ch='#'
            elif rl-gl>45 and rl-bl>35: ch='R'
            elif bl-rl>40: ch='B'
            elif rl>210 and gl>210 and bl<215 and rl-gl<30: ch='y'
            elif rl-gl>25: ch='r'
            elif bl-rl>20: ch='b'
            elif L<190: ch='+'
            row+=ch
        mark = f'{y0+j*sy:4d} ' if (j*sy)%30<sy else '     '
        print(mark+row)

ascii_map(83,255,766,343,'DECISION BOX')
