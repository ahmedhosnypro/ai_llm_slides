from PIL import Image
import collections
im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_018.jpg').convert('RGB')
px = im.load()

print("== fill sample y150..200 x100..400 mode ==")
c=collections.Counter()
for y in range(148,202):
    for x in range(90,410): c[px[x,y]]+=1
print(c.most_common(8))

print("== green column extents ==")
def colext(x):
    ys=[y for y in range(180,540) if px[x,y][1]>110 and px[x,y][0]<110 and px[x,y][2]<110 and px[x,y][1]-px[x,y][0]>40 and px[x,y][1]-px[x,y][2]>30]
    return (min(ys),max(ys),len(ys)) if ys else None
for x in [59,60,61,188,189,300,301,302,507,508]:
    print("col",x,colext(x))
def rowext(y, x0, x1):
    xs=[x for x in range(x0,x1) if px[x,y][1]>110 and px[x,y][0]<110 and px[x,y][2]<110 and px[x,y][1]-px[x,y][0]>40 and px[x,y][1]-px[x,y][2]>30]
    return (min(xs),max(xs),len(xs)) if xs else None
for y in [246,247,248,269,270,271,489,490,491,513,514,515]:
    print("row",y,"A:",rowext(y,40,220),"B:",rowext(y,280,530))

print("== gray connector right zone: x300..540 y140..340 ==")
pts=[(x,y) for y in range(140,345) for x in range(300,545) if abs(px[x,y][0]-px[x,y][1])<14 and abs(px[x,y][1]-px[x,y][2])<14 and 80<px[x,y][0]<195]
print("gray px:", len(pts))
cc=collections.Counter(y for x,y in pts)
print("rows>2:", [ (y,n) for y,n in sorted(cc.items()) if n>2 ])
if pts:
    xs=[p[0] for p in pts]
    print("x range", min(xs), max(xs))
# sample a few
print("sample:", pts[:12])

print("== gray rows y293/y315 x-extents (inset A/B?) ==")
for y in [293,315]:
    g=[x for x in range(20,545) if abs(px[x,y][0]-px[x,y][1])<14 and abs(px[x,y][1]-px[x,y][2])<14 and 80<px[x,y][0]<195]
    if g: print(y, min(g), max(g), len(g))

print("== corner handles? green squares just outside frame corners ==")
def gcount(x0,y0,x1,y1):
    n=0
    for y in range(y0,y1):
        for x in range(x0,x1):
            r,g,b=px[x,y]
            if g>110 and r<110 and b<110 and g-r>40 and g-b>30: n+=1
    return n
print("A TL out:", gcount(50,238,60,248), "A BR out:", gcount(188,490,198,500))
print("B TL out:", gcount(291,261,301,271), "B BR out:", gcount(506,514,516,524))
print("right frame TL out:", gcount(563,94,573,104))
