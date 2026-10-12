from PIL import Image
import numpy as np
V='/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction'
a=np.asarray(Image.open(V+'/unique_slides/slide_017.jpg').convert('RGB')).astype(int)
b=np.asarray(Image.open(V+'/unique_slides/slide_016.jpg').convert('RGB')).astype(int)
d=(np.abs(a-b).max(axis=2)>40)
# column profile of diff in rows 278..340
sub = d[278:341,:]
cols = sub.sum(axis=0)
runs=[]; inr=False
for x,c in enumerate(cols):
    if c>2 and not inr: x0=x; inr=True
    if c<=2 and inr: runs.append((x0,x-1)); inr=False
if inr: runs.append((x0,len(cols)-1))
print('rows278-340 col runs:', runs)

# gray roundrect detection for Apply Model in both frames: fill ~ (230,232,230) modal
def bbox_gray(img, y0,y1,x0,x1):
    reg = img[y0:y1, x0:x1]
    g = (np.abs(reg[:,:,0]-reg[:,:,1])<12) & (np.abs(reg[:,:,1]-reg[:,:,2])<12) & (reg[:,:,0]>200) & (reg[:,:,0]<245)
    ys,xs = np.where(g)
    if len(xs)==0: return None
    return (x0+xs.min(), y0+ys.min(), x0+xs.max(), y0+ys.max())
print('17 apply gray bbox:', bbox_gray(a, 270, 335, 595, 715))
print('16 apply gray bbox:', bbox_gray(b, 270, 335, 595, 715))
# row profile of diff within x595..715
sub2 = d[270:345, 595:715]
rows = sub2.sum(axis=1)
print('rows w diff>3 (y:count):', [(270+y,int(c)) for y,c in enumerate(rows) if c>3][:40])
