from PIL import Image
import numpy as np
from scipy import ndimage
img = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_034.jpg').convert('RGB')
a = np.asarray(img).astype(int)
r,g,b = a[:,:,0],a[:,:,1],a[:,:,2]

def inkbox(x0,x1,y0,y1,cond,label):
    sub = cond[y0:y1,x0:x1]
    ys,xs=np.where(sub)
    if len(xs)==0: print(f"{label}: EMPTY"); return
    print(f"{label}: x {xs.min()+x0}..{xs.max()+x0} y {ys.min()+y0}..{ys.max()+y0}")
    return (xs.min()+x0,xs.max()+x0,ys.min()+y0,ys.max()+y0)

dark = (r<130)&(g<130)&(b<130)
# title + subtitle precise
inkbox(100,860,50,78,dark,"title ink")
inkbox(100,860,78,102,dark,"subtitle dark ink")
orange = (r>200)&(g>120)&(g<200)&(b<110)&((r-b)>110)
inkbox(150,400,80,105,orange,"subtitle orange")
# concept box border: loose green
lgreen = ((g-r)>15)&((g-b)>10)&(g>110)
lab,n=ndimage.label(lgreen[95:280, 40:420])
sizes=[]
for i in range(1,n+1):
    ys,xs=np.where(lab==i)
    if len(xs)<40: continue
    sizes.append((xs.min()+40,xs.max()+40,ys.min()+95,ys.max()+95,len(xs)))
sizes.sort(key=lambda t:-t[4])
print("concept-box loose-green big comps:")
for s in sizes[:6]: print("   ",s)

# eq box in concept (large): dark ink in y 105..165 x 60..240
inkbox(60,245,108,165,dark,"concept large eq ink")
# red embedding symbol in concept top-right
red = (r>140)&((r-g)>60)&((r-b)>60)
inkbox(245,395,105,165,red,"concept [X_i] red ink")
# green d label mid-left + arrow + small eq ink
inkbox(55,150,170,215,lgreen,"concept d-up label")
inkbox(190,235,165,215,lgreen,"concept green arrow")
inkbox(235,395,165,215,dark,"small eq ink")
# annotation lines: blue text
blueT = (b>130)&((b-r)>40)&(r<160)
inkbox(55,395,210,240,blueT,"annot line1 blue")
inkbox(55,395,238,262,blueT,"annot line2 blue")
inkbox(55,395,210,240,dark,"annot line1 dark")
inkbox(55,395,238,262,dark,"annot line2 dark")
inkbox(55,395,210,240,orange,"annot orange hl")
yellow=(r>200)&(g>190)&(b<150)
inkbox(55,395,210,240,yellow,"annot yellow hl")
