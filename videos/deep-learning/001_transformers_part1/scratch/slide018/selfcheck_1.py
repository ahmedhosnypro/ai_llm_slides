from PIL import Image
import collections, sys

R = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/qa/slide018/render_1.png').convert('RGB')
P = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/qa/slide017/render_1.png').convert('RGB')
print("render size:", R.size)
S = R.size[0] / 960.0
r = R.resize((960, 540), Image.LANCZOS) if R.size != (960,540) else R
p = P.resize((960, 540), Image.LANCZOS) if P.size != (960,540) else P
pr, pp = r.load(), p.load()
px = pr

ok = True
def check(name, cond, detail=""):
    global ok
    print(("PASS " if cond else "FAIL ") + name, detail)
    if not cond: ok = False

# ---- 1. inheritance diff: clusters must be confined to delta zones ----
DELTA_ZONES = [(0,80,570,540), (630,340,735,400), (735,255,835,320), (860,40,930,120), (560,90,585,540), (880,510,910,540), (570,240,660,380)]
def in_delta(x,y):
    return any(x0<=x<=x1 and y0<=y<=y1 for (x0,y0,x1,y1) in DELTA_ZONES)
pts=[]
for y in range(540):
    for x in range(960):
        a=pr[x,y]; b=pp[x,y]
        if abs(a[0]-b[0])+abs(a[1]-b[1])+abs(a[2]-b[2])>90: pts.append((x,y))
