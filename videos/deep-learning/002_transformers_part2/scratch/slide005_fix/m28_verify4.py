# m28_verify4.py — closed-loop verification of the arrow fix on render_4.png (150dpi)
# render_px = build_pt * 150/72 ; frame->render: rx = (fx-18.0787)*2.16770, ry = (fy-0.4700)*2.17684
from PIL import Image
import sys
R = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide005/render_4.png").convert("RGB")
W,H = R.size
print("render size:", W, H, "(expect 2001x1125)")
px = R.load()
def lum(x,y):
    r,g,b = px[int(x),int(y)]; return 0.299*r+0.587*g+0.114*b
def is_redp(x,y):
    r,g,b = px[int(x),int(y)]
    return r>130 and g<95 and b<95 and (r-g)>50
def is_pinkp(x,y):
    r,g,b = px[int(x),int(y)]
    return r>150 and 70<g<185 and (r-g)>25 and (r-b)>25
FAIL=[]
def check(name, cond, detail=""):
    print(("PASS " if cond else "FAIL ")+name+(("  "+detail) if detail else ""))
    if not cond: FAIL.append(name)

# --- 0. placeholder check: no red "Image 0 1" placeholder text anywhere ---
# scan for pure-red text-like clusters outside expected red regions: simple proxy —
# count of bright red pixels in the title band / margins should be ~0
def red_count(x0,x1,y0,y1):
    n=0
    for y in range(y0,y1):
        for x in range(x0,x1):
            r,g,b = px[x,y]
            if r>180 and g<80 and b<80: n+=1
    return n
print("red px in left margin band:", red_count(0,60,0,H), "(placeholder text would be large)")

# --- 1. connect_tan: ends ON the MHA inset top border junction (1002.1,514.6) ---
# walk the pink stroke near the end: pink ink at (1000-1005, 505-515)?
def ink_near(pred, cx, cy, rad=6):
    best=None
    for y in range(int(cy-rad), int(cy+rad+1)):
        for x in range(int(cx-rad), int(cx+rad+1)):
            if 0<=x<W and 0<=y<H and pred(x,y):
                d=((x-cx)**2+(y-cy)**2)**0.5
                if best is None or d<best[0]: best=(d,x,y)
    return best
b = ink_near(is_pinkp, 1002.1, 514.6, 8)
check("connect_tan end attaches inset top border", b is not None and b[0]<=4.0, str(b))
# and the OLD short end (979.2,495.8) should NOT be the terminal: pink ink must exist BEYOND it
b2 = ink_near(is_pinkp, 990, 503, 6)
check("connect_tan extends past old endpoint", b2 is not None, str(b2))

# --- 2. NO spurious pink stroke from banner1 (old path x1002-1017, y304-513) ---
n_pink = sum(1 for y in range(310,505) for x in range(998,1024) if is_pinkp(x,y))
check("no spurious banner1->inset pink stroke", n_pink <= 3, f"pink px in corridor={n_pink}")

# --- 3. connect_h gray: starts at border junction (1002,516.7), ends at head base (1025,733.3) ---
def grayp(x,y):
    r,g,b = px[int(x),int(y)]
    return abs(r-g)<14 and abs(g-b)<14 and 140<lum(x,y)<215
b = ink_near(grayp, 1002.1, 518.0, 7)
check("connect_h gray starts at junction", b is not None and b[0]<=4.0, str(b))
b = ink_near(grayp, 1025.0, 733.3, 7)
check("connect_h gray ends at head base", b is not None and b[0]<=4.0, str(b))

# --- 4. tan arrowhead: tip at (493.9,366.3)build=(1029.0,763.1); circle top at 788.8-22.9=765.9? ---
# circle center (1027.9,788.8) r22.9 -> top edge y=765.9. Head tip should be within 4px of 765.9
def darkbrownp(x,y):
    r,g,b = px[int(x),int(y)]
    return r<150 and g<110 and b<90 and (r-b)>30 and lum(x,y)<120
# head ink bbox in window
xs=[];ys=[]
for y in range(735,770):
    for x in range(1015,1042):
        if darkbrownp(x,y): xs.append(x); ys.append(y)
