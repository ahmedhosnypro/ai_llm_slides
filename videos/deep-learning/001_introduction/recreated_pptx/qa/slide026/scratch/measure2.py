from PIL import Image
import numpy as np
im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_026.jpg').convert('RGB')
a = np.asarray(im).astype(int)
H, W = a.shape[:2]
# red pixels anywhere
red = (a[:,:,0]>120)&(a[:,:,1]<90)&(a[:,:,2]<90)
rows = np.where(red.sum(axis=1)>30)[0]
print('red-heavy rows:', rows.min() if len(rows) else None, rows.max() if len(rows) else None)
# group contiguous row bands
bands=[]
if len(rows):
    s=rows[0]; p=rows[0]
    for r in rows[1:]:
        if r>p+1: bands.append((s,p)); s=r
        p=r
    bands.append((s,p))
print('red row bands:', bands)
# for the topmost band, x extent
for (s,e) in bands[:6]:
    sub = red[s:e+1]
    xs = np.where(sub.any(axis=0))[0]
    print('band', (s,e), 'x', xs.min(), xs.max(), 'sample color', a[s, (xs.min()+xs.max())//2])
# blue pixels
blue = (a[:,:,2]>120)&(a[:,:,0]<90)&(a[:,:,1]<110)
rowsB = np.where(blue.sum(axis=1)>20)[0]
bandsB=[]
if len(rowsB):
    s=rowsB[0]; p=rowsB[0]
    for r in rowsB[1:]:
        if r>p+1: bandsB.append((s,p)); s=r
        p=r
    bandsB.append((s,p))
print('blue row bands (first 12):', bandsB[:12], 'total', len(bandsB))
