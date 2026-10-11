from PIL import Image
import collections
im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_018.jpg').convert('RGB')
px = im.load()

def boxscan(pred, y0,y1,x0,x1,tag,minrow=6):
    rows=collections.Counter()
    for y in range(y0,y1):
        for x in range(x0,x1):
            if pred(*px[x,y]): rows[y]+=1
    bands=[]; cur=None
    for y in range(y0,y1):
        if rows[y]>=minrow and cur is None: cur=[y,y]
        elif rows[y]>=minrow and cur: cur[1]=y
        elif rows[y]<minrow and cur: bands.append(tuple(cur)); cur=None
    if cur: bands.append(tuple(cur))
    out=[]
    for (a,b) in bands:
        xs=[x for y in range(a,b+1) for x in range(x0,x1) if pred(*px[x,y])]
        out.append(((a,b),(min(xs),max(xs))))
    print(tag, out)

print("=== A: lavender, rose(Mask), green(SoftMax), yellow(Scale) boxes ===")
boxscan(lambda r,g,b: abs(r-177)<30 and abs(g-160)<30 and abs(b-199)<30, 280,470,62,186, "lavender")
boxscan(lambda r,g,b: abs(r-240)<14 and abs(g-197)<14 and abs(b-217)<14, 350,395,62,186, "rose Mask")
boxscan(lambda r,g,b: abs(r-206)<16 and abs(g-231)<14 and abs(b-210)<16, 310,370,62,186, "palegreen SoftMax")
boxscan(lambda r,g,b: r>235 and g>235 and 120<b<190, 385,425,62,186, "yellow Scale")
print("V/K/Q fills:", px[166,473], px[128,473], px[91,473], "| B:", px[330,498], px[387,498], px[445,498])
print("A circle y-extents: K/V", end=" ")
ys=[y for y in range(455,495) for x in [128,166] if px[x,y][2]>110 and px[x,y][0]<90]
print(min(ys), max(ys))

print("=== B: top Linear box (border scan y255..300) ===")
boxscan(lambda r,g,b: r<160 and g<160 and b<160, 252,300,304,505, "dark border rows", 4)
print("=== B: mauve SDPA box dense ===")
boxscan(lambda r,g,b: abs(r-187)<25 and abs(g-147)<25 and abs(b-174)<25, 300,470,304,505, "mauve", 20)
print("=== B: three Linear boxes (border rows y400..445) ===")
boxscan(lambda r,g,b: r<160 and g<160 and b<160, 398,448,304,505, "dark rows", 4)
# x-extents of the 3 boxes at their mid-row
for y in [412, 420]:
    xs=[x for x in range(304,505) if px[x,y][0]<160 and px[x,y][1]<160]
    print("y",y,"dark x:", xs)

print("=== B: gray shadow copies (light gray fill ~ (217,217,217)?) ===")
boxscan(lambda r,g,b: 200<r<235 and 200<g<235 and 200<b<235 and abs(r-g)<8 and abs(g-b)<8, 250,300,304,505, "shadow top", 8)
boxscan(lambda r,g,b: 200<r<235 and 200<g<235 and 200<b<235 and abs(r-g)<8 and abs(g-b)<8, 398,450,304,505, "shadow linear", 8)

print("=== peach connector ink right of banner? x490..565 y95..148 raw nonbg ===")
pts=[(x,y) for y in range(95,149) for x in range(490,566) if not (px[x,y][0]>243 and px[x,y][1]>243 and px[x,y][2]>238) and not (abs(px[x,y][0]-231)<10 and abs(px[x,y][1]-233)<10 and abs(px[x,y][2]-230)<12)]
print("n=",len(pts), pts[:20])

print("=== inside-B line into h: exact x per y (faint) ===")
for y in range(250,355,10):
    xs=[x for x in range(478,500) if not (px[x,y][0]>243 and px[x,y][1]>243 and px[x,y][2]>238)]
    print(y, xs)
