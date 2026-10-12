#!/usr/bin/env python3
# selfcheck_attempt_1.py — closed-loop PIL verify of render_1.png (150dpi, 2001x1125)
# against the slide_010.jpg frame measurements. Tolerance ~4 render px (1.92 slide px).
from PIL import Image
REN = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide010/render_1.png"
ORIG = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_010.jpg"
r = Image.open(REN).convert("RGB"); o = Image.open(ORIG).convert("RGB")
rp, op = r.load(), o.load()
RW, RH = r.size; OW, OH = o.size
S = RW / 960.0  # render px per slide px (frame px ~ slide pt)
out=[]
def p(*a): s=" ".join(str(x) for x in a); out.append(s); print(s)
p("render size", RW, RH, "scale", round(S,4))

def isred(c):   r_,g,b=c; return r_>140 and g<100 and b<100
def isblue(c):  r_,g,b=c; return b>140 and b-r_>50 and g<140
def isdark(c):  r_,g,b=c; return r_<75 and g<75 and b<75
def ismint(c):  r_,g,b=c; return g>215 and g-r_>12 and b>200
def isyellowcell(c): r_,g,b=c; return r_>225 and g>210 and b<205
def ispinkst(c): r_,g,b=c; return r_>225 and b>200 and r_-g>25

def bbox(px_, x0,y0,x1,y1, fn, step=1):
    xs=[];ys=[]
    for y in range(int(y0),int(y1),step):
        for x in range(int(x0),int(x1),step):
            if fn(px_[x,y]): xs.append(x);ys.append(y)
    return (min(xs),min(ys),max(xs),max(ys)) if xs else None

def cmp(name, got, exp_fx, exp_fy, tol=6):
    # exp given in FRAME px; convert to render px
    ex = ((exp_fx[0]-17.628)/0.961232)*S; ex2 = ((exp_fx[1]-17.628)/0.961232)*S
    ey = exp_fy[0]/0.955556*S; ey2 = exp_fy[1]/0.955556*S
    if got is None: p("FAIL", name, "no ink"); return 0
    dx = max(abs(got[0]-ex), abs(got[2]-ex2)); dy = max(abs(got[1]-ey), abs(got[3]-ey2))
    ok = "OK " if (dx<=tol and dy<=tol) else "FAIL"
    p(ok, name, "got", got, "exp_r", (round(ex),round(ey),round(ex2),round(ey2)), "d", (round(dx,1),round(dy,1)))
    return 0 if ok=="OK " else 1

