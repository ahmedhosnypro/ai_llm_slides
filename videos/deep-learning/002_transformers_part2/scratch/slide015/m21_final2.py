from PIL import Image
import numpy as np
im = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_015.jpg').convert('RGB')).astype(int)
def hx(t): return '#%02X%02X%02X' % tuple(t)
r,g,b = im[:,:,0], im[:,:,1], im[:,:,2]
print('(1) orange ellipse interior: row y=270, x104..200 @3px:')
print('   ', ' '.join(hx(im[270,x]) for x in range(104, 201, 3)))
print('    col x=150, y214..360 @4px:')
print('   ', ' '.join(f'{y}:{hx(im[y,150])}' for y in range(214, 361, 6)))
print('(2) dark-red arrowheads under strips (r>115,g<95,b<95):')
for nm, xc, y0, y1 in [('h5',622,93,106),('h4',585,105,118),('h3',540,123,136),('h2',502,148,160),('h1',455,163,176)]:
    hits = [(x,y) for y in range(y0,y1) for x in range(xc-30, xc+30)
            if im[y,x][0]>115 and im[y,x][1]<95 and im[y,x][2]<95]
    print(f'  {nm}: {hits[:6]}{"..." if len(hits)>6 else ""} n={len(hits)}')
print('(3) parent wochip fill check (text-free spots):')
for (x,y) in [(620,450),(654,463),(620,478),(654,489)]:
    print(f'  parent ({x},{y}):', hx(__import__("numpy").asarray(par)[y,x]) if False else hx(par[y,x]), end='  ')
print()
print('    child h2 chips text-free:')
for (x,y) in [(647,347),(679,359),(647,371),(679,383),(647,395),(679,407)]:
    print(f'  child ({x},{y}):', hx(im[y,x]), end='  ')
print()
print('(4) query container border color + strip cell fills, row y=400, x186..400 @4px:')
print('   ', ' '.join(hx(im[400,x]) for x in range(186, 401, 4)))
