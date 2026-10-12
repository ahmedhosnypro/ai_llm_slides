from PIL import Image
import numpy as np
im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_020.jpg').convert('RGB')
a = np.asarray(im).astype(int)
def runs(y, x0=60, x1=900, minlen=3):
    print(f"--- row y={y} color runs (x0..x1) ---")
    prev=None; start=x0
    for x in range(x0,x1):
        r,g,b = a[y,x]
        # classify
        if r>235 and g>235 and b>235: c='white'
        elif abs(r-233)<10 and abs(g-233)<10 and abs(b-231)<10: c='panel'
        elif r>120 and g<110 and b<110 and (r-g)>50: c='RED'
        elif r>200 and 120<g<200 and 120<b<200: c='pink'
        elif r>190 and 160<g<215 and 120<b<190: c='tan'
        elif r>180 and g>170 and b<160: c='peachy'
        elif g>140 and r<160 and b<170 and g-r>10: c='green'
        elif b>140 and b-r>15 and b-g>0: c='blue'
        elif r<100 and g<100 and b<100: c='dark'
        else: c='other'
        if c!=prev:
            if prev is not None and x-start>=minlen:
                med = np.median(a[y,start:x],axis=0).astype(int)
                print(f"   x[{start:3d}..{x:3d}) w={x-start:3d} {prev:7s} #{med[0]:02X}{med[1]:02X}{med[2]:02X}")
            prev=c; start=x
    if prev is not None and x1-start>=minlen:
        med = np.median(a[y,start:x1],axis=0).astype(int)
        print(f"   x[{start:3d}..{x1:3d}) w={x1-start:3d} {prev:7s} #{med[0]:02X}{med[1]:02X}{med[2]:02X}")
runs(216)
runs(258)
runs(150)
runs(135)
runs(300)
runs(318)
