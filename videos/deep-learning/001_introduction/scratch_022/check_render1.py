from PIL import Image
import numpy as np
im = np.asarray(Image.open('recreated_pptx/qa/slide022/render_1.png').convert('RGB')).astype(int)
H, W = im.shape[:2]
print('render1 size:', W, H)
s = 72/150.0  # render px -> frame px
r, g, b = im[:,:,0], im[:,:,1], im[:,:,2]
lum = (r+g+b)/3
def bb(mask, x0,y0,x1,y1,label, scale=s):
    sub = mask[int(y0/s):int(y1/s), int(x0/s):int(x1/s)]
    ys, xs = np.where(sub)
    if not len(ys): print(f'{label}: none'); return
    print(f'{label}: x {x0+xs.min()*s:.1f}..{x0+xs.max()*s:.1f}  y {y0+ys.min()*s:.1f}..{y0+ys.max()*s:.1f} (frame px)')
# title zone (frame coords): expect ink x228..718 y60..88
redl = (r>120)&(g<110)&(b<110)&(r-g>40)
bb(redl, 60,46,900,95, 'title ink (gt: x228..718 y60..88)')
# aug label (gt: x300..404 y161..173)
blu = (b-r>40)&(b>100)
bb(blu, 280,150,430,185, 'aug label (gt: x300..404 y161..173)')
bb(blu, 650,150,790,185, 'wts label (gt: x670..761 y161..173)')
# case words zone (gt: Class I x615..671 y267..283 etc)
bb(blu, 600,260,760,290, 'case1 right (gt: Class I x615..671 y267..283)')
bb(blu, 600,285,760,310, 'case2 right (gt: Class II ..303)')
bb(blu, 600,308,760,332, 'case3 right (gt: Undefined Class x615..741 ..325)')
# O/P (gt x575..608 y416..428)
bb(lum<120, 560,405,625,440, 'O/P (gt: x575..608 y416..428)')
# callout lines (gt: l1 x649..798 y408..422, l2 x684..763 y426..439)
bb(lum<170, 630,400,820,424, 'callout l1 (gt: x649..798 y408..422)')
bb(lum<170, 630,424,820,445, 'callout l2 (gt: x684..763 y426..439)')
# sigma circle (gt: ring bbox x411..450 y402..439)
cy = (b-r>25)&(b>140)
bb(cy, 400,395,465,445, 'sigma circle bluish (gt: x411..450 y402..439)')
# step block purple ring (gt circle x471..507 y403..439)
pur = (b-r>25)&(r>60)&(r<200)&(g<150)
bb(pur, 455,395,525,445, 'step ring purple (gt: x471..507 y403..439)')
# black bar (gt: y518..539 x38..921)
bb(lum<60, 20,505,940,540, 'black bar (gt: x38..921 y518..539)')
# fan lines sample strip (gt: traces at x306: ys 377,393,409,~428,458,471)
col = int(306/s)
ys = [y*s for y in range(int(352/s), int(506/s)) if lum[y, col] < 235]
print('fan strip x306 (render1):', [round(y,1) for y in ys][:20])
