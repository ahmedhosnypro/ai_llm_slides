#!/usr/bin/env python3
"""Closed-loop self-check for slide 020 attempt 1 (150dpi render vs original measured ink).
Render 2001x1125; frame px * 2001/960 = render px (1px@150dpi = 1/200 in). Tolerance ~4px
(150dpi space) = ~2 frame px per the equation/geometry closed-loop law."""
from PIL import Image
import numpy as np

REN = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/qa/slide020/render_1.png"
S = 2001/960.0
a = np.asarray(Image.open(REN).convert("RGB")).astype(int)
r,g,b = a[:,:,0],a[:,:,1],a[:,:,2]
fails = []
def check(name, got, want, tol=4.0):
    d = max(abs(g-w) for g,w in zip(got, want))
    status = "OK " if d <= tol else "FAIL"
    if d > tol: fails.append(name)
    print(f"[{status}] {name:34s} got={tuple(round(x,1) for x in got)} want={tuple(round(x,1) for x in want)} d={d:.1f}")

def bboxm(mask, ox=0, oy=0):
    ys,xs = np.where(mask)
    if len(ys)==0: return None
    return (xs.min()+ox, ys.min()+oy, xs.max()+ox+1, ys.max()+oy+1)

red = (r>110)&(g<105)&(b<105)&((r-g)>50)
white = (r>235)&(g>235)&(b>235)
black = (r<70)&(g<70)&(b<70)
blue = (b>120)&(b-r>60)&(b-g>40)
green = (g-r>25)&(g-b>15)&(g>70)&(g<210)

# 1. title ink
tred = (r>140)&(g<120)&(b<120)&((r-g)>40)
bb = bboxm(tred[:220, 300:1600], 300, 0)
check("title bbox", (bb[0],bb[1],bb[2]), (219*S, 68*S, 655*S), 8)

# 2. white panel
bb = bboxm(white[150:1000, 100:1900], 100, 150)
check("panel white bbox", (bb[0],bb[1],bb[2],bb[3]), (72*S,102*S,894*S,464*S), 6)

# 3. chain boxes (fill bboxes)
def fillbb(x0,y0,x1,y1,target,tol=30):
    m = (np.abs(a[y0:y1,x0:x1]-np.array(target)).max(axis=2)<=tol)
    return bboxm(m, x0, y0)
bb = fillbb(120,420,420,560,(219,191,161),28)
check("InputSamples fill", bb, (82*S,214*S,156*S,256*S), 8)
bb = fillbb(400,420,640,560,(250,254,216),22)
check("Pre fill", bb, (207*S,211*S,278*S,261*S), 8)
bb = fillbb(660,420,880,560,(226,254,252),22)
check("FE fill", bb, (333*S,211*S,401*S,261*S), 8)
bb = fillbb(860,420,1100,560,(242,254,234),22)
check("FS fill", bb, (430*S,211*S,511*S,261*S), 8)
bb = fillbb(1110,420,1330,560,(160,0,0),45)
check("Class fill", bb, (535*S,209*S,629*S,263*S), 8)
bb = fillbb(1350,430,1560,560,(245,219,245),22)
check("PL fill", bb, (659*S,214*S,739*S,261*S), 8)
bb = fillbb(1660,430,1870,560,(219,191,161),28)
check("Samples fill", bb, (810*S,214*S,883*S,256*S), 8)

# 4. container peach
bb = fillbb(380,390,1360,600,(253,233,217),26)
check("container peach", (bb[0],bb[1],bb[2],bb[3]), (197*S,200*S,634*S,268*S), 10)

# 5. ellipse + dots
bb = fillbb(760,215,990,350,(246,222,194),22)
check("ellipse fill", bb, (374*S,113*S,465*S,157*S), 8)
bb = bboxm(blue[250:320, 730:800], 730, 250)
check("left dot", bb, (362*S,129*S,373*S,141*S), 8)
bb = bboxm(blue[250:320, 950:1030], 950, 250)
check("right dot", bb, (469*S,129*S,480*S,141*S), 8)

# 6. error box (pink) + vertical red text
bb = fillbb(1540,340,1690,650,(246,179,184),26)
check("error box fill", bb, (754*S,173*S,790*S,297*S), 8)
bb = bboxm(red[360:640, 1570:1650], 1570, 360)
check("error text colA", bb, (759*S,182*S,768*S,288*S), 12)
bb = bboxm(red[360:640, 1600:1650], 1600, 360)
check("error text colB", bb, (775*S,183*S,787*S,288*S), 12)

