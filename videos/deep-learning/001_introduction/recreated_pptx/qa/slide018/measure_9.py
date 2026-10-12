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

print("raw y218 x230..300:", [(x,px[x,218]) for x in range(230,300,4)])
print("raw y258 x230..300:", [(x,px[x,258]) for x in range(230,300,4)])
print("raw y236 x230..300:", [(x,px[x,236]) for x in range(230,300,4)])
print("navy runs y236 x100..760:", rr(236, lambda r,g,b: b>70 and b-r>40 and g<b-10, 100,760))
print("navy runs y215 x100..760:", rr(215, lambda r,g,b: b>70 and b-r>40 and g<b-10, 100,760))
print("green runs y236 x400..600:", rr(236, lambda r,g,b: g>110 and g-r>25 and g-b>15, 400,600))
print("raw y236 x290..310:", [(x,px[x,236]) for x in range(288,312)])
print("raw y236 x405..450:", [(x,px[x,236]) for x in range(405,452,2)])
print("raw y236 x555..600:", [(x,px[x,236]) for x in range(555,600,2)])
print("raw y236 x715..755:", [(x,px[x,236]) for x in range(715,756,2)])
print("=== ellipse text bands: dark rows x85..205 y135..205 ===")
for y in range(136,206,2):
    dk=[x for x in range(85,206) if px[x,y][0]<110 and px[x,y][1]<110]
    if dk: print(" y",y,"n",len(dk),"x",min(dk),max(dk))
print("=== curve trace: red runs x85..175 per y 188..268 ===")
def isred(r,g,b): return r>140 and r-g>50 and r-b>50
for y in range(188,270,4):
    r2 = rr(y,isred,85,178)
    if r2: print(" y",y,r2)
print("=== peach band y198..207 mystery: raw y201 x110..250 ===")
print([(x,px[x,201]) for x in range(110,252,6)])
print("=== arc trace: navy runs per x 205..810 step 15, y130..250 ===")
def isnavy(r,g,b): return b>90 and b-r>60 and r<100
for x in range(205,812,15):
    col=[y for y in range(125,255) if isnavy(*px[x,y])]
    if col: print(" x",x,(min(col),max(col)),len(col))
