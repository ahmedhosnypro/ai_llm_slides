from PIL import Image
import numpy as np
V='/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction'
f16=np.asarray(Image.open(V+'/unique_slides/slide_016.jpg').convert('RGB')).astype(int)
f09=np.asarray(Image.open(V+'/unique_slides/slide_009.jpg').convert('RGB')).astype(int)

def peachrows(img,y0,y1,x0,x1,label):
    reg=img[y0:y1+1,x0:x1+1]
    mask=(reg[:,:,0]>225)&(reg[:,:,1]>200)&(reg[:,:,1]<238)&(reg[:,:,2]>170)&(reg[:,:,2]<218)
    rows=mask.sum(axis=1)
    print(f'--- {label} peach row counts (rows with >5) ---')
    inr=False
    for i,c in enumerate(rows):
        if c>5 and not inr: s=i;inr=True
        if c<=5 and inr: print(f'  rows {y0+s}..{y0+i-1}  max={rows[s:i].max()}');inr=False
    if inr: print(f'  rows {y0+s}..{y1} max={rows[s:].max()}')
peachrows(f16,120,220,70,220,'f16')
peachrows(f09,120,220,70,220,'f09')

# ellipse outline (gray ~999999) scan in f16
def edge_rows(img,y0,y1,x0,x1,label):
    reg=img[y0:y1+1,x0:x1+1]
    mask=(np.abs(reg[:,:,0]-reg[:,:,1])<14)&(np.abs(reg[:,:,1]-reg[:,:,2])<14)&(reg[:,:,0]>120)&(reg[:,:,0]<190)
    rows=mask.sum(axis=1)
    idx=[i for i,c in enumerate(rows) if c>3]
    print(label,'gray-edge rows>3:',[(y0+i,int(rows[i])) for i in idx][:12])
edge_rows(f16,125,215,70,220,'f16')
edge_rows(f09,125,215,70,220,'f09')
