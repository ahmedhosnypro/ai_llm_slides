from PIL import Image
import collections
im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_018.jpg').convert('RGB')
im17 = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_017.jpg').convert('RGB')
px = im.load(); p17 = im17.load()

print("=== tan-ish per-row x-extents y150..215 ===")
for y in range(150,216,3):
    xs=[x for x in range(40,520) if 200<px[x,y][0]<235 and 185<px[x,y][1]<218 and 165<px[x,y][2]<200]
    if xs: print(y, min(xs), max(xs), len(xs))

print("=== raw colors x460..500 y150..250 sample grid ===")
for y in range(150,251,20):
    print(y, [px[x,y] for x in range(460,501,8)])

print("=== strip x-profile at y=170,200,230: counts per x ===")
for y in [170,200,230]:
    cc=collections.Counter()
    for x in range(455,500):
        r,g,b = px[x,y]
        if not (r>243 and g>243 and b>238) and not (abs(r-231)<10 and abs(g-233)<10 and abs(b-230)<12): cc[x]+=1
    print(y, sorted(cc.items()))

print("=== circles A: blue cluster x-histogram y460..485 ===")
cc=collections.Counter()
for y in range(460,486):
    for x in range(62,186):
        r,g,b = px[x,y]
        if r<90 and g<80 and b>120: cc[x]+=1
print(sorted(cc.items()))

print("=== circles B: blue cluster x-histogram y485..510 ===")
cc=collections.Counter()
for y in range(485,511):
    for x in range(304,505):
        r,g,b = px[x,y]
        if r<90 and g<80 and b>120: cc[x]+=1
print(sorted(cc.items()))

print("=== h ring colors: points at radius ~9 from (494,367) ===")
import math
for ang in range(0,360,45):
    x = int(494+9*math.cos(math.radians(ang))); y = int(367+9*math.sin(math.radians(ang)))
    print(ang, (x,y), px[x,y])

print("=== 17 vs 18 right-frame corner handles ===")
def gc(p,cx,cy):
    return sum(1 for y in range(cy-6,cy+7) for x in range(cx-6,cx+7) if p[x,y][1]>110 and p[x,y][0]<110 and p[x,y][2]<110 and p[x,y][1]-p[x,y][0]>40)
for cx,cy in [(572,103),(896,103),(572,526),(896,526)]:
    print((cx,cy), "17:", gc(p17,cx,cy), "18:", gc(px,cx,cy))

print("=== Mask/SoftMax actual fills in A: modes at y366..376 x100..140 and y330..344 x95..150 ===")
for (y0,y1,x0,x1,tag) in [(366,377,95,145,'Mask?'),(328,346,90,155,'SoftMax?')]:
    c=collections.Counter()
    for y in range(y0,y1):
        for x in range(x0,x1): c[px[x,y]]+=1
    print(tag, c.most_common(5))
