#!/usr/bin/env python3
"""Darkest-pixel color per zone + V/K panel structure + callouts/boxes."""
from PIL import Image

im = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_031.jpg").convert("RGB")
W, H = im.size
px = im.load()

def darkest(x0, y0, x1, y1):
    best = None; bl = 10**9
    for y in range(y0, y1):
        for x in range(x0, x1):
            c = px[x, y]; l = c[0]+c[1]+c[2]
            if l < bl: bl = l; best = (c, x, y)
    return best

def bbox(p, x0, y0, x1, y1):
    mnx=mny=10**9; mxx=mxy=-1; n=0
    for y in range(y0,y1):
        for x in range(x0,x1):
            if p(px[x,y]):
                n+=1
                mnx=min(mnx,x); mxx=max(mxx,x); mny=min(mny,y); mxy=max(mxy,y)
    return (mnx,mny,mxx,mxy,n) if n else None

# Q matrix cells: cols [221..257],[260..295],[298..334],[336..371]; rows [115..156],[159..197],[200..239],[242..289]
qcols = [(222,257),(260,295),(298,334),(336,371)]
qrows = [(116,156),(159,197),(200,239),(242,289)]
print("== Q matrix darkest px per cell (text core) ==")
for ri,(ry0,ry1) in enumerate(qrows):
    for ci,(cx0,cx1) in enumerate(qcols):
        c,x,y = darkest(cx0+2, ry0+8, cx1-2, ry1-6)
        print(f"  W row{ri+1} col{ci+1}: core{c} at ({x},{y})")

print("\n== V matrix (offset: cols from x620..829 block) ==")
# find V grid gaps: scan row y=200 for white-ish gaps
def vscan(x0,x1,y):
    gaps=[]
    inrun=False; s=0
    for x in range(x0,x1):
        c=px[x,y]
        w = c[0]>235 and c[1]>235 and c[2]>235
        if w and not inrun: inrun=True; s=x
        elif not w and inrun:
            inrun=False
            if x-s>=2: gaps.append((s,x-1))
    if inrun: gaps.append((s,x1-1))
    return gaps
print("  V row200 white gaps:", vscan(620,830,200))
def hscan(y0,y1,x):
    gaps=[]; inrun=False; s=0
    for y in range(y0,y1):
        c=px[x,y]
        w = c[0]>235 and c[1]>235 and c[2]>235
        if w and not inrun: inrun=True; s=y
        elif not w and inrun:
            inrun=False
            if y-s>=2: gaps.append((s,y-1))
    if inrun: gaps.append((s,y1-1))
    return gaps
print("  V col700 white gaps:", hscan(114,295,700))
print("  K col700 white gaps:", hscan(310,510,700) if False else "")
print("  K row420 white gaps:", vscan(200,410,420))
print("  K col250 white gaps:", hscan(310,510,250))

vcols = [(622,657),(660,695),(698,733),(736,771)]
vrows = [(116,156),(159,197),(200,239),(242,289)]
print("\n== V matrix darkest px per cell ==")
for ri,(ry0,ry1) in enumerate(vrows):
    for ci,(cx0,cx1) in enumerate(vcols):
        c,x,y = darkest(cx0+2, ry0+8, cx1-2, ry1-6)
        print(f"  W row{ri+1} col{ci+1}: core{c} at ({x},{y})")

kcols = [(222,257),(260,295),(298,334),(336,371)]
krows = [(313,353),(356,394),(397,436),(439,486)]
print("\n== K matrix darkest px per cell ==")
for ri,(ry0,ry1) in enumerate(krows):
    for ci,(cx0,cx1) in enumerate(kcols):
        c,x,y = darkest(cx0+2, ry0+8, cx1-2, ry1-6)
        print(f"  W row{ri+1} col{ci+1}: core{c} at ({x},{y})")

print("\n== LABEL COLORS (darkest in zone) ==")
zones = [
 ("Q '1xd'", 183, 170, 210, 187),
 ("Q 'X2'", 110, 184, 140, 213),
 ("Q 'W_Q'", 172, 234, 210, 258),
 ("Q 'dxd'", 336, 250, 372, 275),
 ("Q '='", 385, 195, 405, 212),
 ("Q role 'Q'", 415, 96, 445, 115),
 ("V 'X2'", 512, 184, 545, 213),
 ("V 'W_V'", 470, 234, 512, 258),
 ("V '='", 605, 195, 625, 212),
 ("V role 'V'", 815, 96, 845, 115),
 ("K '1xd'", 183, 367, 210, 384),
 ("K 'X2'", 110, 381, 140, 410),
 ("K 'W_K'", 172, 431, 210, 455),
 ("K 'dxd'", 336, 447, 372, 472),
 ("K '='", 385, 392, 405, 409),
 ("K role 'K'", 415, 308, 445, 330),
 ("title left part", 175, 48, 430, 68),
 ("title highlight zone", 436, 48, 770, 68),
 ("subtitle 'Query'", 120, 72, 180, 92),
 ("subtitle 'X2' blue", 230, 72, 280, 92),
 ("callout1 text", 455, 278, 675, 310),
 ("callout2 text", 705, 310, 890, 340),
 ("callout3 text", 455, 338, 675, 370),
 ("emphasis text", 650, 388, 880, 432),
 ("notebox text", 495, 452, 890, 515),
]
for lbl, x0, y0, x1, y1 in zones:
    c, x, y = darkest(x0, y0, x1, y1)
    print(f"  {lbl}: core{c} at ({x},{y})")

