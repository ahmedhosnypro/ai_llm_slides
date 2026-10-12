#!/usr/bin/env python3
# measure1.py — slide_010.jpg (960x540) big-ticket geometry sweep
from PIL import Image
import sys
im = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_010.jpg").convert("RGB")
W, H = im.size
px = im.load()
out = []
def p(*a):
    s = " ".join(str(x) for x in a)
    out.append(s); print(s)

p("size", W, H)

def isred(c):   r,g,b=c; return r>150 and g<90 and b<90
def isblue(c):  r,g,b=c; return b>140 and r<110 and g<110
def isgreen(c): r,g,b=c; return g>120 and r<130 and b<130
def isdark(c):  r,g,b=c; return r<70 and g<70 and b<70
def isyellowish(c): r,g,b=c; return r>200 and g>200 and b<190
def ispink(c):  r,g,b=c; return r>220 and b>200 and g<190

# 1. chrome landmarks
row=300
reds=[x for x in range(0,W) if isred(px[x,row])]
p("chrome red verticals @y300:", reds[:12], "...", reds[-12:] if len(reds)>12 else "")
col=480
tops=[y for y in range(0,H) if isred(px[col,y])]
p("chrome red horiz @x480:", tops[:8], "...", tops[-8:] if len(tops)>8 else "")

# 2. title ink bbox (red) fy 50..100
xs=[];ys=[]
for y in range(50,100):
    for x in range(80,900):
        if isred(px[x,y]): xs.append(x);ys.append(y)
p("title red ink bbox:", (min(xs),min(ys),max(xs),max(ys)) if xs else None)

# 3. subtitle fy 95..130: blue/red/green bboxes
for name,fn in (("sub-blue",isblue),("sub-red",isred),("sub-green",isgreen)):
    xs=[];ys=[]
    for y in range(93,132):
        for x in range(60,900):
            if fn(px[x,y]): xs.append(x);ys.append(y)
    p(name,"bbox:", (min(xs),min(ys),max(xs),max(ys)) if xs else None)

# 4. left panel border (blue) — scan row y=300 for blue verticals x 40..300; col x=150 for blue horiz y 80..540
bs=[x for x in range(40,320) if isblue(px[x,300])]
p("leftpanel blue verticals @y300:", bs)
bs2=[y for y in range(60,540) if isblue(px[150,y])]
p("leftpanel blue horiz @x150:", bs2[:6],"...",bs2[-6:] if len(bs2)>6 else "")

# 5. input circles: pink mask col x=100 (run detection)
runs=[]
prev=False
for y in range(100,540):
    c=ispink(px[100,y])
    if c and not prev: start=y
    if not c and prev: runs.append((start,y-1))
    prev=c
p("pink runs col x=100:", runs)

# 6. neurons: red rim col x=225
runs=[];prev=False
for y in range(100,540):
    c=isred(px[225,y])
    if c and not prev: start=y
    if not c and prev: runs.append((start,y-1))
    prev=c
p("red runs col x=225 (neuron rims):", runs)

# 7. weight label colors: sample column band x 122..160 — find rows with colored ink
import collections
colr=collections.defaultdict(list)
for y in range(110,540):
    for x in range(120,165):
        c=px[x,y]; r,g,b=c
        if isblue(c) or (b>140 and r<160 and g<110 and b-r>60) : colr['blue'].append(y); break
        if isgreen(c): colr['green'].append(y); break
        if r>170 and g<120 and b>150: colr['purple'].append(y); break
        if r>170 and 90<g<190 and b<110: colr['orange'].append(y); break
def groups(ys, gap=3):
    if not ys: return []
    ys=sorted(set(ys)); gs=[[ys[0]]]
    for y in ys[1:]:
        if y-gs[-1][-1]<=gap: gs[-1].append(y)
        else: gs.append([y])
    return [(g[0],g[-1]) for g in gs]
for k in ('blue','purple','orange','green'):
    p("stack",k,"row groups:", groups(colr[k]))

# 8. y output labels + arrows: green mask x 235..300
xs=[];ys=[]
for y in range(110,540):
    for x in range(240,310):
        if isgreen(px[x,y]): xs.append(x);ys.append(y)
p("green ink (y labels/arrows) bbox:", (min(xs),min(ys),max(xs),max(ys)) if xs else None)
ggroups_y = groups(ys,4)
p("green row groups (y-band):", ggroups_y)

# 9. middle panels: blue border scan row y=200 and y=430 for x 270..560; col x=400 for y 80..540
mb=[x for x in range(260,580) if isblue(px[x,200])]
p("midpanel blue verticals @y200:", mb)
mb2=[y for y in range(80,540) if isblue(px[400,y])]
p("midpanel blue horiz @x400:", mb2)

# 10. middle panel fills (gray E8E8E8) sample
p("midpanel fill @(350,230):", px[350,230], " @(350,400):", px[350,400])
p("rightpanel fill @(700,230):", px[700,230], " @(700,430):", px[700,430])

# 11. callout1 black bbox x 360..560 fy 250..345
xs=[];ys=[]
for y in range(240,350):
    for x in range(360,560):
        if isdark(px[x,y]): xs.append(x);ys.append(y)
p("callout1 (IF No Non-linearity) bbox:", (min(xs),min(ys),max(xs),max(ys)) if xs else None)
# callout2 x 740..920
xs=[];ys=[]
for y in range(240,350):
    for x in range(740,925):
        if isdark(px[x,y]): xs.append(x);ys.append(y)
p("callout2 (IF No Bias) bbox:", (min(xs),min(ys),max(xs),max(ys)) if xs else None)

# 12. thick red arrows: center col x 400..500 fy 200..440 red mask per-column bbox
for x in range(420,500,5):
    ys2=[y for y in range(190,450) if isred(px[x,y])]
    if ys2: p("center-red col x=%d y %d..%d n=%d"%(x,min(ys2),max(ys2),len(ys2)))
# right arrow x 820..910 fy 290..400
for x in range(820,915,5):
    ys2=[y for y in range(280,410) if isred(px[x,y])]
    if ys2: p("right-red col x=%d y %d..%d n=%d"%(x,min(ys2),max(ys2),len(ys2)))

# 13. right panels blue borders: row y=200 and y=430 x 520..930; col x=700
rb=[x for x in range(520,935) if isblue(px[x,200])]
p("rightpanel blue verticals @y200:", rb)
rb3=[y for y in range(80,540) if isblue(px[700,y])]
p("rightpanel blue horiz @x700:", rb3)

# 14. bottom black bar rows
for y in (505,510,515,517,520,530,539):
    rowdark=sum(1 for x in range(0,W,10) if isdark(px[x,y]))
    p("dark frac row y=%d: %d/96"%(y,rowdark))

open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide010/measure1_output.txt","w").write("\n".join(out))
