from PIL import Image
import numpy as np
from scipy import ndimage
im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_036.jpg').convert('RGB')
a = np.asarray(im).astype(int)

def ccboxes(x0,y0,x1,y1,mode,minpx=6,merge=3):
    reg = a[y0:y1, x0:x1]
    l = reg.mean(axis=2)
    if mode=='dark':   m = l < 170
    elif mode=='blue': m = (reg[:,:,2] > reg[:,:,0]+40) & (l < 200)
    elif mode=='red':  m = (reg[:,:,0] > reg[:,:,1]+50) & (reg[:,:,0] > 100) & (l < 200)
    elif mode=='tan':  m = (abs(reg[:,:,0]-255)<45)&(abs(reg[:,:,1]-230)<45)&(reg[:,:,2]<200)
    elif mode=='pinkfill': m = (reg[:,:,0]>240)&(abs(reg[:,:,1]-228)<25)&(abs(reg[:,:,2]-228)<25)
    m = m.astype(np.uint8)
    m = ndimage.binary_dilation(m, iterations=merge)  # merge nearby glyphs into words/lines
    lab,n = ndimage.label(m)
    out=[]
    for i in range(1,n+1):
        ys,xs = np.where(lab==i)
        if len(xs)<minpx: continue
        out.append((xs.min()+x0, ys.min()+y0, xs.max()+x0, ys.max()+y0, len(xs)))
    out.sort(key=lambda t:(t[1]//8, t[0]))
    return out

def show(label, boxes):
    print(label)
    for b in boxes: print('   x%d..%d y%d..%d (w%d h%d) n=%d' % (b[0],b[2],b[1],b[3],b[2]-b[0]+1,b[3]-b[1]+1,b[4]))

# VECTOR CONTAINER pieces
show('VEC blue text/borders (x50..268 y103..370):', ccboxes(50,103,268,370,'blue',4,2))
show('VEC red (x50..268 y103..370):', ccboxes(50,103,268,370,'red',8,2))
