from PIL import Image
import numpy as np
im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_048.jpg').convert('RGB')
a = np.asarray(im).astype(int)
R,G,B = a[...,0],a[...,1],a[...,2]
lum = 0.299*R+0.587*G+0.114*B
dark = lum<170
print('== CNN gap scan (slant-corrected gaps, y355..385) ==')
gaps = [('photo-slab1',228,254),('s1-s2',311,336),('s2-s3',393,424),('s3-s4',481,502),('s4-s5',559,578),('s5-s6',635,660),('s6-b7',717,735)]
for nm,g0,g1 in gaps:
    m = dark[355:385, g0:g1]
    ys,xs = np.nonzero(m)
    if len(xs): print(f'  {nm}: x {g0+xs.min()}..{g0+xs.max()} y {355+ys.min()}..{355+ys.max()} n={len(xs)}')
    else: print(f'  {nm}: EMPTY')
print('== probe gap centers y370 ==')
for nm,g0,g1 in gaps:
    c=(g0+g1)//2
    print(f'  {nm} ({c},370):', tuple(a[370,c]), f'({c},369):', tuple(a[369,c]))
print('== slab6 right edge / b7 left gap fine ==')
for x in range(712,736):
    row = ''.join('#' if lum[y,x]<170 else '.' for y in range(363,377))
    print(f'  x{x}: {row}')
