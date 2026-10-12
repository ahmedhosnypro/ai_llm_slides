#!/usr/bin/env python3
"""Stage 10: focused probes — fill rects (row sums), outline strokes (long runs), glyph boxes."""
import numpy as np
from PIL import Image

im = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_040.jpg')).astype(int)
r, g, b = im[:,:,0], im[:,:,1], im[:,:,2]
lum = (r+g+b)/3.0
dark = lum < 140

def S(fx, fy): return ((fx-18.63)/0.96123, fy/0.95556)
def SR(fx0, fx1, fy0, fy1):
    x0, y0 = S(fx0, fy0); x1, y1 = S(fx1, fy1)
    return f"slide x {x0:.1f}..{x1:.1f} (w {x1-x0:.1f})  y {y0:.1f}..{y1:.1f} (h {y1-y0:.1f})"

greenm  = (g-r>25)&(g-b>25)&(g>120)
lavm    = (b-r>25)&(b-g>25)&(b>150)
pinkm   = (r-g>45)&(r-b>45)&(r>210)
orangm  = (r-b>60)&(g-b>40)&(r>210)&(g>140)

def rows_of(mask, x0,x1,y0,y1,label):
    print(label)
    for y in range(y0,y1):
        n = mask[y, x0:x1].sum()
        if n>8:
            xs = np.where(mask[y, x0:x1])[0]
            print(f'  y={y} n={n:4d} x {x0+xs.min()}..{x0+xs.max()}')

rows_of(greenm, 150,545, 220,256, 'GREEN params rows:')
rows_of(lavm, 150,220, 295,335, 'LAV mu_B eq1 rows:')
rows_of(lavm, 150,220, 352,392, 'LAV sig_B eq2 rows:')
rows_of(lavm, 225,325, 392,430, 'LAV mu_B eq3num rows:')
rows_of(lavm, 205,325, 424,452, 'LAV sig_B eq3den rows:')
rows_of(pinkm, 150,215, 402,442, 'PINK xhat eq3 rows:')
rows_of(pinkm, 430,560, 402,442, 'PINK //normalize rows:')
rows_of(orangm, 400,560, 443,484, 'ORANGE //scale rows:')

# outline strokes: long runs
print('EQ3 BLUE OUTLINE: long horiz runs (blue, lum<200)')
blueo = (b-r>50)&(b-g>50)&(b>110)&(lum<215)
for y in range(392,452):
    xs = np.where(blueo[y, 155:330])[0]
    if len(xs) > 60: print(f'  horiz y={y} x {155+xs.min()}..{155+xs.max()} n={len(xs)}')
for x in range(155,335):
    ys = np.where(blueo[392:452, x])[0]
    if len(ys) > 25: print(f'  vert x={x} y {392+ys.min()}..{392+ys.max()} n={len(ys)}')
print('EQ4 RED OUTLINE: long runs')
redo = (r-g>55)&(r-b>55)&(r>140)&(lum<215)
for y in range(446,484):
    xs = np.where(redo[y, 155:390])[0]
    if len(xs) > 60: print(f'  horiz y={y} x {155+xs.min()}..{155+xs.max()} n={len(xs)}')
for x in range(155,395):
    ys = np.where(redo[446:484, x])[0]
    if len(ys) > 14: print(f'  vert x={x} y {446+ys.min()}..{446+ys.max()} n={len(ys)}')

# ellipse: fill + ring colors, exact bbox
print('EQ4 ELLIPSE detail:')
for y in range(448,482):
    xs = np.where((r[y,155:205]-b[y,155:205]>40)&(g[y,155:205]>130))[0]
    if len(xs): print(f'  y={y} x {155+xs.min()}..{155+xs.max()} n={len(xs)}')
# ring color = darkest orange pixels
reg = im[452:478, 162:196].reshape(-1,3)
l = reg.mean(axis=1); idx = np.argsort(l)[:60]
med = np.median(reg[idx], axis=0); print('ellipse dark core:', f'#{int(med[0]):02X}{int(med[1]):02X}{int(med[2]):02X}')
l2 = reg.mean(axis=1); keep = reg[l2>170]; med2 = np.median(keep, axis=0)
print('ellipse light fill:', f'#{int(med2[0]):02X}{int(med2[1]):02X}{int(med2[2]):02X}')

# glyph boxes for size fitting: eq1 arrow+x_i, sum, fraction
print('EQ1 sub-elements (dark):')
def gbox(x0,x1,y0,y1,label):
    dd = np.zeros_like(dark); dd[y0:y1, x0:x1] = dark[y0:y1, x0:x1]
    ys, xs = np.where(dd)
    if len(xs)==0: print(label, 'EMPTY'); return
    print(f'{label}: x {x0+xs.min()}..{x0+xs.max()} y {y0+ys.min()}..{y0+ys.max()}  | '+SR(x0+xs.min(),x0+xs.max(),y0+ys.min(),y0+ys.max()))
gbox(196,232,300,330,'eq1 arrow')
gbox(232,262,290,336,'eq1 frac 1/m')
gbox(262,300,285,340,'eq1 sum+limits')
gbox(300,330,300,330,'eq1 x_i')
gbox(168,200,300,330,'eq1 mu_B ink')
print('EQ2 sub-elements:')
gbox(196,235,355,390,'eq2 arrow')
gbox(235,265,340,395,'eq2 frac')
gbox(265,305,335,395,'eq2 sum')
gbox(305,400,355,390,'eq2 (x_i-mu_B)^2')
gbox(168,200,358,388,'eq2 sigma_B ink')
print('EQ3 sub-elements:')
gbox(168,200,405,440,'eq3 xhat ink')
gbox(196,232,408,438,'eq3 arrow')
gbox(232,330,395,425,'eq3 numerator')
gbox(230,330,425,452,'eq3 denominator+radical')
print('EQ4 sub-elements:')
gbox(190,225,452,478,'eq4 arrow')
gbox(225,260,452,478,'eq4 gamma+xhat')
gbox(258,290,452,478,'eq4 beta+plus')
gbox(288,378,452,478,'eq4 BN part')
# comments: heights
print('COMMENT glyphs:')
gbox(432,547,300,330,'c1 //mini-batch mean')
gbox(411,547,358,385,'c2 //mini-batch variance')
gbox(465,547,410,435,'c3 //normalize')
gbox(438,546,450,478,'c4 //scale and shift')
# header glyph details
gbox(152,200,210,232,'Input: bold label')
gbox(203,425,230,252,'params text')
gbox(151,200,252,275,'Output: bold label')
gbox(203,350,252,275,'output brace expr')
