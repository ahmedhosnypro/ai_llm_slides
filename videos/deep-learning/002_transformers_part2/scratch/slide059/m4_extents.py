from PIL import Image
import numpy as np
from scipy import ndimage
im = Image.open('unique_slides/slide_059.jpg').convert('RGB')
a = np.asarray(im).astype(int)
R, G, B = a[:,:,0], a[:,:,1], a[:,:,2]

def vprofile_dark(y0,y1,x0,x1,thresh,name):
    # count darkish px per column -> border column positions
    cnt = ((R[y0:y1,x0:x1]<thresh[0])&(G[y0:y1,x0:x1]<thresh[1])&(B[y0:y1,x0:x1]<thresh[2])).sum(axis=0)
    cols=[x0+i for i in range(x1-x0) if cnt[i]>= (y1-y0)//2]
    print(name, 'border cols:', cols)

# 1) pooled row: dark border columns in y 150..163
vprofile_dark(150,163,340,680,(200,190,190),'pooled row')
# exact vertical extent at x=390..640: dark rows
cnt = ((R[:,380:630]<190)&(G[:,380:630]<180)&(B[:,380:630]<190)).sum(axis=1)
print('pooled dark rows 140..175:', {y:int(cnt[y]) for y in range(140,176) if cnt[y]>20})

# 2) GAP box black border
blk = (R<110)&(G<110)&(B<110)
cnt_r = blk[:, 170:860].sum(axis=1)
print('GAP black rows 170..215:', {y:int(cnt_r[y]) for y in range(170,216) if cnt_r[y]>200})
ys,xs = np.where(blk[175:212, :])
print('GAP blk bbox x', xs.min(), xs.max())
# columns of left/right border
cnt_c = blk[180:206, :].sum(axis=0)
print('GAP border cols:', [x for x in range(960) if cnt_c[x]>15])

# 3) output row light-blue fill + blue border
lblu = (abs(R-214)<20)&(abs(G-234)<20)&(abs(B-248)<20)
ys,xs = np.where(lblu[215:265,:])
print('outputrow fill bbox x', xs.min(), xs.max(), 'y', ys.min()+215, ys.max()+215, 'n', len(xs))
blue = (R<90)&(G<90)&(B>110)&(B<220)
cnt_r = blue[:, 150:900].sum(axis=1)
print('outputrow blue-border rows 215..265:', {y:int(cnt_r[y]) for y in range(215,266) if cnt_r[y]>60})

# 4) encoder container CD5C5C: x extent at y=340 (between bars)
mred = (abs(R-203)<22)&(abs(G-110)<40)&(abs(B-115)<40)&(R-G>60)
ys,xs = np.where(mred[265:380,:])
print('encoder container bbox x', xs.min(), xs.max(), 'y', ys.min()+265, ys.max()+265, 'n', len(xs))
# dark bar rows (core dark red)
dcore = (R>120)&(R<200)&(G<60)&(B<70)
cnt_r = dcore[:, 160:880].sum(axis=1)
print('encoder darkbar rows 270..380:', {y:int(cnt_r[y]) for y in range(270,381) if cnt_r[y]>200})

# 5) input container pink FADBD8
pink = (abs(R-250)<14)&(abs(G-219)<16)&(abs(B-216)<16)
ys,xs = np.where(pink[375:520,:])
print('input container fill bbox x', xs.min(), xs.max(), 'y', ys.min()+375, ys.max()+375, 'n', len(xs))

# 6) word row green dashed border 009900
grn = (G>110)&(G<190)&(R<110)&(B<110)
cnt_r = grn[:, 100:900].sum(axis=1)
print('green rows 400..450:', {y:int(cnt_r[y]) for y in range(400,451) if cnt_r[y]>60})
ys,xs = np.where(grn[400:450,:])
print('green border bbox x', xs.min(), xs.max())

# 7) position row orange dashed border E67E22
org = (R>190)&(abs(G-120)<45)&(B<90)
cnt_r = org[:, 100:900].sum(axis=1)
print('orange rows 460..515:', {y:int(cnt_r[y]) for y in range(460,516) if cnt_r[y]>60})
ys,xs = np.where(org[460:515,:])
print('orange border bbox x', xs.min(), xs.max())
