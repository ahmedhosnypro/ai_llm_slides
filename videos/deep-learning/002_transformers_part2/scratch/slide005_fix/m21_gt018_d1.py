from PIL import Image
F = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_018.jpg").convert("RGB")
px = F.load()
def is_red(x,y):
    r,g,b = px[x,y]
    return r>130 and g<95 and b<95 and (r-g)>50
from collections import defaultdict
rows=defaultdict(list)
for y in range(240, 400):
    for x in range(500, 680):
        if is_red(x,y): rows[y].append(x)
print("001:18 d1 region red runs:")
for y in sorted(rows):
    xs=sorted(rows[y]); runs=[]; s=xs[0]; p=xs[0]
    for x in xs[1:]:
        if x-p>1: runs.append((s,p)); s=x
        p=x
    runs.append((s,p))
    # compact: only show if interesting (skip long text runs)
    print(" y",y,runs)
