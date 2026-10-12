#!/usr/bin/env python3
# probe3.py — slide 024 follow-up measurements (crops raised these questions).
# Frame: videos/deep-learning/001_introduction/unique_slides/slide_024.jpg 960x540, 1px=1pt.
import numpy as np
from PIL import Image

im = np.array(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_024.jpg').convert('RGB')).astype(int)
H, W, _ = im.shape
def px(x, y): return tuple(im[y, x])
def hexc(c): return '#%02X%02X%02X' % c

print('== 1. PANEL FILL clean samples ==')
for (x, y) in [(120,165),(300,160),(450,155),(620,160),(760,170),(100,400),(300,405),(700,405),(340,320),(520,330)]:
    print(f'  ({x},{y}):', hexc(px(x,y)))
# modal color of clean top strip
strip = im[148:185, 70:790].reshape(-1,3)
from collections import Counter
cnt = Counter(map(tuple, strip))
print('  modal top-strip:', ['%s x%d' % (hexc(c), n) for c, n in cnt.most_common(3)])

print('== 2. SLIDE BORDERS ==')
for (x, y) in [(43,140),(43,300),(43,450),(917,300),(917,450),(480,44),(480,46),(42,60)]:
    print(f'  ({x},{y}):', hexc(px(x,y)))
print('  x-scan y300 x36..52:', [hexc(px(x,300)) for x in range(36,53)])
print('  x-scan y300 x910..926:', [hexc(px(x,300)) for x in range(910,926)])

print('== 3. BLACK BOTTOM BAR ==')
for y in (527, 529, 531, 535, 539):
    row = im[y]
    dark = np.where(row.sum(axis=1) < 150)[0]
    print(f'  y{y}: black x {dark.min() if len(dark) else "-"}..{dark.max() if len(dark) else "-"} n={len(dark)}')

print('== 4. ERROR BAR text core (brightest in bar) ==')
bar = im[190:390, 800:815]
lum = bar.sum(axis=2)
yy, xx = np.unravel_index(np.argsort(lum.ravel())[-30:], lum.shape)
print('  brightest:', Counter(hexc(tuple(bar[yy[i], xx[i]])) for i in range(30)).most_common(3))
print('  bar fill modal:', Counter(map(tuple, bar.reshape(-1,3))).most_common(2))

print('== 5. RINGS (dark ink clusters) ==')
def rings(x0, x1, label):
    for ylo, yhi, yc in [(203,222,212),(276,295,285),(358,377,367)]:
        band = im[ylo:yhi, x0:x1]
        dark = (band.sum(axis=2) < 480)
        cols = np.where(dark.any(axis=0))[0]
        if len(cols):
            # cluster columns with gap>2
            groups, cur = [], [cols[0]]
            for c in cols[1:]:
                if c - cur[-1] <= 2: cur.append(c)
                else: groups.append(cur); cur=[c]
            groups.append(cur)
            centers = [x0 + (g[0]+g[-1])/2 for g in groups]
            print(f'  {label} row yc={yc}: col-groups={[(x0+g[0], x0+g[-1]) for g in groups]} centers={[round(c,1) for c in centers]}')
        else:
            print(f'  {label} row yc={yc}: none')
        # darkest sample
        if len(cols):
            dk = band.sum(axis=2).argmin()
            yy2, xx2 = np.unravel_index(dk, band.sum(axis=2).shape)
            print(f'    darkest: {hexc(tuple(band[yy2, xx2]))}')
rings(185, 242, 'after-col1')
rings(600, 655, 'before-col5')

print('== 6. NEURON BBOXES via fill masks ==')
def bbox_of(mask, x0, x1, y0, y1, label):
    sub = mask[y0:y1, x0:x1]
    ys, xs = np.where(sub)
    if len(xs) == 0: print(f'  {label}: EMPTY'); return None
    r = (x0+xs.min(), x0+xs.max(), y0+ys.min(), y0+ys.max())
    print(f'  {label}: x{r[0]}..{r[1]} y{r[2]}..{r[3]} (w={r[1]-r[0]+1} h={r[3]-r[2]+1} cx={(r[0]+r[1])/2} cy={(r[2]+r[3])/2})')
    return r
R, G, B = im[:,:,0], im[:,:,1], im[:,:,2]
blue = (B > R + 12) & (B > 200) & (R > 150)
green = (G > R + 25) & (G > B + 40) & (G > 190)
orange = (R > B + 60) & (G > B + 30) & (R > 200)
whiteish = (R > 240) & (G > 235) & (B > 230)
for rowi, (y0, y1, yc) in enumerate([(185,245,212),(258,318,285),(340,400,367)]):
    bbox_of(blue, 225, 300, y0, y1, f'col2 r{rowi+1}')
    bbox_of(green, 395, 460, y0, y1, f'col3 r{rowi+1}')
    bbox_of(orange, 555, 620, y0, y1, f'col4 r{rowi+1}')
    bbox_of(whiteish, 645, 700, y0, y1, f'col5 r{rowi+1}')
print('  col1 border zone (dark<170) r1:')
sub = (im[195:232, 135:195].sum(axis=2) < 510)
ys, xs = np.where(sub)
if len(xs): print(f'    ink x{135+xs.min()}..{135+xs.max()} y{195+ys.min()}..{195+ys.max()}')
print('  col1 fill sample (160,212):', hexc(px(160,212)), ' (155,205):', hexc(px(155,205)))
print('  col2 fill core (245,205):', hexc(px(245,205)), 'border sample (267,212):', hexc(px(267,212)))
print('  col3 fill (420,200):', hexc(px(420,200)), 'border (406,212):', hexc(px(406,212)))
print('  col4 fill (580,200):', hexc(px(580,200)), 'border (566,212):', hexc(px(566,212)))
print('  col5 fill (665,205):', hexc(px(665,205)), 'border (653,212):', hexc(px(653,212)))

print('== 7. MESH LINES ==')
print('  horizontal r1->r1 y212 x350..400 reddest:', )
seg = im[208:216, 350:400].reshape(-1,3)
reds = [tuple(p) for p in seg if p[0] > 120 and p[0] > p[1] + 40 and p[0] > p[2] + 40]
print('   red px:', Counter(hexc(c) for c in reds).most_common(4), 'n=', len(reds))
def linecount(y, x0, x1, label):
    row = im[y, x0:x1]
    isred = (row[:,0] > 110) & (row[:,0] > row[:,1] + 35) & (row[:,0] > row[:,2] + 35)
    runs, cur = [], None
    for i, v in enumerate(isred):
        if v and cur is None: cur = i
        if not v and cur is not None: runs.append((x0+cur, x0+i-1)); cur = None
    if cur is not None: runs.append((x0+cur, x0+len(isred)-1))
    print(f'  {label} y={y}: {len(runs)} red runs {runs}')
linecount(250, 300, 395, 'col2-3 gap')
linecount(250, 450, 560, 'col3-4 gap')
linecount(250, 275, 395, 'col2-3 gap tight')

print('== 8. OUTPUT BOXES + red arrows ==')
for rowi, (y0, y1, yc) in enumerate([(172,248,212),(252,320,285),(332,400,367)]):
    sub = im[y0:y1, 705:812]
    dark = sub.sum(axis=2) < 420
    ys, xs = np.where(dark)
    if len(xs):
        print(f'  outbox r{rowi+1}: dark ink x{705+xs.min()}..{705+xs.max()} y{y0+ys.min()}..{y0+ys.max()}')
    # border ring modal dark
    ring = [tuple(p) for p in sub[dark]]
    print(f'    dark modal:', Counter(hexc(c) for c in ring).most_common(3))
    fill = [tuple(p) for p in sub[~dark]]
    print(f'    fill modal:', Counter(hexc(c) for c in fill).most_common(2))
    # red arrow between col5 and box
    seg = im[y0:y1, 683:715]
    isred = (seg[:,:,0] > 110) & (seg[:,:,0] > seg[:,:,1] + 35) & (seg[:,:,0] > seg[:,:,2] + 35)
    ys, xs = np.where(isred)
    if len(xs): print(f'    red arrow x{683+xs.min()}..{683+xs.max()} y{y0+ys.min()}..{y0+ys.max()} n={len(xs)}')

print('== 9. CLASS BOXES ==')
lightgreen = (G > 220) & (R > 180) & (R < 240) & (B < 230) & (G > R + 15) & (G > B + 15)
for rowi, (y0, y1) in enumerate([(195,235),(268,308),(350,390)]):
    bbox_of(lightgreen, 812, 905, y0, y1, f'class r{rowi+1}')
sub = im[203:222, 820:895]
dark = sub.sum(axis=2) < 330
print('  class border/modal dark:', Counter(hexc(tuple(p)) for p in sub[dark]).most_common(3))

print('== 10. CALLOUTS + ARROWS ==')
for name, (x0, x1, y0, y1) in [('prev',(214,315,424,467)),('cur',(378,477,424,467)),('nxt',(553,634,424,467))]:
    sub = im[y0:y1, x0:x1]
    dk = sub.sum(axis=2) < 480
    ys, xs = np.where(dk)
    if len(xs): print(f'  {name}: ink x{x0+xs.min()}..{x0+xs.max()} y{y0+ys.min()}..{y0+ys.max()} border-modal', Counter(hexc(tuple(p)) for p in sub[dk]).most_common(2))
    fl = [tuple(p) for p in sub[(sub[:,:,0]>200)&(sub[:,:,1]>200)]]
    print(f'    fill modal:', Counter(hexc(c) for c in fl).most_common(2))
for name, (x0, x1, y0, y1) in [('arrow_i',(232,300,383,437)),('arrow_j',(398,462,383,437)),('arrow_k',(558,622,383,437))]:
    sub = im[y0:y1, x0:x1]
    dk = sub.sum(axis=2) < 560
    ys, xs = np.where(dk)
    if len(xs):
        print(f'  {name}: ink x{x0+xs.min()}..{x0+xs.max()} y{y0+ys.min()}..{y0+ys.max()} edge-modal', Counter(hexc(tuple(p)) for p in sub[dk]).most_common(3))
    fl = [tuple(p) for p in sub[(sub.sum(axis=2) > 640)]]
    print(f'    bright fill:', Counter(hexc(c) for c in fl).most_common(2))
    # solid tip: saturated colored pixels top 12 rows
    tip = sub[0:12]
    sat = [tuple(p) for p in tip.reshape(-1,3) if abs(p[0]-p[1]) > 25 or abs(p[1]-p[2]) > 25]
    print(f'    tip colored modal:', Counter(hexc(c) for c in sat).most_common(3))

print('== 11. MAGENTA BOXES + dashed line ==')
mag = (R > 180) & (B > 180) & (G < 170)
bbox_of(mag, 50, 145, 100, 175, 'InputSamples fill')
bbox_of(mag, 810, 900, 100, 175, 'SampleLabel fill')
sub = im[110:170, 55:140]
dk = sub.sum(axis=2) < 400
print('  IS border modal:', Counter(hexc(tuple(p)) for p in sub[dk]).most_common(3))
# arrowhead left of dashes x128..150 y135..148
seg = im[132:150, 126:152]
isred = (seg[:,:,0] > 130) & (seg[:,:,0] > seg[:,:,1] + 40)
ys, xs = np.where(isred)
if len(xs): print('  left arrowhead: x%d..%d y%d..%d n=%d' % (126+xs.min(), 126+xs.max(), 132+ys.min(), 132+ys.max(), len(xs)))
seg = im[132:150, 806:824]
isred = (seg[:,:,0] > 130) & (seg[:,:,0] > seg[:,:,1] + 40)
ys, xs = np.where(isred)
if len(xs): print('  right end ink: x%d..%d y%d..%d n=%d' % (806+xs.min(), 806+xs.max(), 132+ys.min(), 132+ys.max(), len(xs)))
# dash pattern at y141
row = im[141, 150:820]
isl = (row[:,0] > 110) & (row[:,0] > row[:,1] + 30)
runs, cur, on = [], None, False
segs_on, segs_off, last = [], [], None
xs_on = np.where(isl)[0]
if len(xs_on):
    gaps = np.diff(xs_on)
    print('  dash: n_ink=%d span=%d..%d  on-len modal=%s gap modal=%s' % (
        len(xs_on), 150+xs_on.min(), 150+xs_on.max(),
        Counter(np.diff(xs_on)[gaps < 8] - 1).most_common(2),
        Counter(gaps[(gaps >= 3) & (gaps < 12)] - 1).most_common(2)))
print('  dash color modal:', Counter(hexc(tuple(im[141, 150+x])) for x in xs_on[:200]).most_common(3))

print('== 12. TITLE color ==')
sub = im[60:95, 320:650]
redm = (sub[:,:,0] > 100) & (sub[:,:,0] > sub[:,:,1] + 50)
print('  title red modal:', Counter(hexc(tuple(p)) for p in sub[redm]).most_common(4))

print('== 13. FAN LINES crossings ==')
for xq in (92, 110, 130):
    col = im[195:380, xq]
    isln = (col.sum(axis=1) < 660) & (col.sum(axis=1) > 450)
    runs = np.where(isln)[0]
    if len(runs):
        groups, cur = [], [runs[0]]
        for r in runs[1:]:
            if r - cur[-1] <= 1: cur.append(r)
            else: groups.append(cur); cur = [r]
        groups.append(cur)
        print(f'  x={xq}: {len(groups)} line crossings at y={[195+int(np.mean(g)) for g in groups]}')

print('== 14. LABEL COLORS ==')
sub = im[195:212, 320:352]
bl = (sub[:,:,2] > 110) & (sub[:,:,2] > sub[:,:,0] + 60)
print('  w label blue modal:', Counter(hexc(tuple(p)) for p in sub[bl]).most_common(3))
sub = im[172:184, 203:233]
rd = (sub[:,:,0] > 110) & (sub[:,:,0] > sub[:,:,1] + 50)
print('  Net label red modal:', Counter(hexc(tuple(p)) for p in sub[rd]).most_common(3))
sub = im[192:215, 280:300]
rd = (sub[:,:,0] > 110) & (sub[:,:,0] > sub[:,:,1] + 50)
print('  O label red modal:', Counter(hexc(tuple(p)) for p in sub[rd]).most_common(3))

print('== 15. PORT DOTS at line endpoints ==')
for name, (x0, x1, y0, y1) in [('col2R r1',(262,275,205,220)),('col3L r1',(398,412,205,220)),('col3R r1',(438,452,205,220)),('col4L r1',(558,572,205,220))]:
    seg = im[y0:y1, x0:x1]
    isred = (seg[:,:,0] > 120) & (seg[:,:,0] > seg[:,:,1] + 40) & (seg[:,:,0] > seg[:,:,2] + 40)
    ys, xs = np.where(isred)
    if len(xs):
        print(f'  {name}: x{x0+xs.min()}..{x0+xs.max()} y{y0+ys.min()}..{y0+ys.max()} n={len(xs)} core', Counter(hexc(tuple(p)) for p in seg[isred]).most_common(2))
    else:
        print(f'  {name}: none')

print('== 16. NEURON INTERNALS col3r1 ==')
sub = im[195:230, 405:445]
print('  darkest px:', hexc(tuple(sub.reshape(-1,3)[sub.sum(axis=2).argmin()])))
# divider at x~425: scan y200..225 x423..427
print('  divider zone (425,210):', hexc(px(425,210)), '(426,210):', hexc(px(426,210)), '(424,210):', hexc(px(424,210)))
# sigma red: left half
lh = im[200:228, 406:424]
isred = (lh[:,:,0] > 120) & (lh[:,:,0] > lh[:,:,1] + 50)
if isred.any(): print('  Sigma red modal:', Counter(hexc(tuple(p)) for p in lh[isred]).most_common(2))
