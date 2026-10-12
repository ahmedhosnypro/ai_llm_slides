from PIL import Image
im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_018.jpg').convert('RGB')
px = im.load()
# star text per-line extents EXCLUDING panel border x>890
for y0,y1,n in [(304,320,'l1'),(320,338,'l2')]:
    xs=[(x,y) for y in range(y0,y1) for x in range(725,891) if px[x,y][0]>140 and px[x,y][0]-px[x,y][1]>50]
    if xs:
        xs2=sorted(set(x for x,_ in xs))
        print(f"{n}: x{xs2[0]}..{xs2[-1]} rows {min(y for _,y in xs)}..{max(y for _,y in xs)}")
# star outline check: any saturated red at spike tips?
for pt in [(736,318),(740,300),(870,320),(860,300),(800,294),(800,344)]:
    print(pt, px[pt[0],pt[1]])
# star vertical extent at x800 (spike top/bottom)
col=[y for y in range(285,355) if px[800,y][0]>240 and px[800,y][1]>238 and px[800,y][2]<235]
print("star col800 yellow:", (min(col),max(col)) if col else None)
# my render star text + star for comparison
im2 = Image.open('render_1-1.png').convert('RGB'); S=1125/540.0; p2=im2.load()
def fr(x,y): return p2[int(x*S),int(y*S)]
isred2 = lambda r,g,b: r>150 and r-g>60 and r-b>60
xs=[(x,y) for y in range(304,338) for x in range(725,891) if isred2(*fr(x,y))]
xs2=sorted(set(x for x,_ in xs))
print("RENDER star text:", f"x{xs2[0]}..{xs2[-1]} rows {min(y for _,y in xs)}..{max(y for _,y in xs)}")
col=[y for y in range(285,355) if fr(800,y)[0]>240 and fr(800,y)[1]>240 and 195<fr(800,y)[2]<235]
print("RENDER star col800:", (min(col),max(col)) if col else None)
print("RENDER chip border sample:", fr(344,146), fr(450,134), fr(450,159))
print("RENDER co text ink:", end=" ")
xs=[(x,y) for y in range(226,252) for x in range(756,890) if sum(fr(x,y))<290]
print(f"x{min(x for x,_ in xs)}..{max(x for x,_ in xs)} y{min(y for _,y in xs)}..{max(y for _,y in xs)}")
