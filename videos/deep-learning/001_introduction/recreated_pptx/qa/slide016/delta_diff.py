from PIL import Image
import numpy as np
V='/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction'
a=np.asarray(Image.open(V+'/unique_slides/slide_016.jpg').convert('RGB')).astype(int)
b=np.asarray(Image.open(V+'/unique_slides/slide_009.jpg').convert('RGB')).astype(int)
print('shapes', a.shape, b.shape)
d=(np.abs(a-b).max(axis=2)>40)
print('diff px total:', d.sum())
# row profile of diff
rows=d.sum(axis=1); cols=d.sum(axis=0)
print('--- rows with diff>5 (row: count) ---')
runs=[]
inr=False
for y,c in enumerate(rows):
    if c>5 and not inr: y0=y; inr=True
    if c<=5 and inr: runs.append((y0,y-1)); inr=False
if inr: runs.append((y0,len(rows)-1))
for r in runs: print('rows',r, 'max row count', rows[r[0]:r[1]+1].max())
print('--- cols with diff>5 ---')
runs=[]; inr=False
for x,c in enumerate(cols):
    if c>5 and not inr: x0=x; inr=True
    if c<=5 and inr: runs.append((x0,x-1)); inr=False
if inr: runs.append((x0,len(cols)-1))
print(runs)
