from PIL import Image
import numpy as np
im = np.asarray(Image.open('unique_slides/slide_022.jpg').convert('RGB')).astype(int)
H, W = im.shape[:2]
r, g, b = im[:,:,0], im[:,:,1], im[:,:,2]
lum = (r+g+b)/3

def bbox(mask, name):
    ys, xs = np.where(mask)
    if not len(ys):
        print(f'{name}: NONE'); return
    print(f'{name}: x {xs.min()}..{xs.max()}  y {ys.min()}..{ys.max()}  n={len(ys)}')

# color classes
red_dark  = (r>150)&(r<215)&(g<60)&(b<60)          # C00000-ish
red_bright= (r>200)&(g<80)&(b<80)                  # FF0000-ish
white     = (r>235)&(g>235)&(b>235)
yellowish = (r>230)&(g>225)&(b<215)&(b>190)        # FFFFE1-ish
tan       = (np.abs(r-216)<30)&(np.abs(g-200)<30)&(np.abs(b-168)<35)&(r>g)&(g>b)
blue      = (b>140)&(r<110)&(g<110)
black     = lum<100

bbox(red_dark, 'red_dark C00000')
bbox(red_bright, 'red_bright FF0000')
bbox(white, 'white')
bbox(yellowish, 'yellowish')
bbox(tan, 'tan')
bbox(blue, 'blue')
bbox(black & (lum<60), 'black60')
print('image size', W, H)

# white boxes: connected components of white
from scipy import ndimage
lab, n = ndimage.label(white)
print('white components:', n)
sizes = ndimage.sum(white, lab, range(1, n+1))
big = [i+1 for i,s in enumerate(sizes) if s > 3000]
for i in big:
    ys, xs = np.where(lab==i)
    print(f'  white comp {i}: x {xs.min()}..{xs.max()} y {ys.min()}..{ys.max()} area {int(sizes[i-1])}')
