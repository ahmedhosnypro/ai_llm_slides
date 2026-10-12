from PIL import Image
import numpy as np
im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_048.jpg').convert('RGB')
W,H = im.size
a = np.asarray(im).astype(int)
R,G,B = a[...,0],a[...,1],a[...,2]
red = (R>120)&(R<235)&(G<80)&(B<80)

rowcount = red.sum(axis=1)
colcount = red.sum(axis=0)
print('rows with >30 red px:')
for r in range(H):
    if rowcount[r]>30: print(f'  row {r}: {rowcount[r]}')
print('cols with >30 red px:')
for c in range(W):
    if colcount[c]>30: print(f'  col {c}: {colcount[c]}')
