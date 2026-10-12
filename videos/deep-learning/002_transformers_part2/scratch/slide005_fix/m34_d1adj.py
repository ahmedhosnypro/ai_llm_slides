# m34_d1adj.py — adjudicate d1end crop claims on the exact PNGs
from PIL import Image
O = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide005/afix_d1end_orig.png").convert("RGB")
R = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide005/afix_d1end_render_4.png").convert("RGB")
po,pr = O.load(), R.load()
print("sizes", O.size, R.size)
def darkred(p,x,y):
    r,g,b = p[x,y]
    return r>150 and g<115 and (r-g)>70 and (r-b)>70
def border_col(p,W,H,label):
    # the box left border: dark red vertical columns near crop x95-110
    from collections import defaultdict
    cols=defaultdict(int)
    for y in range(40,110):
        for x in range(85,120):
            r,g,b = p[x,y]
            if r>140 and g<110 and (r-g)>60: cols[x]+=1
    top = sorted(cols.items(), key=lambda kv:-kv[1])[:6]
    print(label,"red column histogram (x:count):", sorted(top))
border_col(po,*O.size,"ORIG")
border_col(pr,*R.size,"RENDER")
# dashes left of the border: per-row last red x in x0..100
from collections import defaultdict
def dashes(p,W,H,label):
    rows=defaultdict(list)
    for y in range(0,113):
        for x in range(0,100):
            if darkred(p,x,y): rows[y].append(x)
    print(label,"dash rows (y: [x-runs]) :")
    for y in sorted(rows):
        xs=sorted(rows[y]); runs=[]; s=xs[0]; pv=xs[0]
        for x in xs[1:]:
            if x-pv>1: runs.append((s,pv)); s=x
            pv=x
        runs.append((s,pv))
        if y%2==0: print("  y",y,runs)
dashes(po,*O.size,"ORIG")
dashes(pr,*R.size,"RENDER")
