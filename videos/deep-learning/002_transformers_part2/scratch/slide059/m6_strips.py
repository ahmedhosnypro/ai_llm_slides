from PIL import Image
import numpy as np
im = Image.open('unique_slides/slide_059.jpg').convert('RGB')
a = np.asarray(im).astype(int)

def strip(y, x0, x1, step=4, label=''):
    print(f'--- strip y={y} {label}')
    out=[]
    for x in range(x0, x1, step):
        px = tuple(int(v) for v in a[y, x])
        # classify
        r,g,b = px
        c = 'GRAY' if abs(r-231)<14 and abs(g-233)<14 and abs(b-229)<14 else \
            'WHT' if r>242 and g>242 and b>238 else \
            'PINK' if r>235 and 200<g<235 and 195<b<235 else \
            'PEACH' if r>240 and 215<g<240 and 190<b<225 else \
            'LBLUE' if 200<r<230 and 220<g<245 and b>238 else \
            'TAN' if 225<r<248 and 185<g<215 and 145<b<185 else \
            'BLUE' if b>150 and b-r>40 and g<150 else \
            'NAVY' if b>90 and r<80 and g<90 else \
            'DRED' if r>120 and g<70 and b<80 else \
            'MRED' if 160<r<225 and 60<g<140 and 60<b<150 and r-g>60 else \
            'GREEN' if g>110 and g-r>30 and g-b>20 else \
            'ORG' if r>200 and 120<g<190 and b<120 else \
            'DK' 
        out.append(f'{x}:{c}')
    print(' '.join(out))

strip(428, 60, 900, 4, 'word row centerline')
strip(488, 60, 900, 4, 'position row centerline')
strip(240, 60, 900, 4, 'output row centerline')
strip(172, 380, 640, 3, 'arrow4 band')
strip(214, 380, 640, 3, 'arrow3 band')
strip(268, 380, 640, 3, 'arrow2 band')
strip(380, 380, 640, 3, 'arrow1 band')
