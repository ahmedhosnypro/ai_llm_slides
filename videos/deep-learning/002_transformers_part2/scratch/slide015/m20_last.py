from PIL import Image
import numpy as np
im = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_015.jpg').convert('RGB')).astype(int)
par = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_043.jpg').convert('RGB')).astype(int)
def hx(t): return '#%02X%02X%02X' % tuple(t)
r,g,b = im[:,:,0], im[:,:,1], im[:,:,2]

print('(a) wochip fill tint: child h2 q-chip center vs parent h2 q-chip center')
print('  child (663,353):', hx(im[353,663]), ' (655,350):', hx(im[350,655]), ' (670,355):', hx(im[355,670]))
print('  parent (637,457):', hx(par[457,637]), ' (630,455):', hx(par[455,630]), ' (645,458):', hx(par[458,645]))

print('(b) blue rect: right vertical + bottom rule')
navy = (np.abs(r-58)<50) & (np.abs(g-50)<50) & (np.abs(b-149)<60)
for x in range(855, 900):
    ys = np.where(navy[50:516, x])[0]
    if len(ys) > 200: print(f'  right vertical x={x}: y {50+ys.min()}..{50+ys.max()} n={len(ys)}')
for y in range(480, 516):
    xs = np.where(navy[y, 60:910])[0]
    if len(xs) > 300: print(f'  bottom rule y={y}: x {60+xs.min()}..{60+xs.max()} n={len(xs)}')

print('(c) clean swoosh: red minus chips/strip/other reds')
red = (r>150) & (g<110) & (b<110)
red[:60,:] = False; red[440:,:] = False; red[:, :75] = False; red[:, 860:] = False
for (x0,x1,y0,y1) in [(600,635,330,420),(650,690,300,420),(415,495,140,166),(240,300,335,390),(250,300,360,390)]:
    red[y0:y1, x0:x1] = False
ys, xs = np.where(red)
print('  swoosh red bbox: x', xs.min(),'..',xs.max(),' y', ys.min(),'..',ys.max(),' n=',len(xs))
# centerline samples: for x bands, mean y of red
for x0 in range(580, 820, 30):
    sel = (xs>=x0)&(xs<x0+30)
    if sel.sum()>5: print(f'  x {x0}-{x0+30}: y mean {ys[sel].mean():.0f} range {ys[sel].min()}..{ys[sel].max()}')

print('(d) red triangles under strips + gray drop lines')
for nm, xc, y0, y1 in [('h5',622,92,104),('h4',585,104,116),('h3',540,122,134),('h2',502,147,158),('h1',455,162,174)]:
    best = None
    for y in range(y0,y1):
        for x in range(xc-25, xc+25):
            rr,gg,bb = im[y,x]
            if rr>150 and gg<100 and bb<100:
                best = (x,y); break
        if best: break
    print(f'  {nm}: first red px below strip at {best}')
    # gray drop line below arrow
    if best:
        gx = best[0]
        grays = [(y2, hx(im[y2,gx])) for y2 in range(best[1]+2, min(best[1]+40, 440), 6)]
        print(f'    column x={gx} below: {grays[:6]}')

print('(e) W_k tan squares (child ~176..200, rows y226..245 etc.)')
for y in (235, 262, 289, 316):
    print(f'  row y={y}:', ' '.join(hx(im[y,x]) for x in range(170, 232, 6)))
