from PIL import Image
import numpy as np
V='/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction'
f16=np.asarray(Image.open(V+'/unique_slides/slide_016.jpg').convert('RGB')).astype(int)

# 1) last box: rows/cols of tan fill + border color
reg=f16[200:280,740:880]
tan=(reg[:,:,0]>195)&(reg[:,:,0]<235)&(reg[:,:,1]>160)&(reg[:,:,1]<205)&(reg[:,:,2]>120)&(reg[:,:,2]<180)
rows=tan.sum(axis=1);cols=tan.sum(axis=0)
rr=[i for i,c in enumerate(rows) if c>30]; cc=[i for i,c in enumerate(cols) if c>30]
print('tan fill rows:',200+rr[0],'..',200+rr[-1],' cols:',740+cc[0],'..',740+cc[-1])
# border: dark maroon pixels around box
dark=(reg.max(axis=2)<130)
ys,xs=np.where(dark)
print('dark border bbox in x740..880 y200..280:',(740+xs.min(),200+ys.min(),740+xs.max(),200+ys.max()),'count',len(ys))
print('border sample colors:',[tuple(f16[209,x]) for x in (748,750,760,800,860,862)],'left edge',[tuple(f16[y,749]) for y in (210,236,260)])
print('right edge col scan y236:',[(x,tuple(f16[236,x])) for x in range(859,868)])

# text bands inside last box (dark ink on tan)
sub=f16[208:266,752:862]
m=sub.max(axis=2)<120
rws=m.sum(axis=1)
bands=[];inr=False
for i,c in enumerate(rws):
    if c>1 and not inr: s=i;inr=True
    if c<=1 and inr: bands.append((208+s,208+i-1));inr=False
if inr: bands.append((208+s,265))
print('last-box text bands:',bands)
for b in bands:
    mm=f16[b[0]:b[1]+1,752:862].max(axis=2)<120
    ccols=mm.sum(axis=0); xs=np.where(ccols>0)[0]
    print('  band',b,'cols',752+xs.min(),'..',752+xs.max())

# 2) below-box area rows 265..330 x740..900: any red curve or other ink?
sub=f16[266:340,700:920]
red=(sub[:,:,0]>150)&(sub[:,:,1]<90)&(sub[:,:,2]<90)
ys,xs=np.where(red)
print('red ink below post box (y266..340,x700..920):', (700+xs.min(),266+ys.min(),700+xs.max(),266+ys.max()) if len(ys) else None, int(red.sum()))
dark2=(sub.max(axis=2)<150)
ys,xs=np.where(dark2)
print('dark ink below post box:', (700+xs.min(),266+ys.min(),700+xs.max(),266+ys.max()) if len(ys) else None, int(dark2.sum()))
