from PIL import Image
im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_018.jpg').convert('RGB')
W,H = im.size
px = im.load()
def runs_row(y, pred, x0=0, x1=None):
    x1=x1 or W; out=[]; s=None
    for x in range(x0,x1):
        if pred(*px[x,y]):
            if s is None: s=x
        else:
            if s is not None: out.append((s,x-1)); s=None
    if s is not None: out.append((s,x1-1))
    return out
def runs_col(x, pred, y0=0, y1=None):
    y1=y1 or H; out=[]; s=None
    for y in range(y0,y1):
        if pred(*px[x,y]):
            if s is None: s=y
        else:
            if s is not None: out.append((s,y-1)); s=None
    if s is not None: out.append((s,y1-1))
    return out

print("=== Training ellipse peach runs ===")
def ispeach(r,g,b): return r>235 and 200<g<238 and 158<b<218
for y in [135,150,170,190,200,210,215]:
    print(" y",y, runs_row(y,ispeach,50,260))
for x in [90,120,150,180,205,220]:
    print(" x",x, runs_col(x,ispeach,110,240))
print("ellipse edge sample (outline):", px[78,170], px[229,170] if True else None, px[150,131], px[150,219])

print("=== box borders: scan row 236 x110..250 raw ===")
print([(x,px[x,236]) for x in range(126,142)])
print("box_pre col140:", runs_col(140, lambda r,g,b: True, 195,285)[:1], [(y,px[140,y]) for y in range(200,275,5)])
print("=== endtoend chip: row 145 raw x325..340 and x560..580 ===")
print([(x,px[x,145]) for x in range(325,345)])
print([(x,px[x,145]) for x in range(558,578)])
print("chip col 350:", [(y,px[350,y]) for y in range(128,170,3)])
print("=== container: row 200 (above boxes) red runs ===")
def isred(r,g,b): return r>140 and r-g>50 and r-b>50
for y in [196,198,200,202,265,268,270,272]:
    print(" y",y, runs_row(y,isred,100,760))
print("container cols: x115,x118,x728,x732 red runs y190..280")
for x in [112,115,118,726,730,734]:
    print(" x",x, runs_col(x,isred,188,285))
print("=== classifier output borders: row 236 x740..760, x860..875 ===")
print([(x,px[x,236]) for x in range(740,762)])
print([(x,px[x,236]) for x in range(856,876)])
print("co col 760:", [(y,px[760,y]) for y in range(200,275,4)])
print("=== deep arrow rows 268..278 runs ===")
for y in range(268,279):
    rr = runs_row(y,isred,100,760)
    if rr: print(" y",y,rr)
print("=== deep label chip pale green runs row 295..310 ===")
def ispg(r,g,b): return 195<r<240 and 232<g<256 and 195<b<240
for y in [285,290,295,300,305,310,315,318]:
    print(" y",y, runs_row(y,ispg,240,600))
print("=== starburst samples ===")
for pt in [(760,330),(800,335),(820,340),(850,330),(880,335),(810,320),(790,350)]:
    print(pt, px[pt[0],pt[1]])
print("=== statement box border blue: row 415 x270..300, x560..585 ===")
def isblue(r,g,b): return b>140 and b-r>40
for y in [408,415]:
    print(" y",y, runs_row(y,isblue,260,600))
print("st col 420:", runs_col(420,isblue,380,460))
print("st col 420 full:", [(y,px[420,y]) for y in range(390,460,4)])
print("=== callout gray boxes row 335 ===")
def isg(r,g,b): return 200<r<235 and 200<g<235 and 200<b<235 and abs(r-g)<10 and abs(g-b)<10
print(" y335", runs_row(335,isg,60,760))
print(" y312", runs_row(312,isg,60,760))
print(" y360", runs_row(360,isg,60,760))
print("callout col 150:", runs_col(150,isg,295,380))
print("callout col 350:", runs_col(350,isg,295,380))
print("callout col 500:", runs_col(500,isg,295,380))
print("callout col 650:", runs_col(650,isg,295,380))
