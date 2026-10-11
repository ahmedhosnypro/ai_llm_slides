from PIL import Image
import collections
im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_018.jpg').convert('RGB')
px = im.load()

print("== decoder MHA box interior fill mode (x755..815 y280..284 + y300..306) ==")
c=collections.Counter()
for y in list(range(280,285))+list(range(300,307)):
    for x in range(755,816): c[px[x,y]]+=1
print(c.most_common(6))

print("== red x190..505 y235..539 ==")
pts=[(x,y) for y in range(235,540) for x in range(190,506) if px[x,y][0]>150 and px[x,y][1]<85 and px[x,y][2]<85]
print("n=",len(pts))
cc=collections.Counter((x//14*14, y//14*14) for x,y in pts)
for k in sorted(cc):
    if cc[k]>=3: print(k, cc[k])

print("== h circle zone x488..548 y312..378: dark/tan px ==")
pts=[(x,y) for y in range(312,379) for x in range(488,549) if sum(px[x,y])<560]
print("n=",len(pts))
if pts:
    xs=[p[0] for p in pts]; ys=[p[1] for p in pts]
    print("bbox", min(xs),min(ys),max(xs),max(ys))
    cc=collections.Counter((x//6*6,y//6*6) for x,y in pts)
    print(sorted(cc.items()))

print("== gray curve inside frame B: x430..508 y250..330 thin gray ==")
pts=[(x,y) for y in range(248,335) for x in range(425,509) if abs(px[x,y][0]-px[x,y][1])<14 and abs(px[x,y][1]-px[x,y][2])<14 and 80<px[x,y][0]<200]
cc=collections.Counter((x//8*8,y//8*8) for x,y in pts)
print("n=",len(pts)); print(sorted(cc.items()))

print("== bus arrowheads on 18: dark px x630..662 y440..462 / x728..756 y440..462 ==")
for (x0,x1) in [(630,662),(728,756)]:
    pts=[(x,y) for y in range(438,464) for x in range(x0,x1) if sum(px[x,y])<330]
    print((x0,x1), "n=",len(pts), sorted(collections.Counter((x//6*6,y//6*6) for x,y in pts).items())[:12])

print("== enc salmon box red border exact: rows/cols profile ==")
reds=[(x,y) for y in range(348,395) for x in range(640,732) if px[x,y][0]>150 and px[x,y][1]<75 and px[x,y][2]<75]
rc=collections.Counter(y for x,y in reds if px[x,y][0]>150 and px[x,y][1]<75 and px[x,y][2]<75)
top=[ (y,n) for y,n in sorted(rc.items()) if n>20 ]
print("dense rows:", top)
xs=sorted(set(x for x,y in reds))
print("x extent:", min(xs), max(xs))
# left/right edge columns
cc=collections.Counter(x for x,y in reds)
print("dense cols:", [(x,n) for x,n in sorted(cc.items()) if n>8])
