#!/usr/bin/env python3
"""Closed-loop self-check v2 for slide 020 (render vs original measured ink).
Surgical windows; each element measured in isolation. Tolerance 4px @150dpi (~2 frame px)
unless the element is inherently soft (dashed fan, starburst spikes)."""
from PIL import Image
import numpy as np

import sys
REN = sys.argv[1] if len(sys.argv) > 1 else "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/qa/slide020/render_2.png"
S = 2001/960.0
a = np.asarray(Image.open(REN).convert("RGB")).astype(int)
r,g,b = a[:,:,0],a[:,:,1],a[:,:,2]
fails = []
def check(name, got, want, tol=4.0):
    d = max(abs(gg-w) for gg,w in zip(got, want))
    status = "OK " if d <= tol else "FAIL"
    if d > tol: fails.append(name)
    print(f"[{status}] {name:30s} got={tuple(round(float(x),1) for x in got)} want={tuple(round(float(x),1) for x in want)} d={d:.1f}")

def bboxm(mask, ox=0, oy=0):
    ys,xs = np.where(mask)
    if len(ys)==0: return None
    return (xs.min()+ox, ys.min()+oy, xs.max()+ox+1, ys.max()+oy+1)

red = (r>110)&(g<105)&(b<105)&((r-g)>50)
black = (r<110)&(g<110)&(b<110)
blue = (b>120)&(b-r>60)&(b-g>40)
green = (g-r>25)&(g-b>15)&(g>70)&(g<210)

# title (window strictly inside canvas band, above panel border)
tred = (r>140)&(g<120)&(b<120)&((r-g)>40)
bb = bboxm(tred[125:200, 300:1600], 300, 125)
check("title ink", (bb[0]/S,bb[1]/S,bb[2]/S,bb[3]/S), (219,68,655,91.5), 4)

# boxes: fill sample points + border-edge probes
for name, (fx,fy), want in [
    ("Input fill", (120,235), (219,191,161)), ("Pre fill", (240,218), (250,254,216)),
    ("FE fill", (365,218), (226,254,252)), ("FS fill", (470,218), (242,254,234)),
    ("Class fill", (580,220), (160,0,0)), ("PL fill", (700,218), (245,219,245)),
    ("Samples fill", (845,235), (219,191,161)), ("errbox fill", (772,185), (246,179,184)),
    ("ellipse fill", (420,120), (246,222,194)), ("greenbox fill", (300,360), (238,250,218)),
    ("container fill", (200,253), (253,233,217)), ("container fill2", (317,220), (253,233,217)),
]:
    got = tuple(a[int(fy*S), int(fx*S)])
    check(name+" color", got, want, 6)

# box outer edges via fill-extent (tight windows inside each box, avoiding neighbors)
def fillbb(x0,y0,x1,y1,target,tol):
    m = (np.abs(a[y0:y1,x0:x1]-np.array(target)).max(axis=2)<=tol)
    return bboxm(m, x0, y0)
bb = fillbb(180,440,330,545,(219,191,161),10)
check("Input extent", (bb[0]/S,bb[1]/S,bb[2]/S,bb[3]/S), (81,213.5,158,257.5), 4)
bb = fillbb(430,435,580,550,(250,254,216),10)
check("Pre extent", (bb[0]/S,bb[1]/S,bb[2]/S,bb[3]/S), (206.5,210,279.5,262), 4)
bb = fillbb(700,435,830,550,(226,254,252),10)
check("FE extent", (bb[0]/S,bb[1]/S,bb[2]/S,bb[3]/S), (332.5,210,402.5,262), 4)
bb = fillbb(900,435,1060,550,(242,254,234),10)
check("FS extent", (bb[0]/S,bb[1]/S,bb[2]/S,bb[3]/S), (429.5,210,512.5,262), 4)
bb = fillbb(1120,440,1310,550,(160,0,0),30)
check("Class extent", (bb[0]/S,bb[1]/S,bb[2]/S,bb[3]/S), (534,208.5,630,263.5), 4)
bb = fillbb(1380,445,1530,545,(245,219,245),10)
check("PL extent", (bb[0]/S,bb[1]/S,bb[2]/S,bb[3]/S), (658,213.5,740,260.5), 4)
bb = fillbb(1690,445,1845,545,(219,191,161),10)
check("Samples extent", (bb[0]/S,bb[1]/S,bb[2]/S,bb[3]/S), (808.5,213.5,885,257.5), 4)
bb = fillbb(1560,360,1655,640,(246,179,184),14)
check("errbox extent", (bb[0]/S,bb[1]/S,bb[2]/S,bb[3]/S), (753.5,171.5,790.5,297.5), 4)
bb = fillbb(770,230,980,340,(246,222,194),12)
check("ellipse extent", (bb[0]/S,bb[1]/S,bb[2]/S,bb[3]/S), (374.5,112.5,464.5,157.5), 5)
bb = fillbb(545,700,1535,800,(238,250,218),10)
check("greenbox extent", (bb[0]/S,bb[1]/S,bb[2]/S,bb[3]/S), (262.5,340.5,741.5,378.5), 4)

# dots (tight windows excluding arcs)
bb = bboxm(blue[262:300, 752:790], 752, 262)
check("left dot", (bb[0]/S,bb[1]/S,bb[2]/S,bb[3]/S), (362,129.5,373.5,141), 4)
bb = bboxm(blue[262:300, 975:1012], 975, 262)
check("right dot", (bb[0]/S,bb[1]/S,bb[2]/S,bb[3]/S), (469,129.5,480.5,141), 4)

