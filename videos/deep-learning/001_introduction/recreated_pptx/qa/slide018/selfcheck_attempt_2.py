#!/usr/bin/env python3
"""Closed-loop PIL selfcheck attempt 2 (corrected regions). render vs measured original."""
from PIL import Image
im = Image.open('render_3.png').convert('RGB')
W,H = im.size; S=H/540.0; px=im.load()
fails=[]; passes=0
def check(name, cond, detail=""):
    global passes
    if cond: passes+=1
    else: fails.append(f"{name} {detail}")
def bbox(pred,x0,y0,x1,y1):
    xs=[];ys=[]
    for y in range(int(y0*S),int(y1*S)):
        for x in range(int(x0*S),int(x1*S)):
            if pred(*px[x,y]): xs.append(x);ys.append(y)
    if not xs: return None
    return (min(xs)/S,max(xs)/S,min(ys)/S,max(ys)/S)
isred = lambda r,g,b: r>150 and r-g>60 and r-b>60
isnavy = lambda r,g,b: b>85 and b-r>55 and r<110
isdark = lambda r,g,b: r<95 and g<95 and b<95

bb = bbox(isred, 150,58, 730,96)
check("title_ink", bb and abs(bb[0]-223)<7 and abs(bb[1]-654)<9 and abs(bb[2]-69)<5 and abs(bb[3]-88)<5, f"got {bb}")
bb = bbox(isred, 300,95, 700,105)
check("panel_top", bb and abs(bb[2]-99)<4 and abs(bb[3]-103)<4, f"got {bb}")
bb = bbox(isred, 300,458, 700,472)
check("panel_bottom", bb and abs(bb[2]-462)<4 and abs(bb[3]-467)<4, f"got {bb}")
bb = bbox(isred, 195,192, 715,200)
check("container_top", bb and abs(bb[0]-190)<8 and abs(bb[1]-721)<8, f"got {bb}")
bb = bbox(lambda r,g,b: abs(r-250)<8 and abs(g-254)<8 and abs(b-217)<10, 125,210, 245,262)
check("box_pre_fill", bb and abs(bb[0]-131)<5 and abs(bb[1]-235)<6, f"got {bb}")
bb = bbox(isnavy, 124,210, 136,262); check("box_pre_border_L", bb and abs(bb[0]-128)<5, f"got {bb}")
bb = bbox(isnavy, 230,210, 242,262); check("box_pre_border_R", bb and abs(bb[1]-238)<5, f"got {bb}")
bb = bbox(isdark, 140,215, 230,236); check("box_pre_text1", bb and abs(bb[2]-219)<6, f"got {bb}")
bb = bbox(isdark, 140,238, 230,258); check("box_pre_text2", bb and abs(bb[2]-240)<6, f"got {bb}")
bb = bbox(lambda r,g,b: abs(r-226)<10 and abs(g-255)<8 and abs(b-251)<8, 295,210, 410,262)
check("box_ext_fill", bb and abs(bb[0]-295)<6 and abs(bb[1]-409)<7, f"got {bb}")
bb = bbox(lambda r,g,b: r>140 and g<60 and b<60, 585,215, 725,225)
check("class_fill", bb and abs(bb[0]-589)<5 and abs(bb[1]-719)<6, f"got {bb}")
# classification white text band: rows in x600..710 with >18 white px
white_rows=[y for y in range(215,262) if sum(1 for x in range(600,710) if px[int(x*S),int(y*S)][0]>230 and px[int(x*S),int(y*S)][1]>230)>18]
check("class_text_band", white_rows and abs(min(white_rows)-228)<6 and abs(max(white_rows)-246)<7, f"got {min(white_rows) if white_rows else None}..{max(white_rows) if white_rows else None}")
bb = bbox(lambda r,g,b: abs(r-218)<10 and abs(g-191)<10 and abs(b-161)<12, 750,212, 860,262)
check("co_fill", bb and abs(bb[0]-750)<5 and abs(bb[1]-861)<6 and abs(bb[2]-211)<5 and abs(bb[3]-263)<5, f"got {bb}")
bb = bbox(isdark, 754,226, 858,250)
check("co_text_main", bb and abs(bb[0]-753)<7 and abs(bb[2]-231)<6 and abs(bb[3]-245)<6, f"got {bb}")
bb = bbox(isdark, 867,228, 886,248)
check("co_text_overflow_t", bb is not None, f"got {bb}")
bb = bbox(lambda r,g,b: r>235 and 198<g<240 and 155<b<220, 70,120, 215,205)
check("ellipse_fill", bb and abs(bb[0]-79)<6 and abs(bb[1]-207)<7 and abs(bb[2]-131)<6 and abs(bb[3]-204)<7, f"got {bb}")
bb = bbox(isdark, 85,135, 205,160); check("ellipse_text1", bb and abs(bb[2]-140)<6, f"got {bb}")
bb = bbox(isdark, 85,158, 205,185); check("ellipse_text2", bb and abs(bb[2]-160)<6, f"got {bb}")
bb = bbox(lambda r,g,b: 215<r<245 and g>240 and b>240, 335,130, 565,162)
check("chip_fill", bb and abs(bb[0]-344)<7 and abs(bb[1]-556)<8 and abs(bb[2]-134)<5 and abs(bb[3]-159)<5, f"got {bb}")
bb = bbox(isnavy, 350,133, 550,158)
check("chip_text", bb and abs(bb[0]-379)<10 and abs(bb[1]-520)<12 and abs(bb[2]-139)<6, f"got {bb}")
# arc: navy within +-8 of sample points
for xf,ya,yb,name in [(265,150,170,'arc@265'),(535,155,178,'arc@535'),(725,168,192,'arc@725')]:
    hit = any(isnavy(*px[int((xf+dx)*S),int(y*S)]) for dx in range(-8,9) for y in range(ya,yb))
    check(name, hit)
