from PIL import Image
import numpy as np
im = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_023.jpg').convert('RGB')).astype(int)
r, g, b = im[:,:,0], im[:,:,1], im[:,:,2]
luma = (0.299*r + 0.587*g + 0.114*b)

orange = (r>190)&(g>110)&(g<210)&(b<120)&(r-b>90)
print("orange px rows 306..350:")
for y in range(306, 351):
    c = orange[y, 150:899].sum()
    if c: print(f"  y{y}: {int(c)}")
ys, xs = np.where(orange[306:351, :])
print("orange bbox: y", 306+ys.min(), "..", 306+ys.max(), " x", xs.min(), "..", xs.max())
# per-arc x clusters
cp = orange[306:351, :].sum(axis=0)
runs=[]; inr=False
for x in range(150, 899):
    if cp[x]>=1 and not inr: s=x; inr=True
    elif cp[x]<1 and inr:
        if x-s > 5: runs.append((s, x-1))
        inr=False
print("orange arc x runs:", runs)

# +d labels: strong red text below arcs
rs = (r>120)&(r-g>40)&(r-b>40)
sub = rs[318:348, :]
rp = sub.sum(axis=1)
print("red rows 318..347:", [(318+i, int(v)) for i,v in enumerate(rp) if v>=2])
cp = sub.sum(axis=0)
runs=[]; inr=False
for x in range(150, 899):
    if cp[x]>=1 and not inr: s=x; inr=True
    elif cp[x]<1 and inr:
        if x-s >= 2: runs.append((s, x-1))
        inr=False
print("+d label x runs:", runs)
