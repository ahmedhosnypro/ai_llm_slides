# m19_gt018.py — same h-region measured on 001:18's original frame (state source, ~1:1 scale)
from PIL import Image
F = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_018.jpg").convert("RGB")
px = F.load()
print("001:18 frame size:", F.size)
def lum(x,y):
    r,g,b = px[x,y]; return 0.299*r+0.587*g+0.114*b
# window around h circle: 001:18 frame circle x484.9..504.0 y353.0..372.1 -> x470..515 y325..395
from collections import defaultdict
def maskruns(pred, X0,X1,Y0,Y1,label):
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

def is_tan(x,y):
    r,g,b = px[x,y]; L=lum(x,y)
    return r>185 and 140<g<215 and 90<b<195 and (r-b)>25 and abs(g-b)<40 and L<225
def is_dark(x,y):
    r,g,b = px[x,y]; L=lum(x,y)
    return L<120 and not (r>140 and g<70)
maskruns(is_tan, 470,515,325,395,"TAN")
maskruns(is_dark, 470,515,325,395,"DARK")
