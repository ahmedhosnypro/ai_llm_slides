#!/usr/bin/env python3
"""Right panel: structured box detection via fill-run merging, on ORIGINAL frame.
Reports slide-space boxes (x0,y0,x1,y1) per fill family + exact mode colors."""
from PIL import Image
from collections import Counter
import json

img = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_037.jpg").convert("RGB")
px = img.load()
AX, SX = 17.101, 0.962329
BY, SY = -0.224, 0.96053
def S(v): return [round((v[0]-AX)/SX,1), round((v[1]-BY)/SY,1), round((v[2]-AX)/SX,1), round((v[3]-BY)/SY,1)]
out = {}

FAMILIES = {
  # name: (pred, search window x0,y0,x1,y1, min_run, min_rows)
  "peach_panel":  (lambda p: 245<p[0]<256 and 220<p[1]<242 and 208<p[2]<228, 530,95,960,519, 30, 8),
  "green_panel":  (lambda p: 195<p[0]<215 and 245<p[1]<256 and 210<p[2]<232, 530,95,960,519, 30, 8),
  "brown_box":    (lambda p: 150<p[0]<190 and 100<p[1]<145 and 60<p[2]<100, 530,95,960,519, 12, 4),
  "darkbrown":    (lambda p: 130<p[0]<175 and 95<p[1]<130 and 50<p[2]<85, 530,95,960,519, 10, 3),
  "olive_dark":   (lambda p: 120<p[0]<160 and 105<p[1]<140 and 50<p[2]<85, 530,95,960,519, 12, 4),
  "purplepink":   (lambda p: 195<p[0]<230 and 110<p[1]<150 and 180<p[2]<215, 700,300,960,450, 12, 3),
  "salmon":       (lambda p: 190<p[0]<215 and 115<p[1]<140 and 75<p[2]<100, 600,330,760,420, 10, 3),
  "indigo":       (lambda p: 85<p[0]<125 and 105<p[1]<145 and 190<p[2]<235, 730,320,860,360, 8, 2),
  "maroon":       (lambda p: 160<p[0]<200 and 85<p[1]<125 and 85<p[2]<125, 730,395,870,470, 10, 3),
  "yellow_box":   (lambda p: 230<p[0]<256 and 235<p[1]<256 and 20<p[2]<90, 530,95,960,519, 8, 2),
  "red_solid":    (lambda p: 150<p[0]<230 and p[1]<60 and p[2]<60, 530,95,960,519, 6, 2),
  "blue_circ":    (lambda p: p[2]>140 and (p[2]-p[1])>70 and p[0]<90, 530,95,960,519, 4, 2),
  "green_soft":   (lambda p: 150<p[0]<200 and 200<p[1]<245 and 150<p[2]<200, 700,120,900,200, 10, 3),
  "gray_nx":      (lambda p: 165<p[0]<200 and 165<p[1]<200 and 130<p[2]<170, 820,280,900,340, 6, 2),
}

def boxes_for(pred, x0,y0,x1,y1, min_run, min_rows):
    # rows -> horizontal runs of pred
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
    # merge vertically overlapping runs with horizontal overlap
    used=set(); boxes=[]
    ys = sorted(rowruns)
    for y in ys:
        if y in used: continue
        # BFS merge
        stack=[(y,rowruns[y])]; comp_rows=[y]; seen={y}
        allruns=list(rowruns[y])
        while stack:
            cy, cr = stack.pop()
            for ny in (cy-1, cy+1):
                if ny in rowruns and ny not in seen and abs(ny-cy)<=2:
                    # require horizontal overlap
                    if any(not(r2[1]<r[0]-6 or r2[0]>r[1]+6) for r2 in rowruns[ny] for r in cr):
                        seen.add(ny); comp_rows.append(ny)
                        stack.append((ny,rowruns[ny])); allruns.extend(rowruns[ny])
        for r in comp_rows: used.add(r)
        if len(comp_rows)>=min_rows:
            bx0=min(r[0] for r in allruns); bx1=max(r[1] for r in allruns)
            by0=min(comp_rows); by1=max(comp_rows)
            boxes.append((bx0,by0,bx1,by1))
    return boxes

for name,(pred,x0,y0,x1,y1,mr,mrows) in FAMILIES.items():
    bs = boxes_for(pred,x0,y0,x1,y1,mr,mrows)
    bs.sort(key=lambda b:(b[1],b[0]))
    # mode color inside the biggest box
    modes=[]
    for b in bs[:14]:
        c=Counter()
        for y in range(b[1],b[3]+1):
            for x in range(b[0],b[2]+1):
                p=px[x,y]
                if pred(p): c[p]+=1
        modes.append(c.most_common(1)[0][0] if c else None)
    out[name] = {"frame_boxes": bs[:14], "slide_boxes": [S(b) for b in bs[:14]], "modes": [list(m) if m else None for m in modes]}
print(json.dumps(out, indent=1, default=str))
