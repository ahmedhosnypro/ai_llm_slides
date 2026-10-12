from PIL import Image
import numpy as np
im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_048.jpg').convert('RGB')
a = np.asarray(im).astype(int)
R,G,B = a[...,0],a[...,1],a[...,2]
dark = (R<140)&(G<140)&(B<140)
orange = (R>170)&(R<240)&(G>90)&(G<170)&(B<70)
print('== blocks 7/8/9 gap arrows ==')
for (g0,g1,nm) in [(761,782,'b7-b8'),(809,829,'b8-b9')]:
    m = dark[355:385, g0:g1]
    ys,xs = np.nonzero(m)
    print(f'  {nm}: ' + (f'x {g0+xs.min()}..{g0+xs.max()} y {355+ys.min()}..{355+ys.max()} n={len(xs)}' if len(xs) else 'EMPTY'))
print('== photo edge checks (meme) ==')
for x,y in [(246,220),(247,220),(360,220),(361,220),(300,189),(300,190),(300,253),(300,254)]:
    print(f'  ({x},{y}) {tuple(a[y,x])}')
print('== siamese crop corners ==')
for x,y in [(122,313),(123,313),(227,313),(228,313),(122,430),(123,430),(227,430),(228,430),(227,424),(228,424),(226,424),(225,424)]:
    print(f'  ({x},{y}) {tuple(a[y,x])}')
print('== NL text core colors ==')
lum = 0.299*R+0.587*G+0.114*B
m = (lum<150)[416:440, 593:643]
px = a[416:440, 593:643][m]
print('  NL2 darkest:', [tuple(p) for p in px[np.argsort(lum[416:440,593:643][m])[:6]]])
m = (lum<150)[416:440, 270:320]
px = a[416:440, 270:320][m]
print('  NL1 darkest:', [tuple(p) for p in px[np.argsort(lum[416:440,270:320][m])[:6]]])
print('== Conv label cores ==')
m = (lum<170)[318:330, 470:503]
px = a[318:330, 470:503][m]
print('  Conv2 darkest:', [tuple(p) for p in px[np.argsort(lum[318:330,470:503][m])[:6]]])
m = (lum<170)[320:330, 230:252]
px = a[320:330, 230:252][m]
print('  Conv1 darkest:', [tuple(p) for p in px[np.argsort(lum[320:330,230:252][m])[:6]]])
print('== divider exact x-extent (row 269 loose) ==')
loose = ((R-G)>28)&((R-B)>28)&(R>150)
xs = np.nonzero(loose[268:271, 55:900].any(axis=0))[0]+55
print('  divider x:', xs.min(), '..', xs.max())
print('== frame border color cores ==')
for x,y in [(300,135),(300,136),(500,448),(500,449),(65,300),(894,300),(58,300)]:
    print(f'  ({x},{y}) {tuple(a[y,x])}')
print('== slab top-face color (wedge interior) ==')
for x,y in [(528,320),(530,325),(281,320),(279,322),(605,320),(687,322),(450,320),(364,320)]:
    print(f'  ({x},{y}) {tuple(a[y,x])}')
print('== meme photo: any white caption rows (top/bottom)? ==')
wt = (R>235)&(G>235)&(B>230)
for r in range(191,254,4):
    xs = np.nonzero(wt[r, 249:360])[0]
    if len(xs)>3: print(f'  row {r}: n={len(xs)} x {249+xs.min()}..{249+xs.max()}')
