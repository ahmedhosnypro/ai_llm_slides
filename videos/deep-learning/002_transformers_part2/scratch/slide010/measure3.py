#!/usr/bin/env python3
# measure3.py — decisive numeric pass on slide_010.jpg (+ slide_009.jpg comparison for left panel)
from PIL import Image
def load(n): return Image.open(f"/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/{n}").convert("RGB")
im = load("slide_010.jpg"); px = im.load(); W,H = im.size
im9 = load("slide_009.jpg"); px9 = im9.load()
out=[]
def p(*a): s=" ".join(str(x) for x in a); out.append(s); print(s)

def reddish(c): r,g,b=c; return r>110 and r-g>55 and r-b>45
def runs_col(px,x, fn, y0, y1, minlen=1):
    rs=[];prev=False;st=None
    for y in range(y0,y1):
        c=fn(px[x,y])
        if c and not prev: st=y
        if not c and prev and y-st>=minlen: rs.append((st,y-1))
        prev=c
    if prev and y1-st>=minlen: rs.append((st,y1-1))
    return rs
def runs_row(px,y, fn, x0, x1, minlen=1):
    rs=[];prev=False;st=None
    for x in range(x0,x1):
        c=fn(px[x,y])
        if c and not prev: st=x
        if not c and prev and x-st>=minlen: rs.append((st,x-1))
        prev=c
    if prev and x1-st>=minlen: rs.append((st,x1-1))
    return rs

# a. chrome borders raw
p("== CHROME raw ==")
p("row300 x50..70:", [(x,px[x,300]) for x in range(50,70,2)])
p("row300 x893..915:", [(x,px[x,300]) for x in range(893,915,2)])
p("col480 y74..84:", [(y,px[480,y]) for y in range(74,84)])
p("col480 y512..522:", [(y,px[480,y]) for y in range(512,522)])
p("chrome red-ish col58:", runs_col(px,58,reddish,0,540,2), " col900:", runs_col(px,900,reddish,0,540,2))

# b. title tight
ys=range(44,74)
cols=[x for x in range(100,845) if any(reddish(px[x,y]) for y in ys)]
rows=[y for y in ys if any(reddish(px[x,y]) for x in range(100,845))]
p("title bbox x %d..%d y %d..%d"%(min(cols),max(cols),min(rows),max(rows)))

# c. subtitle segments (fy 76..100): per-color column runs
def isblue(c): r,g,b=c; return b>140 and b-r>50 and g<130
def isgreen(c): r,g,b=c; return g>110 and g-r>35 and g-b>35
def bigred(c): r,g,b=c; return r>150 and g<90 and b<90
for name,fn in (("blue",isblue),("red",bigred),("green",isgreen)):
    crs=runs_row(px,0,fn,0,0)  # placeholder
cols_blue=[x for x in range(60,900) if any(isblue(px[x,y]) for y in range(76,100))]
cols_red=[x for x in range(60,900) if any(bigred(px[x,y]) for y in range(76,104))]
cols_grn=[x for x in range(60,900) if any(isgreen(px[x,y]) for y in range(76,100))]
def gaps(xs, g=6):
    if not xs: return []
    xs=sorted(set(xs)); segs=[[xs[0],xs[0]]]
    for x in xs[1:]:
        if x-segs[-1][1]<=g: segs[-1][1]=x
        else: segs.append([x,x])
    return segs
p("sub blue col segs:", gaps(cols_blue))
p("sub red col segs:", gaps(cols_red))
p("sub green col segs:", gaps(cols_grn))
# vertical extents
for name,fn,rg in (("blue",isblue,(76,102)),("redX",bigred,(74,106)),("green",isgreen,(76,102))):
    rr=[y for y in range(*rg) if any(fn(px[x,y]) for x in range(60,900))]
    p("sub",name,"rows:", (min(rr),max(rr)) if rr else None)
p("underline blue rows y96..108:", [(y,len([x for x in range(200,470) if isblue(px[x,y])])) for y in range(96,108)])

