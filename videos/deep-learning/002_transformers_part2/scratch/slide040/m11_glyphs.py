#!/usr/bin/env python3
"""Stage 11: fixed sub-element glyph boxes + outline strokes (tight masks)."""
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

def gbox(x0,x1,y0,y1,label):
    sub = dark[y0:y1, x0:x1]
    ys, xs = np.where(sub)
    if len(xs)==0: print(label, 'EMPTY'); return
    xa, xb, ya, yb = x0+xs.min(), x0+xs.max(), y0+ys.min(), y0+ys.max()
    print(f'{label}: frame x {xa}..{xb} y {ya}..{yb}  | '+SR(xa,xb,ya,yb))

print('EQ1 (row band y 285..340):')
gbox(196,235,295,335,'eq1 arrow <-')
gbox(235,268,285,340,'eq1 frac 1/m')
gbox(264,306,283,342,'eq1 sum+limits')
gbox(302,335,300,335,'eq1 x_i')
print('EQ2 (row band y 335..395):')
gbox(196,238,352,392,'eq2 arrow')
gbox(236,270,338,395,'eq2 frac')
gbox(266,310,333,397,'eq2 sum')
gbox(306,402,352,392,'eq2 (xi-muB)^2')
print('EQ3 (row band y 392..452):')
gbox(168,200,400,440,'eq3 xhat ink')
gbox(196,235,405,445,'eq3 arrow')
gbox(235,335,393,424,'eq3 numerator row')
gbox(228,335,424,452,'eq3 denom+radical')
print('EQ4 (row band y 448..484):')
gbox(158,175,450,480,'eq4 ellipse dark ring')
gbox(193,228,450,480,'eq4 arrow')
gbox(226,258,450,480,'eq4 gamma xhat')
gbox(256,292,450,480,'eq4 beta plus')
gbox(290,380,450,480,'eq4 BN part')
print('HEADER sub:')
gbox(203,525,210,232,'input rest text')
gbox(203,350,252,275,'output brace expr')

print('OUTLINES tight:')
# eq3 blue outline: thin blue strokes; sample ring color
blue_ring = (b-r>70)&(b-g>70)&(b>130)
for y in range(394,452):
    xs = np.where(blue_ring[y, 155:300])[0]
    if len(xs) > 45: print(f'  eq3 horiz y={y} x {155+xs.min()}..{155+xs.max()} n={len(xs)}')
for x in range(155,300):
    ys = np.where(blue_ring[394:452, x])[0]
    if len(ys) > 22: print(f'  eq3 vert x={x} y {394+ys.min()}..{394+ys.max()} n={len(ys)}')
red_ring = (r-g>80)&(r-b>70)&(r>170)
for y in range(444,486):
    xs = np.where(red_ring[y, 150:390])[0]
    if len(xs) > 45: print(f'  eq4 horiz y={y} x {150+xs.min()}..{150+xs.max()} n={len(xs)}')
for x in range(150,395):
    ys = np.where(red_ring[444:486, x])[0]
    if len(ys) > 16: print(f'  eq4 vert x={x} y {444+ys.min()}..{444+ys.max()} n={len(ys)}')
# ring core colors
reg = im[398:402, 170:280].reshape(-1,3); l = reg.mean(axis=1); idx = np.argsort(l)[:20]
med = np.median(reg[idx], axis=0); print('eq3 outline top-stroke core:', f'#{int(med[0]):02X}{int(med[1]):02X}{int(med[2]):02X}')
reg = im[449:453, 200:340].reshape(-1,3); l = reg.mean(axis=1); idx = np.argsort(l)[:20]
med = np.median(reg[idx], axis=0); print('eq4 outline top-stroke core:', f'#{int(med[0]):02X}{int(med[1]):02X}{int(med[2]):02X}')

# title zoom check for serif confirmation
Image.fromarray(np.uint8(im[60:95, 255:420])).resize((660,140), Image.LANCZOS).save('title_4x.png')
Image.fromarray(np.uint8(im[140:165, 385:600])).resize((860,100), Image.LANCZOS).save('l2seg_4x.png')
print('crops saved')
