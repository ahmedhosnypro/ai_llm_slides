from PIL import Image
im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_018.jpg').convert('RGB')
W,H = im.size
print("size", W, H)
px = im.load()

def rowink(y, x0=0, x1=None, pred=None):
    x1 = x1 or W
    runs=[]; s=None
    for x in range(x0,x1):
        r,g,b = px[x,y]
        ok = pred(r,g,b) if pred else (r<150 and g<150 and b<150)
        if ok and s is None: s=x
        if not ok and s is not None: runs.append((s,x-1)); s=None
    if s is not None: runs.append((s,x1-1))
    return runs

def colink(x, y0=0, y1=None, pred=None):
    y1 = y1 or H
    runs=[]; s=None
    for y in range(y0,y1):
        r,g,b = px[x,y]
        ok = pred(r,g,b) if pred else (r<150 and g<150 and b<150)
        if ok and s is None: s=y
        if not ok and s is not None: runs.append((s,y-1)); s=None
    if s is not None: runs.append((s,y1-1))
    return runs

def isred(r,g,b): return r>150 and g<80 and b<80
def isdark(r,g,b): return r<110 and g<110 and b<110
def isnavy(r,g,b): return b>90 and b-r>60 and g<b and r<90

# title band: find red ink rows
print("TITLE red ink rows:")
for y in range(40, 110):
    rr = rowink(y, 60, 900, isred)
    if rr: print(" y",y,[ (a,b) for a,b in rr ][:4], "..." if len(rr)>4 else "")
