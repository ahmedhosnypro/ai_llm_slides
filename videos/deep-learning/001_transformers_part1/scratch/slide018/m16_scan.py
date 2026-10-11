from PIL import Image
import collections
im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_018.jpg').convert('RGB')
px = im.load()

def ink(x,y):
    r,g,b = px[x,y]
    return not (r>243 and g>243 and b>238)  # not white-ish

print("=== FRAME A interior row-profile (ink count per row, x62..186) ===")
prof=[]
for y in range(272,500):
    n=sum(1 for x in range(62,186) if ink(x,y))
    prof.append((y,n))
runs=[]
cur=None
for y,n in prof:
    if n>8 and cur is None: cur=[y,y,n]
    elif n>8 and cur: cur[1]=y; cur[2]=max(cur[2],n)
    elif n<=8 and cur: runs.append(tuple(cur)); cur=None
if cur: runs.append(tuple(cur))
print("ink bands:", runs)

print("=== x-extents per band ===")
for (y0,y1,_) in runs:
    xs=[x for y in range(y0,y1+1) for x in range(62,186) if ink(x,y)]
    print((y0,y1), "x", min(xs), max(xs))

print("=== circles in A: red/navy/blue clusters y455..495 ===")
for pred,name in [(lambda r,g,b: r>150 and g<75 and b<75,"red"),(lambda r,g,b: r<80 and 40<g<110 and 80<b<160,"navy"),(lambda r,g,b: r<90 and g<80 and b>120,"blue")]:
    pts=[(x,y) for y in range(450,500) for x in range(62,186) if pred(*px[x,y])]
    if pts:
        xs=[p[0] for p in pts]; ys=[p[1] for p in pts]
        print(name, (min(xs),min(ys),max(xs),max(ys)), len(pts))

print("=== FRAME B interior row-profile (x304..505) ===")
runs=[]; cur=None
for y in range(250,516):
    n=sum(1 for x in range(304,505) if ink(x,y))
    if n>10 and cur is None: cur=[y,y,n]
    elif n>10 and cur: cur[1]=y; cur[2]=max(cur[2],n)
    elif n<=10 and cur: runs.append(tuple(cur)); cur=None
if cur: runs.append(tuple(cur))
print("ink bands:", runs)
for (y0,y1,_) in runs:
    xs=[x for y in range(y0,y1+1) for x in range(304,505) if ink(x,y)]
    print((y0,y1), "x", min(xs), max(xs))

print("=== circles in B y470..515 ===")
for pred,name in [(lambda r,g,b: r>150 and g<75 and b<75,"red"),(lambda r,g,b: r<80 and 40<g<110 and 80<b<160,"navy"),(lambda r,g,b: r<90 and g<80 and b>120,"blue")]:
    pts=[(x,y) for y in range(465,516) for x in range(304,505) if pred(*px[x,y])]
    if pts:
        xs=[p[0] for p in pts]; ys=[p[1] for p in pts]
        print(name, (min(xs),min(ys),max(xs),max(ys)), len(pts))

print("=== h circle colors (x485..505 y355..380) ===")
c=collections.Counter()
for y in range(355,381):
    for x in range(485,506): c[px[x,y]]+=1
print(c.most_common(8))

print("=== right frame handles? green at (572,103),(896,103),(572,526),(896,526) ===")
def gc(cx,cy):
    return sum(1 for y in range(cy-6,cy+7) for x in range(cx-6,cx+7) if px[x,y][1]>110 and px[x,y][0]<110 and px[x,y][2]<110 and px[x,y][1]-px[x,y][0]>40)
print("fig_frame corners:", gc(572,103), gc(896,103), gc(572,526), gc(896,526))

print("=== y157..161 line colors x300..480 ===")
c=collections.Counter()
for y in range(156,163):
    for x in range(300,480): c[px[x,y]]+=1
print(c.most_common(6))

print("=== GC1 above frame B: faint gray x470..500 y130..246 ===")
pts=[(x,y) for y in range(130,247) for x in range(470,501) if 195<px[x,y][0]<240 and abs(px[x,y][0]-px[x,y][1])<12 and abs(px[x,y][1]-px[x,y][2])<12]
cc=collections.Counter((x//6*6,y//12*12) for x,y in pts)
print("n=",len(pts), sorted(cc.items())[:24])
