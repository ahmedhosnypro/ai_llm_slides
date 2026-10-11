from PIL import Image
import collections
im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_018.jpg').convert('RGB')
W,H = im.size
px = im.load()

print("== y145..215 detail: per-row x-extents of red and any non-bg ==")
for y in range(145,216,2):
    reds=[x for x in range(20,560) if px[x,y][0]>140 and px[x,y][1]<85 and px[x,y][2]<85]
    nonb=[x for x in range(20,560) if not (abs(px[x,y][0]-231)<12 and abs(px[x,y][1]-233)<12 and abs(px[x,y][2]-230)<14) and not (px[x,y][0]>245 and px[x,y][1]>245 and px[x,y][2]>240)]
    if reds or len(nonb)>3:
        print(y, "red:", (min(reds),max(reds),len(reds)) if reds else None, "nonbg:", (min(nonb),max(nonb),len(nonb)) if nonb else None)

print("== banner line2 color sample: y129..140 x150..420 non-peach mode ==")
c=collections.Counter()
for y in range(128,142):
    for x in range(150,430):
        p=px[x,y]
        if not (abs(p[0]-242)<18 and abs(p[1]-198)<18 and abs(p[2]-153)<20): c[p]+=1
print(c.most_common(8))

print("== title bands x-extents ==")
for (y0,y1,tag) in [(215,230,'band1'),(232,246,'band2'),(250,265,'band3')]:
    reds=[(x,y) for y in range(y0,y1) for x in range(20,560) if px[x,y][0]>140 and px[x,y][1]<85 and px[x,y][2]<85]
    if reds:
        xs=sorted(set(x for x,y in reds))
        # split into clusters
        clusters=[]; cur=[xs[0]]
        for x in xs[1:]:
            if x-cur[-1]<=25: cur.append(x)
            else: clusters.append((cur[0],cur[-1])); cur=[x]
        clusters.append((cur[0],cur[-1]))
        print(tag, "clusters:", clusters, "n=",len(reds))

print("== enc MHA box interior text color: y358..384 x655..718 non-tan mode ==")
c=collections.Counter()
for y in range(358,385):
    for x in range(656,718):
        p=px[x,y]
        if not (abs(p[0]-200)<22 and abs(p[1]-126)<26 and abs(p[2]-87)<26): c[p]+=1
print(c.most_common(8))

print("== green frame A handles/interior: mode inside A x62..186 y250..488 ==")
c=collections.Counter()
for y in range(250,488,2):
    for x in range(62,186,2): c[px[x,y]]+=1
print(c.most_common(10))

print("== green frame B interior: mode inside B x304..505 y273..512 ==")
c=collections.Counter()
for y in range(273,512,2):
    for x in range(304,505,2): c[px[x,y]]+=1
print(c.most_common(10))

print("== gray connector line: scan y146..320 x150..300 for gray ink ==")
pts=[(x,y) for y in range(146,330) for x in range(100,310) if abs(px[x,y][0]-px[x,y][1])<12 and abs(px[x,y][1]-px[x,y][2])<12 and 90<px[x,y][0]<190]
print("gray px:", len(pts))
if pts:
    ys=sorted(set(y for x,y in pts))
    print("y range", min(ys), max(ys))
    cc=collections.Counter(y for x,y in pts)
    print("rows>3:", sorted(cc.items()))
