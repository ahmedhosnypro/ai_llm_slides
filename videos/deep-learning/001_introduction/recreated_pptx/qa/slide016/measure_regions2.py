from PIL import Image
import numpy as np
from collections import Counter
V='/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction'
f16=np.asarray(Image.open(V+'/unique_slides/slide_016.jpg').convert('RGB')).astype(int)
f09=np.asarray(Image.open(V+'/unique_slides/slide_009.jpg').convert('RGB')).astype(int)
d=(np.abs(f16-f09).max(axis=2)>40)

def diff_cols(y0,y1):
    sub=d[y0:y1+1]
    cols=sub.sum(axis=0)
    runs=[];inr=False
    for x,c in enumerate(cols):
        if c>2 and not inr: x0=x;inr=True
        if c<=2 and inr: runs.append((x0,x-1));inr=False
    if inr: runs.append((x0,len(cols)-1))
    return runs

print('rows 129..196 diff col-runs:', diff_cols(129,196))
print('rows 272..350 diff col-runs:', diff_cols(272,350))
print('rows 352..394 diff col-runs:', diff_cols(352,394))

def modal(img,y0,y1,x0,x1,q=8):
    reg=img[y0:y1+1,x0:x1+1]
    cnt=Counter(map(tuple,(reg//q*q).reshape(-1,3)))
    return cnt.most_common(3)

print()
print('== f16 Final Result ellipse region (x780..905, y300..360) ==')
print('f16 modal:',modal(f16,300,360,780,905))
print('f09 modal:',modal(f09,300,360,780,905))
print()
print('== f16 curve2 region (x820..900, y235..310) ==')
print('f16 modal:',modal(f16,235,310,820,900))
print('f09 modal:',modal(f09,235,310,820,900))
print()
print('== f16 callout band rows 270..400: gray box scan ==')
# find rounded gray boxes: scan row by row for pixels close to E0E0E0 (224,224,224) +-18
def gray_rows(img):
    mask=(np.abs(img[:,:,0]-img[:,:,1])<12)&(np.abs(img[:,:,1]-img[:,:,2])<12)&(img[:,:,0]>195)&(img[:,:,0]<245)
    rows=mask.sum(axis=1)
    for y in range(260,410):
        if rows[y]>30: pass
    runs=[];inr=False
    for y in range(255,420):
        if rows[y]>30 and not inr: y0=y;inr=True
        if rows[y]<=30 and inr: runs.append((y0,y-1));inr=False
    if inr: runs.append((y0,419))
    return runs
print('f16 gray-band rows:',gray_rows(f16))
print('f09 gray-band rows:',gray_rows(f09))
