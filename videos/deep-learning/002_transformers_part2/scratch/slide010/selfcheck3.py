#!/usr/bin/env python3
# selfcheck3.py — final numeric pass on render_3.png + delimiter geometry + q subs
from PIL import Image
REN = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide010/render_3.png"
ORIG = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_010.jpg"
r = Image.open(REN).convert("RGB"); o = Image.open(ORIG).convert("RGB")
rp, op = r.load(), o.load()
RW, RH = r.size; S = RW / 960.0
out=[]
def p(*a): s=" ".join(str(x) for x in a); out.append(s); print(s)
def isred(c):   r_,g,b=c; return r_>140 and g<100 and b<100
def isblue(c):  r_,g,b=c; return b>140 and b-r_>50 and g<150
def isdark(c):  r_,g,b=c; return r_<75 and g<75 and b<75
def bbox(px_, sx0,sy0,sx1,sy1, fn):
    xs=[];ys=[]
    for y in range(max(0,int(sy0*S)), min(RH,int(sy1*S))):
        for x in range(max(0,int(sx0*S)), min(RW,int(sx1*S))):
            if fn(px_[x,y]): xs.append(x);ys.append(y)
    return (min(xs),min(ys),max(xs),max(ys)) if xs else None
def f2r(fx0,fx1,fy0,fy1):
    return ((fx0-17.628)/0.961232*S, (fx1-17.628)/0.961232*S, fy0/0.955556*S, fy1/0.955556*S)
fails=0
def cmp(name, got, exp_fx, tol=6):
    ex0,ex1,ey0,ey1 = f2r(*exp_fx)
    if got is None: p("FAIL",name,"no ink"); return 1
    dx = max(abs(got[0]-ex0), abs(got[2]-ex1)); dy = max(abs(got[1]-ey0), abs(got[3]-ey1))
    ok = "OK " if (dx<=tol and dy<=tol) else "FAIL"
    p(ok, name, "got", got, "exp_r", tuple(round(v) for v in (ex0,ey0,ex1,ey1)), "d", (round(dx,1),round(dy,1)))
    return 0 if ok=="OK " else 1

fails += cmp("braceL1", bbox(rp, 522,108,552,300, isblue), (522,546,106,289))
fails += cmp("braceR1", bbox(rp, 828,105,852,300, isblue), (820,837,106,289))
fails += cmp("braceL2", bbox(rp, 522,332,552,515, isblue), (522,546,320,503))
fails += cmp("braceR2", bbox(rp, 828,330,852,515, isblue), (820,837,320,503))
fails += cmp("callout2", bbox(rp, 770,285,920,335, isdark), (792,881,293,314))
gBL = bbox(rp, 290,170,302,240, isred); p("bracketL1 ink:", gBL, "exp_r", tuple(round(v) for v in f2r(294,300,178,222)))
gBR = bbox(rp, 438,170,450,240, isred); p("bracketR1 ink:", gBR, "exp_r", tuple(round(v) for v in f2r(441,445,178,222)))
# delimiter geometry: brackets must cover enclosed y-boxes (fy 190..210) AND stadium-ish
if gBL and gBR:
    top=min(gBL[1],gBR[1]); bot=max(gBL[3],gBR[3])
    box_top, box_bot = 190/0.955556*S, 211/0.955556*S
    p("DELIM bracket coverage: ink %.1f..%.1f vs boxes %.1f..%.1f -> %s"%(top/S*0.955556*0,0,0,0,"x")) if False else None
    ok = top <= box_top+2 and bot >= box_bot-2
    p("DELIM brackets cover y-boxes:", "OK" if ok else "FAIL", "(ink_r %d..%d boxes_r %.0f..%.0f)"%(top,bot,box_top,box_bot))
    fails += 0 if ok else 1
# parens coverage: bias boxes fy 128..262 vs parens ink
gP = bbox(rp, 856,110,916,310, isred)
p("bias parens+rims ink:", gP, "exp_r", tuple(round(v) for v in f2r(849,893,117,291)))
# q subscripts: zone between W(506..525) and (Query)(532..590): fx 525..533, fy 88..101
def inkq(c):
    r_,g,b=c
    return (r_>140 and g<110 and b<110) or (b>150 and b-r_>60)
gq1 = bbox(rp, 524,84,534,104, inkq)
p("subtitle W_q subscript ink:", gq1)
gq2 = bbox(rp, 687,84,700,104, inkq)
p("green-note W_q subscript ink:", gq2)
# callout1 text bands (lineSpacing check)
def iswhite(c): r_,g,b=c; return r_>200 and g>200 and b>200
rows=[y for y in range(int(590),int(690)) if sum(1 for x in range(int(880),int(1060)) if iswhite(rp[x,y]))>4]
bands=[]; 
if rows:
    st=rows[0]; prev=rows[0]
    for y in rows[1:]:
        if y-prev>3: bands.append((st,prev)); st=y
        prev=y
    bands.append((st,prev))
p("callout1 white text bands (render):", bands, "pitch:", bands[1][0]-bands[0][0] if len(bands)>1 else None, "(want ~27=13pt)")
# outputs spot: y1 green + halftone presence
def isgreen(c): r_,g,b=c; return g>110 and g-r_>40 and g-b>40
fails += cmp("y1.green", bbox(rp, 240,148,290,182, isgreen), (250,272,154,172))
p("TOTAL FAILS:", fails)
open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide010/selfcheck_attempt_3_output.txt","w").write("\n".join(out))
