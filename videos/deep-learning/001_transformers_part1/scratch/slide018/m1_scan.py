from PIL import Image
import collections
im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_018.jpg').convert('RGB')
W,H = im.size
px = im.load()

def bbox(pred, x0,y0,x1,y1):
    xs=[]; ys=[]
    for y in range(y0,y1):
        for x in range(x0,x1):
            if pred(*px[x,y]):
                xs.append(x); ys.append(y)
    if not xs: return None
    return (min(xs),min(ys),max(xs),max(ys),len(xs))

# 1. peach banner fill (242,198,153) tolerant
peach = bbox(lambda r,g,b: abs(r-242)<14 and abs(g-198)<14 and abs(b-153)<16, 30,80,540,180)
print("banner peach bbox:", peach)

# 2. green pixels (inset frames) across left half
green = bbox(lambda r,g,b: g>110 and r<110 and b<110 and g-r>40 and g-b>30, 20,180,540,540)
print("green bbox left-half:", green)
# vertical green lines: count per column
colc = collections.Counter()
for y in range(180,540):
    for x in range(20,540):
        r,g,b = px[x,y]
        if g>110 and r<110 and b<110 and g-r>40 and g-b>30: colc[x]+=1
print("green columns>30:", sorted([x for x,c in colc.items() if c>30]))
rowc = collections.Counter()
for y in range(180,540):
    for x in range(20,540):
        r,g,b = px[x,y]
        if g>110 and r<110 and b<110 and g-r>40 and g-b>30: rowc[y]+=1
print("green rows>30:", sorted([y for y,c in rowc.items() if c>30]))

# 3. red text (titles) regions in left half
red = bbox(lambda r,g,b: r>150 and g<70 and b<70, 20,150,540,215)
print("red text bbox upper-left:", red)

# 4. yellow L-band extent on 18
yel = bbox(lambda r,g,b: r>200 and g>200 and b<120, 640,230,800,340)
print("yellow band bbox:", yel)

# 5. red outline around encoder MHA: scan x628..728 y350..392 for strong red
reds2 = [(x,y) for y in range(345,395) for x in range(620,735) if px[x,y][0]>150 and px[x,y][1]<70 and px[x,y][2]<70]
if reds2:
    xs=[p[0] for p in reds2]; ys=[p[1] for p in reds2]
    print("red around enc MHA:", min(xs),min(ys),max(xs),max(ys),len(reds2))
else: print("no red around enc MHA")

# 6. red outline around decoder MHA (purple box x746..834 y327..408)
reds3 = [(x,y) for y in range(320,415) for x in range(740,840) if px[x,y][0]>150 and px[x,y][1]<70 and px[x,y][2]<70]
if reds3:
    xs=[p[0] for p in reds3]; ys=[p[1] for p in reds3]
    print("red in purple-box zone:", min(xs),min(ys),max(xs),max(ys),len(reds3))
    # histogram by row
    rc = collections.Counter(y for x,y in reds3)
    print("red rows:", sorted(rc.items())[:30])
else: print("no red in purple zone")

# 7. enc->dec red dashed arrow: region between stacks x727..746 full height, plus above
reds4 = [(x,y) for y in range(100,500) for x in range(725,750) if px[x,y][0]>150 and px[x,y][1]<80 and px[x,y][2]<80]
print("red in enc/dec gap x725-750:", len(reds4), sorted(set(y for x,y in reds4))[:40])

# 8. 'h' annotation in MHA inset: small dark pixels right of stack
print("== sample MHA inset right zone x460..520 y300..420 ==")
c = collections.Counter()
for y in range(300,420):
    for x in range(460,520):
        c[px[x,y]] += 1
print(c.most_common(5))
