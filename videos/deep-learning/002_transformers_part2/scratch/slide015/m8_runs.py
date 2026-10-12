from PIL import Image
import numpy as np
im = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_015.jpg').convert('RGB')).astype(int)
def hx(t): return '#%02X%02X%02X' % tuple(t)

# sample unambiguous card-fill spots
for (nm,x,y) in [('h1 body',400,320),('h2 strip',500,166),('h3 strip',600,146),('h4 strip',700,124),
                 ('h5 strip',780,104),('h1 top strip',300,185),('h2 strip2',350,166),('h3 strip2',450,146)]:
    print(f'{nm:14s} ({x},{y}) {hx(im[y,x])}')

# scan row y=166 (h2 strip) full width, print runs of non-white/non-panel
def runs(y, x0=60, x1=910, minlen=4):
    out=[]; cur=None; start=x0
    for x in range(x0,x1):
        c = hx(im[y,x])
        cls = 'W' if im[y,x].sum()>720 else ('P' if abs(im[y,x][0]-233)+abs(im[y,x][1]-232)+abs(im[y,x][2]-231)<40 else 'C')
        if cur is None: cur=cls; start=x
        elif cls!=cur:
            if x-start>=minlen: out.append((cur,start,x-1))
            cur=cls; start=x
    out.append((cur,start,x1-1))
    return [r for r in out if r[0]!='W' or (r[2]-r[1])>2]

for y in (104,124,146,166,185,205,300,340,390,415):
    rr = runs(y)
    print(f'y={y}: ' + ' | '.join(f'{c}{a}..{b}' for c,a,b in rr))
