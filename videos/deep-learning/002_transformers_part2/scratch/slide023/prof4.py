from PIL import Image
import numpy as np
im = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_023.jpg').convert('RGB')).astype(int)
r, g, b = im[:,:,0], im[:,:,1], im[:,:,2]
blues = (b-r>55)&(b>110)
print("ROW2 strong-blue per-row (x150..880):")
for y in range(182, 232):
    c = blues[y,150:880].sum()
    if c: print(f"  y{y}: {c}")
# columns of strong blue in box-top rows
print("ROW2 y188..192 columns with strong blue:")
m = blues[186:193, :]
cp = m.sum(axis=0)
runs=[]; inr=False
for x in range(150,899):
    if cp[x]>=2 and not inr: s=x; inr=True
    elif cp[x]<2 and inr: runs.append((s,x-1)); inr=False
print(runs)
# ROW3: check pink fill extent and any mid-red (borders on pink)
mid = (r-g>45)&(r>140)&(r<235)
print("ROW3 mid-red per-row (x150..880):")
for y in range(256, 313):
    c = mid[y,150:880].sum()
    if c: print(f"  y{y}: {c}")
