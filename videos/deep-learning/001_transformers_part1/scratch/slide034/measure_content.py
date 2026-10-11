from PIL import Image
import numpy as np
img = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_034.jpg').convert('RGB')
a = np.asarray(img).astype(int)
H,W = a.shape[:2]

def mask_report(name, cond, ymin=0,ymax=H,xmin=0,xmax=W):
    sub = cond[ymin:ymax, xmin:xmax]
    ys,xs = np.where(sub)
    if len(xs)==0: print(f"{name}: NONE"); return None
    x0,x1,y0,y1 = xs.min()+xmin, xs.max()+xmin, ys.min()+ymin, ys.max()+ymin
    print(f"{name}: x {x0}..{x1}  y {y0}..{y1}  ({x1-x0+1}x{y1-y0+1})")
    return (x0,x1,y0,y1)

r,g,b = a[:,:,0],a[:,:,1],a[:,:,2]

# Title only (above subtitle): find dark ink rows in y 40..100 to see row profile
dark = (r<120)&(g<120)&(b<120)
rowsum = dark[:, 100:860].sum(axis=1)
runs=[]
inrun=False
for y in range(40,110):
    if rowsum[y]>0 and not inrun: start=y; inrun=True
    if rowsum[y]==0 and inrun: runs.append((start,y-1)); inrun=False
print("dark ink row runs y40..110:", runs)

# green concept box outline (green stroke, ~00A651 or 00B050)
green = (g>120)&(r<110)&(b<110)&(g-r>50)&(g-b>50)
mask_report("green all", green, 90, 270, 20, 430)
# peach panel
peach = (r>235)&(r<255)&(g>215)&(g<240)&(b>195)&(b<225)&(r-b>25)
mask_report("peach panel", peach, 250, 540, 0, 960)
# yellow input boxes (strong yellow)
yellow = (r>210)&(g>200)&(b<140)
mask_report("yellow (inputs+highlights)", yellow)
# blue borders 0033CC
blue = (b>140)&(b-r>60)&(b-g>40)&(r<120)
mask_report("blue all", blue, 260, 540, 0, 960)
# red block arrows/parens C00000
red = (r>150)&(r-g>70)&(r-b>70)
mask_report("red all (frame excl?)", red, 100, 540, 30, 930)
