from PIL import Image
import numpy as np
im = Image.open('unique_slides/slide_059.jpg').convert('RGB')
a = np.asarray(im).astype(int)
print('y=241 x 250..340 raw (1px):')
for x in range(250, 341):
    r,g,b = a[241,x]
    tag = 'n' if (r<90 and g<90 and b>85) else 'd' if (110<r<200 and g<90 and b<95 and r-g>45) else 'Y' if (r>235 and g>235 and b<215 and b>150) else 'p' if (r>230 and 150<g<225 and 150<b<225 and r-g>20) else 'g' if (g>180 and g-r>12 and g-b>12) else 'l' if (200<r<240 and 215<g<248 and b>235) else 'W' if (r>240 and g>240 and b>232) else '.'
    print(f'{x}{tag}', end=' ')
print()
print('y=487 x 175..245 raw (position row box1):')
for x in range(175, 246):
    r,g,b = a[487,x]
    tag = 'n' if (r<120 and g<120 and b>85) else 'P' if (r>235 and g>225 and b>195 and b<235) else 'o' if (r>195 and 140<g<215 and b<200 and r-b>30) else '.'
    print(f'{x}{tag}', end=' ')
print()
# palette medians of flat regions
def med(y0,y1,x0,x1,name):
    blk = a[y0:y1, x0:x1].reshape(-1,3)
    print(name, tuple(int(v) for v in np.median(blk, axis=0)))
med(450,462, 120,400, 'input container fill')
med(340,348, 200,380, 'encoder container fill')
med(283,293, 200,420, 'bar1 fill')
med(95,108, 200,400, 'tan bar fill')
med(233,242, 300,340, 'output row fill (lblue)')
med(480,490, 310,330, 'position row fill')
med(155,160, 420,430, 'pooled cell2 (green?)')
med(104,110, 500,522, 'circle2 interior (avoid cursor: x 500..522)')
med(154,160, 640,700, 'word... no; gap check')
med(97,100, 176,860, 'tan bar top strip')
med(186,192, 300,360, 'GAP box interior')
# green rect left edge: green at y=413 for x 150..260?
grn = lambda x,y: (lambda p: p[1]>120 and p[1]-p[0]>18 and p[1]-p[2]>8)(tuple(a[y,x]))
print('green presence y=413, x 150..260:', ''.join('G' if grn(x,413) else '.' for x in range(150,261)))
print('green presence y=442, x 150..260:', ''.join('G' if grn(x,442) else '.' for x in range(150,261)))
# output container left/right edge cols: lblue fill extent at y=245
lblue = lambda x,y: (lambda p: 200<p[0]<240 and 215<p[1]<248 and p[2]>238)(tuple(a[y,x]))
xs = [x for x in range(150,930) if lblue(x,245)]
print('output lblue fill x extent at y245:', min(xs), max(xs))
# word row: white box interior check at group gaps: (300,428) bluish-white measured before; gap between groups at y=428: x 275..282
print('word row y=428 x 268..284:', [tuple(int(v) for v in a[428,x]) for x in range(268,285,2)])