if xs:
    print("head ink bbox render: x%d..%d y%d..%d (target base y743.1 tip y763.1, x1023.3..1034.6)"%(min(xs),max(xs),min(ys),max(ys)))
    check("arrowhead tip reaches circle-top zone (y>=760)", max(ys)>=760, f"tip ink max y={max(ys)}")
    check("arrowhead x centered on circle (1023-1036)", 1020<=min(xs) and max(xs)<=1038)
else:
    check("arrowhead ink present", False, "no dark-brown ink found in head window")

# --- 5. h circle: center (1027.9,788.8) r~22.9; tan fill present, ring bbox ---
def tanp(x,y):
    r,g,b = px[int(x),int(y)]
    return r>185 and 140<g<215 and 90<b<195 and (r-b)>25
xs=[];ys=[]
for y in range(755,825):
    for x in range(995,1062):
        if tanp(x,y): xs.append(x); ys.append(y)
if xs:
    cx=(min(xs)+max(xs))/2; cy=(min(ys)+max(ys))/2
    print("circle tan bbox render: x%d..%d y%d..%d center(%.1f,%.1f) (target center 1027.9,788.8 d45.8)"%(min(xs),max(xs),min(ys),max(ys),cx,cy))
    check("h circle center within 4px", abs(cx-1027.9)<=4 and abs(cy-788.8)<=4, f"center ({cx:.1f},{cy:.1f})")
    check("h circle diameter within 4px", abs((max(xs)-min(xs))-45.8)<=5 and abs((max(ys)-min(ys))-45.8)<=5)
else:
    check("h circle present", False)

# --- 6. h_annot black curve: bottom end attaches red rect right border (x=992.7, y807.3) ---
def blackp(x,y):
    return lum(x,y)<110
b = ink_near(blackp, 993.5, 806.0, 7)
check("h_annot lower end on red-rect right border", b is not None and b[0]<=4.0, str(b))
b = ink_near(blackp, 1009.4, 716.7, 8)
check("h_annot top at measured (1009.4,716.7)", b is not None and b[0]<=5.0, str(b))

# --- 7. dash_d1: straight; ends ON enc box left border (1354.2, 775.0) ---
b = ink_near(is_redp, 1354.2, 775.0, 8)
check("dash_d1 end attaches enc MHA box left border", b is not None and b[0]<=4.5, str(b))
b = ink_near(is_redp, 1058.3, 529.2, 8)
check("dash_d1 starts on MHA inset right edge", b is not None and b[0]<=4.5, str(b))
# straightness: red dash ink near the OLD bend midpoint (build 576,300 -> 1200,625)?
# the straight line at rx=1200: ry = (529.2) + (1200-1058.3)*(775.0-529.2)/(1354.2-1058.3) = 529.2+141.7*0.8306=646.9
b = ink_near(is_redp, 1200.0, 646.9, 10)
check("dash_d1 passes straight-line midpoint (no bend)", b is not None and b[0]<=6.0, str(b))

# --- 8. dash_d2: ends ON red rect left border (635.0, 782.3) ---
b = ink_near(is_redp, 635.0, 782.3, 8)
check("dash_d2 end attaches red rect left border", b is not None and b[0]<=4.5, str(b))
b = ink_near(is_redp, 394.8, 578.1, 8)
check("dash_d2 starts on SDPA inset right edge", b is not None and b[0]<=4.5, str(b))
b = ink_near(is_redp, 500.0, 668.5, 10)
check("dash_d2 passes straight-line midpoint", b is not None and b[0]<=6.0, str(b))

# --- 9. dash_d3: slope -0.957; ends on SDPA inset right edge (393.8, 1014.6) ---
b = ink_near(is_redp, 393.8, 1014.6, 8)
check("dash_d3 end on SDPA inset right edge", b is not None and b[0]<=4.5, str(b))
b = ink_near(is_redp, 522.9, 891.7, 8)
check("dash_d3 upper end at measured (522.9,891.7)", b is not None and b[0]<=5.0, str(b))

print("\n==== %d FAIL ====" % len(FAIL))
for f in FAIL: print(" -", f)
sys.exit(1 if FAIL else 0)
