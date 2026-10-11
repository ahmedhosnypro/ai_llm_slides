from PIL import Image
import numpy as np
im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_036.jpg').convert('RGB')
a = np.asarray(im).astype(int)
H,W = a.shape[:2]
lum = a.mean(axis=2)

def ink_mask(x0,y0,x1,y1, mode='dark'):
    reg = a[y0:y1, x0:x1]
    l = reg.mean(axis=2)
    if mode=='dark':   m = l < 170
    elif mode=='blue': m = (reg[:,:,2] > reg[:,:,0]+40) & (l < 200)
    elif mode=='red':  m = (reg[:,:,0] > reg[:,:,1]+50) & (reg[:,:,0] > 100) & (l < 200)
    elif mode=='green':m = (reg[:,:,1] > reg[:,:,0]+30) & (reg[:,:,1] > reg[:,:,2]+20) & (l < 190)
    elif mode=='yellow':m = (reg[:,:,0]>200)&(reg[:,:,1]>200)&(reg[:,:,2]<120)
    return m

def bands(x0,y0,x1,y1,mode='dark',minpx=3):
    m = ink_mask(x0,y0,x1,y1,mode)
    rows = m.sum(axis=1)
    out=[]; start=None
    for i,c in enumerate(rows):
        if c>=minpx and start is None: start=i
        elif c<minpx and start is not None:
            out.append((start+y0, i-1+y0)); start=None
    if start is not None: out.append((start+y0, y1-1))
    res=[]
    for (ya,yb) in out:
        mm = m[ya-y0:yb-y0+1]
        cols = mm.sum(axis=0)
        xs = np.where(cols>=1)[0]
        res.append((ya,yb,xs.min()+x0,xs.max()+x0))
    return res

print("TITLE bands (y 40..85):")
for b in bands(100,40,860,85): print('  y%d..%d x%d..%d' % b, 'h=%d'%(b[1]-b[0]+1))
print("SUBTITLE bands (y 72..105):")
for b in bands(150,72,830,105): print('  y%d..%d x%d..%d' % b)
print("SUBTITLE red mask:")
for b in bands(150,72,830,105,'red'): print('  y%d..%d x%d..%d' % b)
print("SUBTITLE yellow highlight:")
for b in bands(150,72,830,105,'yellow'): print('  y%d..%d x%d..%d' % b)
print()
print("EQBOX text bands (box x308..660 y106..227):")
for b in bands(315,110,655,224): print('  y%d..%d x%d..%d' % b)
print("EQBOX blue text bands:")
for b in bands(315,110,655,224,'blue'): print('  y%d..%d x%d..%d' % b)
print()
print("BELL box internals (x683..893 y110..219):")
for b in bands(686,112,890,217,'dark',2): print('  dark y%d..%d x%d..%d' % b)
for b in bands(686,112,890,217,'blue',2): print('  blue y%d..%d x%d..%d' % b)
for b in bands(686,112,890,217,'red',2): print('  red y%d..%d x%d..%d' % b)
print()
print("STMT1 text (x296..601 y238..279):")
for b in bands(302,242,596,276): print('  dark y%d..%d x%d..%d' % b)
for b in bands(302,242,596,276,'green'): print('  green y%d..%d x%d..%d' % b)
print("STMT2 text (x617..896 y238..280):")
for b in bands(622,242,892,277): print('  dark y%d..%d x%d..%d' % b)
for b in bands(622,242,892,277,'green'): print('  green y%d..%d x%d..%d' % b)
