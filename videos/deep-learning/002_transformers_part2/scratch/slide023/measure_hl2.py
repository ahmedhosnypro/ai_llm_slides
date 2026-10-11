from PIL import Image
import numpy as np
im = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_023.jpg').convert('RGB')).astype(int)
r, g, b = im[:,:,0], im[:,:,1], im[:,:,2]
luma = (0.299*r + 0.587*g + 0.114*b)
ink = luma < 185

lines = [(350,358),(360,362),(368,384),(391,403),(413,428),(434,450),(456,472),(478,503)]
for (y0,y1) in lines:
    sub = ink[y0:y1+1, 80:890]
    cols = np.where(sub.any(axis=0))[0]
    rows = np.where(sub.any(axis=1))[0]
    red = ((r[y0:y1+1,80:890]-g[y0:y1+1,80:890]>45)&(r[y0:y1+1,80:890]-b[y0:y1+1,80:890]>45)).sum()
    mag = ((r[y0:y1+1,80:890]-g[y0:y1+1,80:890]>60)&(b[y0:y1+1,80:890]-g[y0:y1+1,80:890]>60)).sum()
    blu = ((b[y0:y1+1,80:890]-r[y0:y1+1,80:890]>45)&(b[y0:y1+1,80:890]-g[y0:y1+1,80:890]>25)).sum()
    print(f"line y{y0}..{y1}: x {80+cols.min()}..{80+cols.max()}  red {red} mag {mag} blue {blu}")

# fine check of the lead line rows 352..390 x extents per row-group
print()
for y in range(350, 392, 2):
    xs = np.where(ink[y, 80:890])[0]
    if len(xs): print(f"  y{y}: x {80+xs.min()}..{80+xs.max()} n={len(xs)}")
