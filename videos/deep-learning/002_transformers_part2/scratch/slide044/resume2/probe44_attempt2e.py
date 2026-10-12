#!/usr/bin/env python3
import numpy as np
from PIL import Image
BASE = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2'
o = np.asarray(Image.open(f'{BASE}/unique_slides/slide_044.jpg').convert('RGB')).astype(int)
r,g,b = o[:,:,0],o[:,:,1],o[:,:,2]
magB = (r>150)&(b>140)&(g<80)          # bright magenta
magD = (r>60)&(r<150)&(b>60)&(b<150)&(g<40)  # dark magenta
sal = (r>185)&(r-g>60)&(g-b>5)         # bright salmon/orange family
print('== GN magenta-top zone rows (x282..334): bright-mag / dark-mag counts ==')
for y in range(165,185):
    print(f'  y{y}: magB={int(magB[y,282:334].sum()):3d} magD={int(magD[y,282:334].sum()):3d}')
print('== GN salmon zone rows (x340..404): salmon counts ==')
for y in range(163,190):
    print(f'  y{y}: sal={int(sal[y,340:404].sum()):3d}')
print('== GN salmon col x360 (sal runs y165..340) — solid or seamed? ==')
xs=np.where(sal[165:340,360])[0]+165
runs=[]; s=p=None
for y in xs:
    if s is None: s=p=int(y)
    elif y>p+1: runs.append((s,p)); s=int(y)
    p=int(y)
if s is not None: runs.append((s,p))
print('  runs:', runs)
print('== IN salmon col x560 runs y185..360 ==')
xs=np.where(sal[185:360,560])[0]+185
runs=[]; s=p=None
for y in xs:
    if s is None: s=p=int(y)
    elif y>p+1: runs.append((s,p)); s=int(y)
    p=int(y)
if s is not None: runs.append((s,p))
print('  runs:', runs)
print('== IN magenta col x520 runs y185..360 (bright mag) ==')
xs=np.where(magB[185:360,520])[0]+185
runs=[]; s=p=None
for y in xs:
    if s is None: s=p=int(y)
    elif y>p+1: runs.append((s,p)); s=int(y)
    p=int(y)
if s is not None: runs.append((s,p))
print('  runs:', runs)
print('== RT magenta top rows (x700..810): magB/magD counts ==')
for y in range(163,185):
    print(f'  y{y}: magB={int(magB[y,700:810].sum()):3d} magD={int(magD[y,700:810].sum()):3d}')
