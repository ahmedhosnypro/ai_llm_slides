from PIL import Image
import numpy as np
im = np.asarray(Image.open('recreated_pptx/qa/slide022/render_1.png').convert('RGB')).astype(int)
s = 72/150.0
r, g, b = im[:,:,0], im[:,:,1], im[:,:,2]
lum = (r+g+b)/3
def bb(mask, x0,y0,x1,y1,label):
    sub = mask[int(y0/s):int(y1/s), int(x0/s):int(x1/s)]
    ys, xs = np.where(sub)
    if not len(ys): print(f'{label}: none'); return None
    res=(x0+xs.min()*s, y0+ys.min()*s, x0+xs.max()*s, y0+ys.max()*s)
    print(f'{label}: x {res[0]:.1f}..{res[2]:.1f}  y {res[1]:.1f}..{res[3]:.1f}  (w {res[2]-res[0]:.1f} h {res[3]-res[1]:.1f})')
    return res
blackish = (lum<120)&(r<130)&(g<130)&(b<130)
redl = (r>120)&(g<110)&(b<110)&(r-g>40)
blu = (b-r>40)&(b>100)
bb(redl, 150,50,850,86, 'title (gt x228..718 y60..~82bl)')
bb(blu, 290,155,420,180, 'aug label (gt x300..404 y161..176)')
bb(blu, 660,155,780,180, 'wts label (gt x670..761 y161..176)')
bb(blu, 605,264,680,286, 'Class I (gt x615..671 y267..283)')
bb(blu, 605,286,680,308, 'Class II (gt x615..672 y289..305)')
bb(blu, 605,308,760,330, 'Undefined Class (gt x615..741 y311..327)')
bb(blackish, 576,410,620,434, 'O/P black (gt x575..608 y416..428)')
bb(blackish, 640,402,808,423, 'callout l1 (gt x649..798 y408..422)')
bb(blackish, 640,424,808,443, 'callout l2 (gt x684..763 y426..439)')
# vectors: X1 ink (gt x88..101 y159..173), paren spans (gt v1 y112..227)
bb(blackish, 80,150,120,180, 'X1 (gt x88..101 y159..173)')
bb(blackish, 110,100,150,235, 'v1 region (gt parens x117/x140 y112..227)')
bb(blackish, 550,150,600,180, 'W1 (gt x561..578 y159..173)')
