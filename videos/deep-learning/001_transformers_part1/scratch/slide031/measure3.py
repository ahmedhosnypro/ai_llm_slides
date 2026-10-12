#!/usr/bin/env python3
"""Precise numeric scans for slide_031.jpg — panels, capsules, matrices, cells, text bands."""
from PIL import Image

im = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_031.jpg").convert("RGB")
W, H = im.size
px = im.load()

def pred_red(c):   r,g,b=c; return r>140 and r-g>60 and r-b>60
def pred_blue(c):  r,g,b=c; return b>140 and b-r>60 and b-g>40
def pred_green(c): r,g,b=c; return g>110 and g-r>35 and g-b>35
def pred_pink(c):  r,g,b=c; return abs(r-245)<20 and abs(g-184)<28 and abs(b-205)<30
def pred_rose(c):  r,g,b=c; return abs(r-242)<18 and abs(g-185)<22 and abs(b-198)<22
def pred_peri(c):  r,g,b=c; return abs(r-185)<24 and abs(g-194)<24 and abs(b-242)<24
def pred_mgrn(c):  r,g,b=c; return abs(r-199)<20 and abs(g-232)<18 and abs(b-199)<20
def pred_yel(c):   r,g,b=c; return r>235 and g>215 and b<160
def pred_dark(c):  r,g,b=c; return r<110 and g<110 and b<110

def bbox(p, x0, y0, x1, y1):
    mnx=mny=10**9; mxx=mxy=-1; n=0
    for y in range(y0,y1):
        for x in range(x0,x1):
            if p(px[x,y]):
                n+=1
                if x<mnx: mnx=x
                if x>mxx: mxx=x
                if y<mny: mny=y
                if y>mxy: mxy=y
    return (mnx,mny,mxx,mxy,n) if n else None

def rep(name, bb):
    if bb is None: print(f"{name}: NONE"); return
    print(f"{name}: x {bb[0]}..{bb[2]}  y {bb[1]}..{bb[3]}  w={bb[2]-bb[0]+1} h={bb[3]-bb[1]+1} n={bb[4]}")

def border_lines(p, x0, y0, x1, y1, minfrac, axis):
    """axis='rows': return rows where frac of px in [x0,x1) matches; axis='cols' likewise."""
    out=[]
    if axis=="rows":
        span=x1-x0
        for y in range(y0,y1):
            n=sum(1 for x in range(x0,x1) if p(px[x,y]))
            if n>=span*minfrac: out.append((y,n))
    else:
        span=y1-y0
        for x in range(x0,x1):
            n=sum(1 for y in range(y0,y1) if p(px[x,y]))
            if n>=span*minfrac: out.append((x,n))
    return out

print("=== PANEL BORDERS ===")
print("Q red rows (x60..460, y95..315, frac>=.5):", border_lines(pred_red, 60,95,460,315,.5,"rows"))
print("Q red cols (y105..295, x40..480, frac>=.5):", border_lines(pred_red, 40,105,480,295,.5,"cols"))
print("V blue rows (x470..900, y95..315, frac>=.5):", border_lines(pred_blue, 470,95,900,315,.5,"rows"))
print("V blue cols (y105..295, x460..940, frac>=.5):", border_lines(pred_blue, 460,105,940,295,.5,"cols"))
print("K green rows (x60..460, y300..540, frac>=.5):", border_lines(pred_green, 60,300,460,540,.5,"rows"))
print("K green cols (y310..525, x40..480, frac>=.5):", border_lines(pred_green, 40,310,480,525,.5,"cols"))

print("\n=== MATRIX BACKGROUNDS ===")
rep("Q rose matrix bg", bbox(pred_rose, 40,95,480,310))
rep("V peri matrix bg", bbox(pred_peri, 460,95,940,310))
rep("K mgrn matrix bg", bbox(pred_mgrn, 40,295,480,540))

print("\n=== PINK CAPSULES (per panel) ===")
rep("Q pink", bbox(pred_pink, 45,100,475,305))
rep("V pink", bbox(pred_pink, 465,100,935,305))
rep("K pink", bbox(pred_pink, 45,300,475,535))

print("\n=== YELLOW ===")
rep("title highlight Y", bbox(pred_yel, 100,35,900,75))
rep("emphasis box Y", bbox(pred_yel, 500,370,940,450))
rep("badge Y", bbox(pred_yel, 850,40,940,110))

print("\n=== TITLE / SUBTITLE INK (dark) ===")
rep("title band dark ink", bbox(pred_dark, 60,40,860,75))
rep("subtitle band dark-ish ink", bbox(lambda c: sum(c)<430, 60,72,880,92))

print("\n=== TEXT BAND PROFILES (dark ink per row, full width) ===")
for y in range(40, 100):
    n=sum(1 for x in range(40,920) if pred_dark(px[x,y]))
    if n>3: print(f"  y={y}: {n}")

print("\n=== INSIDE Q PANEL: dark ink row profile (x 55..470) ===")
for y in range(100, 310):
    n=sum(1 for x in range(55,470) if pred_dark(px[x,y]))
    if n>4: print(f"  y={y}: {n}")
