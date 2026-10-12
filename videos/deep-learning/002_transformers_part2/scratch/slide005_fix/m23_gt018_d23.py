from PIL import Image
F = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_018.jpg").convert("RGB")
px = F.load()
def is_red(x,y):
    r,g,b = px[x,y]
    return r>130 and g<95 and b<95 and (r-g)>50
from collections import defaultdict
def dump(pred, X0,X1,Y0,Y1,label):
    rows=defaultdict(list)
    for y in range(Y0,Y1):
        for x in range(X0,X1):
            if pred(x,y): rows[y].append(x)
    print(f"--- {label} ---")
    for y in sorted(rows):
        xs=sorted(rows[y]); runs=[]; s=xs[0]; p=xs[0]
        for x in xs[1:]:
            if x-p>1: runs.append((s,p)); s=x
            p=x
        runs.append((s,p))
        print(" y",y,runs)
# 001:18 d2: build [[191,272],[270,345],[294,356]] -> frame ~ (192,273)->(297,359); red rect left border x305
dump(is_red, 190, 312, 260, 362, "001:18 d2")
# 001:18 d3: build [[193,487],[238,433]] -> frame (194,489)->(239,435)
dump(is_red, 188, 262, 425, 495, "001:18 d3")
