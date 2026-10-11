from PIL import Image
import numpy as np
im = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_023.jpg').convert('RGB')).astype(int)

def runs_on_row(y, x0=62, x1=899):
    row = im[y, x0:x1]
    out=[]
    cur=None; start=x0
    for i,px in enumerate(row):
        c = tuple((px//24)*24)
        if c != cur:
            if cur is not None: out.append((start, x0+i-1, cur))
            cur=c; start=x0+i
    out.append((start, x1-1, cur))
    return [o for o in out if o[1]-o[0] >= 2]

print("ROW1 y=136:"); 
for o in runs_on_row(136): print("  ", o)
print("ROW2 y=206:")
for o in runs_on_row(206): print("  ", o)
print("ROW3 y=283:")
for o in runs_on_row(283): print("  ", o)
