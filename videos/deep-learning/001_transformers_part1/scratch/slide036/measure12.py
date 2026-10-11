from PIL import Image
import numpy as np
from scipy import ndimage
im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_036.jpg').convert('RGB')
a = np.asarray(im).astype(int)

def ccboxes(x0,y0,x1,y1,mode,minpx=5,merge=2):
    reg = a[y0:y1, x0:x1]
    l = reg.mean(axis=2)
    if mode=='dark':   m = l < 170
    elif mode=='blue': m = (reg[:,:,2] > reg[:,:,0]+40) & (l < 200)
    elif mode=='red':  m = (reg[:,:,0] > reg[:,:,1]+40) & (reg[:,:,0] > 80) & (l < 210)
    m = ndimage.binary_dilation(m.astype(np.uint8), iterations=merge)
    lab,n = ndimage.label(m)
    out=[]
    for i in range(1,n+1):
        ys,xs = np.where(lab==i)
        if len(xs)<minpx: continue
        out.append((xs.min()+x0, ys.min()+y0, xs.max()+x0, ys.max()+y0, len(xs)))
    out.sort(key=lambda t:(t[1], t[0]))
    return out

print('RIGHT V2 col region x206..270 y128..245:')
print(' blue:');  [print('   x%d..%d y%d..%d (w%d h%d)'%(b[0],b[2],b[1],b[3],b[2]-b[0]+1,b[3]-b[1]+1)) for b in ccboxes(206,128,270,245,'blue')]
print(' red:');   [print('   x%d..%d y%d..%d (w%d h%d)'%(b[0],b[2],b[1],b[3],b[2]-b[0]+1,b[3]-b[1]+1)) for b in ccboxes(206,128,270,245,'red')]
print()
print('BOTTOM strip x46..270 y340..372:')
print(' red:');   [print('   x%d..%d y%d..%d (w%d h%d)'%(b[0],b[2],b[1],b[3],b[2]-b[0]+1,b[3]-b[1]+1)) for b in ccboxes(46,340,270,372,'red')]
print()
print('12-M col region x165..205 y128..345 (blue):')
bs = ccboxes(165,128,205,345,'blue')
print('   count', len(bs)); [print('   x%d..%d y%d..%d (w%d h%d)'%(b[0],b[2],b[1],b[3],b[2]-b[0]+1,b[3]-b[1]+1)) for b in bs]
print()
print('LEFT V1 col region x48..90 y128..345 (red):')
bs = ccboxes(48,128,90,345,'red')
print('   count', len(bs)); [print('   x%d..%d y%d..%d (w%d h%d)'%(b[0],b[2],b[1],b[3],b[2]-b[0]+1,b[3]-b[1]+1)) for b in bs]
print()
print('LEFT V2 col region x92..150 y128..232 (red):')
bs = ccboxes(92,128,150,232,'red')
print('   count', len(bs)); [print('   x%d..%d y%d..%d (w%d h%d)'%(b[0],b[2],b[1],b[3],b[2]-b[0]+1,b[3]-b[1]+1)) for b in bs]
