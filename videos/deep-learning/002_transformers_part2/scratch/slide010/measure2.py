#!/usr/bin/env python3
# measure2.py — slide_010.jpg targeted sweeps + crops
from PIL import Image
im = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_010.jpg").convert("RGB")
W,H = im.size; px = im.load()
out=[]
def p(*a): s=" ".join(str(x) for x in a); out.append(s); print(s)

def isred(c):   r,g,b=c; return r>140 and g<100 and b<100
def isblueish(c): r,g,b=c; return b>120 and b-r>40 and g<140
def isdark(c):  r,g,b=c; return r<75 and g<75 and b<75

def runs_col(x, fn, y0, y1, minlen=1):
    rs=[];prev=False
    for y in range(y0,y1):
        c=fn(px[x,y])
        if c and not prev: st=y
        if not c and prev and y-st>=minlen: rs.append((st,y-1))
        prev=c
    if prev and y1-st>=minlen: rs.append((st,y1-1))
    return rs
def runs_row(y, fn, x0, x1, minlen=1):
    rs=[];prev=False
    for x in range(x0,x1):
        c=fn(px[x,y])
        if c and not prev: st=x
        if not c and prev and x-st>=minlen: rs.append((st,x-1))
        prev=c
    if prev and x1-st>=minlen: rs.append((st,x1-1))
    return rs

# chrome verify
p("chrome col x=58 red runs:", runs_col(58, isred, 0, 540, 2))
p("chrome row y=79 red runs:", runs_row(79, isred, 30, 940, 2))
p("chrome row y=300 red x<70:", runs_row(300, isred, 0, 75, 1), " x>890:", runs_row(300, isred, 890, 960, 1))
p("chrome col x=480 red runs y<70:", runs_col(480, isred, 0, 75, 1), "y>440:", runs_col(480, isred, 440, 540, 1))

# title rows profile (red count per row)
for y in range(45, 95, 2):
    n=sum(1 for x in range(100,900) if isred(px[x,y]))
    if n: p("title redcount y=%d: %d"%(y,n))

# subtitle: per-row ink counts (blue/red/green)
def cnt(y,x0,x1,fn): return sum(1 for x in range(x0,x1) if fn(px[x,y]))
def isblue(c): r,g,b=c; return b>150 and b-r>60 and g<120
def isgreen(c): r,g,b=c; return g>110 and g-r>40 and g-b>30
for y in range(90, 132, 2):
    p("sub y=%d blue=%d red=%d green=%d"%(y,cnt(y,60,900,isblue),cnt(y,60,900,isred),cnt(y,60,900,isgreen)))

# left panel border: row y=300 near x 270..290; col x=90 y 95..540
p("leftpanel row300 x260..295 raw:", [(x,px[x,300]) for x in range(268,292,2)])
p("leftpanel col90 blueish runs:", runs_col(90, isblueish, 90, 540, 1))
p("leftpanel row300 blueish x40..300:", runs_row(300, isblueish, 40, 300, 1))

# input circle 1: sample around (89,164)
p("input1 px(89,164):", px[89,164], "px(95,158):", px[95,158], "px(83,170):", px[83,170])
p("col x=89 pinkish runs y100..540:", runs_col(89, lambda c: c[0]>210 and c[2]>200 and c[1]<200, 100, 540, 3))

# neuron rims: row y=168 reddish x 195..260; col x=225 reddish y 100..540
p("neuron row168 reddish runs:", runs_row(168, lambda c: c[0]>120 and c[0]-c[1]>40 and c[0]-c[2]>30, 195, 265, 1))
p("neuron col225 reddish runs y100..540:", runs_col(225, lambda c: c[0]>120 and c[0]-c[1]>40 and c[0]-c[2]>30, 100, 540, 1))

# below neuron1: dark/gray ink (b_i? halftone?) sample bbox
xs=[];ys=[]
for y in range(192,240):
    for x in range(200,260):
        c=px[x,y]
        if isdark(c) or (abs(c[0]-c[1])<12 and abs(c[1]-c[2])<12 and c[0]<190): xs.append(x);ys.append(y)
p("below-neuron1 gray/dark bbox:", (min(xs),min(ys),max(xs),max(ys)) if xs else None)

# y1 label crop check: green ink bbox around (245..300, 145..190)
def isgreen2(c): r,g,b=c; return g>100 and g-r>25 and g-b>25
xs=[];ys=[]
for y in range(140,195):
    for x in range(238,305):
        if isgreen2(px[x,y]): xs.append(x);ys.append(y)
