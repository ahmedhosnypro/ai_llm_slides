#!/usr/bin/env python3
"""Stage 7c: clean fill colors (non-text pixels), saturated text cores, remaining geometry."""
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

def fill_color(y0,y1,x0,x1):
    """median of LIGHT pixels (excludes dark text) = fill color."""
    reg = im[y0:y1, x0:x1].reshape(-1,3)
    l = reg.mean(axis=1)
    keep = reg[l>170]
    med = np.median(keep, axis=0)
    return f"#{int(med[0]):02X}{int(med[1]):02X}{int(med[2]):02X} (n={len(keep)})"

def sat_core(y0,y1,x0,x1, hue):
    """median of the top-15% most-hue-saturated pixels."""
    reg = im[y0:y1, x0:x1].reshape(-1,3)
    rr,gg,bb = reg[:,0],reg[:,1],reg[:,2]
    if hue=='blue': s = bb - (rr+gg)/2
    elif hue=='green': s = gg - (rr+bb)/2
    elif hue=='red': s = rr - (gg+bb)/2
    idx = np.argsort(s)[-max(int(len(s)*0.15),5):]
    med = np.median(reg[idx], axis=0)
    return f"#{int(med[0]):02X}{int(med[1]):02X}{int(med[2]):02X} (n={len(idx)})"

print('== FILL COLORS (light pixels only) ==')
print('green params fill:', fill_color(230,247,210,420))
print('lavender mu_B eq1:', fill_color(306,324,166,186))
print('lavender sig_B eq2:', fill_color(363,381,170,189))
print('lavender mu_B eq3 num:', fill_color(402,420,257,278))
print('lavender sig_B eq3 den:', fill_color(426,444,231,285))
print('pink xhat eq3:', fill_color(413,431,171,191))
print('pink //normalize:', fill_color(413,431,458,545))
print('orange //scale:', fill_color(454,472,428,545))
print('orange ellipse y_i:', fill_color(454,472,166,188))
print('panel white:', fill_color(280,290,400,500))

print('== SATURATED TEXT CORES ==')
print('L1 blue:', sat_core(117,135,536,823,'blue'))
print('L2 green text:', sat_core(142,160,390,531,'green'))
print('L2 red text:', sat_core(142,160,663,828,'red'))
print('L3 red text:', sat_core(167,182,105,435,'red'))
print('title red:', sat_core(66,90,261,676,'red'))
print('gamma 537-544:', sat_core(142,160,535,546,'green'))
print('beta 584-591:', sat_core(142,160,582,593,'green'))
print('and 551-576:', sat_core(142,160,549,578,'green'))

def fill_rect(mask, x0,x1,y0,y1, minrowfrac=0.35):
    mm = np.zeros_like(mask); mm[y0:y1, x0:x1] = mask[y0:y1, x0:x1]
    rows = mm.sum(axis=1); width = x1-x0
    solid = [y0+i for i,v in enumerate(rows) if v > minrowfrac*width]
    if not solid: return None
    ra, rb = solid[0], solid[-1]
    colsum = mm[ra:rb+1].sum(axis=0)
    cols = np.where(colsum > (rb-ra+1)*0.4)[0]
    if len(cols)==0: return None
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
        print(f'  bar y={y} x {225+xs3.min()}..{225+xs3.max()} n={row.sum()}')

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
print('letterbox top row 519 -> slide y', round(519/0.95556,1))

print('== GREEN BAND ROWS ==')
mm = np.zeros_like(greenm); mm[218:258, 150:540] = greenm[218:258, 150:540]
prof = [(218+i, int(row.sum())) for i,row in enumerate(mm) if row.sum()>5]
print(prof)

# blue outline eq3 + red outline eq4 (thin strokes)
print('== OUTLINES ==')
blueo = (b-r>60)&(b-g>60)&(b>120)&(lum<200)
mm = np.zeros_like(blueo); mm[388:452, 155:330] = blueo[388:452, 155:330]
ys5, xs5 = np.where(mm)
print(f'eq3 blue outline px bbox x {xs5.min()}..{xs5.max()} y {ys5.min()}..{ys5.max()} n={len(xs5)} | '+SR(xs5.min(),xs5.max(),ys5.min(),ys5.max()))
redo = (r-g>60)&(r-b>60)&(r>150)&(lum<210)
mm = np.zeros_like(redo); mm[446:484, 155:385] = redo[446:484, 155:385]
ys6, xs6 = np.where(mm)
print(f'eq4 red outline px bbox x {xs6.min()}..{xs6.max()} y {ys6.min()}..{ys6.max()} n={len(xs6)} | '+SR(xs6.min(),xs6.max(),ys6.min(),ys6.max()))
