from PIL import Image
import numpy as np
im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_036.jpg').convert('RGB')
a = np.asarray(im).astype(int)
H, W = a.shape[:2]

# Find horizontal border lines: rows where a long horizontal run of near-same color exists
def hruns(row, minlen=80):
    r = a[row]
    runs=[]
    x=0
    while x < W-1:
        seg=[r[x]]; j=x+1
        while j < W and abs(r[j]-r[x]).sum() <= 90 and j-x < 500:
            seg.append(r[j]); j+=1
        if len(seg) >= minlen:
            runs.append((x, j-1, tuple(np.array(seg).mean(axis=0).astype(int))))
        x = j if j>x else x+1
    return runs

for row in range(40, 540, 2):
    rr = hruns(row, 90)
    for s,e,c in rr:
        # skip gray/white bg
        if abs(c[0]-233)<12 and abs(c[1]-233)<12 and abs(c[2]-231)<12: continue
        if c[0]>245 and c[1]>245 and c[2]>245: continue
        print(f'row {row}: x{s}..{e} color {c}')
