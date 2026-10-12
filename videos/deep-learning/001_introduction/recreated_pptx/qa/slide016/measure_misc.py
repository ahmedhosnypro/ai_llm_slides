from PIL import Image
import numpy as np
from collections import Counter
V='/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction'
f16=np.asarray(Image.open(V+'/unique_slides/slide_016.jpg').convert('RGB')).astype(int)
f09=np.asarray(Image.open(V+'/unique_slides/slide_009.jpg').convert('RGB')).astype(int)
d=(np.abs(f16-f09).max(axis=2)>40)
sub=d[265:360,700:800]
ys,xs=np.where(sub)
print('diff px in x700..800 y265..360:',len(ys))
if len(ys):
    print(' bbox y',265+ys.min(),'..',265+ys.max(),' x',700+xs.min(),'..',700+xs.max())
    # what is in f16 there?
    y0,y1,x0,x1=265+ys.min(),265+ys.max(),700+xs.min(),700+xs.max()
    reg=f16[y0:y1+1,x0:x1+1]
    cnt=Counter(map(tuple,reg.reshape(-1,3)))
    print(' f16 modal:',cnt.most_common(5))
    print(' f09 modal:',Counter(map(tuple,f09[y0:y1+1,x0:x1+1].reshape(-1,3))).most_common(3))
# box4 region diff
sub=d[205:268,560:745]
print('box4 zone diff px:',int(sub.sum()))
# box5 border ring diff (outer 2px)
sub=d[205:268,744:868]
print('box5 zone diff px:',int(sub.sum()))
# callout corner radius: callout A top-left corner (x85..100, y291..305)
print('callout A corner map (x84..104, y290..306):')
for y in range(290,307):
    line=''
    for x in range(84,105):
        r,g,b=f16[y,x]
        if abs(r-g)<12 and abs(g-b)<12 and 195<r<246: line+='#'
        elif r>200 and g>200 and b>200: line+='.'
        elif max(r,g,b)<120: line+='K'
        else: line+='o'
    print(f'{y:3d} {line}')
# callout A border modal (ring pixels darker gray)
reg=f16[289:334,84:280]
m=(np.abs(reg[:,:,0]-reg[:,:,1])<14)&(np.abs(reg[:,:,1]-reg[:,:,2])<14)&(reg[:,:,0]>150)&(reg[:,:,0]<215)
cnt=Counter(map(tuple,reg[m]))
print('callout A ring modal:',cnt.most_common(4))