# d. left panel border color core + box
p("== LEFT PANEL ==")
dark=[(px[x,300],x) for x in range(274,280)]
p("right border darkest:", min(dark))
dark=[(px[x,300],x) for x in range(78,84)]
p("left border darkest:", min(dark))
p("col150 border rows 99..104:", [(y,px[150,y]) for y in range(99,104)])
p("col150 border rows 506..512:", [(y,px[150,y]) for y in range(506,512)])

# e. header ink
def isdark(c): r,g,b=c; return r<80 and g<80 and b<80
rows=[y for y in range(106,140) if any(isdark(px[x,y]) for x in range(85,175))]
cols=[x for x in range(85,205) if any(isdark(px[x,y]) or bigred(px[x,y]) for y in range(106,140))]
p("header all-ink bbox x %d..%d y %d..%d"%(min(cols),max(cols),min(rows),max(rows)))
xr=[x for x in range(170,215) if any(bigred(px[x,y]) for y in range(104,140))]
yr=[y for y in range(104,140) if any(bigred(px[x,y]) for x in range(170,215))]
p("header X red bbox x %s..%s y %s..%s"%(min(xr),max(xr),min(yr),max(yr)))
hb=[y for y in range(106,140) if any(isdark(px[x,y]) for x in range(85,175))]
p("header black rows:", (min(hb),max(hb)) if hb else None)

# f. inputs (pink circles) both frames
def ispink(c): r,g,b=c; return r>225 and b>210 and g<215 and r-g>35
p("== INPUTS s10 ==")
for i,(y0,y1) in enumerate(((135,190),(245,300),(355,410),(455,512))):
    xs=[];ys2=[]
    for y in range(y0,y1):
        for x in range(70,112):
            if ispink(px[x,y]): xs.append(x);ys2.append(y)
    if xs: p("input%d pink bbox (%d,%d,%d,%d) c=(%.1f,%.1f)"%(i+1,min(xs),min(ys2),max(xs),max(ys2),(min(xs)+max(xs))/2,(min(ys2)+max(ys2))/2))
p("== INPUTS s9 ==")
for i,(y0,y1) in enumerate(((135,190),(245,300),(355,410),(455,512))):
    xs=[];ys2=[]
    for y in range(y0,y1):
        for x in range(70,112):
            if ispink(px9[x,y]): xs.append(x);ys2.append(y)
    if xs: p("input%d pink bbox (%d,%d,%d,%d) c=(%.1f,%.1f)"%(i+1,min(xs),min(ys2),max(xs),max(ys2),(min(xs)+max(xs))/2,(min(ys2)+max(ys2))/2))

# g. neurons both frames: red-rim col scans at several x + row scans
p("== NEURONS s10 ==")
for i,(y0,y1) in enumerate(((130,195),(235,300),(340,405),(440,505))):
    best=None
    for x in range(215,245):
        rs=runs_col(px,x,reddish,y0,y1,1)
        if len(rs)>=2:
            span=rs[-1][1]-rs[0][0]
            if best is None or span>best[1]: best=(x,span,rs)
    p("neuron%d colscan"%(i+1), best)
p("== NEURONS s9 ==")
for i,(y0,y1) in enumerate(((140,200),(245,310),(355,420),(460,522))):
    best=None
    for x in range(215,245):
        rs=runs_col(px9,x,reddish,y0,y1,1)
        if len(rs)>=2:
            span=rs[-1][1]-rs[0][0]
            if best is None or span>best[1]: best=(x,span,rs)
    p("neuron%d colscan"%(i+1), best)

# h. connection line colors: samples along input->neuron1 lines
p("== LINE COLORS s10 ==")
p("x1->n1 t.5 (160,162):", px[160,162])
p("x2->n1 (150,225):", px[150,225], " x3->n1 (155,280):", px[155,280], " x4->n1 (165,330):", px[165,330])
p("x1->n4 (120,300):", px[120,300], " x2->n4 (135,390):", px[135,390], " x3->n4 (150,440):", px[150,440], " x4->n4 (160,480):", px[160,480])

