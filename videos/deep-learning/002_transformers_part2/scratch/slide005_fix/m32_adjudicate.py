# m32_adjudicate.py — PIL adjudication of the hassembly crop-comparison claims
# against the EXACT PNGs the vision model saw.
from PIL import Image
O = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide005/afix_hassembly_orig.png").convert("RGB")
R = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide005/afix_hassembly_render_4.png").convert("RGB")
print("sizes:", O.size, R.size)
po, pr = O.load(), R.load()
def lum(p,x,y):
    r,g,b = p[x,y]; return 0.299*r+0.587*g+0.114*b

def tan_bbox(p,W,H):
    xs=[];ys=[]
    for y in range(H):
        for x in range(W):
            r,g,b = p[x,y]
            if r>185 and 140<g<215 and 90<b<195 and (r-b)>25 and (r-g)<80: xs.append(x); ys.append(y)
    return (min(xs),max(xs),min(ys),max(ys)) if xs else None
to = tan_bbox(po,*O.size); tr = tan_bbox(pr,*R.size)
print("TAN circle bbox  orig:",to," render:",tr)
if to and tr:
    print("  orig center(%.1f,%.1f) d=(%d,%d) | render center(%.1f,%.1f) d=(%d,%d)"%(
        (to[0]+to[1])/2,(to[2]+to[3])/2,to[1]-to[0],to[3]-to[2],
        (tr[0]+tr[1])/2,(tr[2]+tr[3])/2,tr[1]-tr[0],tr[3]-tr[2]))

# dark curve paths: dark ink x<95 region (curve zone), per-row runs
def dark_rows(p,W,H,x0,x1,y0,y1,thr=120):
    from collections import defaultdict
    rows=defaultdict(list)
    for y in range(y0,y1):
        for x in range(x0,x1):
            if lum(p,x,y)<thr:
                r,g,b=p[x,y]
                if not(r>140 and g<70): rows[y].append(x)
    return rows
print("\nDARK curve rows ORIG (x30..80):")
rows=dark_rows(po,*O.size,30,80,60,180)
for y in sorted(rows):
    xs=sorted(rows[y]); runs=[]; s=xs[0]; pv=xs[0]
    for x in xs[1:]:
        if x-pv>1: runs.append((s,pv)); s=x
        pv=x
    runs.append((s,pv)); print(" y",y,runs)
print("DARK curve rows RENDER (x30..80):")
rows=dark_rows(pr,*R.size,30,80,60,180)
for y in sorted(rows):
    xs=sorted(rows[y]); runs=[]; s=xs[0]; pv=xs[0]
    for x in xs[1:]:
        if x-pv>1: runs.append((s,pv)); s=x
        pv=x
    runs.append((s,pv)); print(" y",y,runs)
