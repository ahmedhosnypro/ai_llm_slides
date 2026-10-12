#!/usr/bin/env python3
"""Stage 16: arrow region ascii + intro highlight fill + gamma/beta colors + eq4 detail."""
import numpy as np
from PIL import Image

im = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_040.jpg')).astype(int)
lum = (im[:,:,0]+im[:,:,1]+im[:,:,2])/3.0
r, g, b = im[:,:,0], im[:,:,1], im[:,:,2]

def amap(x0, x1, y0, y1, thr, label):
    print(f'--- {label} x{x0}..{x1} y{y0}..{y1} thr{thr} ---')
    print('     ' + ''.join(str((x//10)%10) for x in range(x0, x1)))
    for y in range(y0, y1):
        row = ''.join('#' if lum[y, x] < thr else '.' for x in range(x0, x1))
        print(f'{y:4d} {row}')

amap(190, 240, 296, 336, 195, 'EQ1 arrow zone')
amap(190, 240, 452, 478, 195, 'EQ4 arrow zone')

# intro L2 "learn parameters" highlight fill (light pixels)
reg = im[144:158, 392:528].reshape(-1,3)
l = reg.mean(axis=1); keep = reg[l>170]
med = np.median(keep, axis=0)
print(f'intro "learn parameters" fill: #{int(med[0]):02X}{int(med[1]):02X}{int(med[2]):02X} (n={len(keep)})')
# exact extent of that highlight (green-ish rows)
greenm = (g-r>18)&(g-b>18)&(g>140)
print('intro highlight rows:')
for y in range(138, 165):
    xs = np.where(greenm[y, 380:545])[0]
    if len(xs) > 20: print(f'  y={y} x {380+xs.min()}..{380+xs.max()} n={len(xs)}')

# gamma / beta cores in intro (darkest 25% of glyph zone)
def core(y0,y1,x0,x1,frac=0.25):
    reg = im[y0:y1, x0:x1].reshape(-1,3)
    l = reg.mean(axis=1); idx = np.argsort(l)[:max(int(len(l)*frac),4)]
    med = np.median(reg[idx], axis=0)
    return f'#{int(med[0]):02X}{int(med[1]):02X}{int(med[2]):02X}'
print('intro gamma core:', core(142,160,535,547))
print('intro beta core:', core(142,160,582,594))
print('intro and core:', core(142,160,549,579))
# intro black text core
print('intro L2 black core:', core(142,160,105,384))

# eq4: gamma/xhat/beta/BN glyph boxes at thr 195 (1px)
def gbox(x0,x1,y0,y1,label):
    sub = lum[y0:y1, x0:x1] < 195
    ys, xs = np.where(sub)
    if len(xs)==0: print(label,'EMPTY'); return
    print(f'{label}: x {x0+xs.min()}..{x0+xs.max()} y {y0+ys.min()}..{y0+ys.max()} n={len(xs)}')
print('EQ4 sub-elements thr195:')
gbox(193,212,452,478,'eq4 arrow')
gbox(212,226,452,478,'eq4 gamma')
gbox(226,246,452,478,'eq4 xhat')
gbox(246,262,452,478,'eq4 plus')
gbox(262,278,452,478,'eq4 beta')
gbox(278,298,452,478,'eq4 equiv')
gbox(296,325,452,478,'eq4 BN')
gbox(323,372,452,478,'eq4 (xi)')
# eq3 denom: epsilon + paren
gbox(256,292,424,450,'eq3 (+ eps) tail')
# panel border color: left border column ~145
print('panel left border core:', core(300,400,144,147,0.5))
print('panel top border core:', core(203,206,300,500,0.5))
print('intro border core:', core(103,107,300,600,0.5))
