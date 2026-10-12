from PIL import Image
import numpy as np
from scipy import ndimage
im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_020.jpg').convert('RGB')
a = np.asarray(im).astype(int)
r,g,b = a[:,:,0],a[:,:,1],a[:,:,2]

# 1) ellipse: tan fill mask in region y105..175 x340..510
tan = (np.abs(a-np.array([244,222,193])).max(axis=2)<=18)
sub = tan[100:180, 330:520]
ys,xs = np.where(sub)
print("ellipse tan bbox: x", xs.min()+330, xs.max()+330, "y", ys.min()+100, ys.max()+100)
# ellipse outline: dark ring? scan row y=135.. through ellipse edge
row = a[113, 330:520]
# find dark pixels (outline) in ellipse region
dark = (r<120)&(g<120)&(b<140)
sub2 = dark[100:180, 330:520]
ys2,xs2 = np.where(sub2)
if len(ys2): print("dark outline/text bbox in ellipse region: x", xs2.min()+330, xs2.max()+330, "y", ys2.min()+100, ys2.max()+100)
# per-row tan extent to model ellipse
for y in range(108, 172, 6):
    row_m = tan[y, 330:520]
    w = np.where(row_m)[0]
    if len(w): print(f"  y={y} tan x[{w.min()+330}..{w.max()+330}]")
# dots: blue mask near ellipse
blue = (b>120)&(b-r>60)&(b-g>40)
for name, (x0,x1,y0,y1) in {"left dot":(350,385,125,148),"right dot":(462,492,125,148)}.items():
    m = blue[y0:y1, x0:x1]
    ys3,xs3 = np.where(m)
    if len(ys3): print(f"{name}: x[{xs3.min()+x0}..{xs3.max()+x0}] y[{ys3.min()+y0}..{ys3.max()+y0}] med={tuple(np.median(a[ys3+y0,xs3+x0],axis=0).astype(int))}")

# 2) dashed container: peach fill FDE9D9 mask
peach = (np.abs(a-np.array([250,220,196])).max(axis=2)<=22)
# columns through container area at x=200 (peach zone left of Pre processing)
for x in [196, 200, 315, 632]:
    col = peach[150:300, x]
    w = np.where(col)[0]
    if len(w): print(f"container peach col x={x}: y[{w.min()+150}..{w.max()+150}] count={len(w)}")
# container top/bottom rows
for y in [195, 200, 268, 272, 275]:
    rowm = peach[y, 150:700]
    w = np.where(rowm)[0]
    if len(w): print(f"container peach row y={y}: x[{w.min()+150}..{w.max()+150}] count={len(w)}")
# red dashed border of container: red mask above/below boxes
red = (r>120)&(g<100)&(b<100)&((r-g)>60)
for y in [193,194,195,196, 270,271,272,273,274]:
    rowm = red[y, 150:700]
    print(f"red row y={y}: cols {np.where(rowm)[0][:6]+150 if rowm.sum() else '-'} count={rowm.sum()}")

# 3) blue arrow paths: blue mask bbox per row (excluding ellipse dots region x350..500)
print("--- blue mask rows ---")
for y in range(105, 215, 5):
    m = blue[y, :]
    w = np.where(m)[0]
    if len(w): print(f"  y={y}: x-ranges {w.min()}..{w.max()} n={len(w)} groups={np.split(w, np.where(np.diff(w)>4)[0]+1).__len__()}")
# right dotted arrow below y135: where does it end?
for y in [180, 190, 200, 205, 210]:
    m = blue[y, 500:960]
    w = np.where(m)[0]
    if len(w): print(f"  y={y} right zone: x[{w.min()+500}..{w.max()+500}] n={len(w)}")
