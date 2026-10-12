#!/usr/bin/env python3
"""Remaining PIL unknowns."""
from PIL import Image
from collections import Counter
import json

img = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_037.jpg").convert("RGB")
px = img.load()
AX, SX = 17.101, 0.962329
BY, SY = -0.224, 0.96053
def SX_(fx): return round((fx-AX)/SX,1)
def SY_(fy): return round((fy-BY)/SY,1)
out = {}

def bbox_of(pred, x0,y0,x1,y1):
    xs=[];ys=[]
    for y in range(y0,y1):
        for x in range(x0,x1):
            if pred(px[x,y]): xs.append(x);ys.append(y)
    return (min(xs),min(ys),max(xs),max(ys)) if xs else None
def SL(b):
    return None if b is None else [SX_(b[0]),SY_(b[1]),SX_(b[2]),SY_(b[3])]

# 1. feedback arc: loose red mask, x846-896 only (exclude house border)
fbp = lambda p: p[0]>75 and (p[0]-p[1])>30 and (p[0]-p[2])>30
arc = []
for y in range(105,519):
    xs=[x for x in range(846,897) if fbp(px[x,y])]
    if xs: arc.append((y,min(xs),max(xs)))
out["arc_rows"] = [[y, SX_(a), SX_(b)] for y,a,b in arc]

# 2. funnel: all red rows x196-646, y145-460, print every 2nd row
redp = lambda p: p[0]>110 and (p[0]-p[1])>55 and (p[0]-p[2])>55
fun = []
for y in range(145,460):
    xs=[x for x in range(196,647) if redp(px[x,y])]
    if xs: fun.append((y,min(xs),max(xs),len(xs)))
out["funnel_all"] = [[y, SX_(a), SX_(b), n] for y,a,b,n in fun]

# 3. dec_top stack: exact boxes
g1 = lambda p: 160<p[0]<200 and 225<p[1]<252 and 175<p[2]<215   # softmax A8ECBC-ish
g2 = lambda p: 160<p[0]<200 and 215<p[1]<245 and 195<p[2]<225   # linear B0E4CE-ish
yel = lambda p: p[0]>230 and p[1]>230 and p[2]<130
out["softmax_box"] = SL(bbox_of(g1, 740,140,830,175))
out["linear_box"]  = SL(bbox_of(g2, 740,165,830,200))
out["output_box"]  = SL(bbox_of(yel, 745,105,820,140))
# Probabilities text row (dark in y130-145)
dark = lambda p: p[0]<90 and p[1]<90 and p[2]<90
out["probab_ink"] = SL(bbox_of(dark, 745,128,830,148))
out["softmax_text"] = SL(bbox_of(dark, 740,148,830,172))
out["linear_text"] = SL(bbox_of(dark, 740,172,830,198))

# 4. trunk + chevrons: column x838-843 (trunk), navy chevrons under boxes
trk = []
for y in range(195,425):
    p = px[840,y]
    if p[1]>110 and (p[1]-p[0])>30: trk.append(y)
out["trunk_rows_at_x840"] = (min(trk), max(trk), len(trk)) if trk else None
navy = lambda p: p[2]>90 and p[0]<70 and p[1]<70
nb = bbox_of(navy, 745,190,840,420)
out["navy_chevrons_bbox"] = SL(nb)

# 5. yellow band part3 (740-790, 300-330)
out["yband3"] = SL(bbox_of(yel, 735,296,800,335))
# part1/2 exact
out["yband12"] = SL(bbox_of(yel, 660,240,750,310))

# 6. embed label boxes (white inner boxes)
wht = lambda p: p[0]>235 and p[1]>235 and p[2]>230
out["enc_embed_label"] = SL(bbox_of(wht, 640,440,730,480))
out["dec_embed_label"] = SL(bbox_of(wht, 745,440,825,480))

# 7. V/K feed lines from encoder to decoder cross: sample rows x723-760 y255-330
feeds = []
for y in range(250,335):
    xs=[x for x in range(718,762) if dark(px[x,y])]
    if xs: feeds.append((y,min(xs),max(xs)))
out["feeds_dark_rows"] = [[y, SX_(a), SX_(b)] for y,a,b in feeds]

# 8. exact mode colors in tight windows (original frame)
def mode_at(x0,y0,x1,y1,pred=None):
    c = Counter()
    for y in range(y0,y1):
        for x in range(x0,x1):
            p = px[x,y]
            if pred is None or pred(p): c[p]+=1
    return [[list(k),v] for k,v in c.most_common(4)]
out["mode_encAaN_top"]  = mode_at(660,270,700,285)     # A&N top zone (frame)
out["mode_encFF"]       = mode_at(660,285,700,310)
out["mode_encAaN_bot"]  = mode_at(660,335,700,350)
out["mode_encContainer"]= mode_at(636,320,648,340)
out["mode_softmax_dec"] = mode_at(755,152,810,163)
out["mode_linear_dec"]  = mode_at(755,178,810,190)
out["mode_decStack_top"]= mode_at(760,205,800,218)
out["mode_decStack_mid"]= mode_at(760,252,800,262)
out["mode_encPanel"]    = mode_at(585,120,600,140)
out["mode_decPanel"]    = mode_at(860,130,875,150)
out["mode_leftWhite"]   = mode_at(100,270,150,280)
out["mode_lembed"]      = mode_at(120,415,160,425)

print(json.dumps(out, indent=0, default=str))
