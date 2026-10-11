from PIL import Image
import collections
im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_018.jpg').convert('RGB')
px = im.load()

def bbox(pred, x0,y0,x1,y1,label):
    pts=[(x,y) for y in range(y0,y1) for x in range(x0,x1) if pred(*px[x,y])]
    if not pts: print(label, "NONE"); return None
    xs=[p[0] for p in pts]; ys=[p[1] for p in pts]
    r=(min(xs),min(ys),max(xs),max(ys),len(pts))
    print(label, "bbox", r[:4], "n=",r[4])
    return r

print("=== FRAME A (SDPA) x59..189 y269..491 ===")
bbox(lambda r,g,b: abs(r-177)<28 and abs(g-160)<28 and abs(b-199)<28, 62,272,186,488, "lavender MatMul(s)")
bbox(lambda r,g,b: r>235 and g>235 and 120<b<190, 62,272,186,488, "yellow Scale")
bbox(lambda r,g,b: r>225 and 175<g<225 and 225<b<255, 62,272,186,488, "pink Mask")
bbox(lambda r,g,b: 180<r<215 and 210<g<240 and 160<b<200, 62,272,186,488, "green SoftMax")
bbox(lambda r,g,b: r>150 and g<75 and b<75, 62,440,186,500, "red Q circle zone")
bbox(lambda r,g,b: r<80 and 50<g<110 and 90<b<150, 62,440,186,500, "navy K circle zone")
bbox(lambda r,g,b: r<90 and 90<g<160 and b>150, 62,440,186,500, "blue V circle zone")

print("=== per-row lavender in A (two MatMul boxes?) ===")
lav=[(x,y) for y in range(272,488) for x in range(62,186) if abs(px[x,y][0]-177)<28 and abs(px[x,y][1]-160)<28 and abs(px[x,y][2]-199)<28]
rc=collections.Counter(y for x,y in lav)
print("dense rows:", [(y,n) for y,n in sorted(rc.items()) if n>25])

print("=== FRAME B (MHA) x300..508 y246..515 ===")
bbox(lambda r,g,b: abs(r-187)<25 and abs(g-147)<25 and abs(b-174)<25, 303,249,505,512, "mauve SDPA box")
bbox(lambda r,g,b: r>235 and g>235 and 120<b<190, 303,249,505,512, "yellow Concat")
bbox(lambda r,g,b: r>150 and g<75 and b<75, 303,455,505,520, "red Q circle zone B")
bbox(lambda r,g,b: r<80 and 50<g<110 and 90<b<150, 303,455,505,520, "navy/blue circles zone B")
bbox(lambda r,g,b: abs(r-178)<22 and abs(g-134)<22 and abs(b-89)<22, 303,249,505,512, "tan-brown fill inside B")
# gray/white Linear boxes: white boxes with thin gray border inside B — find border-ish gray rows
print("=== Linear boxes in B: white-fill bbox with gray border — scan rows with many light-gray px ===")
gr=[(x,y) for y in range(249,512) for x in range(303,505) if 150<px[x,y][0]<215 and abs(px[x,y][0]-px[x,y][1])<10 and abs(px[x,y][1]-px[x,y][2])<10]
rc=collections.Counter(y for x,y in gr)
print("grayish rows:", [(y,n) for y,n in sorted(rc.items()) if n>20])
cc=collections.Counter(x for x,y in gr)
print("grayish cols:", [(x,n) for x,n in sorted(cc.items()) if n>12])

print("=== red rect inside B precise ===")
rr=[(x,y) for y in range(340,410) for x in range(285,485) if px[x,y][0]>150 and px[x,y][1]<85 and px[x,y][2]<85]
rc=collections.Counter(y for x,y in rr)
print("rows:", [(y,n) for y,n in sorted(rc.items()) if n>15])
cc=collections.Counter(x for x,y in rr)
print("cols:", [(x,n) for x,n in sorted(cc.items()) if n>8])

print("=== corner handles: green squares at frame corners (5px) ===")
def gc(x0,y0,x1,y1):
    return sum(1 for y in range(y0,y1) for x in range(x0,x1) if px[x,y][1]>110 and px[x,y][0]<110 and px[x,y][2]<110 and px[x,y][1]-px[x,y][0]>40)
for name,(cx,cy) in {"A_TL":(59,269),"A_TR":(189,269),"A_BL":(59,491),"A_BR":(189,491),"B_TL":(300,246),"B_TR":(508,246),"B_BL":(300,515),"B_BR":(508,515)}.items():
    print(name, gc(cx-6,cy-6,cx+7,cy+7))
