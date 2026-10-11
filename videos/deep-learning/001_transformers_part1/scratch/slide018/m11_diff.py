from PIL import Image
import collections
a = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_017.jpg').convert('RGB')
b = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_018.jpg').convert('RGB')
pa, pb = a.load(), b.load()
W,H = a.size
pts=[]
for y in range(90,540):
    for x in range(540,960):
        ra,ga,ba = pa[x,y]; rb,gb,bb = pb[x,y]
        if abs(ra-rb)+abs(ga-gb)+abs(ba-bb) > 90:
            pts.append((x,y))
print("arch diff px:", len(pts))
# connected-ish clusters via grid flood on 8px cells
cell=collections.defaultdict(list)
for x,y in pts: cell[(x//8, y//8)].append((x,y))
seen=set(); clusters=[]
def flood(c):
    stack=[c]; comp=[]
    while stack:
        cur=stack.pop()
        if cur in seen or cur not in cell: continue
        seen.add(cur); comp+=cell[cur]
        cx,cy=cur
        for dx in(-1,0,1):
            for dy in(-1,0,1):
                stack.append((cx+dx,cy+dy))
    return comp
for c in list(cell):
    if c in seen: continue
    comp=flood(c)
    if len(comp)>=12:
        xs=[p[0] for p in comp]; ys=[p[1] for p in comp]
        clusters.append((min(xs),min(ys),max(xs),max(ys),len(comp)))
clusters.sort(key=lambda t:-t[4])
for cl in clusters[:20]:
    x0,y0,x1,y1,n = cl
    # sample 17 vs 18 colors at cluster center rows
    sampA = pa[(x0+x1)//2, (y0+y1)//2]; sampB = pb[(x0+x1)//2, (y0+y1)//2]
    print("cluster", (x0,y0,x1,y1), "n=",n, "A@ctr",sampA, "B@ctr",sampB)
