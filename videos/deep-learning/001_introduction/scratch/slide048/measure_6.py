from PIL import Image
import numpy as np
im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_048.jpg').convert('RGB')
a = np.asarray(im)
def p(x,y): print(f'({x:3d},{y:3d}) {tuple(a[y,x])}')
print('--- horizontal probes at y=300 (mid frame):')
for x in [20,40,50,55,57,58,59,60,62,64,65,66,67,70,880,890,892,893,894,895,900,920,940]: p(x,300)
print('--- vertical probes at x=300:')
for y in [10,20,30,40,42,44,46,48,50,100,120,130,132,133,134,137,140,443,446,447,450,455,470,490,505,510,512,514,516,518,520]: p(300,y)
print('--- black bar check:')
R,G,B = a[...,0].astype(int),a[...,1].astype(int),a[...,2].astype(int)
black = (R<60)&(G<60)&(B<60)
rc = black.sum(axis=1)
for r in range(H:=a.shape[0]):
    if rc[r]>200: 
        xs=np.nonzero(black[r,:])[0]; print(f'  row {r}: n={rc[r]} x {xs.min()}..{xs.max()}')
