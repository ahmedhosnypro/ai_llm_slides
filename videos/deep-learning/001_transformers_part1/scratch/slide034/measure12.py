from PIL import Image
import numpy as np
from scipy import ndimage
img = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_034.jpg').convert('RGB')
a = np.asarray(img).astype(int)
r,g,b = a[:,:,0],a[:,:,1],a[:,:,2]

def comps(mask, minpx=40, label=""):
    lab,n = ndimage.label(mask)
    out=[]
    for i in range(1,n+1):
        ys,xs = np.where(lab==i)
        if len(xs)<minpx: continue
        out.append((int(xs.min()),int(xs.max()),int(ys.min()),int(ys.max()),len(xs)))
    out.sort(key=lambda t:(t[2],t[0]))
    print(f"== {label}")
    for x0,x1,y0,y1,npx in out: print(f"   x {x0}..{x1} y {y0}..{y1} px{npx}")

# input boxes: yellow fill, per column
yellow=(r>200)&(g>180)&(b<160)&((r-b)>70)
for i,(x0,x1) in enumerate([(125,185),(392,455),(660,725)]):
    comps(yellow[350:495, x0:x1], 60, f"col{i+1} input yellow boxes (x+{x0},y+350)")
    # print with offsets applied
# redo with offsets
def comps_off(mask, ox, oy, minpx, label):
    lab,n = ndimage.label(mask)
    out=[]
    for i in range(1,n+1):
        ys,xs = np.where(lab==i)
        if len(xs)<minpx: continue
        out.append((int(xs.min())+ox,int(xs.max())+ox,int(ys.min())+oy,int(ys.max())+oy,len(xs)))
    out.sort(key=lambda t:(t[2],t[0]))
    print(f"== {label}")
    for x0,x1,y0,y1,npx in out: print(f"   x {x0}..{x1} y {y0}..{y1} px{npx}")

for i,(x0,x1) in enumerate([(125,185),(392,455),(660,725)]):
    comps_off(yellow[350:495, x0:x1], x0, 350, 60, f"col{i+1} input boxes")

# output boxes: white fill surrounded by blue border -> detect blue border comps per column
blue=(b>120)&((b-r)>40)&(r<170)
for i,(x0,x1) in enumerate([(245,320),(512,590),(780,855)]):
    comps_off(blue[350:495, x0:x1], x0, 350, 25, f"col{i+1} output blue")

# red pixel x-histogram in warning strip
band_r = ((r-b)>50)&(r>140)&(g<200)
sub = band_r[289:307, 395:870]
ys,xs=np.where(sub)
hist,edges=np.histogram(xs+395,bins=np.arange(395,875,15))
print("warning RED x-hist:", {int(edges[i]):int(v) for i,v in enumerate(hist) if v>0})
sub2 = blue[289:307, 395:870]
ys,xs=np.where(sub2)
hist,edges=np.histogram(xs+395,bins=np.arange(395,875,15))
print("warning BLUE x-hist:", {int(edges[i]):int(v) for i,v in enumerate(hist) if v>0})
