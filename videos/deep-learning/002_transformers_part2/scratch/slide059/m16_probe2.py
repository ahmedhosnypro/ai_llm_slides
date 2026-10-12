from PIL import Image
import numpy as np
im = Image.open('unique_slides/slide_059.jpg').convert('RGB')
a = np.asarray(im).astype(int)
print('y=428 x 145..215 (1px):')
for x in range(145, 216):
    r,g,b = a[428,x]
    tag = 'd' if (110<r<210 and g<95 and b<100 and r-g>40) else 'Y' if (r>235 and g>235 and 150<b<225) else 'g' if (g>180 and g-r>12 and g-b>12) else 'G' if (g>110 and g-r>25 and g-b>15) else 'p' if (r>230 and 150<g<225 and 150<b<225 and r-g>20) else 'W' if (r>240 and g>240 and b>225) else '.'
    print(f'{x}{tag}', end=' ')
print()
print('y=429 x 145..215:')
for x in range(145, 216):
    r,g,b = a[429,x]
    tag = 'd' if (110<r<210 and g<95 and b<100 and r-g>40) else 'Y' if (r>235 and g>235 and 150<b<225) else 'g' if (g>180 and g-r>12 and g-b>12) else 'G' if (g>110 and g-r>25 and g-b>15) else 'p' if (r>230 and 150<g<225 and 150<b<225 and r-g>20) else 'W' if (r>240 and g>240 and b>225) else '.'
    print(f'{x}{tag}', end=' ')
print()
# red line in position row: count + extent
dred2 = (a[:,:,0]>120)&(a[:,:,0]<215)&(a[:,:,1]<110)&(a[:,:,2]<110)&(a[:,:,0]-a[:,:,1]>50)
for y in (489,490,491,492,493,494):
    xs = np.where(dred2[y, 130:900])[0]
    if len(xs): print('red line y=%d: n=%d x %d..%d' % (y, len(xs), xs.min()+130, xs.max()+130))
# same check word row y 428..436
for y in (430,431,432,433,434):
    xs = np.where(dred2[y, 130:900])[0]
    if len(xs)>30: print('word red line y=%d: n=%d x %d..%d' % (y, len(xs), xs.min()+130, xs.max()+130))
# clean output-row fill median (top band)
blk = a[229:232, 300:600].reshape(-1,3); print('output fill median:', tuple(int(v) for v in np.median(blk, axis=0)))
# GAP border cols threshold<170
dk2 = (a[:,:,0]<170)&(a[:,:,1]<170)&(a[:,:,2]<170)
cnt = dk2[186:204, :].sum(axis=0)
print('GAP border cols:', [x for x in range(150,920) if cnt[x]>10])
# encoder container: exact top/bottom at x=700
print('enc top x=700:', [(y, tuple(int(v) for v in a[y,700])) for y in range(272,280)])
print('enc bottom x=700:', [(y, tuple(int(v) for v in a[y,700])) for y in range(368,377)])
# tan bar exact top/bottom at x=250
print('tan top/bot x=250:', [(y, tuple(int(v) for v in a[y,250])) for y in range(86,95)]+[(y, tuple(int(v) for v in a[y,250])) for y in range(108,118)])
# input container top edge at x=700
print('input top x=700:', [(y, tuple(int(v) for v in a[y,700])) for y in range(382,392)])
print('input bottom x=700:', [(y, tuple(int(v) for v in a[y,700])) for y in range(510,518)])