# i. weight stack x extents (s10)
def isbluetxt(c): r,g,b=c; return b>140 and b-r>60
def ispurptxt(c): r,g,b=c; return r>140 and b>140 and g<120
def isorngtxt(c): r,g,b=c; return r>170 and 80<g<190 and b<110
def isgrntxt(c): r,g,b=c; return g>110 and g-r>35 and g-b>35
bands={"blue":((145,240),isbluetxt),"purple":((238,320),ispurptxt),"orange":((325,400),isorngtxt),"green":((398,480),isgrntxt)}
for nm,((y0,y1),fn) in bands.items():
    xs=[x for x in range(115,175) if any(fn(px[x,y]) for y in range(y0,y1))]
    p("stack",nm,"x extent:", (min(xs),max(xs)) if xs else None)

# j. outputs: green y labels + arrows per neuron
p("== OUTPUTS s10 ==")
def isgrn2(c): r,g,b=c; return g>100 and g-r>25 and g-b>25
for i,(y0,y1) in enumerate(((140,195),(242,297),(347,402),(447,502))):
    xs=[];ys2=[]
    for y in range(y0,y1):
        for x in range(240,305):
            if isgrn2(px[x,y]): xs.append(x);ys2.append(y)
    if xs: p("out%d green bbox (%d,%d,%d,%d)"%(i+1,min(xs),min(ys2),max(xs),max(ys2)))
p("y1 text vs arrow rows: y155..175 x245..300 green counts:", [(y,len([x for x in range(245,300) if isgrn2(px[x,y])])) for y in range(152,178,2)])

# k. mid panels borders raw
p("== MIDPANEL raw ==")
p("row150 x284..296:", [(x,px[x,150]) for x in range(284,296)])
p("row150 x500..515:", [(x,px[x,150]) for x in range(500,515)])
p("col350 y88..102:", [(y,px[350,y]) for y in range(88,102)])
p("col350 y284..298:", [(y,px[350,y]) for y in range(284,298)])
p("col350 y302..320:", [(y,px[350,y]) for y in range(302,320)])
p("col350 y498..512:", [(y,px[350,y]) for y in range(498,512)])

# l. mid contents: Y^T tight, brackets, pink stadium, boxes row raw
p("== MID1 contents ==")
xs=[x for x in range(335,405) if any(bigred(px[x,y]) for y in range(148,192))]
ys2=[y for y in range(148,192) if any(bigred(px[x,y]) for x in range(335,405))]
p("Yt1 tight bbox x %d..%d y %d..%d"%(min(xs),max(xs),min(ys2),max(ys2)))
xs=[x for x in range(290,320) if any(bigred(px[x,y]) for y in range(175,245))]
ys2=[y for y in range(175,245) if any(bigred(px[x,y]) for x in range(290,320))]
p("bracketL1 bbox x %d..%d y %d..%d"%(min(xs),max(xs),min(ys2),max(ys2)))
xs=[x for x in range(415,445) if any(bigred(px[x,y]) for y in range(175,245))]
ys2=[y for y in range(175,245) if any(bigred(px[x,y]) for x in range(415,445))]
p("bracketR1 bbox x %d..%d y %d..%d"%(min(xs),max(xs),min(ys2),max(ys2)))
def ispinkish(c): r,g,b=c; return r>225 and b>200 and r-g>25
xs=[];ys3=[]
for y in range(178,235):
    for x in range(300,440):
        if ispinkish(px[x,y]): xs.append(x);ys3.append(y)
p("stadium1 pink bbox:", (min(xs),min(ys3),max(xs),max(ys3)) if xs else None)
p("boxrow1 y198 raw x312..432:", [(x,px[x,198]) for x in range(312,432,4)])
p("box fill samples:", px[325,196], px[360,196], px[395,196], "text px:", px[328,199])
p("== MID2 contents ==")
xs=[x for x in range(335,405) if any(bigred(px[x,y]) for y in range(360,400))]
ys2=[y for y in range(360,400) if any(bigred(px[x,y]) for x in range(335,405))]
p("Yt2 tight bbox x %d..%d y %d..%d"%(min(xs),max(xs),min(ys2),max(ys2)))
xs=[];ys3=[]
for y in range(388,445):
    for x in range(300,440):
        if ispinkish(px[x,y]): xs.append(x);ys3.append(y)
