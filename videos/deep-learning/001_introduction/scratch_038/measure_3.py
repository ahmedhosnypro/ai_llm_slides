from PIL import Image
import numpy as np
im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_038.jpg').convert('RGB')
a = np.asarray(im).astype(int)
H, W, _ = a.shape
r, g, b = a[...,0], a[...,1], a[...,2]
reddish = ((r-g)>40) & ((r-b)>40) & (r>110)
bluish  = ((b-r)>40) & ((b-g)>20) & (b>110)
dark  = (r<100) & (g<100) & (b<100)

print("--- BLUE rows (long runs = box borders) ---")
for y in range(H):
    c = bluish[y].sum()
    if c>100:
        xs = np.nonzero(bluish[y])[0]
        print(f"y={y} count={c} x {xs.min()}..{xs.max()}")
print("--- RED rows with long runs (rule/borders) ---")
for y in range(H):
    c = reddish[y].sum()
    if c>300:
        xs = np.nonzero(reddish[y])[0]
        print(f"y={y} count={c} x {xs.min()}..{xs.max()}")
print("--- BLUE columns (vertical borders) ---")
for x in range(W):
    c = bluish[:,x].sum()
    if c>40:
        ys = np.nonzero(bluish[:,x])[0]
        print(f"x={x} count={c} y {ys.min()}..{ys.max()}")
print("--- RED columns (vertical borders) ---")
for x in range(W):
    c = reddish[:,x].sum()
    if c>100:
        ys = np.nonzero(reddish[:,x])[0]
        print(f"x={x} count={c} y {ys.min()}..{ys.max()}")
print("--- title red column profile rows 60..105 ---")
sub = reddish[60:106]
colsum = sub.sum(axis=0)
xs = np.nonzero(colsum)[0]
print("x extent", xs.min(), xs.max())
# find gaps
gaps=[]
prev=None
for x in range(xs.min(), xs.max()+1):
    if colsum[x]==0:
        if prev is None: prev=x
    else:
        if prev is not None:
            if x-prev>4: gaps.append((prev,x-1))
            prev=None
print("gaps>4:", gaps)
