from PIL import Image
import numpy as np
img = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_034.jpg').convert('RGB')
a = np.asarray(img).astype(int)
r,g,b = a[:,:,0],a[:,:,1],a[:,:,2]
dark=(r<170)&(g<170)&(b<170)
def ink(x0,x1,y0,y1,label):
    ys,xs=np.where(dark[y0:y1,x0:x1])
    if len(xs)==0: print(label,"EMPTY"); return
    print(f"{label}: x {xs.min()+x0}..{xs.max()+x0} y {ys.min()+y0}..{ys.max()+y0} n={len(xs)}")
ink(60,880,55,76,"TITLE")
ink(60,880,79,100,"SUBTITLE")
ink(398,862,288,308,"WARNING text")
ink(170,250,298,320,"SoftMax header label")
ink(130,180,482,514,"col1 caption")
ink(420,560,482,514,"col2 caption")
ink(690,820,482,514,"col3 caption")
ink(55,270,215,240,"annot line1")
ink(55,270,240,262,"annot line2")
ink(246,400,284,340,"fraction eq ink")
ink(60,200,115,160,"large eq ink")
# panel eq box white fill rows
