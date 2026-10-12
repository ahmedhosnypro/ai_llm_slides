from PIL import Image
import numpy as np
from collections import Counter
im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_020.jpg').convert('RGB')
a = np.asarray(im).astype(int)
r,g,b = a[:,:,0],a[:,:,1],a[:,:,2]
red = (r>110)&(g<105)&(b<105)&((r-g)>50)
white = (r>235)&(g>235)&(b>235)
dark = (r<110)&(g<110)&(b<110)

def bbox(mask,label):
    ys,xs = np.where(mask)
    if len(ys)==0: print(label,"EMPTY"); return None
    print(f"{label:30s} x[{xs.min()}..{xs.max()+1}) y[{ys.min()}..{ys.max()+1}) w={xs.max()-xs.min()+1} h={ys.max()-ys.min()+1} n={len(ys)}")
    return (xs.min(),ys.min(),xs.max()+1,ys.max()+1)

def modal(x0,y0,x1,y1,label,q=6):
    reg = a[y0:y1,x0:x1].reshape(-1,3)
    qq=(reg//q*q); cnt=Counter(map(tuple,qq)); (c,n)=cnt.most_common(1)[0]
    print(f"{label:30s} modal#{c[0]+3:02X}{c[1]+3:02X}{c[2]+3:02X} n={n}/{len(reg)}")

# block arrows core
modal(596,395,612,420,"blockarrow1 core")
modal(771,320,787,342,"blockarrow2 core")
# borders cores
modal(205,206,278,209,"Pre top border row")
modal(333,206,400,209,"FE top border row")
modal(430,206,510,209,"FS top border row")
modal(536,206,628,209,"Class top border row")
modal(660,213,737,216,"PL top border row")
modal(84,213,154,216,"Input top border row")
modal(810,213,882,216,"Samples top border row")
# classification white text
bbox(white[225:248, 536:628], "Classification white text (+536,+225)")
# error box text: red inside x755..789 y175..296
sub = red[175:296, 755:790]
ys,xs = np.where(sub)
print("error text red: x", xs.min()+755, xs.max()+755, "y", ys.min()+175, ys.max()+175)
# per-column red counts to find the two vertical lines
colcnt = sub.sum(axis=0)
print("err text colcounts:", {i+755:int(colcnt[i]) for i in range(len(colcnt)) if colcnt[i]>3})
# title bbox (threshold lower)
tred = (r>140)&(g<120)&(b<120)&((r-g)>40)
sub2 = tred[50:100, 100:900]
ys,xs = np.where(sub2)
print("title red: x", xs.min()+100, xs.max()+100, "y", ys.min()+50, ys.max()+50)
# ellipse text (dark inside ellipse fill x376..464 y114..156)
sub3 = dark[114:156, 376:464]
ys,xs = np.where(sub3)
print("ellipse text: x", xs.min()+376, xs.max()+376, "y", ys.min()+114, ys.max()+114)
rows = sub3.sum(axis=1)
print("ellipse text rows:", {i+114:int(rows[i]) for i in range(len(rows)) if rows[i]>0})
# green box text lines
gtext = (g-r>30)&(g-b>20)&(g<180)
sub4 = gtext[340:378, 266:740]
ys,xs = np.where(sub4)
print("green text: x", xs.min()+266, xs.max()+266, "y", ys.min()+340, ys.max()+340)
rows = sub4.sum(axis=1)
bands=[]; inb=False
for i,c in enumerate(rows):
    if c>0 and not inb: inb=True; s=i
    if c==0 and inb: inb=False; bands.append((s+340,i+340))
if inb: bands.append((s+340,len(rows)+340))
print("green text line bands:", bands)
# starburst: yellow modal + red outline bbox + text
yellow = (r>230)&(g>225)&(b<190)
sub5 = yellow[370:445, 700:890]
ys,xs = np.where(sub5)
print("starburst yellow: x", xs.min()+700, xs.max()+700, "y", ys.min()+370, ys.max()+370, "n", len(ys))
modal(770,400,840,418,"starburst yellow core")
sub6 = red[370:445, 700:890]
ys,xs = np.where(sub6)
print("starburst red outline: x", xs.min()+700, xs.max()+700, "y", ys.min()+370, ys.max()+370)
# starburst text (red inside yellow area): red within x735..855 y390..430
sub7 = red[390:432, 735:860]
ys,xs = np.where(sub7)
print("starburst text: x", xs.min()+735, xs.max()+735, "y", ys.min()+390, ys.max()+390)
# black bar
black = (r<70)&(g<70)&(b<70)
sub8 = black[505:540, :]
ys,xs = np.where(sub8)
print("black bar: x", xs.min(), xs.max()+1, "y", ys.min()+505, ys.max()+505+1)
rows = sub8.sum(axis=1)
print("blackbar rows:", {i+505:int(rows[i]) for i in range(len(rows)) if rows[i]>100})
