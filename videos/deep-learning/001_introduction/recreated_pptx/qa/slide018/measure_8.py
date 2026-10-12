from PIL import Image
im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_018.jpg').convert('RGB')
W,H = im.size
px = im.load()
def rr(y,pred,x0,x1):
    out=[];s=None
    for x in range(x0,x1):
        if pred(*px[x,y]):
            if s is None: s=x
        else:
            if s is not None: out.append((s,x-1)); s=None
    if s is not None: out.append((s,x1-1))
    return out
def rc(x,pred,y0,y1):
    out=[];s=None
    for y in range(y0,y1):
        if pred(*px[x,y]):
            if s is None: s=y
        else:
            if s is not None: out.append((s,y-1)); s=None
    if s is not None: out.append((s,y1-1))
    return out
def isred(r,g,b): return r>140 and r-g>50 and r-b>50
def isnavy(r,g,b): return b>70 and b-r>40 and g<b-10
def isgreen(r,g,b): return g>110 and g-r>30 and g-b>20
def isnotwhite(r,g,b): return r<235 or g<235 or b<235

print("=== four boxes: fill runs at y218 (above text) and y258 (below text) ===")
for y in [218, 258]:
    print("y",y,"nonwhite runs x110..740:", [(a,b) for a,b in rr(y,isnotwhite,110,740) if b-a>3])
print("=== classification fill extent row 220 ===")
print(rr(220,isred,560,760))
print("=== box borders vertical: col scans ===")
for x in [131, 290, 442, 589, 717]:
    print(f"x{x}:", rc(x, lambda r,g,b: isnotwhite(r,g,b), 195, 285))
print("=== box_pre interior col 160 raw y205..275 ===")
print([(y,px[160,y]) for y in range(205,276,3)])
print("=== classification: white text band rows (fill gap) ===")
gaps=[y for y in range(210,266) if len(rr(y,isred,585,725))<3]
print("non-fill rows in classification:", gaps)
print("=== CO box: text ink bbox (dark px x745..895 y222..252) ===")
xs=[];ys=[]
for y in range(220,255):
    for x in range(745,895):
        r,g,b=px[x,y]
        if r<90 and g<90 and b<90: xs.append(x);ys.append(y)
print("CO text ink bbox:", (min(xs),max(xs),min(ys),max(ys)) if xs else None)
print("CO box top/bottom border rows at x800:", [(y,px[800,y]) for y in range(204,214)], [(y,px[800,y]) for y in range(260,270)])
print("=== ellipse: peach count per row y125..232 (x60..245) ===")
def ispeach(r,g,b): return r>235 and 198<g<240 and 155<b<220
for y in range(126,232,3):
    c=[x for x in range(60,246) if ispeach(*px[x,y])]
    if c: print(" y",y,"x",min(c),max(c),"n",len(c))
print("=== ellipse outline check: raw col 155 y126..135, y200..212; row 130 x75..90 ===")
print([(y,px[155,y]) for y in range(125,136)])
print([(y,px[155,y]) for y in range(198,213)])
print([(x,px[x,132]) for x in range(72,95)])
print([(x,px[x,205]) for x in range(150,180)])
