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

print("=== CHIP: fill+border runs row 146 (r<245) x320..600 ===")
print(rr(146, lambda r,g,b: r<245 or b<235, 320,600))
print("chip rows: col 346 & 556 vertical extent (nonwhite y125..170)")
for x in [346,400,450,500,556]:
    print(f" x{x}:", [(y,px[x,y]) for y in range(128,166,3)])
print("chip text color: darkest pixels in x360..560 y138..154")
best=[]
for y in range(136,156):
    for x in range(360,560):
        r,g,b=px[x,y]
        if r+g+b < 330: best.append((r,g,b,x,y))
best.sort(key=lambda t:t[0]+t[1]+t[2])
print(best[:8])
print("=== ARC dense: navy y per x 205..812 step 4 (exclude y206..211 box borders) ===")
def isnavy(r,g,b): return b>85 and b-r>55 and r<110
for x in range(205,813,4):
    ys=[y for y in range(125,255) if not (205<=y<=212) and isnavy(*px[x,y])]
    if ys:
        # group into runs
        runs=[];s=ys[0];p=ys[0]
        for y in ys[1:]:
            if y-p>2: runs.append((s,p)); s=y
            p=y
        runs.append((s,p))
        print(f" x{x}: {runs}")