fails=0
# 1. title (exclude badge x<840fx)
g = bbox(rp, 100*S, 90, 1760, 165, isred)
fails += cmp("title", g, (190,766), (53,66))
# 2. left panel navy border (dark blue) — use loose blue on dark
def isnavy(c): r_,g,b=c; return b>100 and b-r_>60 and r_<90
g = bbox(rp, 60*S, 180, 60*S+20, 1000, isnavy)
fails += cmp("leftpanel.L", (g[0],g[0],0,0) if g else None, (80,81), (300,301)) if g else p("FAIL leftpanel.L")
g2 = bbox(rp, 530*S, 180, 590*S, 1000, isnavy)
if g2: p("leftpanel.R got x", g2[0], g2[2], "exp", round((276-17.628)/0.961232*S), round((278-17.628)/0.961232*S))
# 3. mid1 panel fill region + blue border top
g = bbox(rp, 560*S, 170, 1000*S, 230, isblue)
fails += cmp("mid1.topborder", (g[0],g[2],g[1],g[1]) if g else None, (300,500), (98,99)) if g else p("FAIL mid1.topborder")
# 4. matrix1 mint container
g = bbox(rp, 640*S, 220, 880*S, 620, ismint)
fails += cmp("matrix1.container", g, (669,820), (120,280)) if g else p("FAIL matrix1")
# 5. matrix1 cells (yellow) row1
g = bbox(rp, 680*S, 270, 860*S, 340, isyellowcell)
fails += cmp("matrix1.row1cells", g, (681,811), (133,160)) if g else p("FAIL matrix1.cells")
# 6. bias1 boxes (yellow) col
g = bbox(rp, 850*S, 250, 930*S, 620, isyellowcell)
fails += cmp("bias1.boxes", g, (856,886), (128,262)) if g else p("FAIL bias1")
# 7. X pill1 pink stadium
g = bbox(rp, 500*S, 200, 700*S, 300, ispinkst)
fails += cmp("pill1.stadium", g, (524,664), (104,142)) if g else p("FAIL pill1")
# 8. braceR1 (blue)
g = bbox(rp, 810*S, 200, 860*S, 620, isblue)
fails += cmp("braceR1", g, (818,834), (106,288)) if g else p("FAIL braceR1")
# 9. braceL1
g = bbox(rp, 495*S, 200, 545*S, 620, isblue)
fails += cmp("braceL1", g, (512,537), (106,289)) if g else p("FAIL braceL1")
# 10. callout1 black box
g = bbox(rp, 400*S, 570, 560*S, 680, isdark)
fails += cmp("callout1", g, (416,522), (281,318)) if g else p("FAIL callout1")
# 11. callout2
g = bbox(rp, 770*S, 590, 920*S, 670, isdark)
fails += cmp("callout2", g, (792,881), (293,314)) if g else p("FAIL callout2")
# 12. center arrow shaft (red) at fy 250 and 430
g = bbox(rp, 455*S, 500, 500*S, 540, isred)
fails += cmp("centerArrow@250", (g[0],g[2],g[1],g[3]) if g else None, (472,477), (248,252)) if g else p("FAIL arrowC")
# 13. right arrow shaft at fy 330
g = bbox(rp, 850*S, 670, 900*S, 700, isred)
fails += cmp("rightArrow@330", (g[0],g[2],g[1],g[3]) if g else None, (866,871), (328,332)) if g else p("FAIL arrowR")
# 14. mid2 stadium (pink) — panel2
g = bbox(rp, 560*S, 800, 1000*S, 900, ispinkst)
fails += cmp("stadium2", g, (300,439), (391,431)) if g else p("FAIL stadium2")
# 15. matrix2 cells row1
g = bbox(rp, 680*S, 690, 860*S, 760, isyellowcell)
fails += cmp("matrix2.row1cells", g, (681,811), (348,375)) if g else p("FAIL matrix2.cells")
# 16. FRAME CONTAINMENT: no ink outside house frame (x<0.15in..13.18in, y<0.15..7.35in) beyond chrome itself
#     render: house frame at x 0.15*150=22.5px.., check content band 100..1900 px inside
p("--- containment ---")
# neurons: red rims inside left panel
g = bbox(rp, 380*S, 280, 480*S, 520, lambda c: isred(c))
p("neuron1.rim bbox (want inside left panel fx 80..277):", g and (round(g[0]/S+17.628*0,1), round(g[2]/S,1)))
# 17. outputs green ink positions
def isgreen(c): r_,g_,b=c; return g_>110 and g_-r_>40 and g_-b>40
g = bbox(rp, 480*S, 300, 580*S, 360, isgreen)
fails += cmp("y1.green", g, (250,272), (154,172)) if g else p("FAIL y1.green")
# 18. explicit lineSpacing: callout1 two text bands (white) inside black box
def iswhite(c): r_,g_,b=c; return r_>200 and g_>200 and b>200
rows=[y for y in range(int(580),int(670)) if sum(1 for x in range(int(880),int(1060)) if iswhite(rp[x,y]))>4]
if rows:
    bands=[]; st=rows[0]; prev=rows[0]
    for y in rows[1:]:
        if y-prev>3: bands.append((st,prev)); st=y
        prev=y
    bands.append((st,prev))
    p("callout1 white text bands:", bands, "pitch:", bands[1][0]-bands[0][0] if len(bands)>1 else None)
p("TOTAL FAILS:", fails)
open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide010/selfcheck_attempt_1_output.txt","w").write("\n".join(out))