# 7. straight arrows: red runs at render y 490 (frame y235)
rowm = np.where(red[489, 100:1900])[0]+100
groups = np.split(rowm, np.where(np.diff(rowm)>12)[0]+1)
got = [f"{gp.min()/S:.0f}-{gp.max()/S:.0f}" for gp in groups]
print("arrows y235 render runs (frame px):", got)
want_runs = ["162-193","284-320","408-429","516-530","637-657","741-750","792-806"]
def close(runs, wants, tol=5):
    ok = len(runs)==len(wants)
    msgs=[]
    for got_s, w_s in zip(runs, wants):
        g0,g1 = map(float, got_s.split("-")); w0,w1 = map(float, w_s.split("-"))
        d = max(abs(g0-w0), abs(g1-w1))
        msgs.append(f"{d:.0f}")
        if d>tol: ok=False
    print(f"[{'OK ' if ok else 'FAIL'}] arrows x-extents vs want  deltas={msgs}")
    if not ok: fails.append("arrows x-extents")
close(got, want_runs)

# 8. block arrows (BD3F4B-ish fill)
ba = (np.abs(a-np.array([189,63,75])).max(axis=2)<=45)
bb = bboxm(ba[790:910, 1180:1330], 1180, 790)
check("blockarrow1", bb, (593*S,385*S,615*S,426*S), 8)
bb = bboxm(ba[620:760, 1560:1700], 1560, 620)
check("blockarrow2", bb, (768*S,309*S,790*S,350*S), 8)

# 9. curves ink
bb = bboxm(blue[380:470, 200:300], 200, 380)
check("arcL head", bb, (114*S,199*S,127*S,211*S), 8)
bb = bboxm(blue[380:470, 1700:1810], 1700, 380)
check("arcR head", bb, (837*S,198*S,851*S,211*S), 8)
bb = bboxm(green[530:600, 470:540], 470, 530)
check("green head Pre", bb, (238*S,261*S,249*S,275*S), 8)
bb = bboxm(green[530:600, 750:830], 750, 530)
check("green head Ext", bb, (360*S,261*S,371*S,275*S), 8)
bb = bboxm(green[530:600, 950:1030], 950, 530)
check("green head Sel", bb, (466*S,261*S,477*S,275*S), 8)
bb = bboxm(green[530:600, 1180:1260], 1180, 530)
check("green head Cls", bb, (576*S,261*S,587*S,275*S), 8)
bb = bboxm(green[600:660, 1540:1640], 1540, 600)
check("green stem", bb, (750*S,298*S,774*S,312*S), 12)

# 10. green box + text
bb = fillbb(520,690,1600,810,(238,250,218),18)
check("greenbox fill", bb, (263*S,341*S,741*S,377*S), 8)
bb = bboxm(green[700:790, 620:1480], 620, 700)
check("greentext ink", bb, (302*S,343*S,700*S,376*S), 10)

# 11. starburst + text
bb = bboxm(red[770:930, 1450:1860], 1450, 770)
check("starburst red outline", bb, (709*S,378*S,882*S,437*S), 16)
bb = bboxm(red[820:890, 1560:1720], 1560, 820)
check("starburst text", bb, (759*S,399*S,817*S,424*S), 10)

# 12. black bar
bb = bboxm(black[1070:1125, 50:1950], 50, 1070)
check("blackbar", bb, (38*S,518*S,922*S,537.5*S), 6)

# 13. text metrics: chain label ink (Extraction target w=65 frame px, cap 10)
sub = black[455:530, 660:850]
bb = bboxm(sub, 660, 455)
if bb:
    print(f"     'Extraction' ink frame-px w={(bb[2]-bb[0])/S:.1f} (want ~65), cap-h approx y-band {bb[1]:.0f}..{bb[3]:.0f} render")
# Classification white text
wt = (r>190)&(g>170)&(b>170)
bb = bboxm(wt[470:510, 1120:1310], 1120, 470)
check("Classification text", bb, (540*S,231*S,621*S,240*S), 10)

print()
print("FAILURES:", fails if fails else "none")
