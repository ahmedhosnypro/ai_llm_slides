#!/usr/bin/env python3
"""Stage 7: final measurement pass — everything needed for the build, frame px + slide pt.
Mapping: slide_x = (frame_x-18.63)/0.96123 ; slide_y = frame_y/0.95556  (certified, 002/039)."""
import numpy as np
from PIL import Image

im = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_040.jpg')).astype(int)
r, g, b = im[:,:,0], im[:,:,1], im[:,:,2]

def S(fx, fy):
    return ((fx-18.63)/0.96123, fy/0.95556)
def SR(fx0, fx1, fy0, fy1):
    x0, y0 = S(fx0, fy0); x1, y1 = S(fx1, fy1)
    return f"slide x {x0:.1f}..{x1:.1f} (w {x1-x0:.1f})  y {y0:.1f}..{y1:.1f} (h {y1-y0:.1f})"

lum = (r+g+b)/3.0
mx = np.maximum(np.maximum(r,g),b); mn = np.minimum(np.minimum(r,g),b)
sat = mx-mn
dark = lum < 140

# ---------- per-line color runs in intro paragraph ----------
print('== INTRO PARAGRAPH RUNS ==')
bands = [(117,134,'L1'), (142,159,'L2'), (167,181,'L3')]
classes = {
    'blue':   (np.abs(r-34)<70) & (np.abs(g-34)<70) & (b>120) & (b-r>60),
    'green':  (g>110) & (g-r>40) & (g-b>40),
    'red':    (r>130) & (r-g>60) & (r-b>60),
    'black':  dark,
}
for (y0,y1,name) in bands:
    prof = np.zeros(im.shape[1], bool)
    for cls, m in classes.items():
        mm = np.zeros_like(m); mm[y0:y1+1, 95:888] = m[y0:y1+1, 95:888]
        prof |= mm.any(axis=0)
    cols = np.where(prof)[0]
    # split into runs separated by >=6 white cols
    runs, start, prev = [], cols[0], cols[0]
    for c in cols[1:]:
        if c-prev >= 6: runs.append((start,prev)); start=c
        prev=c
    runs.append((start,prev))
    print(f'{name} y{y0}..{y1}:')
    for (xa,xb) in runs:
        # dominant class in run
        votes = {}
        for cls, m in classes.items():
            mm = np.zeros_like(m); mm[y0:y1+1, xa:xb+1] = m[y0:y1+1, xa:xb+1]
            votes[cls] = int(mm.sum())
        dom = max(votes, key=votes.get)
        # mean core color of non-white pixels
        sel = (sat[y0:y1+1, xa:xb+1] > 40) | (dark[y0:y1+1, xa:xb+1])
        if sel.sum() > 3:
            mr = np.median(r[y0:y1+1, xa:xb+1][sel]); mg = np.median(g[y0:y1+1, xa:xb+1][sel]); mb = np.median(b[y0:y1+1, xa:xb+1][sel])
            cc = f'#{int(mr):02X}{int(mg):02X}{int(mb):02X}'
        else: cc='?'
        print(f'   x {xa}..{xb}  dom={dom} {votes} core={cc}  | {SR(xa,xb,y0,y1)}')

# ---------- title color + metrics ----------
print('== TITLE ==')
ys, xs = np.where((r>130)&(g<90)&(b<90))
tm = (ys>=60)&(ys<=95)&(xs>=200)&(xs<=750)
print('title red bbox frame:', xs[tm].min(), xs[tm].max(), ys[tm].min(), ys[tm].max(), '|', SR(xs[tm].min(), xs[tm].max(), ys[tm].min(), ys[tm].max()))
core = tm & (r[ys, xs]>150)&(g[ys, xs]<60)
print('title core median RGB:', np.median(r[ys[core], xs[core]]), np.median(g[ys[core], xs[core]]), np.median(b[ys[core], xs[core]]))

# ---------- highlight rects (solid rows) ----------
print('== HIGHLIGHT SOLID RECTS ==')
def fill_rect(mask, x0,x1,y0,y1, minrowfrac=0.5):
    mm = np.zeros_like(mask); mm[y0:y1, x0:x1] = mask[y0:y1, x0:x1]
    rows = mm.sum(axis=1); width = x1-x0
    solid = [y0+i for i,v in enumerate(rows) if v > minrowfrac*width]
    if not solid: return None
    ra, rb = solid[0], solid[-1]
    colsum = mm[ra:rb+1].sum(axis=0)
    cols = np.where(colsum > (rb-ra+1)*0.5)[0]
    return (int(cols.min()), int(cols.max()), ra, rb)

