#!/usr/bin/env python3
"""Circles (V/K/Q), highlight circle + glow, pin, funnel dashed lines, feedback arc."""
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

redp  = lambda p: p[0]>130 and (p[0]-p[1])>70 and (p[0]-p[2])>70
bluep = lambda p: p[2]>120 and (p[2]-p[1])>60 and (p[2]-p[0])>60
grnp  = lambda p: p[1]>110 and (p[1]-p[0])>50 and (p[1]-p[2])>30
yelgl = lambda p: p[0]>230 and p[1]>210 and 100<p[2]<190

# --- V/K/Q circles: cluster red/blue ink per column region
for label, (x0,y0,x1,y1) in {
  "enc_vkq": (630,375,740,405),
  "dec_masked_vkq": (735,378,835,410),
  "dec_cross_vkq": (735,300,835,330),
}.items():
    rb = bbox_of(redp, x0,y0,x1,y1)
    bb = bbox_of(bluep, x0,y0,x1,y1)
    out[label] = {"red": S(rb) if rb else None, "blue": S(bb) if bb else None}
    # individual circle bboxes via column clustering
    def clusters(pred):
        xs=[x for y in range(y0,y1) for x in range(x0,x1) if pred(px[x,y])]
        if not xs: return []
        xs=sorted(set(xs)); groups=[]; cur=[xs[0]]
        for a in xs[1:]:
            if a-cur[-1]<=3: cur.append(a)
            else: groups.append(cur); cur=[a]
        groups.append(cur)
        res=[]
        for g in groups:
            if len(g)<4: continue
            ys=[y for y in range(y0,y1) for x in g if pred(px[x,y])]
            res.append((round((g[0]+g[-1])/2,1), round((min(ys)+max(ys))/2,1), g[-1]-g[0]+1, max(ys)-min(ys)+1))
        return res
    out[label+"_red_c"] = clusters(redp)
    out[label+"_blue_c"] = clusters(bluep)

# --- highlight circle: red mask around x630-740, y320-430 (exclude pin area y<270)
hb = bbox_of(redp, 630,315,745,435)
out["highlight_red_bbox_slide"] = S(hb) if hb else None
# yellow glow around it
gb = bbox_of(yelgl, 630,300,760,440)
out["glow_bbox_slide"] = S(gb) if gb else None
# circle horizontal extent at its center row
if hb:
    cy = (hb[1]+hb[3])//2
    row = [x for x in range(600,780) if redp(px[x,cy])]
    out["highlight_row_at_cy"] = (min(row), max(row), cy)

# --- pin: red mask x560-680 y140-270 + white text inside
pb = bbox_of(redp, 555,140,690,275)
out["pin_bbox_slide"] = S(pb) if pb else None
if pb:
    # white text inside pin
    wht = lambda p: p[0]>230 and p[1]>230 and p[2]>230
    wb = bbox_of(wht, pb[0]+5, pb[1]+5, pb[2]-5, pb[3]-5)
    out["pin_white_text_bbox_slide"] = S(wb) if wb else None
    out["pin_mode"] = Counter(px[x,y] for y in range(pb[1],pb[3]) for x in range(pb[0],pb[2]) if redp(px[x,y])).most_common(2)

# --- funnel dashed red lines: red px in corridor x195-640, y240-440 (excluding insets)
seg = {}
for y in range(240,445):
    xs=[x for x in range(196,640) if redp(px[x,y])]
    if xs: seg[y]=(min(xs),max(xs),len(xs))
ys_sorted = sorted(seg)
out["funnel_rows_count"] = len(ys_sorted)
out["funnel_rows"] = {str(y): seg[y] for y in ys_sorted[::4]}
out["funnel_y_ext"] = (ys_sorted[0], ys_sorted[-1]) if ys_sorted else None

# --- feedback arc: red px right of decoder stack x855-905, y110-520
arc = {}
for y in range(110,519):
    xs=[x for x in range(852,912) if redp(px[x,y])]
    if xs: arc[y]=(min(xs),max(xs))
out["feedback_arc"] = {str(y): v for y,v in arc.items()}

# --- encoder-side Nx probe x578-635 y315-370
out["enc_nx_probe"] = {}
for y in range(315,370,3):
    row=[]
    for x in range(578,636,3):
        row.append(px[x,y])
    out["enc_nx_probe"][y] = row
print(json.dumps(out, indent=1, default=str))
