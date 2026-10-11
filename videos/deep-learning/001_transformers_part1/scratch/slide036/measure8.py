from PIL import Image
import numpy as np
im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_036.jpg').convert('RGB')
a = np.asarray(im).astype(int)

def masks(x0,y0,x1,y1):
    reg = a[y0:y1, x0:x1]
    l = reg.mean(axis=2)
    dark = l < 170
    blue = (reg[:,:,2] > reg[:,:,0]+40) & (l < 200)
    red  = (reg[:,:,0] > reg[:,:,1]+50) & (reg[:,:,0] > 100) & (l < 200)
    green= (reg[:,:,1] > reg[:,:,0]+25) & (reg[:,:,1] > reg[:,:,2]+15) & (reg[:,:,1] > 90) & (l < 200)
    orange=(reg[:,:,0]>200)&(reg[:,:,1]>100)&(reg[:,:,1]<200)&(reg[:,:,2]<100)
    return dark,blue,red,green,orange,l

def bands(x0,y0,x1,y1,mi,minpx=3,gap=2):
    m = masks(x0,y0,x1,y1)[mi]
    rows = m.sum(axis=1)
    out=[]; start=None; last=None
    for i,c in enumerate(rows):
        if c>=minpx:
            if start is None: start=i
            last=i
        elif start is not None and i-last>gap:
            out.append((start,last)); start=None
    if start is not None: out.append((start,last))
    res=[]
    for (ya,yb) in out:
        mm = m[ya:yb+1]
        cols = mm.sum(axis=0)
        xs = np.where(cols>=1)[0]
        res.append((ya+y0,yb+y0,xs.min()+x0,xs.max()+x0))
    return res

names={0:'dark',1:'blue',2:'red',3:'green',4:'orange'}
print("== VECTOR CONTAINER x46..270 y99..373 ==")
for mi in [0,1,2,4]:
    bs = bands(50,103,268,370,mi,2)
    print(f' {names[mi]}:')
    for b in bs: print('   y%d..%d x%d..%d' % b)
print()
print("== FBOX1 x291..443 y306..363 ==")
for mi in [0,1,2]:
    for b in bands(295,310,440,360,mi,2): print(f' {names[mi]} y%d..%d x%d..%d' % b)
print("== FBOX2 x503..655 y296..373 ==")
for mi in [0,1,2]:
    for b in bands(507,300,652,370,mi,2): print(f' {names[mi]} y%d..%d x%d..%d' % b)
print("== FBOX3 x705..857 y308..359 ==")
for mi in [0,1,2]:
    for b in bands(709,312,854,356,mi,2): print(f' {names[mi]} y%d..%d x%d..%d' % b)
print()
print("== REMEMBER x44..223 y386..507 ==")
for mi in [0,1,2]:
    print(f' {names[mi]}:')
    for b in bands(48,390,220,504,mi,2): print('   y%d..%d x%d..%d' % b)
print()
print("== FLOWCHART1 x286..502 y379..523 ==")
for mi in [0,1,2]:
    print(f' {names[mi]}:')
    for b in bands(290,383,499,520,mi,2): print('   y%d..%d x%d..%d' % b)
print()
print("== FLOWCHART2 x512..899 y378..524 ==")
for mi in [0,1,2]:
    print(f' {names[mi]}:')
    for b in bands(516,382,896,521,mi,2): print('   y%d..%d x%d..%d' % b)
