from PIL import Image
import numpy as np
im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_048.jpg').convert('RGB')
W,H = im.size
a = np.asarray(im).astype(int)
R,G,B = a[...,0],a[...,1],a[...,2]
red = (R>120)&(R<235)&(G<80)&(B<80)

# ASCII map of red mask, 12x8 blocks
bs_x, bs_y = 12, 8
print('RED map (x: 80 cols of 12px, y: 68 rows of 8px), col grid marks every 10:')
hdr = ''.join([str((i*bs_x//100)%10) if (i*bs_x)%100<12 else ' ' for i in range(80)])
print('     '+hdr)
for by in range(0, H, bs_y):
    line=''
    for bx in range(0, W, bs_x):
        blk = red[by:by+bs_y, bx:bx+bs_x]
        frac = blk.mean()
        line += '#' if frac>0.3 else ('+' if frac>0.12 else ('.' if frac>0.03 else ' '))
    print(f'{by:4d} '+line)
