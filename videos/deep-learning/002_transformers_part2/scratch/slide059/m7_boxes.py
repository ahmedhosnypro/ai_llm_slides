from PIL import Image
import numpy as np
im = Image.open('unique_slides/slide_059.jpg').convert('RGB')
a = np.asarray(im).astype(int)
R, G, B = a[:,:,0], a[:,:,1], a[:,:,2]

# vertical dumps
for x in (300, 700):
    print(f'--- vertical x={x} y215..265 (output row)')
    for y in range(215, 266): print(y, tuple(int(v) for v in a[y, x]))
    break
print('--- vertical x=300 y408..448 (word row)')
for y in range(408, 449): print(y, tuple(int(v) for v in a[y, 300]))
print('--- vertical x=300 y465..510 (position row)')
for y in range(465, 511): print(y, tuple(int(v) for v in a[y, 300]))
