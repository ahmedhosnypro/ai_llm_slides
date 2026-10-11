from PIL import Image
import numpy as np
img = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_034.jpg').convert('RGB')
a = np.asarray(img).astype(int)
r,g,b = a[:,:,0],a[:,:,1],a[:,:,2]
dark=(r<200)&(g<200)&(b<200)
def ink(x0,x1,y0,y1,label):
    ys,xs=np.where(dark[y0:y1,x0:x1])
    if len(xs)==0: print(label,"EMPTY"); return
    print(f"{label}: x {xs.min()+x0}..{xs.max()+x0} y {ys.min()+y0}..{ys.max()+y0} n={len(xs)}")
for lab,(x0,x1) in [("col1",(60,320)),("col2",(400,640)),("col3",(660,900))]:
    ink(x0,x1,480,518,f"{lab} caption")
def fine(x0,x1,y0,y1,label):
    print(f"== {label}")
    for y in range(y0,y1):
        row=""
        for x in range(x0,x1):
            R,G,B=a[y,x]
            if R+G+B<430: row+='K'
            elif R>235 and G>235 and B>225: row+=' '
            else: row+='.'
        print(f"{y:3d} {row}")
fine(125,320,482,516,"col1 caption fine")
