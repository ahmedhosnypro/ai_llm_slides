#!/usr/bin/env python3
import numpy as np
from PIL import Image
BASE = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2'
orig = np.asarray(Image.open(f'{BASE}/unique_slides/slide_044.jpg').convert('RGB')).astype(int)
r0,g0,b0 = orig[:,:,0], orig[:,:,1], orig[:,:,2]
cream = (r0>242)&(g0>240)&(b0>215)&(b0<248)&(g0-b0>8)   # (250,251,235)-class fill
redL = (r0>150)&(r0-g0>30)&(r0-b0>30)
print('== LY cream-fill row runs ==')
for y in (460,465,470,480,485,495,499):
    xs=np.where(cream[y,40:940])[0]
    if len(xs):
        # find contiguous runs
        runs=[]; s=xs[0]; p=xs[0]
        for x in xs[1:]:
            if x>p+3: runs.append((s+40,p+40)); s=x
            p=x
        runs.append((s+40,p+40))
        print(f'  y{y}: runs {runs}')
    else: print(f'  y{y}: none')
print('== GN/IN cream-fill rows (control) ==')
for y,lbl,x0,x1 in [(437,'GN',250,460),(433,'IN',460,900)]:
    xs=np.where(cream[y,x0:x1])[0]
    print(f'  {lbl} y{y}: {xs.min()+x0}..{xs.max()+x0} n={len(xs)}' if len(xs) else f'  {lbl} y{y}: none')
print('== FV shaft top: rows y92..125 x648..676 (redL) ==')
for y in range(92,126):
    xs=np.where(redL[y,648:676])[0]
    if len(xs): print(f'  y{y}: x {xs.min()+648}..{xs.max()+648} n={len(xs)}')
print('== LY top border extent (redL row y455, x40..940) ==')
xs=np.where(redL[455,40:940])[0]
print(f'  y455: x {xs.min()+40}..{xs.max()+40} n={len(xs)}')
xs=np.where(redL[501,40:940])[0]
print(f'  y501: x {xs.min()+40}..{xs.max()+40} n={len(xs)}')
print('== samples ==')
for (x,y,l) in [(70,470,'LY?'),(75,470,'LY?'),(80,470,'LY?'),(890,470,'LY-right?'),(880,470,'LY-right?'),(66,485,'LY-left2'),(72,485,'LY-left3')]:
    print(f'  orig({x},{y}) {l}: {tuple(int(v) for v in orig[y,x])}')