print("\n== V/K PANEL BORDERS + caps (geometric scans) ==")
def border_cols(p, x0, x1, y0, y1, minn):
    out=[]
    for x in range(x0,x1):
        n=sum(1 for y in range(y0,y1) if p(px[x,y]))
        if n>=minn: out.append((x,n))
    return out
def border_rows(p, x0, x1, y0, y1, minn):
    out=[]
    for y in range(y0,y1):
        n=sum(1 for x in range(x0,x1) if p(px[x,y]))
        if n>=minn: out.append((y,n))
    return out
def pred_red(c):   r,g,b=c; return r>140 and r-g>60 and r-b>60
def pred_blue(c):  r,g,b=c; return b>140 and b-r>60 and b-g>40
def pred_green(c): r,g,b=c; return g>110 and g-r>35 and g-b>35
print("  V blue rows y95..305 (x470..900, n>=100):", border_rows(pred_blue, 470,900,95,305,100))
print("  V blue cols x470..940 (y105..295, n>=100):", border_cols(pred_blue, 470,940,105,295,100))
print("  K green rows y300..540 (x60..460, n>=100):", border_rows(pred_green, 60,460,300,540,100))
print("  K green cols x40..480 (y315..520, n>=100):", border_cols(pred_green, 40,480,315,520,100))
print("  V outcap blue cols x820..895 (y120..280, n>=60):", border_cols(pred_blue, 820,895,120,280,60))
print("  K outcap green cols x400..470 (y330..500, n>=60):", border_cols(pred_green, 400,470,330,500,60))

print("\n== CALLOUT GEOMETRY ==")
def pred_pinkf(c): r,g,b=c; return r>235 and 165<g<215 and 175<b<230 and r-g>30
def pred_ltgreen(c): r,g,b=c; return g>225 and r<245 and b<245 and g-r>8 and g-b>8
print("  callout1 pink fill bbox:", bbox(pred_pinkf, 440,270,690,320))
print("  callout2 fill sample:", [px[x,y] for x,y in [(715,315),(715,338),(885,312),(885,338),(800,310),(800,340)]])
print("  callout3 ltgreen fill bbox:", bbox(pred_ltgreen, 440,330,690,380))
print("  callout3 fill sample:", [px[x,y] for x,y in [(460,345),(460,368),(630,345),(630,368),(545,342),(545,368)]])
print("  callout1 fill sample:", [px[x,y] for x,y in [(455,290),(455,306),(630,283),(670,300),(470,282)]])
# dashed border extents
def pred_green(c): r,g,b=c; return g>110 and g-r>35 and g-b>35
def pred_blue(c):  r,g,b=c; return b>140 and b-r>60 and b-g>40
print("  callout1 green rows:", border_rows(pred_green, 450,680,270,318,8))
print("  callout3 green rows:", border_rows(pred_green, 450,680,330,378,8))
print("  callout2 blue rows:", border_rows(pred_blue, 700,900,303,348,8))
print("  callout1 green cols:", border_cols(pred_green, 440,690,272,314,6))
print("  callout2 blue cols:", border_cols(pred_blue, 695,900,305,345,6))
print("  callout3 green cols:", border_cols(pred_green, 440,690,334,372,6))

print("\n== EMPHASIS + NOTE BOX ==")
def pred_yel(c): r,g,b=c; return r>235 and g>215 and b<160
print("  emphasis yellow bbox:", bbox(pred_yel, 500,370,940,450))
def pred_dark(c): r,g,b=c; return r<110 and g<110 and b<110
def pred_redtxt(c): r,g,b=c; return r>120 and r-g>60 and r-b>60 and r<230
print("  emphasis red text bbox:", bbox(pred_redtxt, 645,382,885,440))
def pred_bluetxt(c): r,g,b=c; return b>100 and b-r>50 and b-g>40
print("  notebox blue text bbox:", bbox(pred_bluetxt, 480,450,900,520))
print("  notebox red text bbox:", bbox(pred_redtxt, 480,450,900,520))
# note box text lines
for y in range(452, 518):
    n=sum(1 for x in range(495,890) if sum(px[x,y])<600)
    if n>10: print(f"    nb y={y}: {n}")
