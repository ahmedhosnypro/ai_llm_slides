from PIL import Image
import numpy as np
a = np.asarray(Image.open('videos/deep-learning/002_transformers_part2/unique_slides/slide_046.jpg').convert('RGB')).astype(int)
def sx(fx): return (fx-17.582)/0.962329
def sy(fy): return fy/0.955556
print('caption band raw colors, y 502..516, x 245..600 step 15:')
for y in range(502, 517):
    print(f'{y:4d} ' + ' '.join(f'{x}:{tuple(a[y,x])}' for x in range(245, 600, 45)))
print()
print('caption text ink (dark px R<160,G<100) per row, x 240..620:')
for y in range(502, 517):
    xs = [x for x in range(240, 620) if a[y,x][0] < 170 and a[y,x][1] < 110 and a[y,x][2] < 110]
    if xs: print(f'  y={y}: n={len(xs)} span {xs.min()}..{xs.max()}')
print()
print('pink-ish (FFB6C1+-ish) per row x 240..620:')
for y in range(502, 517):
    xs = [x for x in range(240, 620) if abs(a[y,x][0]-255)<35 and abs(a[y,x][1]-182)<50 and abs(a[y,x][2]-193)<50]
    if xs: print(f'  y={y}: n={len(xs)} span {xs.min()}..{xs.max()}')
print()
print('X-row bottom edge / row band via col1 gray cell x 214..228:')
for y in range(482, 512):
    seg = a[y, 214:229]
    nw = int((seg.max(axis=1) < 246).sum())
    print(f'  y={y}: nonwhite={nw}', tuple(a[y,220]))
