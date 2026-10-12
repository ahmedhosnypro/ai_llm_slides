from PIL import Image
from collections import Counter
im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_018.jpg').convert('RGB')
W,H = im.size
px = im.load()
def rr(y,pred,x0,x1):
    out=[];s=None
    for x in range(x0,x1):
        if pred(*px[x,y]):
            if s is None: s=x
        else:
            if s is not None: out.append((s,x-1)); s=None
    if s is not None: out.append((s,x1-1))
    return out
def modal(x0,y0,x1,y1,pred):
    c=Counter()
    for y in range(y0,y1):
        for x in range(x0,x1):
            p=px[x,y]
            if pred(*p): c[p]+=1
    return c.most_common(5)

iswhite = lambda r,g,b: r>246 and g>246 and b>246
print("=== deep label chip ===")
print("row 290 raw x295..330:", [(x,px[x,290]) for x in range(295,332,2)])
print("row 290 raw x505..530:", [(x,px[x,290]) for x in range(505,531,2)])
print("col 310 y270..305:", [(y,px[310,y]) for y in range(270,306,2)])
print("col 500 y270..305:", [(y,px[500,y]) for y in range(270,306,2)])
print("modal fill:", modal(310,284,330,296, lambda r,g,b: r>190 and g>225 and 190<b<235))
print("label text dark bbox:", end=" ")
xs=[];ys=[]
for y in range(278,302):
    for x in range(300,530):
        r,g,b=px[x,y]
        if r<100 and g<100 and b<100: xs.append(x); ys.append(y)
print((min(xs),max(xs),min(ys),max(ys)) if xs else None)
print("=== callout boxes: column gray-count profile y304..372 ===")
prof=[]
for x in range(70,760):
    c=sum(1 for y in range(304,373) if 195<px[x,y][0]<235 and 195<px[x,y][1]<235 and abs(px[x,y][0]-px[x,y][2])<12)
    prof.append((x,c))
# find spans where c>20
spans=[];s=None
for x,c in prof:
    if c>20 and s is None: s=x
    if c<=20 and s is not None: spans.append((s,x-1)); s=None
if s is not None: spans.append((s,759))
print("gray spans:", [sp for sp in spans if sp[1]-sp[0]>20])
print("=== callout rows: per-box vertical extent ===")
for (a,b) in [sp for sp in spans if sp[1]-sp[0]>20]:
    ys=[y for y in range(295,380) if 195<px[(a+b)//2,y][0]<235 and abs(px[(a+b)//2,y][0]-px[(a+b)//2,y][2])<12]
    # take longest run
    runs=[];ss=None;pp=None
    for y in range(295,380):
        p=px[(a+b)//2,y]
        ok = 195<p[0]<235 and 195<p[1]<235 and abs(p[0]-p[2])<12
        if ok and ss is None: ss=y
        if not ok and ss is not None: runs.append((ss,pp)); ss=None
        pp=y
    if ss is not None: runs.append((ss,pp))
    runs=[r for r in runs if r[1]-r[0]>5]
    print(f" box x{a}..{b}: mid col runs {runs}")
print("callout modal gray:", modal(100,340,160,352, lambda r,g,b: 200<r<232 and 200<g<232 and 200<b<232))
print("=== starburst ===")
print("yellowish bbox x700..930 y295..385:")
xs=[];ys=[]
for y in range(295,386):
    for x in range(700,931):
        r,g,b=px[x,y]
        if r>240 and g>238 and b<235: xs.append(x); ys.append(y)
print((min(xs),max(xs),min(ys),max(ys)) if xs else None)
print("modal yellow:", modal(745,315,800,345, lambda r,g,b: r>240 and g>238 and b<235))
print("star red text bbox:")
xs=[];ys=[]
for y in range(300,380):
    for x in range(730,920):
        r,g,b=px[x,y]
        if r>140 and r-g>50 and r-b>50: xs.append(x); ys.append(y)
print((min(xs),max(xs),min(ys),max(ys)) if xs else None)
print("=== statement box ===")
print("border samples: px[279,415]",px[279,415]," px[281,420]",px[281,420]," px[568,415]",px[568,415]," px[420,391]",px[420,391]," px[420,444]",px[420,444])
print("modal fill:", modal(300,395,560,440, lambda r,g,b: r>248 and g>244 and b>215))
print("red text rows: per y count in x285..565 y395..445")
for y in range(395,446):
    c=sum(1 for x in range(285,566) if px[x,y][0]>140 and px[x,y][0]-px[x,y][1]>50)
    if c>3: print("  y",y,"n",c)
print("=== CO text: dark px x753..858 y215..258 excluding borders ===")
xs=[];ys=[]
for y in range(215,259):
    for x in range(753,859):
        r,g,b=px[x,y]
        if r<95 and g<95 and b<95: xs.append(x); ys.append(y)
print("CO text bbox:", (min(xs),max(xs),min(ys),max(ys)) if xs else None)
print("=== box fills modal (verify palette) ===")
print("box_pre:", modal(150,220,220,230, lambda r,g,b: True)[:2])
print("box_ext:", modal(310,220,400,230, lambda r,g,b: True)[:2])
print("box_sel:", modal(460,220,540,230, lambda r,g,b: True)[:2])
print("class:", modal(610,218,700,226, lambda r,g,b: True)[:2])
print("CO tan:", modal(760,250,850,258, lambda r,g,b: True)[:2])
