from PIL import Image
import collections
im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_018.jpg').convert('RGB')
px = im.load()

print("== y528..540 red line full extent ==")
for y in range(526,539):
    xs=[x for x in range(80,940) if px[x,y][0]>150 and px[x,y][1]<85 and px[x,y][2]<85]
    if xs: print(y, min(xs), max(xs), len(xs))

print("== faint red x185..300 y235..350 and y440..540 (thr r>120) ==")
for (y0,y1) in [(235,350),(440,540)]:
    pts=[(x,y) for y in range(y0,y1) for x in range(185,301) if px[x,y][0]>120 and px[x,y][1]<100 and px[x,y][2]<100]
    cc=collections.Counter((x//10*10,y//10*10) for x,y in pts)
    print((y0,y1), "n=",len(pts), sorted(cc.items())[:18])

print("== thin line into h: x476..506 y240..372 any non-white non-green-border ==")
pts=[]
for y in range(240,372):
    for x in range(476,507):
        r,g,b=px[x,y]
        if g>110 and r<110: continue  # green border
        if r>244 and g>244 and b>240: continue  # white
        pts.append((x,y,r,g,b))
cc=collections.Counter((x//6*6,y//8*8) for x,y,*_ in pts)
print("n=",len(pts))
for k in sorted(cc): print(k, cc[k])

print("== sample line pixel colors near (490,300) ==")
for y in range(290,320,3):
    print(y, [px[x,y] for x in range(480,500,4)])
