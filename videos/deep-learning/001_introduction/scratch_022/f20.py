from PIL import Image
import numpy as np
from collections import Counter
im = np.asarray(Image.open('unique_slides/slide_022.jpg').convert('RGB')).astype(int)
r, g, b = im[:,:,0], im[:,:,1], im[:,:,2]
lum = (r+g+b)/3
def modal_ink(x0,y0,x1,y1,label,maxlum=200):
    reg = im[y0:y1, x0:x1].reshape(-1,3)
    ink = reg[reg.mean(axis=1) < maxlum]
    if not len(ink): print(label, 'no ink'); return
    c = Counter(map(tuple, (ink//8*8)))
    top = c.most_common(4)
    print(f'{label}:', ' | '.join('%02X%02X%02X x%d' % (t[0][0],t[0][1],t[0][2],t[1]) for t in top))
modal_ink(413,404,452,440,'sigma circle (ring+fill)')
modal_ink(416,410,445,432,'sigma interior fill')
modal_ink(414,403,452,409,'sigma ring top')
modal_ink(468,405,512,438,'circle2 (ring+fill)')
modal_ink(450,418,470,424,'arrow1 line')
modal_ink(512,419,560,423,'arrow2 line')
modal_ink(575,415,610,430,'O/P text')
modal_ink(244,354,262,370,'input x1 label')
modal_ink(244,486,262,502,'input 1 label (red)')
modal_ink(288,354,318,370,'weight w1 label')
modal_ink(360,368,396,416,'fan line sample area')
modal_ink(630,400,818,446,'callout fill', 250)
# darkest callout text
reg = im[405:442, 635:812].reshape(-1,3)
ink = reg[reg.mean(axis=1) < 130]
c = Counter(map(tuple, (ink//8*8)))
print('callout text dark modal:', ' | '.join('%02X%02X%02X x%d' % (t[0][0],t[0][1],t[0][2],t[1]) for t in c.most_common(4)))
# label blue modals
for (x0,y0,x1,y1,lab) in [(300,158,406,176,'aug label'),(668,158,764,176,'weights label'),(288,354,318,500,'weights col diagram'),(555,262,748,330,'cases')]:
    reg = im[y0:y1, x0:x1].reshape(-1,3)
    ink = reg[(reg[:,2]-reg[:,0] > 40)]
    if len(ink):
        c = Counter(map(tuple, (ink//8*8)))
        print(lab, 'blue modal:', ' | '.join('%02X%02X%02X x%d' % (t[0][0],t[0][1],t[0][2],t[1]) for t in c.most_common(3)))
# input/weight label rows: dark+blue bands in left two columns of diagram
def rowbands(x0,x1,y0,y1,label):
    sub = ((lum<150) | ((b-r)>35))[y0:y1, x0:x1]
    rc = sub.sum(axis=1); bands=[]; s=None
    for i,v in enumerate(rc):
        if v>0 and s is None: s=i
        elif v==0 and s is not None: bands.append((y0+s,y0+i-1)); s=None
    if s is not None: bands.append((y0+s,y1-1))
    print(label, bands)
rowbands(242,266,352,508,'input labels rows')
rowbands(286,322,352,508,'weight labels rows')
def colbands(y0,y1,x0,x1,label):
    sub = ((lum<150) | ((b-r)>35) | ((r-g)>40))[y0:y1, x0:x1]
    cc = sub.sum(axis=0); bands=[]; s=None
    for i,v in enumerate(cc):
        if v>0 and s is None: s=i
        elif v==0 and s is not None: bands.append((x0+s,x0+i-1)); s=None
    if s is not None: bands.append((x0+s,x1-1))
    print(label, bands)
colbands(352,508,236,330,'label cols')
