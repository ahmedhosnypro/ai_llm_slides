from PIL import Image
import numpy as np
im = Image.open('unique_slides/slide_059.jpg').convert('RGB')
a = np.asarray(im).astype(int)
print('--- vertical x=300 y489..512 (position row bottom)')
for y in range(489, 513): print(y, tuple(int(v) for v in a[y, 300]))
def hstrip(y, x0, x1, label):
    print(f'--- fine strip y={y} {label}')
    s=[]
    for x in range(x0, x1):
        r,g,b = (int(v) for v in a[y, x])
        s.append(f'{x}:{r},{g},{b}')
    print(' '.join(s))
hstrip(488, 165, 250, 'position row box1 region')
hstrip(428, 205, 300, 'word row box1 region')
