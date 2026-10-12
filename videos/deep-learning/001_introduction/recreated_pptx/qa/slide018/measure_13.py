from PIL import Image
from collections import Counter
im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_018.jpg').convert('RGB')
W,H = im.size
px = im.load()
isgray = lambda r,g,b: 192<r<240 and 192<g<240 and abs(r-g)<12 and abs(r-b)<16
def grayruns(y,x0,x1):
    out=[];s=None
    for x in range(x0,x1):
        if isgray(*px[x,y]):
            if s is None: s=x
        else:
            if s is not None:
                if x-s>4: out.append((s,x-1))
                s=None
    if s is not None and x1-s>4: out.append((s,x1-1))
    return out
print("=== callout boxes: gray runs at many rows ===")
for y in [310,313,316,320,348,352,356,360,364,367]:
    print(" y",y, grayruns(y,70,760))
print("=== per-callout ink row histograms ===")
zones = {"c1":(80,278),"c2":(282,448),"c3":(450,592),"c4":(596,748)}
for name,(a,b) in zones.items():
    print(f" {name}:")
    for y in range(302,375):
        dk=sum(1 for x in range(a,b) if px[x,y][0]<115 and px[x,y][1]<115)
        rd=sum(1 for x in range(a,b) if px[x,y][0]>140 and px[x,y][0]-px[x,y][1]>50)
        if dk>2 or rd>2: print(f"   y{y} dk{dk} rd{rd}")
print("=== starburst: nonwhite bbox (excl red text) x720..935 y285..390 ===")
xs=[];ys=[]
for y in range(285,391):
    for x in range(720,936):
        r,g,b=px[x,y]
        if not(r>244 and g>244 and b>244): xs.append(x);ys.append(y)
print("nonwhite bbox:", (min(xs),max(xs),min(ys),max(ys)))
print("=== red/pink pixels below y345 in star zone: x locations ===")
for y in [350,360,370,380]:
    rd=[x for x in range(720,936) if px[x,y][0]>140 and px[x,y][0]-px[x,y][1]>50]
    print(f"  y{y}: {rd} colors {[px[x,y] for x in rd[:3]]}")
print("=== star text line x-extents ===")
for y0,y1,n in [(306,319,'l1'),(320,336,'l2')]:
    xs=[x for y in range(y0,y1) for x in range(725,935) if px[x,y][0]>140 and px[x,y][0]-px[x,y][1]>50]
    print(f" {n}: x{min(xs)}..{max(xs)}" if xs else f"{n}: none")
print("=== endtoend chip: fill modal + text x extent ===")
c=Counter()
for y in range(136,158):
    for x in range(346,554):
        p=px[x,y]
        if p[0]>215 and p[1]>235 and p[2]>240: c[p]+=1
print("fill modal:", c.most_common(3))
xs=[x for y in range(138,154) for x in range(350,552) if px[x,y][0]<120 and px[x,y][2]>px[x,y][0]]
print("text x:", (min(xs),max(xs)) if xs else None)
print("=== statement border modal ===")
c=Counter()
for x in range(282,566):
    for y in [390,391,392,443,444,445]:
        p=px[x,y]
        if p[2]>100 and p[2]-p[0]>40: c[p]+=1
print(c.most_common(5))
print("=== deep arrow: exact head extents y266..278 x110..135 / x705..735 ===")
for y in range(266,279):
    l=[x for x in range(108,140) if px[x,y][0]>140 and px[x,y][0]-px[x,y][1]>50]
    r2=[x for x in range(700,740) if px[x,y][0]>140 and px[x,y][0]-px[x,y][1]>50]
    print(f"  y{y}: L{l} R{r2}")
