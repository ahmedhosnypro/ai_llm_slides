from PIL import Image
import numpy as np
im = np.asarray(Image.open('unique_slides/slide_022.jpg').convert('RGB')).astype(int)
r, g, b = im[:,:,0], im[:,:,1], im[:,:,2]
reddish = (r - g > 30) & (r - b > 20) & (r > 120)
lum = (r+g+b)/3
dark = lum < 110

def bb(mask, x0,y0,x1,y1, label):
    sub = mask[y0:y1, x0:x1]
    ys, xs = np.where(sub)
    if not len(ys): print(f'{label}: none'); return None
    res = (x0+xs.min(), y0+ys.min(), x0+xs.max(), y0+ys.max())
    print(f'{label}: x {res[0]}..{res[2]}  y {res[1]}..{res[3]}  n={len(ys)}')
    return res

# title zone
bb(reddish, 40,46,920,90, 'title reddish ink')
bb(dark, 40,46,920,90, 'title dark ink')
# panel edge scan row 270
row = im[270, 36:50]
print('panel edge y270 x36..49:', [f'{36+i}:{tuple(v)}' for i,v in enumerate(row)])
row = im[500, 36:50]
print('panel edge y500 x36..49:', [f'{36+i}:{tuple(v)}' for i,v in enumerate(row)])
col = im[40:50, 500]
print('panel top x500 y40..49:', [f'{40+i}:{tuple(v)}' for i,v in enumerate(col)])
# box borders with reddish test
for label,(x0,y0,x1,y1) in {
 'augL': (78,150,90,200), 'augT': (200,84,300,94), 'augR': (412,150,424,200), 'augB': (200,240,300,250),
 'decL': (78,280,90,320), 'decT': (300,252,400,262), 'decB': (300,336,400,346),
 'diaL': (224,400,236,470), 'diaT': (300,346,400,356), 'diaB': (300,500,400,512),
 'calL': (614,400,640,450), 'calT': (640,378,780,392), 'calB': (640,455,780,470),
}.items():
    sub = reddish[y0:y1, x0:x1]
    ys, xs = np.where(sub)
    if len(ys):
        pts = sorted(set((x0+x) for x in xs))
        rows_ = sorted(set((y0+y) for y in ys))
        print(f'{label}: reddish n={len(ys)} cols {pts[:4]}..{pts[-4:] if len(pts)>4 else ""} rows {rows_[:3]}..{rows_[-3:]}')
    else:
        print(f'{label}: no reddish')
