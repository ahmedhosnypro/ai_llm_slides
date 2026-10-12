from PIL import Image
import numpy as np
im = np.asarray(Image.open('unique_slides/slide_022.jpg').convert('RGB')).astype(int)
r, g, b = im[:,:,0], im[:,:,1], im[:,:,2]
lum = (r+g+b)/3
dark   = lum < 120
red    = (r>120)&(g<95)&(b<95)&(r-g>60)
blue   = (b>130)&(b-r>60)&(b-g>40)
cyan   = (b>200)&(g>190)&(r<190)&(b-r>40)
pink   = (r>200)&(b>140)&(g<190)&(r-b>20)&(r-g>40)

def bb(mask, x0,y0,x1,y1,label):
    sub = mask[y0:y1, x0:x1]
    ys, xs = np.where(sub)
    if not len(ys): print(f'{label}: none'); return
    print(f'{label}: x {x0+xs.min()}..{x0+xs.max()}  y {y0+ys.min()}..{y0+ys.max()}  n={len(ys)}')

def rowbands(mask, x0,y0,x1,y1,label,minpx=2):
    sub = mask[y0:y1, x0:x1]
    rc = sub.sum(axis=1)
    bands=[]; s=None
    for i,v in enumerate(rc):
        if v>=minpx and s is None: s=i
        elif v<minpx and s is not None: bands.append((y0+s, y0+i-1)); s=None
    if s is not None: bands.append((y0+s, y0+y1-y0-1))
    print(f'{label} row bands:', bands)

def colbands(mask, x0,y0,x1,y1,label,minpx=2):
    sub = mask[y0:y1, x0:x1]
    cc = sub.sum(axis=0)
    bands=[]; s=None
    for i,v in enumerate(cc):
        if v>=minpx and s is None: s=i
        elif v<minpx and s is not None: bands.append((x0+s, x0+i-1)); s=None
    if s is not None: bands.append((x0+s, x0+x1-x0-1))
    print(f'{label} col bands:', bands[:20])

print('== TITLE ==')
bb(dark|red, 62,46,900,88, 'title ink (excl borders)')
rowbands(dark|red, 62,46,900,88, 'title')

print('== AUG BOX (x84..417 y90..244) ==')
bb(dark, 84,90,418,245, 'aug black ink')
bb(red, 84,90,418,245, 'aug red ink')
bb(blue, 84,90,418,245, 'aug blue ink')
rowbands(dark|red, 84,92,340,244, 'aug eq rows (left of label)')
colbands(dark, 84,92,340,244, 'aug eq cols', 1)

print('== WEIGHTS BOX (x530..791 y90..244) ==')
bb(dark, 530,90,792,245, 'weights black ink')
bb(red, 530,90,792,245, 'weights red ink')
bb(blue, 530,90,792,245, 'weights blue ink')
rowbands(dark|red, 530,92,660,244, 'weights eq rows')
colbands(dark|red, 530,92,660,244, 'weights eq cols', 1)

print('== DECISION BOX (x83..765 y257..340) ==')
bb(dark, 83,257,766,341, 'dec black ink')
bb(red, 83,257,766,341, 'dec red ink')
bb(blue, 83,257,766,341, 'dec blue ink')
rowbands(dark|red|blue, 83,257,766,341, 'dec rows')
colbands(dark, 83,257,766,341, 'dec black cols', 1)

print('== CALLOUT (right of diagram box) ==')
bb(red, 614,350,900,520, 'callout red ink (border+text)')
bb(dark, 614,350,900,520, 'callout dark ink')
# find callout fill bbox: tan-ish
tan = (np.abs(r-226)<14)&(np.abs(g-224)<14)&(np.abs(b-195)<18)
bb(tan, 600,350,900,520, 'callout tan fill')
rowbands(tan, 600,350,900,520, 'callout fill rows', 30)
colbands(tan, 600,350,900,520, 'callout fill cols', 10)