p("stadium2 pink bbox:", (min(xs),min(ys3),max(xs),max(ys3)) if xs else None)
xs=[x for x in range(290,320) if any(bigred(px[x,y]) for y in range(385,455))]
ys2=[y for y in range(385,455) if any(bigred(px[x,y]) for x in range(290,320))]
p("bracketL2 bbox x %d..%d y %d..%d"%(min(xs),max(xs),min(ys2),max(ys2)))
p("boxrow2 y412 raw x312..432:", [(x,px[x,412]) for x in range(312,432,4)])

# m. arrows
p("== ARROWS ==")
p("center col474 red runs y190..440:", runs_col(px,474,bigred,190,440,1))
p("center row405 red runs:", runs_row(px,405,bigred,455,500,1))
p("center row210 red runs:", runs_row(px,210,bigred,455,500,1))
p("right col868 red runs y275..355:", runs_col(px,868,bigred,275,355,1))
p("right row336 red runs:", runs_row(px,336,bigred,850,895,1))
p("right row295 red runs:", runs_row(px,295,bigred,850,895,1))

# n. right panels borders raw
p("== RIGHTPANEL raw ==")
p("row200 x515..525:", [(x,px[x,200]) for x in range(515,525)])
p("row200 x898..912:", [(x,px[x,898-898+898+0]) for x in []] )
p("row200 x900..914:", [(x,px[x,200]) for x in range(900,914)])
p("col600 y92..106:", [(y,px[600,y]) for y in range(92,106)])
p("col600 y284..296:", [(y,px[600,y]) for y in range(284,296)])
p("col600 y304..318:", [(y,px[600,y]) for y in range(304,318)])
p("col600 y498..512:", [(y,px[600,y]) for y in range(498,512)])
p("fill samples:", px[600,250], px[660,250], px[600,450], px[660,450])

# o. braceL bbox
def isblue2(c): r,g,b=c; return b>120 and b-r>50 and g<150
xs=[x for x in range(512,548) if any(isblue2(px[x,y]) for y in range(95,310))]
ys2=[y for y in range(95,310) if any(isblue2(px[x,y]) for x in range(512,548))]
p("braceL1 bbox x %s..%s y %s..%s"%(min(xs),max(xs),min(ys2),max(ys2)) if xs else "braceL1 none")
xs=[x for x in range(512,548) if any(isblue2(px[x,y]) for y in range(308,515))]
ys2=[y for y in range(308,515) if any(isblue2(px[x,y]) for x in range(512,548))]
p("braceL2 bbox x %s..%s y %s..%s"%(min(xs),max(xs),min(ys2),max(ys2)) if xs else "braceL2 none")

# p. X pill1: stadium fill bbox, brackets, circles
p("== XPILL1 ==")
xs=[];ys2=[]
for y in range(95,155):
    for x in range(515,675):
        if ispinkish(px[x,y]): xs.append(x);ys2.append(y)
p("pill1 pinkfill bbox:", (min(xs),min(ys2),max(xs),max(ys2)) if xs else None)
xs=[x for x in range(515,675) if any(bigred(px[x,y]) for y in range(100,150))]
p("pill1 red col segs:", gaps(xs,4))
p("pill1 row130 red runs x535..660:", runs_row(px,130,bigred,535,660,1))
p("circle fill sample:", px[560,130], px[590,130], "label ink:", px[562,132])
xs=[x for x in range(545,660) if any(bigred(px[x,y]) for y in range(140,180))]
ys2=[y for y in range(140,180) if any(bigred(px[x,y]) for x in range(545,660))]
p("bigX1 bbox x %d..%d y %d..%d"%(min(xs),max(xs),min(ys2),max(ys2)))

