from PIL import Image
import numpy as np
NS = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction"
ren = np.asarray(Image.open(f"{NS}/recreated_pptx/qa/slide012/render_1.png").convert('RGB')).astype(int)
org = np.asarray(Image.open(f"{NS}/unique_slides/slide_012.jpg").convert('RGB')).astype(int)
S = ren.shape[1]/960.0
def bb(arr,k,y0,y1,x0,x1,skipx=None):
    H,W=arr.shape[:2]
    pts=[(y,x) for y in range(max(0,int(y0*k)),min(H-1,int(y1*k))+1) for x in range(max(0,int(x0*k)),min(W-1,int(x1*k))+1)
         if arr[y,x].sum()<430 and not (skipx and skipx[0]<=x/k<=skipx[1])]
    if not pts: return None
    ys=[p[0] for p in pts]; xs=[p[1] for p in pts]
    return (min(ys)/k,max(ys)/k,min(xs)/k,max(xs)/k)
bands = [("bullet1",228,256,None),("bullet2",272,300,None),("bullet3",316,344,(184,216)),("bullet4",360,388,None)]
for name,y0,y1,skip in bands:
    o = bb(org,1.0,y0,y1,100,870,skip)
    r = bb(ren,S,y0,y1,100,870,tuple(v*S for v in skip) if skip else None)
    d = [r[i]-o[i] for i in range(4)]
    print(f"  {name}: orig y{o[0]:.1f}..{o[1]:.1f} x{o[2]:.1f}..{o[3]:.1f} | rend y{r[0]:.1f}..{r[1]:.1f} x{r[2]:.1f}..{r[3]:.1f} | d {d[0]:+.1f}/{d[1]:+.1f}/{d[2]:+.1f}/{d[3]:+.1f} {'OK' if all(abs(v)<=4 for v in d) else 'CHECK'}")
