#!/usr/bin/env python3
"""Stage 13: eq1 right part (x_i + sum limits), eq3 fraction fills, radical/bar geometry, eq4 ellipse ring."""
import numpy as np
from PIL import Image

im = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_040.jpg')).astype(int)
r, g, b = im[:,:,0], im[:,:,1], im[:,:,2]
lum = (r+g+b)/3.0

def S(fx, fy): return ((fx-18.63)/0.96123, fy/0.95556)

# --- eq1 right of sum: any ink x 275..430, y 285..345 at looser threshold?
print('== EQ1 x 275..435 loose ink (lum<185) ==')
dark = lum < 185
for xa in range(275, 435, 8):
    sub = dark[285:345, xa:xa+8]
    ys, xs = np.where(sub)
    if len(xs)==0: continue
    print(f'  x {xa}-{xa+8}: y {285+ys.min()}..{285+ys.max()} n={len(xs)}')

# --- eq2 right: x 340..410 (the ^2 after paren)
print('== EQ2 x 335..415 loose ==')
for xa in range(335, 415, 8):
    sub = dark[333:398, xa:xa+8]
    ys, xs = np.where(sub)
    if len(xs)==0: continue
    print(f'  x {xa}-{xa+8}: y {333+ys.min()}..{333+ys.max()} n={len(xs)}')

# --- eq1 fraction detail: bar row + numerator/denominator split
print('== EQ1 FRACTION (x 233..268) ==')
for y in range(288, 345):
    xs = np.where(dark[y, 233:268])[0]
    if len(xs) > 12:
        print(f'  y={y} x {233+xs.min()}..{233+xs.max()} n={len(xs)}')

# --- eq2 fraction detail
print('== EQ2 FRACTION (x 233..268) ==')
for y in range(332, 398):
    xs = np.where(dark[y, 233:268])[0]
    if len(xs) > 12:
        print(f'  y={y} x {233+xs.min()}..{233+xs.max()} n={len(xs)}')

# --- eq3 fraction bar + radical
print('== EQ3 FRACTION/RADICAL (x 225..330) ==')
for y in range(390, 452):
    xs = np.where((lum[y, 225:330] < 185))[0]
    if len(xs) > 14:
        print(f'  y={y} x {225+xs.min()}..{225+xs.max()} n={len(xs)}')

# --- eq3 fills: numerator band (y 396..420) and denominator band (y 428..448) per x-run
print('== EQ3 NUMERATOR FILL RUNS (y 396..420) ==')
reg = im[396:420, 228:335]
rl = lum[396:420, 228:335]
# classify: lavender b-r>25, lightblue b-r>25 & lighter... sample distinct colors
cols = {}
for x in range(reg.shape[1]):
    colpix = reg[:, x][rl[:, x] < 235]
    if len(colpix) < 3: continue
    med = np.median(colpix, axis=0).astype(int)
    key = f'#{med[0]:02X}{med[1]:02X}{med[2]:02X}'
    cols.setdefault(key, []).append(228+x)
for k, v in cols.items():
    if len(v) > 4: print(f'  {k}: x {min(v)}..{max(v)} n={len(v)}')
print('== EQ3 DENOMINATOR FILL RUNS (y 428..449) ==')
reg = im[428:449, 228:335]
rl = lum[428:449, 228:335]
cols = {}
for x in range(reg.shape[1]):
    colpix = reg[:, x][rl[:, x] < 235]
    if len(colpix) < 3: continue
    med = np.median(colpix, axis=0).astype(int)
    key = f'#{med[0]:02X}{med[1]:02X}{med[2]:02X}'
    cols.setdefault(key, []).append(228+x)
for k, v in cols.items():
    if len(v) > 4: print(f'  {k}: x {min(v)}..{max(v)} n={len(v)}')

# --- light-blue A6D0F2-class mask over whole panel
lb = (np.abs(r-0xA6)<38)&(np.abs(g-0xD0)<38)&(np.abs(b-0xF2)<30)&(b-r>30)
ys, xs = np.where(lb[204:497, 148:552])
print('== A6D0F2-class pixels in panel ==')
if len(xs):
    print(f'  bbox x {148+xs.min()}..{148+xs.max()} y {204+ys.min()}..{204+ys.max()} n={len(xs)}')
    # cluster rows
    rows = sorted(set((204+ys).tolist()))
    groups=[]; s=rows[0]; p=rows[0]
    for y in rows[1:]:
        if y-p>3: groups.append((s,p)); s=y
        p=y
    groups.append((s,p))
    for (a,bb) in groups:
        sel = (ys+204>=a)&(ys+204<=bb)
        print(f'  band y {a}..{bb} x {148+xs[sel].min()}..{148+xs[sel].max()} n={sel.sum()}')

# --- eq4 ellipse ring color (darkest orange in ring zone)
reg = im[452:478, 168:194].reshape(-1,3)
l = reg.mean(axis=1)
idx = np.argsort(l)[:40]
med = np.median(reg[idx], axis=0)
print(f'== EQ4 ellipse ring core: #{int(med[0]):02X}{int(med[1]):02X}{int(med[2]):02X}')

# --- eq4: green gamma/beta highlight rects precise
greenm = (g-r>25)&(g-b>25)&(g>120)
print('== EQ4 GREEN rows ==')
for y in range(450, 478):
    xs2 = np.where(greenm[y, 205:285])[0]
    if len(xs2) > 6:
        print(f'  y={y} x {205+xs2.min()}..{205+xs2.max()} n={len(xs2)}')

# --- comment baseline: comments c1..c4 vertical centers
print('== COMMENT bands ==')
for (y0,y1,name) in [(300,335,'c1'),(355,392,'c2'),(408,438,'c3'),(448,480,'c4')]:
    dd = (lum[y0:y1, 390:552] < 170)
    ys3, xs3 = np.where(dd)
    if len(xs3): print(f'  {name}: x {390+xs3.min()}..{390+xs3.max()} y {y0+ys3.min()}..{y0+ys3.max()}')