# q. matrix1: container + cells
def ismint(c): r,g,b=c; return g>225 and g-r>12 and b>200
p("== MATRIX1 ==")
p("mint row200 runs x655..840:", runs_row(px,200,ismint,655,840,2))
p("mint col672 runs y100..300:", runs_col(px,672,ismint,100,300,2))
p("cell row138 raw x678..818:", [(x,px[x,138]) for x in range(678,818,6)])
p("cell col684 runs y125..275 (yellow):", runs_col(px,684,lambda c: c[0]>225 and c[1]>215 and c[2]<210,125,275,2))
p("cell text colors:", px[695,145], px[731,145], px[695,183], px[695,222], px[695,260])

# r. braceR1, plus1, bias1
p("== BRACE/PLUS/BIAS1 ==")
xs=[x for x in range(812,842) if any(isblue2(px[x,y]) for y in range(100,300))]
ys2=[y for y in range(100,300) if any(isblue2(px[x,y]) for x in range(812,842))]
p("braceR1 bbox x %d..%d y %d..%d"%(min(xs),max(xs),min(ys2),max(ys2)))
xs=[x for x in range(835,860) if any(bigred(px[x,y]) for y in range(185,210))]
ys2=[y for y in range(185,210) if any(bigred(px[x,y]) for x in range(835,860))]
p("plus1 bbox x %d..%d y %d..%d"%(min(xs),max(xs),min(ys2),max(ys2)))
p("bias row130 raw x845..900:", [(x,px[x,130]) for x in range(845,900,3)])
p("bias col858 yellow runs y100..300:", runs_col(px,858,lambda c: c[0]>225 and c[1]>215 and c[2]<210,100,300,2))
xs=[x for x in range(845,905) if any(bigred(px[x,y]) for y in range(105,300))]
p("bias1 red col segs:", gaps(xs,3))

# s. panel2 key items
p("== PANEL2 items ==")
xs=[];ys2=[]
for y in range(305,370):
    for x in range(515,675):
        if ispinkish(px[x,y]): xs.append(x);ys2.append(y)
p("pill2 pinkfill bbox:", (min(xs),min(ys2),max(xs),max(ys2)) if xs else None)
p("pill2 row343 red runs x535..660:", runs_row(px,343,bigred,535,660,1))
xs=[x for x in range(545,660) if any(bigred(px[x,y]) for y in range(352,395))]
ys2=[y for y in range(352,395) if any(bigred(px[x,y]) for x in range(545,660))]
p("bigX2 bbox x %d..%d y %d..%d"%(min(xs),max(xs),min(ys2),max(ys2)))
p("matrix2 mint row412 runs x655..840:", runs_row(px,412,ismint,655,840,2))
p("matrix2 col672 mint runs y300..520:", runs_col(px,672,ismint,300,520,2))
p("cell col684 yellow runs y330..510:", runs_col(px,684,lambda c: c[0]>225 and c[1]>215 and c[2]<210,330,510,2))
xs=[x for x in range(812,842) if any(isblue2(px[x,y]) for y in range(310,515))]
ys2=[y for y in range(310,515) if any(isblue2(px[x,y]) for x in range(812,842))]
p("braceR2 bbox x %d..%d y %d..%d"%(min(xs),max(xs),min(ys2),max(ys2)))
xs=[x for x in range(835,860) if any(bigred(px[x,y]) for y in range(395,425))]
ys2=[y for y in range(395,425) if any(bigred(px[x,y]) for x in range(835,860))]
p("plus2 bbox x %d..%d y %d..%d"%(min(xs),max(xs),min(ys2),max(ys2)))
p("bias2 col858 yellow runs y310..515:", runs_col(px,858,lambda c: c[0]>225 and c[1]>215 and c[2]<210,310,515,2))
xs=[x for x in range(845,905) if any(bigred(px[x,y]) for y in range(315,515))]
p("bias2 red col segs:", gaps(xs,3))
p("bias2 row343 raw x845..900:", [(x,px[x,343]) for x in range(845,900,3)])

open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide010/measure3_output.txt","w").write("\n".join(out))
