from PIL import Image
import numpy as np
from scipy import ndimage
im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_036.jpg').convert('RGB')
a = np.asarray(im).astype(int)

def px(x,y): return tuple(a[y,x])
def fill(x,y,label):
    print(f'{label}: {px(x,y)} {px(x+3,y)} {px(x,y+3)}')

# fills
fill(450,180,'EQBOX fill')
fill(480,255,'STMT1 fill')
fill(750,255,'STMT2 fill')
fill(750,330,'FBOX3 fill')
fill(400,330,'FBOX1 fill')
fill(100,450,'REMEMBER fill')
fill(700,450,'FC2 fill')
fill(120,200,'VEC container fill')
fill(340,480,'FC1 fill')
fill(780,160,'BELL fill')

# BELL internals: grid lines, curve, axes, dashed line, M label
print()
reg = a[110:220, 683:894]
l = reg.mean(axis=2)
# gray grid (D9D9D9 ~217): find rows/cols mostly 200-235 gray
gray = (abs(reg[:,:,0]-217)<28)&(abs(reg[:,:,1]-217)<28)&(abs(reg[:,:,2]-217)<28)&(abs(reg[:,:,0]-reg[:,:,2])<14)
rows = np.where(gray.sum(axis=1)>100)[0]+110
cols = np.where(gray.sum(axis=0)>60)[0]+683
print('BELL grid rows:', list(rows))
print('BELL grid cols:', list(cols))
# curve 9DB2C8 ~(157,178,200)
curve = (abs(reg[:,:,0]-157)<45)&(abs(reg[:,:,1]-178)<40)&(abs(reg[:,:,2]-200)<40)&(reg[:,:,2]>reg[:,:,0]+20)
ys,xs = np.where(curve)
if len(xs): print('BELL curve bbox: x%d..%d y%d..%d n=%d' % (xs.min()+683,xs.max()+683,ys.min()+110,ys.max()+110,len(xs)))
# red axes
red = (reg[:,:,0]>reg[:,:,1]+50)&(reg[:,:,0]>100)&(l<200)
ys,xs = np.where(red)
if len(xs):
    print('BELL red bbox: x%d..%d y%d..%d n=%d' % (xs.min()+683,xs.max()+683,ys.min()+110,ys.max()+110,len(xs)))
    # axis lines: columns/rows with many red px
    colsum = red.sum(axis=0); rowsum = red.sum(axis=1)
    print('  red cols>30:', [c+683 for c in np.where(colsum>30)[0]])
    print('  red rows>30:', [r+110 for r in np.where(rowsum>30)[0]])
# blue dashed vertical
blue = (reg[:,:,2]>reg[:,:,0]+40)&(l<210)
ys,xs = np.where(blue)
colsum = blue.sum(axis=0)
print('BELL blue cols>10:', [c+683 for c in np.where(colsum>10)[0]])
# M label below x-axis: blue text y207..216? earlier bands: blue y207..216 = border. Search inside y195..218 x686..889
lab = a[195:218, 690:890]
ll = lab.mean(axis=2)
bl = (lab[:,:,2]>lab[:,:,0]+40)&(ll<210)
ys,xs = np.where(bl)
if len(xs): print('BELL M label blue bbox: x%d..%d y%d..%d n=%d' % (xs.min()+690,xs.max()+690,ys.min()+195,ys.max()+195,len(xs)))
