from PIL import Image
import numpy as np
im = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_023.jpg').convert('RGB')).astype(int)
r, g, b = im[:,:,0], im[:,:,1], im[:,:,2]
luma = (0.299*r+0.587*g+0.114*b)
ink = luma < 205

def lines(y0, y1, x0, x1, name, minpx=2):
    prof = ink[y0:y1+1, x0:x1].sum(axis=1)
    bands=[]; prev=False
    for i,v in enumerate(prof):
        y=y0+i
        if v>=minpx and not prev: s=y
        if v<minpx and prev: bands.append((s,y-1))
        prev=v>=minpx
    if prev: bands.append((s,y1))
    for (a,bb) in bands:
        cols = np.where(ink[a:bb+1, x0:x1].any(axis=0))[0]
        print(f"{name} line y{a}..{bb} x {x0+cols.min()}..{x0+cols.max()}")

lines(110, 165, 62, 155, "R1label")
lines(182, 238, 62, 155, "R2label")
lines(255, 312, 62, 155, "R3label")

# arc1 full trace: non-bg in x 185..285, y 300..335
bg = (abs(r-233)<14)&(abs(g-233)<14)&(abs(b-231)<16)
print("\narc zone rows (x150..880, non-bg):")
for y in range(296, 336):
    cs = [x for x in range(150,881) if not bg[y,x]]
    if cs:
        # cluster
        cl=[]; 
        for x in cs:
            if cl and x-cl[-1][-1]<=6: cl[-1].append(x)
            else: cl.append([x])
        print(f"  y{y}: {[(c[0],c[-1]) for c in cl]}")