# error text: two columns (tight column windows), vertical extent
sub = red[360:640, 1571:1610]
ys,xs = np.where(sub)
check("err colA", ((xs.min()+1571)/S,(ys.min()+360)/S,(xs.max()+1571+1)/S,(ys.max()+360+1)/S), (759,181.5,768.5,288.5), 6)
sub = red[360:640, 1612:1650]
ys,xs = np.where(sub)
check("err colB", ((xs.min()+1612)/S,(ys.min()+360)/S,(xs.max()+1612+1)/S,(ys.max()+360+1)/S), (775,182.5,787.5,287.5), 6)

# arrows: probe shaft presence + tip x at y=489 (avoid Class fill: windows per arrow)
probes = [("a1", (340,410), 162, 193), ("a2", (600,680), 282, 320), ("a3", (855,915), 406, 429),
          ("a4", (1080,1120), 514, 530), ("a5", (1330,1390), 635, 657),
          ("a6", (1545,1575), 740, 750), ("a7", (1652,1690), 792, 806)]
for name,(wx0,wx1),w0,w1 in probes:
    m = np.where(red[486:494, wx0:wx1])[0]
    if len(m)==0:
        print(f"[FAIL] {name}: no red ink in window"); fails.append(name); continue
    check(name, ((m.min()+wx0)/S, (m.max()+wx0+1)/S), (w0, w1), 5)

# curves: heads (tight windows at the tips), stem
bb = bboxm(blue[415:450, 225:275], 225, 415)
check("arcL head", (bb[0]/S,bb[1]/S,bb[2]/S,bb[3]/S), (113.5,199.5,127,211.5), 5)
bb = bboxm(blue[415:450, 1735:1790], 1735, 415)
check("arcR head", (bb[0]/S,bb[1]/S,bb[2]/S,bb[3]/S), (837.5,199.5,851,211.5), 5)
bb = bboxm(green[540:580, 480:540], 480, 540)
check("green head Pre", (bb[0]/S,bb[1]/S,bb[2]/S,bb[3]/S), (238.5,261,248,275), 5)
bb = bboxm(green[540:580, 745:800], 745, 540)
check("green head Ext", (bb[0]/S,bb[1]/S,bb[2]/S,bb[3]/S), (360.5,261,370.5,275), 5)
bb = bboxm(green[540:580, 960:1015], 960, 540)
check("green head Sel", (bb[0]/S,bb[1]/S,bb[2]/S,bb[3]/S), (466.5,261,476.5,275), 5)
bb = bboxm(green[540:580, 1195:1250], 1195, 540)
check("green head Cls", (bb[0]/S,bb[1]/S,bb[2]/S,bb[3]/S), (576.5,261,586.5,275), 5)
bb = bboxm(green[615:660, 1555:1630], 1555, 615)
check("green stem", (bb[0]/S,bb[1]/S,bb[2]/S,bb[3]/S), (750,297.5,773.5,312), 8)

# green text: two line bands
sub = green[700:800, 500:1550]
rows = sub.sum(axis=1)
bands=[]; inb=False
for i,c in enumerate(rows):
    if c>0 and not inb: inb=True; s0=i
    if c==0 and inb: inb=False; bands.append((s0+700,i+700))
if inb: bands.append((s0+700,800))
if len(bands)==2:
    for i,(y0,y1),(wx0,wx1) in zip((1,2), bands, [(307,701),(302,699)]):
        s2 = green[y0:y1, 500:1550]
        ys2,xs2 = np.where(s2)
        check(f"greentext L{i}", ((xs2.min()+500)/S, y0/S, (xs2.max()+500+1)/S, y1/S), (wx0, 343 if i==1 else 362, wx1, 356 if i==1 else 376), 8)
else:
    print(f"[FAIL] greentext bands: {bands}"); fails.append("greentext")

# chain text inks (per-line where separable): report + check union extents
for name,(x0,x1),(wx0,wx1) in [
    ("Pre text", (420,590), (210,276)), ("FE text", (680,850), (331,395)),
    ("FS text", (900,1070), (442,500)), ("PL text", (1380,1545), (665,729)),
    ("Input text", (180,330), (93,150)), ("Samples text", (1685,1840), (814,881)),
]:
    s3 = black[440:540, x0:x1]
    ys3,xs3 = np.where(s3)
    if len(ys3):
        check(f"{name}", ((xs3.min()+x0)/S, (ys3.min()+440)/S, (xs3.max()+x0+1)/S, (ys3.max()+440)/S), (wx0, 222.5, wx1, 250.5), 6)

# ellipse text
s4 = black[240:330, 790:970]
ys4,xs4 = np.where(s4)
if len(ys4):
    check("ellipse text", ((xs4.min()+790)/S, (ys4.min()+240)/S, (xs4.max()+790+1)/S, (ys4.max()+240)/S), (391,121.5,444,147.5), 6)

# starburst text + fill sanity
s5 = red[820:895, 1565:1720]
ys5,xs5 = np.where(s5)
check("starburst text", ((xs5.min()+1565)/S, (ys5.min()+820)/S, (xs5.max()+1565+1)/S, (ys5.max()+820)/S), (759,398.5,817,424.5), 8)
got = tuple(a[int(392*S), int(742*S)])
check("star fill color", got, (255,255,204), 12)

# Classification white text
wt = (r>190)&(g>170)&(b>170)
s6 = wt[470:510, 1120:1310]
ys6,xs6 = np.where(s6)
check("Classification text", ((xs6.min()+1120)/S, (ys6.min()+470)/S, (xs6.max()+1120+1)/S, (ys6.max()+470)/S), (540,230.5,621.5,240), 6)

print()
print("FAILURES:", fails if fails else "none")
sys.exit(1 if fails else 0)
