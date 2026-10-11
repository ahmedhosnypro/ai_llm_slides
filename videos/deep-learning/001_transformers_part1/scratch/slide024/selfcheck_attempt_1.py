# Self-check A: geometry forensics of the 150dpi render vs the original frame.
# 150dpi render: 2000x1125 -> scale vs 960x540 frame = 2000/960 = 2.0833
from PIL import Image
import numpy as np
import math
import sys

ren = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/scratch/slide024/render/slide-1.png').convert('RGB')
print('render size', ren.size)
S = ren.size[0] / 960.0
a = np.asarray(ren).astype(int)
r, g, b = a[..., 0], a[..., 1], a[..., 2]

fail = []
def check(name, cond, detail):
    print(('PASS ' if cond else 'FAIL ') + name + '  ' + detail)
    if not cond: fail.append(name)

# ---- 1. chrome already checked (house_chrome_check PASS) ----

# ---- 2. node positions/sizes in render vs original (tolerance 6 frame-px) ----
NODES = {'in': (202.5,143.5,92,'FEFFE5'), 'garden': (359.5,163,92,'FEFFE5'), 'the': (119,294.5,93,'FEFFE5'),
         'Boy': (268,288,97,'D5FFAF'), 'tree': (432,366,95,'FEFFE5'), 'climbs': (253,449.5,92,'FEFFE5'),
         'Boy_out': (743,290.5,100,'D5FFAF'), 'Boy_in2': (607.5,445,97,'D5FFAF')}
for name,(cx,cy,d,col) in NODES.items():
    rr,gg,bb = int(col[0:2],16), int(col[2:4],16), int(col[4:6],16)
    m = (np.abs(r-rr)<14)&(np.abs(g-gg)<14)&(np.abs(b-bb)<16)
    x0,x1v = int((cx-d/2-8)*S), int((cx+d/2+8)*S)
    y0,y1v = int((cy-d/2-8)*S), int((cy+d/2+8)*S)
    sub = m[y0:y1v, x0:x1v]
    ys,xs = np.nonzero(sub)
    if len(xs)<50:
        check(f'node {name} ink', False, f'only {len(xs)} px'); continue
    mcx, mcy = (xs.mean()+x0)/S, (ys.mean()+y0)/S
    # mean-of-fill approximates circle center (label pixels knocked out symmetrically)
    dev = math.hypot(mcx-cx, mcy-cy)
    check(f'node {name} center', dev <= 6, f'measured ctr=({mcx:.0f},{mcy:.0f}) vs ({cx},{cy}) dev={dev:.1f}fpx n={len(xs)}')

# ---- 3. big circle: pale-cyan ring present; center/radius (restrict x<500 to exclude
#         the same-fill sentence box) ----
m = (np.abs(r-0xEE)<10)&(np.abs(g-0xFE)<8)&(np.abs(b-0xFB)<8)
m[:, int(500*S):] = False
ys,xs = np.nonzero(m)
check('circle fill present', len(xs)>300000, f'n={len(xs)}')
if len(xs)>1000:
    bx0,bx1,by0,by1 = xs.min()/S, xs.max()/S, ys.min()/S, ys.max()/S
    mcx,mcy = (bx0+bx1)/2, (by0+by1)/2
    check('circle fill center', math.hypot(mcx-278,mcy-291)<=8, f'({mcx:.0f},{mcy:.0f}) vs (278,291)')
    rad = ((bx1-bx0)+(by1-by0))/4
    check('circle radius', abs(rad-234.5)<=10, f'r={rad:.0f} vs 234.5 (bbox incl border)')

# ---- 4. edges: red ink along measured lines (loose red on render) ----
red = (r>140)&(g<120)&(b<120)
def cov(x1,y1,x2,y2,halfw_frame=4):
    n=60; hits=0
    dx,dy=x2-x1,y2-y1; L=math.hypot(dx,dy); pxx,pyy=-dy/L,dx/L
    for i in range(n+1):
        t=i/n; x,y=(x1+dx*t)*S,(y1+dy*t)*S
        xi,yi=int(round(x)),int(round(y))
        w=int(halfw_frame*S)
        if red[max(0,yi-w):yi+w+1, max(0,xi-w):xi+w+1].any(): hits+=1
    return hits/(n+1)
