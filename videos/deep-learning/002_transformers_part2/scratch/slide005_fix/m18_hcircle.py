# m18_hcircle.py — exact masks: tan circle, dark arrowhead, black curve, gray ghost ring
from PIL import Image
F = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_005.jpg").convert("RGB")
px = F.load()
def get(x,y): return px[x,y]
def lum(x,y):
    r,g,b = get(x,y); return 0.299*r+0.587*g+0.114*b

X0,X1,Y0,Y1 = 462, 518, 318, 392
tan=[]; dark=[]; gray=[]
for y in range(Y0,Y1):
    for x in range(X0,X1):
        r,g,b = get(x,y); L=lum(x,y)
        if r>185 and 140<g<215 and 90<b<195 and (r-b)>25 and abs(g-b)<40 and L<225:
            tan.append((x,y))
        if L<120 and not (r>140 and g<70):
            dark.append((x,y))
        if 150<L<200 and abs(r-g)<12 and abs(g-b)<12:
            gray.append((x,y))

def bbox(pts,label):
    if not pts: print(label,"EMPTY"); return
    xs=[p[0] for p in pts]; ys=[p[1] for p in pts]
    print(f"{label}: n={len(pts)} bbox x{min(xs)}..{max(xs)} y{min(ys)}..{max(ys)}")
    return (min(xs),max(xs),min(ys),max(ys))

tb_ = bbox(tan,"TAN fill")
dk  = bbox(dark,"DARK ink")
gy  = bbox(gray,"GRAY ink")

print("\nTAN per-row runs (rows with ink):")
from collections import defaultdict
rows=defaultdict(list)
for x,y in tan: rows[y].append(x)
for y in sorted(rows):
    xs=sorted(rows[y]); runs=[]; s=xs[0]; p=xs[0]
    for x in xs[1:]:
        if x-p>1: runs.append((s,p)); s=x
        p=x
    runs.append((s,p))
    print(" y",y,runs)

print("\nDARK per-row runs:")
rows=defaultdict(list)
for x,y in dark: rows[y].append(x)
for y in sorted(rows):
    xs=sorted(rows[y]); runs=[]; s=xs[0]; p=xs[0]
    for x in xs[1:]:
        if x-p>1: runs.append((s,p)); s=x
        p=x
    runs.append((s,p))
    print(" y",y,runs)

print("\nGRAY per-row runs (only y<352 to isolate ghost ring/stroke):")
rows=defaultdict(list)
for x,y in gray:
    if y<352: rows[y].append(x)
for y in sorted(rows):
    xs=sorted(rows[y]); runs=[]; s=xs[0]; p=xs[0]
    for x in xs[1:]:
        if x-p>1: runs.append((s,p)); s=x
        p=x
    runs.append((s,p))
    print(" y",y,runs)
