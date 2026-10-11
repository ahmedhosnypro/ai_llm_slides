from PIL import Image
import numpy as np
from scipy import ndimage
img = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_034.jpg').convert('RGB')
a = np.asarray(img).astype(int)
r,g,b = a[:,:,0],a[:,:,1],a[:,:,2]

def comps(name, mask, minpx=30):
    lab,n = ndimage.label(mask)
    out=[]
    for i in range(1,n+1):
        ys,xs = np.where(lab==i)
        if len(xs)<minpx: continue
        out.append((xs.min(),xs.max(),ys.min(),ys.max(),len(xs)))
    out.sort(key=lambda t:(t[2],t[0]))
    print(f"== {name} ({len(out)} comps)")
    for x0,x1,y0,y1,npx in out: print(f"   x {x0}..{x1} y {y0}..{y1} px{npx}")
    return out

# peach panel (looser)
peach = (r>235)&(g>210)&(g<245)&(b>190)&(b<235)&((r-b)>20)
comps("peach", peach)
# yellow: input value boxes + highlights
yellow = (r>200)&(g>190)&(b<150)&((r-b)>80)
comps("yellow", yellow)
# white boxes w/ colored borders: find RED border boxes (input frame? no—inputs are yellow fill w/ red border)
# find thick red block arrows (solid red blobs)
red = (r>150)&((r-g)>70)&((r-b)>70)
comps("red-blobs", red, 100)
# blue: output boxes' borders + parens + warning border/text
blue = (b>130)&((b-r)>50)&((b-g)>30)&(r<150)
comps("blue", blue, 25)
# green text/arrow
green = ((g-r)>40)&((g-b)>40)&(g>100)
comps("green", green, 25)
