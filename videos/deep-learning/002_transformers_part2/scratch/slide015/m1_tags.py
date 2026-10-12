from PIL import Image
import numpy as np
from scipy import ndimage

im = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_015.jpg').convert('RGB')).astype(int)
H, W = im.shape[:2]

# 1) black h=N tag ovals: very dark pixels
dark = (im.sum(axis=2) < 150)
lab, n = ndimage.label(dark)
print('--- black tag ovals (parent: k=0 at 563..593 x, 280..294.5 y; step +46x, -20.5y) ---')
for i, sl in enumerate(ndimage.find_objects(lab)):
    h_ = sl[0].stop - sl[0].start; w_ = sl[1].stop - sl[1].start
    npx = (lab[sl] == i+1).sum()
    if 18 <= w_ <= 60 and 8 <= h_ <= 24 and npx > 120:
        fill = npx / (w_ * h_)
        if fill > 0.55:
            print(f'  tag x {sl[1].start}..{sl[1].stop}  y {sl[0].start}..{sl[0].stop}  (w{w_} h{h_} fill {fill:.2f})')

# 2) magenta X2 chip in query row (parent strips: x222..258 y496..511, hot 2nd)
mag = (np.abs(im - np.array([0xFF, 0x66, 0xCC])).sum(axis=2) < 160)
print('--- magenta pixels bbox:', end=' ')
ys, xs = np.where(mag)
if len(xs): print(f'x {xs.min()}..{xs.max()}  y {ys.min()}..{ys.max()}  n={len(xs)}')
else: print('none')

# 3) red query bar (parent: x205..251 y467..479 pure red)
red = (np.abs(im - np.array([0xCC, 0x00, 0x00])).sum(axis=2) < 120)
lab2, n2 = ndimage.label(red)
print('--- large solid-red components (query bar, W boxes, swoosh) ---')
for i, sl in enumerate(ndimage.find_objects(lab2)):
    npx = (lab2[sl] == i+1).sum()
    if npx > 250:
        print(f'  red x {sl[1].start}..{sl[1].stop}  y {sl[0].start}..{sl[0].stop}  n={npx}')