p("y1 green ink bbox:", (min(xs),min(ys),max(xs),max(ys)) if xs else None)

# mid panels: border blue — row y=115 (above Y^T) x 270..560; col x=310 y 90..540
p("midpanel row115 blueish runs x270..560:", runs_row(115, isblueish, 270, 560, 1))
p("midpanel col310 blueish runs y90..540:", runs_col(310, isblueish, 90, 540, 1))
p("midpanel fill sample (320,120):", px[320,120], "(320,470):", px[320,470])
# midpanel contents: Y^T red bbox x 300..420 y 150..190
xs=[];ys=[]
for y in range(145,195):
    for x in range(300,430):
        if isred(px[x,y]): xs.append(x);ys.append(y)
p("Yt1 red bbox:", (min(xs),min(ys),max(xs),max(ys)) if xs else None)
xs=[];ys=[]
for y in range(355,405):
    for x in range(300,430):
        if isred(px[x,y]): xs.append(x);ys.append(y)
p("Yt2 red bbox:", (min(xs),min(ys),max(xs),max(ys)) if xs else None)
# y-box row mid1: yellowish boxes + red bracket ink x 285..460 y 180..225
def isyellow(c): r,g,b=c; return r>210 and g>200 and b<200
xs=[];ys=[]
for y in range(178,228):
    for x in range(285,465):
        if isyellow(px[x,y]): xs.append(x);ys.append(y)
p("yboxrow1 yellow bbox:", (min(xs),min(ys),max(xs),max(ys)) if xs else None)
p("yboxrow1 row200 yellow runs:", runs_row(200, isyellow, 285, 465, 2))
xs=[];ys=[]
for y in range(388,438):
    for x in range(285,465):
        if isyellow(px[x,y]): xs.append(x);ys.append(y)
p("yboxrow2 yellow bbox:", (min(xs),min(ys),max(xs),max(ys)) if xs else None)
p("yboxrow2 row410 yellow runs:", runs_row(410, isyellow, 285, 465, 2))
# pink outline around y-box group: pinkish runs row 205 x 280..470
p("yboxrow1 row205 pinkish runs:", runs_row(205, lambda c: c[0]>215 and c[2]>190 and c[1]<200, 275, 475, 1))
# = Sigmoid / = Linear blue bboxes
xs=[];ys=[]
for y in range(185,225):
    for x in range(430,530):
        if isblue(px[x,y]): xs.append(x);ys.append(y)
p("sigmoid blue bbox:", (min(xs),min(ys),max(xs),max(ys)) if xs else None)
xs=[];ys=[]
for y in range(395,435):
    for x in range(430,530):
        if isblue(px[x,y]): xs.append(x);ys.append(y)
p("linear blue bbox:", (min(xs),min(ys),max(xs),max(ys)) if xs else None)

# callouts: large dark fill — rows where dark run > 40
for name,(x0,x1,y0,y1) in (("callout1",(370,530,255,350)),("callout2",(790,930,255,350))):
    rows=[]
    for y in range(y0,y1):
        rs=runs_row(y, isdark, x0, x1, 30)
        if rs: rows.append((y,rs))
    if rows:
        ys=[r[0] for r in rows]
        xr=[x for r in rows for run in r[1] for x in run]
        p(name,"dark-fill rows y %d..%d, x %d..%d"%(min(ys),max(ys),min(xr),max(xr)))

# center red arrow bbox
xs=[];ys=[]
for y in range(195,440):
    for x in range(440,510):
        if isred(px[x,y]): xs.append(x);ys.append(y)
p("center arrow red bbox:", (min(xs),min(ys),max(xs),max(ys)) if xs else None)
p("center arrow row300 red runs:", runs_row(300, isred, 440, 510, 1))
p("center arrow row250 red runs:", runs_row(250, isred, 440, 510, 1))
p("center arrow row420 red runs:", runs_row(420, isred, 440, 510, 1))
# right red arrow
xs=[];ys=[]
for y in range(290,400):
    for x in range(840,910):
        if isred(px[x,y]): xs.append(x);ys.append(y)
p("right arrow red bbox:", (min(xs),min(ys),max(xs),max(ys)) if xs else None)
p("right arrow row330 red runs:", runs_row(330, isred, 840, 910, 1))

