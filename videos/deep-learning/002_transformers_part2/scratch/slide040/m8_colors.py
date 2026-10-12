#!/usr/bin/env python3
"""Stage 7b: title/blue/green/red CORE colors + highlight rects + eq rows + bar + ellipse + header + boxes."""
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

def core_color(y0,y1,x0,x1, satmin=0):
    """median of the darkest 30% pixels (core ink, avoids anti-alias halo)."""
    reg = im[y0:y1, x0:x1].reshape(-1,3)
    l = reg.mean(axis=1)
    idx = np.argsort(l)[:max(int(len(l)*0.3), 4)]
    med = np.median(reg[idx], axis=0)
    return f"#{int(med[0]):02X}{int(med[1]):02X}{int(med[2]):02X} (n={len(idx)})"

print('== CORE COLORS ==')
print('title:', core_color(66,90,261,676))
print('L1 black words:', core_color(117,135,105,530))
print('L1 blue words:', core_color(117,135,536,823))
print('L2 black words:', core_color(142,160,105,384))
print('L2 green "learn parameters":', core_color(142,160,390,531))
print('L2 glyph537-544:', core_color(142,160,535,546))
print('L2 glyph551-576:', core_color(142,160,549,578))
print('L2 glyph584-591:', core_color(142,160,582,593))
print('L2 black "that can":', core_color(142,160,596,658))
print('L2 red "convert...":', core_color(142,160,663,828))
print('L3 red:', core_color(167,182,105,435))
print('panel border:', core_color(204,206,300,400))
print('intro border:', core_color(104,106,300,600))
print('badge ring:', core_color(55,60,870,885))
print('eq ink (Input line):', core_color(213,229,152,520))
print('comment ink eq1:', core_color(302,330,417,547))
print('green fill interior:', core_color(232,246,210,420, 0))
print('lavender fill eq1 interior:', core_color(306,324,166,186))
print('pink fill eq3 interior:', core_color(414,431,172,189))
print('orange fill //scale interior:', core_color(455,471,430,543))

# highlight rects (solid-row method)
def fill_rect(mask, x0,x1,y0,y1, minrowfrac=0.5):
    mm = np.zeros_like(mask); mm[y0:y1, x0:x1] = mask[y0:y1, x0:x1]
    rows = mm.sum(axis=1); width = x1-x0
    solid = [y0+i for i,v in enumerate(rows) if v > minrowfrac*width]
    if not solid: return None
    ra, rb = solid[0], solid[-1]
    colsum = mm[ra:rb+1].sum(axis=0)
    cols = np.where(colsum > (rb-ra+1)*0.5)[0]
    return (int(cols.min()), int(cols.max()), ra, rb)

greenm  = (g-r>25)&(g-b>25)&(g>120)
lavm    = (b-r>25)&(b-g>25)&(b>150)
pinkm   = (r-g>45)&(r-b>45)&(r>210)
orangm  = (r-b>60)&(g-b>40)&(r>210)&(g>140)
print('== HIGHLIGHT SOLID RECTS ==')
for name, m, box in [
    ('green params line', greenm, (150,540,220,258)),
    ('lav mu_B eq1',      lavm,   (150,220,293,337)),
    ('lav sig_B eq2',     lavm,   (150,220,350,394)),
    ('lav mu_B eq3num',   lavm,   (225,325,390,430)),
    ('lav sig_B eq3den',  lavm,   (205,325,424,455)),
    ('pink xhat eq3',     pinkm,  (150,215,400,442)),
    ('pink //normalize',  pinkm,  (430,560,400,442)),
    ('orange //scale',    orangm, (400,560,443,484)),
]:
    rr = fill_rect(m, *box)
    print(f'{name}: frame {rr}' + ('' if rr is None else '  | '+SR(rr[0],rr[1],rr[2],rr[3])))

print('== EQ ROWS (dark ink) ==')
for (y0,y1,name) in [(283,335,'eq1'),(336,392,'eq2'),(392,449,'eq3'),(449,484,'eq4')]:
    dd = np.zeros_like(dark); dd[y0:y1, 148:552] = dark[y0:y1, 148:552]
    ys2, xs2 = np.where(dd)
    cm = np.zeros_like(dark); cm[y0:y1, 385:552] = dark[y0:y1, 385:552]
    cys, cxs = np.where(cm)
    cinfo = f'comment x {cxs.min()}..{cxs.max()} y {cys.min()}..{cys.max()}' if len(cxs) else 'no comment ink'
    print(f'{name}: ink x {xs2.min()}..{xs2.max()} y {ys2.min()}..{ys2.max()} | {cinfo}')
    print(f'    | {SR(xs2.min(), xs2.max(), ys2.min(), ys2.max())}')

print('== EQ3 FRACTION BAR ==')
for y in range(412, 428):
    row = dark[y, 225:345]
    if row.sum() > 40:
        xs3 = np.where(row)[0]
        print(f'  bar y={y} x {225+xs3.min()}..{225+xs3.max()} n={row.sum()} | '+SR(225+xs3.min(),225+xs3.max(),y,y))

print('== EQ4 ELLIPSE ==')
yy, xx = np.mgrid[0:540, 0:960]
om = (r-b>40)&(g>120)&(g<215)&(r>200)&(yy>=443)&(yy<=484)&(xx>=150)&(xx<=210)
ys4, xs4 = np.where(om)
print(f'ellipse bbox frame x {xs4.min()}..{xs4.max()} y {ys4.min()}..{ys4.max()} n={len(xs4)} | '+SR(xs4.min(),xs4.max(),ys4.min(),ys4.max()))

print('== HEADER ==')
for (y0,y1,name) in [(206,231,'Input'),(231,253,'Params'),(253,277,'Output')]:
    dd = np.zeros_like(dark); dd[y0:y1, 148:552] = dark[y0:y1, 148:552]
    ys2, xs2 = np.where(dd)
    print(f'{name}: ink x {xs2.min()}..{xs2.max()} y {ys2.min()}..{ys2.max()} | '+SR(xs2.min(),xs2.max(),ys2.min(),ys2.max()))

print('== BOXES ==')
print('intro box frame 88..892 x 104..185 |', SR(88,892,104,185))
print('panel frame 145..552 x 204..497  |', SR(145,552,204,497))
print('letterbox top row 519 -> slide y', round(519/0.95556,1), '(slide bottom 540)')

# green params band rows detail
print('== GREEN BAND ROW PROFILE ==')
mm = np.zeros_like(greenm); mm[220:258, 150:540] = greenm[220:258, 150:540]
for i,row in enumerate(mm):
    if row.sum()>10: print('  y', 220+i, 'n', row.sum())
