from PIL import Image
import numpy as np
im = np.asarray(Image.open('unique_slides/slide_022.jpg').convert('RGB')).astype(int)
r, g, b = im[:,:,0], im[:,:,1], im[:,:,2]
lum = (r+g+b)/3

# raw row scans through the aug box at several heights: find ALL non-background pixels
def scanrow(y, x0, x1, label, thr=215):
    hits=[]
    for x in range(x0,x1):
        L=lum[y,x]
        if L<thr:
            hits.append(f'{x}:({r[y,x]},{g[y,x]},{b[y,x]})')
    print(f'y={y} {label}:', ' '.join(hits[:40]))

scanrow(113, 84, 300, 'aug row1-ish')
scanrow(127, 84, 300, 'aug row x1')
scanrow(149, 84, 300, 'aug row x2')
scanrow(165, 84, 300, 'aug row dots')
scanrow(190, 84, 300, 'aug row dots2')
scanrow(215, 84, 300, 'aug row xn')
