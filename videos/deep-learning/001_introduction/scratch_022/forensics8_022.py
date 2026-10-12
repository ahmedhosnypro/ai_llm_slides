from PIL import Image
import numpy as np
from scipy import ndimage
im = np.asarray(Image.open('unique_slides/slide_022.jpg').convert('RGB')).astype(int)
r, g, b = im[:,:,0], im[:,:,1], im[:,:,2]
lum = (r+g+b)/3
red = (r>120)&(g<95)&(b<95)&(r-g>60)
dark = lum < 120
blue = (b>130)&(b-r>60)&(b-g>40)

def comps(mask, x0,y0,x1,y1,label,mine=6):
    sub = mask[y0:y1, x0:x1]
    lab, n = ndimage.label(sub, structure=np.ones((3,3)))
    out=[]
    for i in range(1, n+1):
        ys, xs = np.where(lab==i)
        if len(ys) < mine: continue
        out.append((x0+xs.min(), y0+ys.min(), x0+xs.max(), y0+ys.max(), len(ys)))
    out.sort(key=lambda t:(t[1],t[0]))
    print(label)
    for c in out: print('   x %d..%d y %d..%d n%d' % c)

print('--- decision box RED components ---')
comps(red, 83,255,766,343, 'red')
print('--- decision box BLACK components (cols grouped) ---')
comps(dark, 83,255,560,343, 'black-left')
print('--- decision box BLUE comps ---')
comps(blue, 540,255,766,343, 'blue')
print('--- aug box RED comps ---')
comps(red, 84,90,418,245, 'red')
print('--- weights box RED comps ---')
comps(red, 530,90,792,245, 'red')
print('--- diagram box: cyan / pink / red / blue ---')
cyan = (b>200)&(g>190)&(r<200)&(b-r>30)
comps(cyan, 230,352,612,507, 'cyan')
pinkm = (r>210)&(b>150)&(g<200)&(r-g>30)
comps(pinkm, 230,352,612,507, 'pink')
comps(red, 230,352,612,507, 'red')
comps(blue, 230,352,612,507, 'blue')
