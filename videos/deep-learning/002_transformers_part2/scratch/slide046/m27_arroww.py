from PIL import Image
import numpy as np
a = np.asarray(Image.open('videos/deep-learning/002_transformers_part2/unique_slides/slide_046.jpg').convert('RGB')).astype(int)
nvy = (a[:,:,2]>110)&(a[:,:,0]<100)&(a[:,:,1]<100)
for fam, y0, y1 in [('FFN->postFFN', 190, 208), ('postLN->FFN', 262, 280), ('MHA->outatt', 400, 419), ('X->MHA', 467, 487)]:
    print(f'== {fam} ==')
    for y in range(y0, y1):
        xs = np.where(nvy[y, 195:218])[0]
        if len(xs): print(f'  y={y}: x {xs.min()+195}..{xs.max()+195} n={len(xs)}')
