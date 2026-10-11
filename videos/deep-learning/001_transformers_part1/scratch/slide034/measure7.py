from PIL import Image
import numpy as np
from scipy import ndimage
img = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_034.jpg').convert('RGB')
a = np.asarray(img).astype(int)
r,g,b = a[:,:,0],a[:,:,1],a[:,:,2]

def inkbox(x0,x1,y0,y1,cond,label):
    sub = cond[y0:y1,x0:x1]
    ys,xs=np.where(sub)
    if len(xs)==0: print(f"{label}: EMPTY"); return None
    res=(xs.min()+x0,xs.max()+x0,ys.min()+y0,ys.max()+y0)
    print(f"{label}: x {res[0]}..{res[1]} y {res[2]}..{res[3]}")
    return res

dark=(r<130)&(g<130)&(b<130)
red=(r>140)&((r-g)>60)&((r-b)>60)
blue=(b>120)&((b-r)>40)&(r<170)
green=((g-r)>30)&((g-b)>25)&(g>100)
yellow=(r>200)&(g>190)&(b<150)
orange=(r>200)&(g>110)&(g<205)&(b<120)

# peach panel bbox precise (loose peach, largest comp already x48..868 y276..529)
print("PANEL: x 48..868 y 276..529 (from comp)")
# header row: embedding box red border
inkbox(40,140,270,360,red,"emb box red border")
# SoftMax label
inkbox(150,250,285,335,red,"SoftMax red label")
# softmax fraction eq: dark ink + gray borders
gray=(abs(r-g)<18)&(abs(g-b)<18)&(r>90)&(r<215)
inkbox(240,400,275,350,dark,"frac eq dark ink")
inkbox(240,400,275,350,gray,"frac eq gray")
# warning strip: blue border + text
inkbox(390,880,270,340,blue,"warning blue all")
# demo column headers (green)
inkbox(60,200,310,360,green,"col1 header green")
inkbox(390,460,310,360,green,"col2 header green")
inkbox(660,740,310,360,green,"col3 header green")
# input stacks: yellow boxes bbox per column
inkbox(125,180,350,495,yellow,"col1 yellow boxes")
inkbox(395,450,350,495,yellow,"col2 yellow boxes")
inkbox(663,720,350,495,yellow,"col3 yellow boxes")
# output stacks: white boxes w/ blue borders -> find blue bboxes
inkbox(240,320,350,495,blue,"col1 blue all")
inkbox(505,590,350,495,blue,"col2 blue all")
inkbox(775,860,350,495,blue,"col3 blue all")
# orange SoftMax labels above arrows
inkbox(170,260,395,425,orange,"col1 SoftMax orange")
inkbox(435,530,395,425,orange,"col2 SoftMax orange")
inkbox(700,800,395,425,orange,"col3 SoftMax orange")
# captions below: dark ink
inkbox(60,200,485,520,dark,"col1 caption")
inkbox(430,560,485,520,dark,"col2 caption")
inkbox(700,830,485,520,dark,"col3 caption")
# input values dark text inside yellow
inkbox(133,166,360,485,dark,"col1 input digits")
