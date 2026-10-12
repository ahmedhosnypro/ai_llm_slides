from PIL import Image
F = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_005.jpg").convert("RGB")
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
# d2: SDPA inset top-right (frame ~200,258) -> red rect left edge (~309,340-380)
dump(is_red, 192, 315, 252, 345, "d2 red dashes")
# d3: fragment near (204,467)->(247,415)
dump(is_red, 192, 260, 405, 475, "d3 red dashes")
# red rect left edge + SDPA inset right edge anchors
print("--- SDPA inset frame right edge (green) x196..206 y255..500 ---")
def is_green(x,y):
    r,g,b = px[x,y]
    return g>85 and r<100 and (g-r)>40 and (g-b)>30
rows=defaultdict(list)
for y in range(252, 500):
    for x in range(194, 210):
        if is_green(x,y): rows[y].append(x)
for y in sorted(rows):
    print(" y",y,rows[y])