out=[(x,y) for (x,y) in pts if not in_delta(x,y)]
print("inheritance diff px:", len(pts), "outside delta zones:", len(out))
# ignore sub-pixel noise: cluster outs
if out:
    cc=collections.Counter((x//16*16,y//16*16) for x,y in out)
    big=[(k,v) for k,v in cc.items() if v>=6]
    print("outside clusters >=6px:", sorted(big)[:20])
    check("inheritance-diff confined to delta zones", len(big)==0, str(sorted(big)[:8]))
else:
    check("inheritance-diff confined to delta zones", True)

# ---- 2. geometry vs measured frame targets (tolerance px) ----
def bbox(pred,x0,y0,x1,y1):
    pts=[(x,y) for y in range(y0,y1) for x in range(x0,x1) if pred(*pr[x,y])]
    if not pts: return None
    xs=[q[0] for q in pts]; ys=[q[1] for q in pts]
    return (min(xs),min(ys),max(xs),max(ys))
def near(got, want, tol):
    return got and all(abs(g-w)<=tol for g,w in zip(got,want))

b1 = bbox(lambda R_,G_,B_: abs(R_-242)<15 and abs(G_-198)<15 and abs(B_-153)<17, 40,80,540,230)
check("banner1 bbox ~ (71,104,488,145)", near(b1,(71,104,488,145),6), str(b1))
b2 = bbox(lambda R_,G_,B_: abs(R_-222)<9 and abs(G_-205)<9 and abs(B_-187)<9, 100,150,425,206)
check("banner2 bbox ~ (109,157,415,199)", near(b2,(109,157,415,199),8), str(b2))
fa = bbox(lambda R_,G_,B_: G_>90 and R_<100 and B_<110 and G_-R_>30, 40,240,220,520)
check("frameA green ~ (59,269,189,491)", near(fa,(59,269,189,491),7), str(fa))
fb = bbox(lambda R_,G_,B_: G_>90 and R_<100 and B_<110 and G_-R_>30, 270,220,540,540)
check("frameB green ~ (300,246,508,515)", near(fb,(300,246,508,515),7), str(fb))
def redpx(x,y):
    R_,G_,B_ = pr[x,y]
    return R_>150 and G_<85 and B_<85
def edge_has(x0,y0,x1,y1,frac=0.5):
    pts=[(x,y) for y in range(y0,y1+1) for x in range(x0,x1+1) if redpx(x,y)]
    return len(pts) >= frac*max(1,(y1-y0+1)*(x1-x0+1))**0.5, len(pts)
g,c = edge_has(310,354,468,356); check("red rect B top edge", g, "n=%d"%c)
g,c = edge_has(310,394,468,397); check("red rect B bottom edge", g, "n=%d"%c)
g,c = edge_has(303,360,305,390,0.3); check("red rect B left edge", g, "n=%d"%c)
g,c = edge_has(473,360,476,390,0.3); check("red rect B right edge", g, "n=%d"%c)
g,c = edge_has(655,355,718,357); check("enc MHA top edge", g, "n=%d"%c)
g,c = edge_has(655,385,718,388); check("enc MHA bottom edge", g, "n=%d"%c)
g,c = edge_has(649,360,652,382,0.3); check("enc MHA left edge", g, "n=%d"%c)
g,c = edge_has(719,360,723,382,0.3); check("enc MHA right edge", g, "n=%d"%c)
g,c = edge_has(755,277,815,279,0.4); check("dec MHA top edge (dashed)", g, "n=%d"%c)
g,c = edge_has(755,308,815,311,0.4); check("dec MHA bottom edge (dashed)", g, "n=%d"%c)
g,c = edge_has(747,282,750,305,0.3); check("dec MHA left edge", g, "n=%d"%c)
g,c = edge_has(818,282,822,305,0.3); check("dec MHA right edge", g, "n=%d"%c)
g,c = edge_has(660,358,712,384,0.2); check("enc MHA salmon fill", g, "n=%d"%c)

# ---- 3. containment: inset content inside frames; nothing outside house frame ----
def ink(x,y):
    R_,G_,B_ = pr[x,y]
    return not (R_>243 and G_>243 and B_>238) and not (abs(R_-233)<9 and abs(G_-233)<9 and abs(B_-231)<10)
viol=[]
for y in range(272,489):
    for x in range(62,187):
        if ink(x,y) and not (59-1<=x<=189+1 and 269-1<=y<=491+1): viol.append((x,y))
# allow the dashed connectors crossing the frame borders (d2/d3) and title above
viol=[(x,y) for (x,y) in viol if not (180<=x<=300)]
print("frameA content violations (raw):", len(viol), viol[:10])
check("frameA content contained", len(viol)<=4, str(viol[:6]))
viol=[]
for y in range(249,513):
    for x in range(303,506):
        if ink(x,y) and not (300-1<=x<=508+1 and 246-1<=y<=515+1): viol.append((x,y))
viol=[(x,y) for (x,y) in viol if not (470<=x<=508 and 340<=y<=395)]  # h circle zone + connectors crossing
print("frameB content violations (raw):", len(viol), viol[:10])
check("frameB content contained", len(viol)<=4, str(viol[:6]))
# house frame containment: no ink outside x42..918 (panel) other than white margin
outp=[(x,y) for y in range(0,540,2) for x in list(range(2,40))+list(range(922,958)) if ink(x,y) and not (pr[x,y][0]>250 and pr[x,y][1]>250)]
print("ink in white margins:", len(outp))
check("house margin clean", len(outp)==0, str(outp[:6]))

# ---- 4. key element presence (ink in measured regions) ----
def has_ink(x0,y0,x1,y1,n=8):
    c=sum(1 for y in range(y0,y1) for x in range(x0,x1) if ink(x,y))
    return c>=n, c
for name,(x0,y0,x1,y1) in {
  "h circle":(485,357,504,378), "conn into h":(485,250,495,350),
  "d1 diagonal":(505,245,650,370), "d2 diagonal":(191,272,295,357),
  "banner1 text":(120,105,440,144), "banner2 text":(150,160,380,198),
  "sdpa title":(60,228,200,264), "mha title":(300,210,490,232),
}.items():
    good,c = has_ink(x0,y0,x1,y1)
    check("ink present: "+name, good, "n=%d"%c)

# circles present
for name,(cx,cy,d) in {"A q":(91.5,473.5,15),"A k":(128,473,17),"A v":(166.5,473,18),
                       "B v":(330,498,18),"B k":(387.5,498,18),"B q":(445,498.5,16)}.items():
    good,c = has_ink(int(cx-d/2)-1,int(cy-d/2)-1,int(cx+d/2)+2,int(cy+d/2)+2, 12)
    check("circle: "+name, good, "n=%d"%c)

print("SELFCHECK RESULT:", "PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
