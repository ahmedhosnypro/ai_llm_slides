from PIL import Image
import numpy as np
im = np.asarray(Image.open('unique_slides/slide_022.jpg').convert('RGB')).astype(int)
r, g, b = im[:,:,0], im[:,:,1], im[:,:,2]
lum = (r+g+b)/3
dark = lum < 120

def rowbands(mask, x0,y0,x1,y1,label,minpx=1,gap=1):
    sub = mask[y0:y1, x0:x1]
    rc = sub.sum(axis=1)
    bands=[]; s=None; miss=0
    for i,v in enumerate(rc):
        if v>=minpx:
            if s is None: s=i
            miss=0
        else:
            if s is not None:
                miss+=1
                if miss>gap: bands.append((y0+s, y0+i-miss)); s=None; miss=0
    if s is not None: bands.append((y0+s, y0+y1-y0-1))
    print(f'{label} rows:', bands)

def colbands(mask, x0,y0,x1,y1,label,minpx=1,gap=2):
    sub = mask[y0:y1, x0:x1]
    cc = sub.sum(axis=0)
    bands=[]; s=None; miss=0
    for i,v in enumerate(cc):
        if v>=minpx:
            if s is None: s=i
            miss=0
        else:
            if s is not None:
                miss+=1
                if miss>gap: bands.append((x0+s, x0+i-miss)); s=None; miss=0
    if s is not None: bands.append((x0+s, x0+x1-x0-1))
    print(f'{label} cols:', bands)

# brace stroke raw colors
for (x,y) in [(550,270),(551,280),(550,300),(551,320),(550,265),(552,290)]:
    print(f'brace stroke ({x},{y}):', tuple(im[y,x]))
# case line 1 first glyphs raw
print('case1 first glyph (557,275):', tuple(im[275,557]), '(560,275):', tuple(im[275,560]))

print('== AUG left vector (x84..200) ==')
rowbands(dark, 86,95,175,240, 'augL', 1)
colbands(dark, 86,95,200,240, 'augL', 1)
print('== AUG right vector (x215..300) ==')
rowbands(dark|((r>120)&(g<95)&(b<95)&(r-g>60)), 215,95,300,240, 'augR', 1)
colbands(dark, 215,95,300,240, 'augR-dark', 1)
red = (r>120)&(g<95)&(b<95)&(r-g>60)
colbands(red, 84,95,300,240, 'aug-red', 1)
rowbands(red, 84,95,300,240, 'aug-red-rows', 1)
print('== WEIGHTS vector (x555..670) ==')
rowbands(dark|red, 555,95,670,240, 'wts', 1)
colbands(dark|red, 555,95,670,240, 'wts', 1)
print('== AUG label (blue) ==')
blue = (b>130)&(b-r>60)&(b-g>40)
rowbands(blue, 295,150,420,185, 'auglabel', 1)
colbands(blue, 295,150,420,185, 'auglabel', 1)
print('== WEIGHTS label (blue) ==')
rowbands(blue, 660,150,780,185, 'wtslabel', 1)
colbands(blue, 660,150,780,185, 'wtslabel', 1)
print('== CALLOUT border scan ==')
for y in (398,399,446,447,448):
    xs = [x for x in range(615,830) if r[y,x]-g[y,x]>30 and r[y,x]>110]
    print(f'callout border row y={y}:', xs[:8], '...' if len(xs)>8 else '')
for x in (624,625,626,627,820,821,822):
    ys = [y for y in range(395,455) if r[y,x]-g[y,x]>30 and r[y,x]>110]
    print(f'callout border col x={x}:', ys[:6], '...' if len(ys)>6 else '')
print('callout text (dark-red) rows/cols:')
redd = (r>110)&(r-g>40)&(r-b>25)
rowbands(redd, 630,402,817,444, 'callout text', 1)
colbands(redd, 630,402,817,444, 'callout text', 1)
