from PIL import Image
import numpy as np
im = np.asarray(Image.open('unique_slides/slide_022.jpg').convert('RGB')).astype(int)
r, g, b = im[:,:,0], im[:,:,1], im[:,:,2]
lum = (r+g+b)/3
# brace bar precise: scan rows for the darkest pixel in x544..560
for y in (270, 290, 310, 320):
    seg = [(x, tuple(im[y,x]), round(lum[y,x])) for x in range(544,562)]
    dk = [s for s in seg if s[2] < 240]
    print(f'y={y} brace-zone nonbg:', dk)
# callout border at fill edges
for y in (399,400,401,444,445,446):
    xs = [x for x in range(620,830) if r[y,x]-g[y,x]>25 and r[y,x]>110]
    if xs: print(f'callout red row y={y}:', xs[:10])
for x in (626,627,628,629,630,817,818,819,820):
    ys = [y for y in range(395,452) if r[y,x]-g[y,x]>25 and r[y,x]>110]
    if ys: print(f'callout red col x={x}:', ys[:10])
# blue darkest
reg = im[158:178, 298:408].reshape(-1,3)
bl = reg[reg[:,2]-reg[:,0] > 40]
bl2 = bl[np.argsort(bl.mean(axis=1))][:12]
print('aug label darkest blue px:', [tuple(v) for v in bl2])
reg = im[262:330, 552:748].reshape(-1,3)
bl = reg[reg[:,2]-reg[:,0] > 40]
bl2 = bl[np.argsort(bl.mean(axis=1))][:12]
print('cases darkest blue px:', [tuple(v) for v in bl2])
# sigma ring raw
print('sigma ring top y404:', [tuple(im[404,x]) for x in range(424,444,4)])
print('sigma ring left x414:', [tuple(im[y,414]) for y in range(412,432,4)])
print('circle2 ring y406:', [tuple(im[406,x]) for x in range(474,506,4)])
print('circle2 fill (482,425):', tuple(im[425,482]), '(490,410):', tuple(im[410,490]))
# fan lines: vertical strip scans
for x in (330, 350, 370, 385):
    ys = [y for y in range(354,506) if lum[y,x] < 235 and abs(r[y,x]-b[y,x])<60]
    # group
    out=[]; 
    for y in ys:
        if out and y-out[-1][-1]<=2: out[-1].append(y)
        else: out.append([y])
    print(f'fan strip x={x}:', [(o[0],o[-1]) for o in out])
# junction blob colors
print('junction core (400,421):', tuple(im[421,400]), '(398,420):', tuple(im[420,398]))
