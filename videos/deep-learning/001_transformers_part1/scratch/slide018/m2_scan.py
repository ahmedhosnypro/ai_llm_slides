from PIL import Image
import collections
im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_018.jpg').convert('RGB')
W,H = im.size
px = im.load()

print("== BANNER per-row: peach / red-text / black-text counts x60..500 y95..215 ==")
for y in range(95,215,2):
    p=r_=b_=0
    for x in range(60,500):
        R,G,B = px[x,y]
        if abs(R-242)<16 and abs(G-198)<16 and abs(B-153)<18: p+=1
        elif R>150 and G<80 and B<80: r_+=1
        elif R<90 and G<90 and B<90: b_+=1
    if p or r_ or b_: print(y, "peach",p, "red",r_, "black",b_)

print("== banner border color: top edge scan y100..110 x200..300 ==")
c=collections.Counter()
for y in range(98,112):
    for x in range(200,300): c[px[x,y]]+=1
print(c.most_common(8))

print("== ENC MHA red outline: row hist x640..730, col hist y345..392 ==")
reds=[(x,y) for y in range(340,395) for x in range(635,735) if px[x,y][0]>150 and px[x,y][1]<75 and px[x,y][2]<75]
rc=collections.Counter(y for x,y in reds); cc=collections.Counter(x for x,y in reds)
print("rows:", sorted(rc.items()))
print("cols:", sorted(cc.items()))

print("== PURPLE box zone looser red: x742..838 y323..412 ==")
reds=[(x,y) for y in range(323,412) for x in range(742,838) if px[x,y][0]>140 and px[x,y][1]<95 and px[x,y][2]<95]
rc=collections.Counter(y for x,y in reds); cc=collections.Counter(x for x,y in reds)
print("rows:", sorted(rc.items()))
print("cols:", sorted(cc.items()))

print("== RED corridor gap: x700..775 y245..335 full map ==")
reds=[(x,y) for y in range(245,335) for x in range(695,780) if px[x,y][0]>150 and px[x,y][1]<85 and px[x,y][2]<85]
xs=sorted(set(x for x,y in reds))
print("count",len(reds),"x range",min(xs) if xs else None,max(xs) if xs else None)
cc=collections.Counter(x for x,y in reds)
print("cols:", sorted(cc.items()))
rc=collections.Counter(y for x,y in reds)
print("rows:", sorted(rc.items()))

print("== RED text titles above frames: y196..270 x20..540 ==")
reds=[(x,y) for y in range(196,272) for x in range(20,545) if px[x,y][0]>140 and px[x,y][1]<85 and px[x,y][2]<85]
if reds:
    xs=[p[0] for p in reds]; ys=[p[1] for p in reds]
    print("bbox", min(xs),min(ys),max(xs),max(ys),len(reds))
    rc=collections.Counter(y for x,y in reds)
    print("rows:", sorted(rc.items()))
else: print("none")
