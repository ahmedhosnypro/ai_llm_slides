#!/usr/bin/env python3
# selfcheck2.py — fixed-scale closed-loop checks + bracket/arrow ink measurement
from PIL import Image
REN = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide010/render_2.png"
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
def f2r(fx0,fx1,fy0,fy1):  # frame px -> render px box
    return ((fx0-17.628)/0.961232*S, (fx1-17.628)/0.961232*S, fy0/0.955556*S, fy1/0.955556*S)
def cmp(name, got, exp_fx, tol=6):
    ex0,ex1,ey0,ey1 = f2r(*exp_fx)
    if got is None: p("FAIL",name,"no ink"); return 1
    dx = max(abs(got[0]-ex0), abs(got[2]-ex1)); dy = max(abs(got[1]-ey0), abs(got[3]-ey1))
    ok = "OK " if (dx<=tol and dy<=tol) else "FAIL"
    p(ok, name, "got", got, "exp_r", tuple(round(v) for v in (ex0,ey0,ex1,ey1)), "d", (round(dx,1),round(dy,1)))
    return 0 if ok=="OK " else 1

fails=0
fails += cmp("title", bbox(rp, 100,50,860,72, isred), (190,766,53,66))
fails += cmp("mid1.topborder", bbox(rp, 455,100,500,108, isblue), (455,500,97,100))
fails += cmp("matrix1.container", bbox(rp, 640,110,880,300, lambda c: c[1]>215 and c[1]-c[0]>12 and c[2]>200), (669,820,120,280))
fails += cmp("pill1.stadium", bbox(rp, 500,95,700,155, lambda c: c[0]>225 and c[2]>200 and c[0]-c[1]>25), (524,664,104,142))
fails += cmp("braceR1", bbox(rp, 828,105,852,295, isblue), (820,837,106,289))
fails += cmp("braceL1", bbox(rp, 505,105,549,295, isblue), (520,545,106,289))
fails += cmp("callout1", bbox(rp, 400,275,560,335, isdark), (416,522,281,318))
fails += cmp("callout2", bbox(rp, 770,285,920,322, isdark), (792,881,293,314))
fails += cmp("matrix2.row1cells", bbox(rp, 680,335,860,395, lambda c: c[0]>225 and c[1]>210 and c[2]<205), (681,811,348,375))
fails += cmp("bias1.boxes", bbox(rp, 850,115,930,275, lambda c: c[0]>225 and c[1]>210 and c[2]<205), (856,886,128,262))

p("--- bracket ink (mid1) ---")
# bracket L column band fx 292..302, R fx 438..448; frame exp fy 184..226
gL = bbox(rp, 292,180,302,245, isred)
p("bracketL1 ink:", gL, "exp_r", tuple(round(v) for v in f2r(294,300,184,226)))
gR = bbox(rp, 436,180,448,245, isred)
p("bracketR1 ink:", gR, "exp_r", tuple(round(v) for v in f2r(441,445,184,226)))
p("--- X-pill bracket ink ---")
gxL = bbox(rp, 540,100,556,155, isred)
p("xpill.bracketL ink:", gxL, "exp_r", tuple(round(v) for v in f2r(544,550,108,138)))
p("--- center arrow ink extent ---")
gA = bbox(rp, 470,200,482,460, isred)
p("centerArrow ink:", gA, "exp_r", tuple(round(v) for v in f2r(472,477,210,415)))
p("--- right arrow ink extent ---")
gAr = bbox(rp, 878,270,895,360, isred)
p("rightArrow ink:", gAr, "exp_r", tuple(round(v) for v in f2r(866,871,267,342)))
p("--- subtitle q-subscript zones (ink present?) ---")
def inkany(c): r_,g,b=c; return (r_<160 and g_<160 and b_<190) or (r_>140 and g<100 and b<100) or (b>140 and b-r_>50)
gq1 = bbox(rp, 524,80,534,105, inkany)
p("W_q sub zone ink (fx 526..532, fy 88..100):", gq1)
gq2 = bbox(rp, 688,80,700,105, inkany)
p("green-note q zone ink (fx 692..697):", gq2)
p("--- render title left edge check (red ink min x, slide px) ---")
gt = bbox(rp, 60,40,880,80, isred)
if gt: p("title ink render bbox:", gt, "-> slide x", round(gt[0]/S,1), "..", round(gt[2]/S,1))
p("TOTAL FAILS:", fails)
open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide010/selfcheck2_output.txt","w").write("\n".join(out))
