from PIL import Image
import numpy as np
from scipy import ndimage
im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_020.jpg').convert('RGB')
a = np.asarray(im).astype(int)
H,W,_ = a.shape
# content ink = anything far from white and far from panel gray E9E9E7
dwhite = np.abs(a - np.array([254,255,253])).max(axis=2)
dgray  = np.abs(a - np.array([233,233,231])).max(axis=2)
ink = (dwhite > 25) & (dgray > 25)
lab, n = ndimage.label(ink)
objs = ndimage.find_objects(lab)
sizes = ndimage.sum(ink, lab, range(1, n+1))
comps = []
for i, sl in enumerate(objs):
    if sizes[i] >= 120:
        ys, xs = sl
        x0,y0,x1,y1 = xs.start, ys.start, xs.stop, ys.stop
        # median color of component pixels
        m = (lab[sl] == i+1)
        cols = a[sl][m]
        med = np.median(cols, axis=0).astype(int)
        comps.append((int(sizes[i]), x0,y0,x1,y1, tuple(med)))
comps.sort(key=lambda c: (c[2], c[1]))
for s,x0,y0,x1,y1,med in comps:
    print(f"px={s:6d} x[{x0:3d}..{x1:3d}) y[{y0:3d}..{y1:3d}) w={x1-x0:3d} h={y1-y0:3d} med=#{med[0]:02X}{med[1]:02X}{med[2]:02X} {med}")
