from PIL import Image
from collections import Counter
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
isgray = lambda r,g,b: 195<r<238 and 195<g<238 and abs(r-g)<10 and abs(r-b)<14
print("=== callout horizontal extents at clean rows ===")
for y in [307,309,368,370,372]:
    print(" y",y,[r for r in rr(y,isgray,70,760) if r[1]-r[0]>8])
print("=== callout vertical extents (clean cols near each box left edge) ===")
for x in [90, 292, 458, 606]:
    runs=[];s=None
    for y in range(298,380):
        ok=isgray(*px[x,y])
        if ok and s is None: s=y
        if not ok and s is not None:
            if y-s>3: runs.append((s,y-1))
            s=None
    print(f" x{x}:", runs)
print("=== callout text ink bboxes (dark or red in each zone) ===")
zones = {"c1":(80,275),"c2":(280,445),"c3":(450,595),"c4":(598,745)}
for name,(a,b) in zones.items():
    xs=[];ys=[];red=[]
    for y in range(300,378):
        for x in range(a,b):
            r,g,b2=px[x,y]
            if r<110 and g<110 and b2<110: xs.append(x);ys.append(y)
            if r>140 and r-g>50 and r-b2>50: xs.append(x);ys.append(y);red.append((x,y))
    if xs:
        print(f" {name}: ink x{min(xs)}..{max(xs)} y{min(ys)}..{max(ys)} red_n{len(red)}", 
              ("red rows "+str(sorted(set(y for _,y in red))[:3])+".."+str(sorted(set(y for _,y in red))[-3:])) if red else "")
print("=== starburst: per-row yellow/red counts x730..920 ===")
for y in range(295,385,4):
    yel=sum(1 for x in range(725,925) if px[x,y][0]>240 and px[x,y][1]>238 and px[x,y][2]<235)
    red=sum(1 for x in range(725,925) if px[x,y][0]>140 and px[x,y][0]-px[x,y][1]>50)
    if yel or red: print(f"  y{yel and y or y}: yel{yel} red{red}")
print("=== statement red text x-extents per line ===")
for y0,y1,name in [(398,418,'line1'),(420,442,'line2')]:
    xs=[x for y in range(y0,y1) for x in range(280,570) if px[x,y][0]>140 and px[x,y][0]-px[x,y][1]>50]
    print(f" {name}: x{min(xs)}..{max(xs)}" if xs else f" {name}: none")
print("=== CO right-edge glyphs: per-row dark x860..880 ===")
for y in range(226,252,2):
    dk=[x for x in range(858,882) if px[x,y][0]<95 and px[x,y][1]<95 and px[x,y][2]<95]
    if dk: print(f"  y{y}: {dk}")
print("=== chip border modal (pixels at chip edge band) ===")
c=Counter()
for y in range(134,160):
    for x in range(341,347):
        c[px[x,y]]+=1
print(c.most_common(4))
print("=== title: per-word check 26pt fit: ink x223..654 w431 ===")
print("=== deep-label chip: top/bottom border rows at x350,x470 ===")
for x in [350,470]:
    print(f" x{x}:", [(y,px[x,y]) for y in range(278,305,2)])
