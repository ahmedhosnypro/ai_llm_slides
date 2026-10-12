#!/usr/bin/env python3
"""Stage 14: ASCII maps of dense equation regions (numeric, threshold-based)."""
import numpy as np
from PIL import Image

im = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_040.jpg')).astype(int)
lum = (im[:,:,0]+im[:,:,1]+im[:,:,2])/3.0
r, g, b = im[:,:,0], im[:,:,1], im[:,:,2]

def amap(x0, x1, y0, y1, thr=160, label=''):
    print(f'--- {label} x{x0}..{x1} y{y0}..{y1} thr{thr} (2px v-res) ---')
    hdr = '     ' + ''.join(str((x//10)%10) for x in range(x0, x1))
    print(hdr)
    for y in range(y0, y1, 2):
        row = ''.join('#' if lum[y, x] < thr else '.' for x in range(x0, x1))
        print(f'{y:4d} {row}')

# eq1 fraction + sum region
amap(230, 300, 288, 342, 160, 'EQ1 frac+sum')
# eq2 fraction region (same shape expected)
amap(230, 345, 332, 398, 160, 'EQ2 frac+sum+(x)^2')
# eq3 whole math region
amap(165, 300, 388, 452, 160, 'EQ3 xhat..fraction')
# eq4 math region
amap(160, 385, 448, 480, 170, 'EQ4 ellipse..BN')
