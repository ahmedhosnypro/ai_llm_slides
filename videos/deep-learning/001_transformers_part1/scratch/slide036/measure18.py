from PIL import Image
import numpy as np
from scipy import ndimage
im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_036.jpg').convert('RGB')
a = np.asarray(im).astype(int)

def ccboxes(x0,y0,x1,y1,mode,minpx=10,merge=1):
    reg = a[y0:y1, x0:x1]
    l = reg.mean(axis=2)
    if mode=='red':  m = (reg[:,:,0] > reg[:,:,1]+45) & (reg[:,:,0] > 90) & (l < 210)
    elif mode=='blue': m = (reg[:,:,2] > reg[:,:,0]+40) & (l < 210)
    elif mode=='tan': m = (reg[:,:,0]>230)&(reg[:,:,1]>195)&(reg[:,:,1]<235)&(reg[:,:,2]<190)
    m = ndimage.binary_dilation(m.astype(np.uint8), iterations=merge)
    lab,n = ndimage.label(m)
    out=[]
    for i in range(1,n+1):
        ys,xs = np.where(lab==i)
        if len(xs)<minpx: continue
        out.append((xs.min()+x0, ys.min()+y0, xs.max()+x0, ys.max()+y0, len(xs)))
    out.sort(key=lambda t:(t[1], t[0]))
    return out

print('FC1 LEFT: red CC x295..345 y408..522:')
for b in ccboxes(295,408,345,522,'red'): print('   x%d..%d y%d..%d (w%d h%d) n=%d'%(b[0],b[2],b[1],b[3],b[2]-b[0]+1,b[3]-b[1]+1,b[4]))
print('FC1 LEFT: tan CC:')
for b in ccboxes(295,408,345,522,'tan',6): print('   x%d..%d y%d..%d (w%d h%d) n=%d'%(b[0],b[2],b[1],b[3],b[2]-b[0]+1,b[3]-b[1]+1,b[4]))
print('FC1 RIGHT: blue CC x415..495 y383..522:')
for b in ccboxes(415,383,495,522,'blue'): print('   x%d..%d y%d..%d (w%d h%d) n=%d'%(b[0],b[2],b[1],b[3],b[2]-b[0]+1,b[3]-b[1]+1,b[4]))
# colors of chip borders + fills
print('chip border color (310,426):', tuple(a[426,310]), ' (310,456):', tuple(a[456,310]), ' (310,488):', tuple(a[488,310]))
print('chip fill (315,440):', tuple(a[440,315]), '(315,470):', tuple(a[470,315]), '(315,497):', tuple(a[497,315]))
print('right chip border (450,395):', tuple(a[395,450]), 'fill (450,405):', tuple(a[405,450]))
print('paren colors: (303,440):', tuple(a[440,303]), '(334,440):', tuple(a[440,334]), '(425,450):', tuple(a[450,425]), '(481,450):', tuple(a[450,481]))
print('arrow color (380,457):', tuple(a[457,380]), 'label color (365,436):', tuple(a[436,365]))
