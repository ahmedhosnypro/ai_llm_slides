from PIL import Image
import numpy as np
im = Image.open('unique_slides/slide_059.jpg').convert('RGB')
a = np.asarray(im).astype(int)

def classify(px):
    r,g,b = px
    if abs(r-231)<12 and abs(g-233)<12 and abs(b-229)<12: return '.'
    if r>235 and g>235 and b>230: return 'W'
    if r>190 and 140<g<215 and 140<b<215 and r-g>30: return 'p'  # pale pink
    if r>200 and g<75 and b<85: return 'B'   # bar dark red core
    if 150<r<210 and 70<g<130 and 70<b<140: return 'm'  # muted red
    if r>120 and g<75 and b<85: return 'b'
    return '?'

print('--- encoder band y=288 (bar1 center) x 160..880 step 3')
print(''.join(classify(a[288,x]) for x in range(160, 880, 3)))
print('--- encoder band y=335 (title line) x 150..880 step 3')
print(''.join(classify(a[335,x]) for x in range(150, 880, 3)))
print('--- encoder band y=324 x 150..880 step 3')
print(''.join(classify(a[324,x]) for x in range(150, 880, 3)))
print('--- encoder band y=346 x 150..880 step 3')
print(''.join(classify(a[346,x]) for x in range(150, 880, 3)))
print('--- container edges y=340: x 135..175')
print([ (x, tuple(int(v) for v in a[340,x])) for x in range(135,176,2) ])
print('--- container edges y=340: x 850..895')
print([ (x, tuple(int(v) for v in a[340,x])) for x in range(850,896,2) ])
print('--- container top/bottom at x=200: y 270..282, 366..380')
print([ (y, tuple(int(v) for v in a[y,200])) for y in list(range(270,283))+list(range(366,381)) ])
print('--- word row band tint: (400,417) (500,438) (350,416) (600,439)')
for x,y in ((400,417),(500,438),(350,416),(600,439)): print((x,y), tuple(int(v) for v in a[y,x]))
print('--- gap box: vertical x=400 y 172..212')
prev=None
for y in range(172, 213):
    px = tuple(int(v) for v in a[y,400])
    if prev is None or max(abs(px[i]-prev[i]) for i in range(3))>22: print(y, px)
    prev=px