# right panels: borders — row y=115 x 510..935; col x=670 y 90..540; col x=310 equivalent for right
p("rightpanel row115 blueish runs x505..940:", runs_row(115, isblueish, 505, 940, 1))
p("rightpanel col670 blueish runs y90..540:", runs_col(670, isblueish, 90, 540, 1))
p("rightpanel fill (560,110):", px[560,110], "(560,470):", px[560,470], "(650,290):", px[650,290])

# right panel 1 contents: X pill pinkish bbox x 520..680 y 95..145
xs=[];ys=[]
for y in range(90,150):
    for x in range(515,690):
        c=px[x,y]
        if c[0]>215 and c[2]>190 and c[1]<205: xs.append(x);ys.append(y)
p("Xpill1 pink bbox:", (min(xs),min(ys),max(xs),max(ys)) if xs else None)
# circles red rims row y=120 x 520..680
p("Xpill1 row120 reddish runs:", runs_row(120, lambda c: c[0]>150 and c[0]-c[1]>50 and c[0]-c[2]>40, 520, 690, 1))
# big X below: red bbox x 560..640 y 140..180
xs=[];ys=[]
for y in range(140,185):
    for x in range(555,650):
        if isred(px[x,y]): xs.append(x);ys.append(y)
p("bigX1 red bbox:", (min(xs),min(ys),max(xs),max(ys)) if xs else None)
# matrix1: green container bbox + yellow cells
def ismint(c): r,g,b=c; return g>230 and r<235 and b>200 and g-r>15
xs=[];ys=[]
for y in range(90,300):
    for x in range(650,840):
        if ismint(px[x,y]): xs.append(x);ys.append(y)
p("matrix1 mint bbox:", (min(xs),min(ys),max(xs),max(ys)) if xs else None)
xs=[];ys=[]
for y in range(90,300):
    for x in range(650,840):
        if isyellow(px[x,y]): xs.append(x);ys.append(y)
p("matrix1 yellow bbox:", (min(xs),min(ys),max(xs),max(ys)) if xs else None)
p("matrix1 row145 yellow runs:", runs_row(145, isyellow, 650, 840, 3))
p("matrix1 col700 yellow runs:", runs_col(700, isyellow, 90, 300, 3))
# brace1: blue x 815..850 y 100..300
xs=[];ys=[]
for y in range(95,305):
    for x in range(810,855):
        if isblue(px[x,y]): xs.append(x);ys.append(y)
p("brace1 blue bbox:", (min(xs),min(ys),max(xs),max(ys)) if xs else None)
# plus1: red x 845..870 y 180..215
xs=[];ys=[]
for y in range(175,220):
    for x in range(838,875):
        if isred(px[x,y]): xs.append(x);ys.append(y)
p("plus1 red bbox:", (min(xs),min(ys),max(xs),max(ys)) if xs else None)
# bias1: red parens + yellow boxes x 850..935 y 100..300
xs=[];ys=[]
for y in range(95,305):
    for x in range(848,940):
        if isyellow(px[x,y]): xs.append(x);ys.append(y)
p("bias1 yellow bbox:", (min(xs),min(ys),max(xs),max(ys)) if xs else None)
p("bias1 row145 yellow runs:", runs_row(145, isyellow, 848, 940, 2))
p("bias1 col880 yellow runs y95..305:", runs_col(880, isyellow, 95, 305, 2))
xs=[];ys=[]
for y in range(95,305):
    for x in range(848,940):
        if isred(px[x,y]): xs.append(x);ys.append(y)
p("bias1 red(parens/rims) bbox:", (min(xs),min(ys),max(xs),max(ys)) if xs else None)

# ---- crops for visual inspection ----
crops = {
  "c_neuron1":   (195, 100, 300, 245),
  "c_mid1":      (280, 90, 560, 350),
  "c_right1":    (505, 90, 940, 305),
  "c_title_sub": (60, 40, 940, 135),
  "c_callouts":  (360, 240, 940, 360),
  "c_right2":    (505, 300, 940, 520),
}
for name,(x0,y0,x1,y1) in crops.items():
    im.crop((x0,y0,x1,y1)).resize(((x1-x0)*2,(y1-y0)*2), Image.LANCZOS).save(f"/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide010/{name}.png")
p("crops saved")
open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide010/measure2_output.txt","w").write("\n".join(out))