greenm  = (np.abs(r-0x90)<50)&(np.abs(g-0xEE)<40)&(np.abs(b-0x90)<50)&(g-r>30)&(g-b>30)
lavm    = (np.abs(r-0xA9)<40)&(np.abs(g-0xA6)<40)&(np.abs(b-0xE2)<40)&(b-r>30)
pinkm   = (r>215)&(np.abs(g-0xA9)<45)&(np.abs(b-0xAF)<45)&(r-g>50)
orangm  = (r>215)&(g>140)&(g<215)&(b<160)&(r-b>60)
for name, m, box in [
    ('green params line', greenm, (150,540,222,255)),
    ('lav mu_B eq1',      lavm,   (150,220,295,335)),
    ('lav sig_B eq2',     lavm,   (150,220,352,392)),
    ('lav mu_B eq3num',   lavm,   (230,320,392,428)),
    ('lav sig_B eq3den',  lavm,   (210,320,424,452)),
    ('pink xhat eq3',     pinkm,  (150,215,402,440)),
    ('pink //normalize',  pinkm,  (430,560,402,440)),
    ('orange //scale',    orangm, (400,560,445,482)),
]:
    rr = fill_rect(m, *box)
    print(f'{name}: frame {rr}' + ('' if rr is None else '  | '+SR(rr[0],rr[1],rr[2],rr[3])))

# ---------- equation dark bands + comment extents ----------
print('== EQ ROWS (dark ink) ==')
for (y0,y1,name) in [(285,335,'eq1'),(338,392,'eq2'),(392,449,'eq3'),(449,482,'eq4')]:
    dd = np.zeros_like(dark); dd[y0:y1, 148:552] = dark[y0:y1, 148:552]
    ys2, xs2 = np.where(dd)
    if len(xs2)==0: continue
    # comment = ink right of x 390
    cm = np.zeros_like(dark); cm[y0:y1, 390:552] = dark[y0:y1, 390:552]
    cys, cxs = np.where(cm)
    cinfo = f'comment x {cxs.min()}..{cxs.max()} y {cys.min()}..{cys.max()}' if len(cxs) else 'no comment ink'
    print(f'{name}: ink x {xs2.min()}..{xs2.max()} y {ys2.min()}..{ys2.max()} | {cinfo}')
    print(f'    | {SR(xs2.min(), xs2.max(), ys2.min(), ys2.max())}')

# ---------- fraction bar of eq3 + radical ----------
print('== EQ3 BAR ==')
for y in range(415, 430):
    row = dark[y, 230:340]
    if row.sum() > 50: print(f'  bar row y={y} run x 230+{np.where(row)[0].min()}..230+{np.where(row)[0].max()} n={row.sum()}')

# ---------- ellipse around y_i (eq4) ----------
print('== EQ4 ELLIPSE ==')
om = orangm & (np.arange(im.shape[0])[:,None]>=445) & (np.arange(im.shape[0])[:,None]<=482) & (np.arange(im.shape[1])[None,:]>=155) & (np.arange(im.shape[1])[None,:]<=205)
ys3, xs3 = np.where(om)
print(f'ellipse orange bbox frame x {xs3.min()}..{xs3.max()} y {ys3.min()}..{ys3.max()} n={len(xs3)} | '+SR(xs3.min(),xs3.max(),ys3.min(),ys3.max()))

# ---------- header lines ----------
print('== HEADER ==')
for (y0,y1,name) in [(208,231,'Input'),(231,252,'Params'),(252,275,'Output')]:
    dd = np.zeros_like(dark); dd[y0:y1, 148:552] = dark[y0:y1, 148:552]
    ys2, xs2 = np.where(dd)
    print(f'{name}: ink x {xs2.min()}..{xs2.max()} y {ys2.min()}..{ys2.max()} | '+SR(xs2.min(),xs2.max(),ys2.min(),ys2.max()))

# ---------- panel + intro box + letterbox ----------
print('== BOXES ==')
print('intro box frame 88..892 x 104..185 |', SR(88,892,104,185))
print('panel frame 145..552 x 204..497  |', SR(145,552,204,497))
print('letterbox rows 519..539 -> slide y >=', 519/0.95556)