hit = any(isred(*px[int(x*S),int(220*S)]) for x in [98,100,102])
check("curve@y220", hit)
bb = bbox(isred, 130,269, 700,277)
check("deep_arrow_shaft", bb and abs(bb[2]-270)<3 and abs(bb[3]-274)<3, f"got {bb}")
bb = bbox(isred, 110,264, 135,279); check("deep_arrow_headL", bb and abs(bb[0]-115)<5, f"got {bb}")
bb = bbox(isred, 705,264, 735,279); check("deep_arrow_headR", bb and abs(bb[1]-727)<6, f"got {bb}")
bb = bbox(lambda r,g,b: abs(r-236)<10 and abs(g-251)<9 and abs(b-222)<10, 295,276, 525,305)
check("deep_label_fill", bb and abs(bb[0]-306)<7 and abs(bb[1]-515)<8 and abs(bb[2]-283)<5 and abs(bb[3]-300)<5, f"got {bb}")
bb = bbox(isdark, 320,282, 500,302)
check("deep_label_text", bb and abs(bb[0]-343)<9 and abs(bb[1]-477)<10 and abs(bb[2]-286)<5, f"got {bb}")
exp = [("c1",86,268,312,352),("c2",286,438,308,366),("c3",453,574,308,366),("c4",601,716,319,351)]
for name,x0,x1,y0,y1 in exp:
    bb = bbox(lambda r,g,b: 200<r<240 and 200<g<240 and abs(r-g)<8 and abs(r-b)<12, x0-4,y0-4,x1+4,y1+4)
    check(name+"_box", bb and abs(bb[0]-x0)<6 and abs(bb[1]-x1)<7 and abs(bb[2]-y0)<6 and abs(bb[3]-y1)<7, f"got {bb}")
red1 = bbox(isred, 90,330, 264,350); check("c1_red_line", red1 and abs(red1[2]-333)<6, f"got {red1}")
red2 = bbox(isred, 290,310, 434,330); check("c2_red_line", red2 and abs(red2[2]-314)<6, f"got {red2}")
red3 = bbox(isred, 457,310, 570,330); check("c3_red_line", red3 and abs(red3[2]-312)<6, f"got {red3}")
red4 = bbox(isred, 605,318, 712,350); check("c4_no_red", red4 is None, f"got {red4}")
bb = bbox(lambda r,g,b: r>240 and g>240 and 195<b<232, 725,288, 890,352)
check("star_fill", bb and abs(bb[0]-736)<8 and abs(bb[1]-874)<10 and abs(bb[2]-296)<7 and abs(bb[3]-343)<8, f"got {bb}")
redS = bbox(isred, 738,302, 888,340)
check("star_text_no_outline", redS and redS[0]>755 and redS[1]<888, f"got {redS}")
bb = bbox(isred, 760,302, 888,338)
check("star_text", bb and abs(bb[2]-307)<6 and abs(bb[3]-333)<6, f"got {bb}")
bb = bbox(lambda r,g,b: r>248 and g>248 and 215<b<240, 285,395, 562,442)
check("stmt_fill", bb and abs(bb[0]-283)<7 and abs(bb[1]-564)<8 and abs(bb[2]-394)<6 and abs(bb[3]-442)<6, f"got {bb}")
bb = bbox(isnavy, 275,388, 572,450)
check("stmt_border", bb and abs(bb[0]-279)<5 and abs(bb[1]-569)<6, f"got {bb}")
bb = bbox(isred, 290,395, 560,442)
check("stmt_text", bb and abs(bb[2]-400)<6 and abs(bb[3]-439)<6, f"got {bb}")
bb = bbox(isdark, 20,512, 940,540)
check("blackbar", bb and abs(bb[0]-38)<4 and abs(bb[1]-921)<5 and abs(bb[2]-518)<4, f"got {bb}")
stray=[]
for y in range(105,460):
    for x in list(range(int(66*S),int(69*S)))+list(range(int(896*S),int(899*S))):
        r,g,b = px[x,y]
        if (r>150 and r-g>60 and r-b>60): stray.append((x/S,y/S))
check("containment", len(stray)==0, f"{len(stray)} stray e.g. {stray[:5]}")
print(f"PASS {passes}  FAIL {len(fails)}")
for f in fails: print(" FAIL:", f)
