#!/usr/bin/env python3
"""Targeted scans 2 for slide_031.jpg."""
from PIL import Image

im = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_031.jpg").convert("RGB")
W, H = im.size
px = im.load()

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

print("=== POINT SAMPLES ===")
pts = [
 ("callout1 fill", 550, 295), ("callout1 fill b", 520, 300),
 ("callout2 fill", 800, 325), ("callout2 fill b", 760, 322),
 ("callout3 fill", 550, 352), ("callout3 fill b", 580, 355),
 ("note box interior", 700, 470), ("note box border top?", 700, 449),
 ("Q matrix bg (gap)", 215, 200), ("Q matrix cell fill", 250, 200),
 ("V matrix bg", 640, 200), ("K matrix bg", 215, 420), ("K matrix cell", 250, 420),
 ("Q capsule fill", 80, 155), ("V capsule fill", 500, 155), ("K capsule fill", 80, 435),
 ("peach margin", 45, 200), ("white canvas", 100, 480),
 ("y43 artifact", 200, 43), ("y43 artifact b", 600, 43), ("y44", 200, 44),
]
for lbl, x, y in pts:
    print(f"  {lbl} ({x},{y}): {px[x,y]}")

def pred_pink(c):  r,g,b=c; return abs(r-245)<20 and abs(g-184)<28 and abs(b-205)<30
def pred_rose(c):  r,g,b=c; return (abs(r-242)<18 and abs(g-185)<22 and abs(b-198)<22)
def pred_peri(c):  r,g,b=c; return abs(r-185)<24 and abs(g-194)<24 and abs(b-242)<24
def pred_mgrn(c):  r,g,b=c; return abs(r-199)<20 and abs(g-232)<18 and abs(b-199)<20
def pred_red(c):   r,g,b=c; return r>140 and r-g>60 and r-b>60
def pred_blue(c):  r,g,b=c; return b>140 and b-r>60 and b-g>40
def pred_green(c): r,g,b=c; return g>110 and g-r>35 and g-b>35
def pred_dark(c):  r,g,b=c; return r<110 and g<110 and b<110
def nonwhite(c):   r,g,b=c; return not(r>235 and g>235 and b>235)

print("\n=== MATRIX BLOCKS (nonwhite in center region) ===")
rep("Q matrix block", bbox(nonwhite, 200,102,405,295))
rep("V matrix block", bbox(nonwhite, 620,102,830,295))
rep("K matrix block", bbox(nonwhite, 200,310,405,520))

print("\n=== MATRIX BGs restricted ===")
rep("Q rose in 200..410", bbox(pred_rose, 200,102,410,295))
rep("V peri in 620..830", bbox(pred_peri, 620,102,830,295))
rep("K mgrn in 200..410", bbox(pred_mgrn, 200,310,410,520))

print("\n=== INPUT CAPSULES (pink, left region) ===")
rep("Q capsule", bbox(pred_pink, 50,102,205,230))
rep("V capsule", bbox(pred_pink, 470,102,625,230))
rep("K capsule", bbox(pred_pink, 50,315,205,440))

print("\n=== OUTPUT CAPSULES (pink cells, right region) ===")
rep("Q out pink", bbox(pred_pink, 405,102,460,295))
rep("V out pink", bbox(pred_pink, 830,102,885,295))
rep("K out pink", bbox(pred_pink, 405,315,460,520))

print("\n=== OUTPUT CAPSULE OUTLINE STROKES (col scans) ===")
for lbl, x0, x1, y0, y1, p in [
    ("Q red cols", 400, 465, 110, 280, pred_red),
    ("V blue cols", 820, 890, 110, 280, pred_blue),
    ("K green cols", 400, 465, 320, 500, pred_green),
]:
    out=[]
    span=y1-y0
    for x in range(x0,x1):
        n=sum(1 for y in range(y0,y1) if p(px[x,y]))
        if n>=span*0.4: out.append((x,n))
    print(f"  {lbl}: {out}")
    # vertical extent of the first stroke
    if out:
        xs=out[0][0]
        ys=[y for y in range(y0,y1) if p(px[xs,y])]
        print(f"    stroke x={xs}: y {min(ys)}..{max(ys)}")

print("\n=== K PANEL BORDERS (lower threshold) ===")
def border_rows(p, x0,x1,y0,y1,frac):
    out=[]
    span=x1-x0
    for y in range(y0,y1):
        n=sum(1 for x in range(x0,x1) if p(px[x,y]))
        if n>=span*frac: out.append((y,n))
    return out
print("  K green rows y295..340 frac>=.3:", border_rows(pred_green, 60,460,295,340,.3))
print("  K green cols x440..480:", [(x,sum(1 for y in range(315,520) if pred_green(px[x,y]))) for x in range(440,480) if sum(1 for y in range(315,520) if pred_green(px[x,y]))>80])

print("\n=== CALLOUT BORDERS ===")
# dashed green/blue rounded rects around (451..670, 278..312) etc. Find ink bbox per callout region
rep("callout1 all-ink", bbox(nonwhite, 445,272,680,315))
rep("callout2 all-ink", bbox(nonwhite, 700,305,920,345))
rep("callout3 all-ink", bbox(nonwhite, 445,332,680,375))
print("  callout1 green border px:", bbox(pred_green, 445,272,680,315))
print("  callout2 blue border px:", bbox(pred_blue, 700,305,920,345))
print("  callout3 green border px:", bbox(pred_green, 445,332,680,375))

print("\n=== NOTE BOX border ===")
# thin light border — scan for gray-ish lines
def pred_grayline(c): r,g,b=c; return 120<r<215 and 120<g<215 and 120<b<215 and abs(r-g)<25 and abs(g-b)<25
print("  gray rows y440..530 (x500..900, frac>=.8):", [(y,sum(1 for x in range(500,900) if pred_grayline(px[x,y]))) for y in range(440,530) if sum(1 for x in range(500,900) if pred_grayline(px[x,y]))>320])
print("  gray cols x440..940 (y455..520, frac>=.8):", [(x,sum(1 for y in range(455,520) if pred_grayline(px[x,y]))) for x in range(440,940) if sum(1 for y in range(455,520) if pred_grayline(px[x,y]))>52])
rep("notebox ink", bbox(lambda c: sum(c)<600, 430,445,935,530))

print("\n=== LABELS in Q panel ===")
rep("Q 'X2' red label (below capsule)", bbox(pred_red, 50,160,205,235))
rep("Q '1xd' dark (below capsule)", bbox(pred_dark, 50,160,205,200))
rep("Q 'W_Q' red (matrix bottom-left)", bbox(pred_red, 200,240,290,295))
rep("Q 'dxd' dark (matrix bottom-right)", bbox(pred_dark, 330,240,410,295))
rep("Q '=' dark (matrix..outcap)", bbox(pred_dark, 370,170,412,250))
rep("Q role letter red (above outcap)", bbox(pred_red, 405,98,465,140))
rep("Q capsule cell labels dark", bbox(pred_dark, 55,120,205,175))
