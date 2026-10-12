#!/usr/bin/env python3
"""Component analysis: find ink bboxes per color family across the whole frame."""
import numpy as np
from PIL import Image
from scipy import ndimage

im = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_009.jpg').convert('RGB')).astype(int)
H, W, _ = im.shape
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]

def comps(mask, minpx=12, label=''):
    lab, n = ndimage.label(mask)
    out = []
    for sl in ndimage.find_objects(lab):
        h = sl[0].stop - sl[0].start; w = sl[1].stop - sl[1].start
        npx = int(mask[sl].sum())
        if npx < minpx:
            continue
        out.append((sl[1].start, sl[0].start, sl[1].stop, sl[0].stop, npx))
    out.sort(key=lambda t: (t[1], t[0]))
    print(f'--- {label}: {len(out)} comps (x0,y0,x1,y1,npx)')
    for c in out:
        print(f'    {c[0]:4d},{c[1]:4d} .. {c[2]:4d},{c[3]:4d}  ({c[4]}px)')
    return out

# pink circles / pink boxes: r high, b high, g much lower
pink = (r > 200) & (b > 170) & (g < 190) & (r - g > 40)
comps(pink, 40, 'PINK (fills)')

# yellow fills: r,g high, b much lower
yellow = (r > 215) & (g > 200) & (b < 190) & (r - b > 40)
comps(yellow, 30, 'YELLOW fills')

# light green fills (matrix container): g high, r lower, b mid
lgreen = (g > 220) & (r < 225) & (b < 225) & (g - r > 10)
comps(lgreen, 60, 'LIGHT GREEN fills')

# red text/lines
red = (r > 110) & (r - g > 55) & (r - b > 55)
comps(red, 20, 'RED ink')

# blue text (0000CC / 0033CC): b high, r low, g low-mid
blue = (b > 130) & (r < 110) & (b - r > 60)
comps(blue, 15, 'BLUE ink')

# purple text 9933CC
purple = (r > 100) & (r < 200) & (b > 150) & (g < 110) & (b - g > 60)
comps(purple, 12, 'PURPLE ink')

# orange FF9900
orange = (r > 200) & (g > 110) & (g < 200) & (b < 110) & (r - b > 90)
comps(orange, 12, 'ORANGE ink')

# green 009900 (labels + arrows)
green = (g > 100) & (r < 120) & (b < 120) & (g - r > 50) & (g - b > 50)
comps(green, 12, 'GREEN ink')
