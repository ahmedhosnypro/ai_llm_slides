from PIL import Image
F = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_005.jpg").convert("RGB")
px = F.load()
# loose red-ish: any pixel notably redder than gray bg
def reddish(x,y):
    r,g,b = px[x,y]
    return r>140 and (r-g)>45 and (r-b)>45
from collections import defaultdict
def dump(pred, X0,X1,Y0,Y1,label):
    rows=defaultdict(list)
    for y in range(Y0,Y1):
        for x in range(X0,X1):
            if pred(x,y): rows[y].append(x)
    print(f"--- {label} ---")
    hit=False
    for y in sorted(rows):
        hit=True
        print(" y",y,rows[y])
    if not hit: print(" (no reddish ink)")
# d1 gap corridor: between last dash (618,336) and box border (643), under band b
dump(reddish, 620, 643, 330, 360, "d1 gap corridor x620-643 y330-360 (loose)")
# d2 gap corridor: between last dash (257,314) and red rect border (~311)
dump(reddish, 258, 311, 300, 345, "d2 gap corridor x258-311 y300-345 (loose)")
# also verify the exact red-rect left border x and top edge y, and inset corner handle zone
print("red rect top-left corner scan x300..330 y334..350:")
for y in range(334, 351):
    runs=[]; cur=None
    for x in range(300, 331):
        r,g,b = px[x,y]
        if r>130 and g<95 and b<95 and (r-g)>50:
            if cur is None: cur=x
        else:
            if cur is not None: runs.append((cur,x-1)); cur=None
    if cur is not None: runs.append((cur,330))
    if runs: print(" y",y,runs)
