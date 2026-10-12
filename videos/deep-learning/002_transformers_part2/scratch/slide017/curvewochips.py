from PIL import Image
import numpy as np
F = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_017.jpg").convert("RGB")
a = np.asarray(F).astype(int)
r, g, b = a[:,:,0], a[:,:,1], a[:,:,2]

# strong red curve pixels in bottom zone (exclude the token container area x<370 y>470? no - include all, then cluster)
red = (r>170)&(g<80)&(b<80)
ys, xs = np.where(red)
sel = (ys>=430)&(ys<=520)&(xs>=90)&(xs<=660)
ys2, xs2 = ys[sel], xs[sel]
print("bottom red px:", len(xs2))
# cluster by x-bands of 30
import collections
bands = collections.Counter((x//30)*30 for x in xs2)
print("x-band histogram:", dict(sorted(bands.items())))
# vertical profile per band
for x0 in sorted(bands):
    m = (xs2>=x0)&(xs2<x0+30)
    print("  band %d-%d: y %d..%d n=%d" % (x0, x0+30, ys2[m].min(), ys2[m].max(), m.sum()))

# swoosh: dark-red curve in right zone x 570..810 y 300..470
dred = (r>110)&(r<200)&(g<80)&(b<80)&(r-g>60)
ys, xs = np.where(dred)
sel = (ys>=290)&(ys<=475)&(xs>=560)&(xs<=820)
ys3, xs3 = ys[sel], xs[sel]
print("swoosh dark-red px:", len(xs3))
if len(xs3):
    bands = collections.Counter((x//30)*30 for x in xs3)
    for x0 in sorted(bands):
        m = (xs3>=x0)&(xs3<x0+30)
        print("  band %d-%d: y %d..%d n=%d" % (x0, x0+30, ys3[m].min(), ys3[m].max(), m.sum()))

# wochips: white boxes (with colored borders) in x 575..800, y 340..520
wht = (r>240)&(g>240)&(b>240)
# find horizontal white runs per row
for y in range(345, 520, 6):
    row = wht[y, 575:800]
    runs=[]; x=0
    while x < len(row):
        if row[x]:
            x0=x
            while x<len(row) and row[x]: x+=1
            if x-x0>=8: runs.append((x0+575, x-1+575))
        else: x+=1
    if runs: print("y=%d white runs:" % y, runs)