EDGES = [('in-garden',230,108,329,131),('in-the',203,192,156,255),('the-garden',306,164,155,256),
         ('the-Boy',167,292,216,291),('the-tree',158,330,389,396),('Boy-garden',306,258,326,190),
         ('Boy-tree',318,290,386,364),('Boy-climbs',264,336,258,403),('garden-tree',391,197,431,318)]
for name,x1,y1,x2,y2 in EDGES:
    c = cov(x1,y1,x2,y2)
    check(f'edge {name} ink', c>=0.75, f'coverage={c:.2f}')
# dashed mapping link
c = cov(657,502,789,383)
check('dashed link ink', c>=0.4, f'dash coverage={c:.2f} (dashes lower bound)')

# ---- 5. block arrow: hatch + outline ink in region ----
sub = red[int(281*S):int(316*S), int(518*S):int(681*S)]
check('block arrow outline ink', sub.sum()>2000, f'n={int(sub.sum())}')

# ---- 6. sentence box + text ink ----
blk = (r<80)&(g<80)&(b<80)
sub = blk[int(112*S):int(140*S), int(500*S):int(880*S)]
ys,xs = np.nonzero(sub)
check('sentence text ink', len(xs)>300, f'n={len(xs)}')
if len(xs)>50:
    tx0,tx1 = (xs.min()+int(500*S))/S, (xs.max()+int(500*S))/S
    check('sentence text span', abs(tx0-521)<=14 and abs(tx1-851)<=14, f'x[{tx0:.0f},{tx1:.0f}] vs [521,851]')

# ---- 7. title ink ----
sub = blk[int(55*S):int(95*S), int(400*S):int(790*S)]
ys,xs = np.nonzero(sub)
check('title ink', len(xs)>500, f'n={len(xs)}')
if len(xs)>50:
    tx0,tx1 = (xs.min()+int(400*S))/S, (xs.max()+int(400*S))/S
    ty0,ty1 = (ys.min()+int(55*S))/S, (ys.max()+int(55*S))/S
    check('title span', abs((tx0+tx1)/2-590)<=10 and abs((ty0+ty1)/2-72)<=8, f'x[{tx0:.0f},{tx1:.0f}] y[{ty0:.0f},{ty1:.0f}] vs x[414,766] y[60,86]')

# ---- 8. vector icons: blue outline ink at 5 left positions + orange icon ----
blue = (b>140)&(b-r>60)&(g<170)
for name, cx, cy in [('in-icon',137,172),('the-icon',96.5,372),('Boy-icon',321,341),('climbs-icon',321,476),('tree-icon',393.5,436),('in2-icon',642,497)]:
    x0,y0 = int((cx-18)*S), int((cy-32)*S)
    sub = blue[y0:int((cy+32)*S), x0:int((cx+18)*S)]
    check(f'icon {name} outline ink', sub.sum()>150, f'n={int(sub.sum())}')
orange = (r>200)&(g>60)&(g<190)&(b<110)
sub = orange[int(330*S):int(418*S), int(790*S):int(822*S)]
check('orange icon bars ink', sub.sum()>800, f'n={int(sub.sum())}')

# ---- 9. frame containment: no content ink outside panel/beyond circle for inner elements ----
# content must sit inside red panel: x 42..918, y 45..540 (frame px)
for name,(x0f,y0f,x1f,y1f) in {'circle':(44,57,513,526),'sentbox':(475,106,902,144)}.items():
    pass
# global: black text ink must be inside panel bounds (y>=44 allows 1-2px AA above boxes)
ys,xs = np.nonzero(blk)
inx = (xs/S >= 43) & (xs/S <= 917) & (ys/S >= 44)
check('all text inside panel', bool(inx.all()), f'min_x={xs.min()/S:.0f} max_x={xs.max()/S:.0f} min_y={ys.min()/S:.0f}')
# title must be a SINGLE line: black ink rows in title band must span <= 40px
sub = blk[int(40*S):int(112*S), int(380*S):int(810*S)]
yy2,_ = np.nonzero(sub)
rows = np.unique(yy2)
check('title single line', (rows.max()-rows.min())/S <= 40, f'ink rows y[{(rows.min()+40*S)/S:.0f},{(rows.max()+40*S)/S:.0f}]')

print('\nRESULT:', 'ALL PASS' if not fail else f'FAILURES: {fail}')
sys.exit(0 if not fail else 1)
