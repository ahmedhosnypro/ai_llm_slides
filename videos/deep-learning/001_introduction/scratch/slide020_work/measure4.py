from PIL import Image
import numpy as np
from collections import Counter
im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_020.jpg').convert('RGB')
a = np.asarray(im).astype(int)
r,g,b = a[:,:,0],a[:,:,1],a[:,:,2]

def modal_mask(mask,label,q=8):
    reg = mask
    if len(reg)==0: print(label,"EMPTY"); return
    qq = (reg//q*q); cnt = Counter(map(tuple,qq))
    (c,n)=cnt.most_common(1)[0]
    print(f"{label:28s} modal#{c[0]+4:02X}{c[1]+4:02X}{c[2]+4:02X} n={n}/{len(reg)}")

blue = (b>120)&(b-r>60)&(b-g>40)
green = (g-r>25)&(g-b>15)&(g>70)&(g<210)
red = (r>120)&(g<100)&(b<100)&((r-g)>60)

modal_mask(a[125:145,290:375][blue[125:145,290:375]],"blue shaft left core")
modal_mask(a[295:330,700:790][green[295:330,700:790]],"green conv core")
modal_mask(a[230:242,160:195][red[230:242,160:195]],"red arrow core")
modal_mask(a[60:95,215:660][red[60:95,215:660]],"title red core")
modal_mask(a[195:280,190:640][red[195:280,190:640]],"container dash red core")

print("--- green rows (y260..334) ---")
for y in range(260,335,3):
    m = np.where(green[y,:])[0]
    if len(m):
        groups = np.split(m, np.where(np.diff(m)>6)[0]+1)
        print(f"  y={y}: {'  '.join(f'{gp.min()}-{gp.max()}' for gp in groups)}")
print("--- blue rows x>480 (y128..214) ---")
for y in range(128,215,3):
    m = np.where(blue[y,480:960])[0]
    if len(m):
        groups = np.split(m, np.where(np.diff(m)>6)[0]+1)
        print(f"  y={y}: {'  '.join(f'{gp.min()+480}-{gp.max()+480}' for gp in groups)}")
m = np.where(red[235,60:900])[0]+60
groups = np.split(m, np.where(np.diff(m)>4)[0]+1)
print("red y=235 runs:", [f"{gp.min()}-{gp.max()}" for gp in groups])
m = np.where(red[237,60:900])[0]+60
groups = np.split(m, np.where(np.diff(m)>4)[0]+1)
print("red y=237 runs:", [f"{gp.min()}-{gp.max()}" for gp in groups])
for (x0,x1,lbl) in [(160,196,"a1 In->Cont"),(280,332,"a2 Pre->FE"),(402,430,"a3 FE->FS"),(512,535,"a4 FS->Cl"),(630,660,"a5 Cl->PL"),(739,754,"a6 PL->Err"),(791,808,"a7 Sm->Err")]:
    sub = red[225:245, x0:x1]
    ys,xs = np.where(sub)
    if len(ys): print(f"  {lbl}: x[{xs.min()+x0}..{xs.max()+x0}] y[{ys.min()+225}..{ys.max()+225}]")
