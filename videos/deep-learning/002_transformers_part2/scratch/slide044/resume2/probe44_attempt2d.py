#!/usr/bin/env python3
import numpy as np
from PIL import Image
BASE = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2'
orig = np.asarray(Image.open(f'{BASE}/unique_slides/slide_044.jpg').convert('RGB')).astype(int)
r0,g0,b0 = orig[:,:,0], orig[:,:,1], orig[:,:,2]
lum = 0.299*r0 + 0.587*g0 + 0.114*b0
darkL = lum < 120
redL = (r0>150)&(r0-g0>30)&(r0-b0>30)
print('== oval true bbox (lum<75, x700..915 y440..486) ==')
m = lum < 75
ys,xs = np.where(m[440:486,700:915])
print(f'  oval: x {xs.min()+700}..{xs.max()+700}  y {ys.min()+440}..{ys.max()+440}  n={len(xs)}')
print('  row extents:')
for y in range(448,482,2):
    r=np.where(m[y,700:915])[0]
    if len(r): print(f'    y{y}: x {r.min()+700}..{r.max()+700} n={len(r)}')
print('== mystery ink x820..915 y405..445 (dark|grn-ish) ==')
grn = (g0>110)&(g0-r0>40)&(g0-b0>40)
mm = darkL|grn
for y in range(405,446):
    r=np.where(mm[y,820:915])[0]
    if len(r): print(f'  y{y}: x {r.min()+820}..{r.max()+820} n={len(r)}')
print('== IN body L2/L3 true extents (dark|grn, x460..870 only) ==')
for (y0,y1,l) in [(394,415,'L2'),(415,436,'L3')]:
    ys,xs = np.where(mm[y0:y1,460:870])
    if len(xs): print(f'  {l}: x {xs.min()+460}..{xs.max()+460} y {ys.min()+y0}..{ys.max()+y0}')
print('== LY right-edge samples ==')
for (x,y) in [(816,455),(820,455),(850,455),(880,455),(816,501),(820,501),(850,501),(880,501),(820,470),(840,499),(900,455),(900,501)]:
    print(f'  orig({x},{y}): {tuple(int(v) for v in orig[y,x])}')
print('== oval yellow text bbox ==')
yel = (r0>190)&(g0>170)&(b0<140)
ys,xs = np.where(yel[440:486,700:915])
if len(xs): print(f'  yellow text: x {xs.min()+700}..{xs.max()+700} y {ys.min()+440}..{ys.max()+440}')
