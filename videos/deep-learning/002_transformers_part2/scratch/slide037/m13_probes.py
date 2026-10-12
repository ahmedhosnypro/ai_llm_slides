#!/usr/bin/env python3
"""Fine probes: circle colors, funnel lines, feedback arc, encoder Nx, feeds, yellow band."""
from PIL import Image
from collections import Counter
import json

img = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_037.jpg").convert("RGB")
px = img.load()
AX, SX = 17.101, 0.962329
BY, SY = -0.224, 0.96053
def S(b): return [round((b[0]-AX)/SX,1), round((b[1]-BY)/SY,1), round((b[2]-AX)/SX,1), round((b[3]-BY)/SY,1)]
out = {}

def bbox_of(pred, x0,y0,x1,y1):
    xs=[];ys=[]
    for y in range(y0,y1):
        for x in range(x0,x1):
            if pred(px[x,y]): xs.append(x);ys.append(y)
    return (min(xs),min(ys),max(xs),max(ys)) if xs else None

redp  = lambda p: p[0]>110 and (p[0]-p[1])>55 and (p[0]-p[2])>55
bluep = lambda p: p[2]>110 and (p[2]-p[1])>55 and (p[2]-p[0])>55
grnp  = lambda p: p[1]>100 and (p[1]-p[0])>45 and (p[1]-p[2])>25
darkp = lambda p: p[0]<90 and p[1]<90 and p[2]<90

# A. encoder V circle zone x645-690 y375-415: what color?
zone = Counter()
for y in range(375,415):
    for x in range(645,690):
        p=px[x,y]
        if not (p[0]>235 and p[1]>225): zone[(p[0]//10*10,p[1]//10*10,p[2]//10*10)]+=1
out["encV_zone_top"] = [[list(k),v] for k,v in zone.most_common(8)]
vb = bbox_of(grnp, 645,375,692,415)
out["encV_green_bbox_slide"] = S(vb) if vb else None

# B. decoder masked circles row scan (frame y 385-410, x 735-835)
rowdata = {}
for fy in [388, 392, 396, 400, 404]:
    rowdata[fy] = [list(px[x,fy]) for x in range(738, 830, 4)]
out["dec_masked_rows"] = rowdata
rb = bbox_of(redp, 795,380,835,415)
out["decQ_red_slide"] = S(rb) if rb else None
bb = bbox_of(bluep, 735,380,800,415)
out["decVK_blue_slide"] = S(bb) if bb else None

# C. decoder cross circles row scan (frame y 300-330, x 735-835)
rowdata = {}
for fy in [300, 305, 310, 315, 320]:
    rowdata[fy] = [list(px[x,fy]) for x in range(738, 830, 4)]
out["dec_cross_rows"] = rowdata

# D. funnel: all red rows in corridor x196-645 y150-450 (full)
fun = {}
for y in range(150,455):
    xs=[x for x in range(196,646) if redp(px[x,y])]
    if xs: fun[y]=(min(xs),max(xs),len(xs))
out["funnel_full"] = {str(k): v for k,v in fun.items()}

# E. feedback arc, loose red-dark mask right of x850
fbp = lambda p: p[0]>80 and (p[0]-p[1])>35 and (p[0]-p[2])>35
arc = {}
for y in range(105,519):
    xs=[x for x in range(848,915) if fbp(px[x,y])]
    if xs: arc[y]=(min(xs),max(xs))
out["feedback_loose"] = {str(k): v for k,v in arc.items()}

# F. encoder Nx circle exact bbox + mode
tanp = lambda p: 180<p[0]<225 and 135<p[1]<180 and 70<p[2]<120
nb = bbox_of(tanp, 585,310,640,365)
out["encNx_bbox_slide"] = S(nb) if nb else None
if nb:
    out["encNx_mode"] = Counter(px[x,y] for y in range(nb[1],nb[3]) for x in range(nb[0],nb[2]) if tanp(px[x,y])).most_common(3)

# G. yellow band full extent (x660-760, y240-280)
yelb = lambda p: p[0]>230 and p[1]>230 and p[2]<120
yb = bbox_of(yelb, 650,235,770,285)
out["yellowband_slide"] = S(yb) if yb else None

# H. feeds from encoder to decoder: dark lines between x723-760, y250-330
fds = {}
for y in range(245,335):
    xs=[x for x in range(715,765) if darkp(px[x,y])]
    if xs: fds[y]=(min(xs),max(xs))
out["feeds_dark"] = {str(k): v for k,v in fds.items()}

# I. decoder right green trunk (parent green_trunk x841) present?
tr = {}
for y in range(200,420,7):
    row=[list(px[x,y]) for x in range(836,850)]
    tr[y]=row
out["trunk_probe"] = tr

print(json.dumps(out, indent=0, default=str))
