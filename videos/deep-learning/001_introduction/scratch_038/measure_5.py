from PIL import Image
import numpy as np
im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_038.jpg').convert('RGB')
a = np.asarray(im).astype(int)
H, W, _ = a.shape
r, g, b = a[...,0], a[...,1], a[...,2]
ink   = ((r<160)|(g<160)|(b<160))
reddish = ((r-g)>40) & ((r-b)>40) & (r>110)
bluish  = ((b-r)>40) & ((b-g)>20) & (b>110)
greenish= ((g-r)>30) & ((g-b)>30) & (g>90)

print("--- rows 195..255: ink spans full width ---")
for y in range(195, 256):
    c = ink[y, 90:880].sum()
    if c>2:
        xs = np.nonzero(ink[y, 90:880])[0] + 90
        print(f"y={y} ink={c} r={reddish[y,90:880].sum()} b={bluish[y,90:880].sum()} g={greenish[y,90:880].sum()} x {xs.min()}..{xs.max()}")
print("--- blue pixel rows at x=400,410,516 ---")
for x in (400,410,516):
    ys = np.nonzero(bluish[:,x])[0]
    print(f"x={x}:", ys.tolist()[:80])
print("--- line3 column profile rows 205..228 ---")
sub = ink[205:229, 90:880]
colsum = sub.sum(axis=0)
xs = np.nonzero(colsum)[0]+90
segs=[]; prev=None; start=None
for x in range(int(xs.min()), int(xs.max())+2):
    on = colsum[x-90]>0 if x<=int(xs.max()) else False
    if on and start is None: start=x
    if not on and start is not None:
        segs.append((start,x-1)); start=None
print("segments:", segs)
