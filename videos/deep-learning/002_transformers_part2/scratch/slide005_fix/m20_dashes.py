# m20_dashes.py — dashed connectors d1/d2/d3: endpoints, attachment, arrowheads
from PIL import Image
F = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_005.jpg").convert("RGB")
px = F.load()
def lum(x,y):
    r,g,b = px[x,y]; return 0.299*r+0.587*g+0.114*b
def is_red(x,y):
    r,g,b = px[x,y]
    return r>130 and g<95 and b<95 and (r-g)>50
from collections import defaultdict
def dump_runs(pred, X0,X1,Y0,Y1,label,axis="y"):
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

# d1: from MHA inset top-right corner (frame ~506,236) to enc MHA box left edge (~643,340-371)
dump_runs(is_red, 500, 660, 230, 380, "d1 red dashes: inset corner -> enc MHA box")
