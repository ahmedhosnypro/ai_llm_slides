#!/usr/bin/env python3
"""Left + center insets: run-merged box detection + circles + arrows + header lines."""
from PIL import Image
from collections import Counter
import json

img = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_037.jpg").convert("RGB")
px = img.load()
AX, SX = 17.101, 0.962329
BY, SY = -0.224, 0.96053
def S(b): return [round((b[0]-AX)/SX,1), round((b[1]-BY)/SY,1), round((b[2]-AX)/SX,1), round((b[3]-BY)/SY,1)]
out = {}

def boxes_for(pred, x0,y0,x1,y1, min_run=8, min_rows=3, join=2):
    rowruns = {}
    for y in range(y0,y1):
        runs=[]; start=None
        for x in range(x0,x1):
            if pred(px[x,y]):
                if start is None: start=x
            else:
                if start is not None and x-start>=min_run: runs.append((start,x-1))
                start=None
        if start is not None and x1-start>=min_run: runs.append((start,x1-1))
        if runs: rowruns[y]=runs
    used=set(); boxes=[]
    for y in sorted(rowruns):
        if y in used: continue
        stack=[(y,rowruns[y])]; comp=[y]; seen={y}; allruns=list(rowruns[y])
        while stack:
            cy, cr = stack.pop()
            for ny in (cy-1, cy+1):
                if ny in rowruns and ny not in seen and abs(ny-cy)<=join:
                    if any(not(r2[1]<r[0]-6 or r2[0]>r[1]+6) for r2 in rowruns[ny] for r in cr):
                        seen.add(ny); comp.append(ny); stack.append((ny,rowruns[ny])); allruns.extend(rowruns[ny])
        for r in comp: used.add(r)
        if len(comp)>=min_rows:
            boxes.append((min(r[0] for r in allruns), min(comp), max(r[1] for r in allruns), max(comp)))
    return boxes

def mode_in(b, pred):
    c = Counter()
    for y in range(b[1],b[3]+1):
        for x in range(b[0],b[2]+1):
            p=px[x,y]
            if pred(p): c[p]+=1
    return c.most_common(2)

lav = lambda p: 175<p[0]<215 and 165<p[1]<205 and 195<p[2]<235
yel = lambda p: p[0]>235 and p[1]>235 and 165<p[2]<215
pnk = lambda p: 210<p[0]<248 and 180<p[1]<220 and 200<p[2]<240
sft = lambda p: 150<p[0]<205 and 200<p[1]<245 and 150<p[2]<200
wht = lambda p: p[0]>242 and p[1]>242 and p[2]>238
mauve = lambda p: 170<p[0]<210 and 125<p[1]<170 and 155<p[2]<200
shadow = lambda p: 210<p[0]<245 and 210<p[1]<245 and 210<p[2]<245

# LEFT inset boxes
for name, pred, win in [
    ("L_lav", lav, (60,270,200,330)),
    ("L_softmax", sft, (60,300,200,350)),
    ("L_pink", pnk, (60,340,200,385)),
    ("L_yellow", yel, (60,375,200,415)),
    ("L_lav2", lav, (60,400,200,460)),
]:
    bs = boxes_for(pred, *win)
    out[name] = {"slide": [S(b) for b in bs], "mode": [list(m) for m,_ in mode_in(bs[0], pred)] if bs else None}

# LEFT circles: red + blue clusters
redp  = lambda p: p[0]>120 and (p[0]-p[1])>60 and (p[0]-p[2])>60
bluep = lambda p: p[2]>110 and (p[2]-p[1])>55 and (p[2]-p[0])>55
for nm, pred in [("L_red",redp), ("L_blue",bluep)]:
    bs = boxes_for(pred, 60,445,200,500, min_run=4, min_rows=4, join=2)
    out[nm] = {"slide": [S(b) for b in bs]}

# LEFT arrows/bypass (black ink columns inside frame)
dark = lambda p: p[0]<85 and p[1]<85 and p[2]<85
cols = Counter()
for y in range(270,470):
    for x in range(60,200):
        if dark(px[x,y]): cols[x]+=1
out["L_dark_tall_cols_frame"] = sorted([(x,c) for x,c in cols.items() if c>=30])
out["L_dark_tall_cols_slide"] = [(round((x-AX)/SX,1),c) for x,c in out["L_dark_tall_cols_frame"]]

# LEFT header lines (red ink rows already known: 225-235, 243-253 frame) -> bboxes per line
redm = lambda p: p[0]>110 and (p[0]-p[1])>55 and (p[0]-p[2])>55
for nm,(y0,y1) in [("L_hdr_line1",(222,238)),("L_hdr_line2",(240,257))]:
    xs=[];ys=[]
    for y in range(y0,y1):
        for x in range(50,215):
            if redm(px[x,y]): xs.append(x);ys.append(y)
    if xs: out[nm] = {"slide": S((min(xs),min(ys),max(xs),max(ys)))}

# CENTER inset boxes
for name, pred, win in [
    ("C_shadow_top", shadow, (290,250,520,290)),
    ("C_concat", yel, (290,295,520,335)),
    ("C_mauve", mauve, (290,335,520,405)),
    ("C_linear_row", wht, (290,395,480,430)),
    ("C_shadows_lin", shadow, (290,385,520,430)),
]:
    bs = boxes_for(pred, *win)
    out[name] = {"slide": [S(b) for b in bs[:6]], "mode": [list(m) for m,_ in mode_in(bs[0], pred)] if bs else None}

# CENTER circles
for nm, pred in [("C_red",redp), ("C_blue",bluep)]:
    bs = boxes_for(pred, 290,470,480,520, min_run=4, min_rows=4, join=2)
    out[nm] = {"slide": [S(b) for b in bs]}

# CENTER header line bbox
xs=[];ys=[]
for y in range(205,235):
    for x in range(285,530):
        if redm(px[x,y]): xs.append(x);ys.append(y)
out["C_hdr"] = {"slide": S((min(xs),min(ys),max(xs),max(ys)))} if xs else None

# center arrows (dark cols)
cols = Counter()
for y in range(250,470):
    for x in range(300,520):
        if dark(px[x,y]): cols[x]+=1
out["C_dark_tall_cols_frame"] = sorted([(x,c) for x,c in cols.items() if c>=30])
out["C_dark_tall_cols_slide"] = [(round((x-AX)/SX,1),c) for x,c in out["C_dark_tall_cols_frame"]]

print(json.dumps(out, indent=1, default=str))
