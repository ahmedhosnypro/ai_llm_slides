from PIL import Image
import numpy as np
im = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_015.jpg').convert('RGB')).astype(int)
r,g,b = im[:,:,0], im[:,:,1], im[:,:,2]

# (a) plane-over-salmon: salmon darkened+desaturated: expect ~(206,145,151)
pos = (np.abs(r-206)<22) & (np.abs(g-145)<22) & (np.abs(b-151)<22)
print('plane-over-salmon rows:')
for y in range(150, 235, 8):
    xs = np.where(pos[y])[0]
    if len(xs)>4:
        d = np.split(xs, np.where(np.diff(xs)>8)[0]+1)
        seg = max(d, key=len)
        print(f'  y={y}: x {seg.min()}..{seg.max()} n={len(seg)}')
# plane-over-lavender ~ (0.6*197+61, 0.6*193+61, 0.6*244+61) = (179,177,207)
pol = (np.abs(r-179)<18) & (np.abs(g-177)<18) & (np.abs(b-207)<18)
for y in range(150, 200, 8):
    xs = np.where(pol[y])[0]
    if len(xs)>4: print(f'  plane-over-lav y={y}: x {xs.min()}..{xs.max()} n={len(xs)}')

# (b) blue inner rectangle: verticals at x~73 / x~893, bottom ~y500
navy = (np.abs(r-58)<45) & (np.abs(g-50)<45) & (np.abs(b-149)<55)
for x in (72,73,74,891,892,893,894):
    ys = np.where(navy[45:516, x])[0]
    if len(ys)>50: print(f'navy vertical x={x}: y {45+ys.min()}..{45+ys.max()} n={len(ys)}')
for y in (498,500,502,504):
    xs = np.where(navy[y])[0]
    if len(xs)>50: print(f'navy horiz y={y}: x {xs.min()}..{xs.max()} n={len(xs)}')

# (c) strip bboxes
def bbox(mask):
    ys, xs = np.where(mask)
    return (xs.min(), xs.max(), ys.min(), ys.max(), len(xs)) if len(xs) else None
zones = {'h5 peach': ((np.abs(r-250)<25)&(np.abs(g-220)<25)&(np.abs(b-192)<28), 500,700,60,95),
         'h4 green': ((np.abs(r-140)<70)&(np.abs(g-225)<40)&(np.abs(b-100)<60), 480,680,84,106),
         'h3 yellow': ((r>215)&(g>225)&(b<80), 440,640,102,128),
         'h2 olive': ((np.abs(r-122)<25)&(np.abs(g-128)<25)&(np.abs(b-92)<25), 420,560,124,148),
         'h1 brick': ((r>150)&(r<210)&(g>55)&(g<95)&(b<40), 400,520,144,166)}
for nm,(m,x0,x1,y0,y1) in zones.items():
    mm = np.zeros_like(m); mm[y0:y1, x0:x1] = m[y0:y1, x0:x1]
    print(f'{nm}: {bbox(mm)}')

# (e) hlabel: blue italic text zone (parent 612..708,392..408 -> child ~638..730, 290..306)
blue = (b>120) & (b-r>50) & (b-g>30)
mm = np.zeros_like(blue); mm[280:320, 600:780] = blue[280:320, 600:780]
print('hlabel blue ink:', bbox(mm))
