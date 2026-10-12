from PIL import Image
import numpy as np
im = Image.open('videos/deep-learning/002_transformers_part2/unique_slides/slide_014.jpg').convert('RGB')
A = np.asarray(im).astype(int)

def crop(x0,y0,x1,y1): return A[y0:y1, x0:x1]

def bbox(mask, label, ox=0, oy=0):
    ys, xs = np.nonzero(mask)
    if len(xs)==0: print(f"{label}: EMPTY"); return None
    print(f"{label}: x {ox+xs.min()}..{ox+xs.max()}  y {oy+ys.min()}..{oy+ys.max()}  n={len(xs)}")
    return (ox+int(xs.min()), ox+int(xs.max()), oy+int(ys.min()), oy+int(ys.max()))

def runs1d(idx, gap=3):
    if len(idx)==0: return []
    out=[]; s=idx[0]; p=idx[0]
    for v in idx[1:]:
        if v-p>gap: out.append((int(s),int(p))); s=v
        p=v
    out.append((int(s),int(p)))
    return out

BLUE = lambda c: (c[:,:,2]-c[:,:,0]>60)&(c[:,:,2]-c[:,:,1]>50)&(c[:,:,2]>110)
WHEAT = lambda c: (abs(c[:,:,0]-242)<20)&(abs(c[:,:,1]-222)<18)&(abs(c[:,:,2]-184)<20)&(c[:,:,0]>c[:,:,1])&(c[:,:,1]>c[:,:,2])
PEACH = lambda c: (abs(c[:,:,0]-245)<16)&(abs(c[:,:,1]-203)<18)&(abs(c[:,:,2]-167)<20)
PINK = lambda c: (c[:,:,0]>230)&(abs(c[:,:,1]-182)<26)&(abs(c[:,:,2]-193)<26)&(c[:,:,0]-c[:,:,1]>45)
PGREEN = lambda c: (c[:,:,1]-c[:,:,0]>18)&(c[:,:,1]-c[:,:,2]>18)&(c[:,:,1]>215)
RED = lambda c: (c[:,:,0]>150)&(c[:,:,0]-c[:,:,1]>90)&(c[:,:,0]-c[:,:,2]>90)
DARK = lambda c: (c[:,:,0]<100)&(c[:,:,1]<100)&(c[:,:,2]<100)
YEL = lambda c: (c[:,:,0]>220)&(c[:,:,1]>210)&(c[:,:,2]<140)
LGREEN = lambda c: (abs(c[:,:,0]-144)<40)&(c[:,:,1]>210)&(abs(c[:,:,2]-144)<45)

print("=== LEFT PANEL border (crop 50..310, 90..519) ===")
c = crop(50,90,310,519)
m = BLUE(c)
cols = np.nonzero(m.sum(axis=0)>=150)[0]; print("blue cols(+50):", [int(v)+50 for v in cols])
rows = np.nonzero(m.sum(axis=1)>=150)[0]; print("blue rows(+90):", [int(v)+90 for v in rows])

print("=== DESIGN BOX wheat (crop 295..910, 95..245) ===")
c = crop(295,95,910,245)
m = WHEAT(c)
b = bbox(m, "wheat fill", 295, 95)
if b:
    rows = runs1d(np.nonzero((m.sum(axis=1)>60))[0], 3)
    print("wheat row runs(+95):", [(a+95,d+95) for a,d in rows])
    colsb = runs1d(np.nonzero(m.sum(axis=0)>60)[0], 4)
    print("wheat col runs(+295):", [(a+295,d+295) for a,d in colsb])

print("=== DESIGN BOX border (dark red 800000) (crop 295..910, 95..245) ===")
c = crop(295,95,910,245)
m = (c[:,:,0]>90)&(c[:,:,0]<170)&(c[:,:,1]<70)&(c[:,:,2]<70)
bbox(m, "maroon border", 295, 95)

print("=== SCHEMATIC container (crop 295..910, 230..519) ===")
c = crop(295,230,910,519)
m = BLUE(c)
cols = np.nonzero(m.sum(axis=0)>=150)[0]; print("blue cols(+295):", [int(v)+295 for v in cols])
rows = np.nonzero(m.sum(axis=1)>=200)[0]; print("blue rows(+230):", [int(v)+230 for v in rows])

print("=== Y rows peach (crop 300..460, 235..519) ===")
c = crop(300,235,460,519)
m = PEACH(c)
ys = np.nonzero(m.sum(axis=1)>40)[0]
print("peach row runs(+235):", [(a+235,d+235) for a,d in runs1d(ys,4)])
xs = np.nonzero(m.sum(axis=0)>10)[0]
print("peach col runs(+300):", [(a+300,d+300) for a,d in runs1d(xs,4)])

print("=== PINK X nodes (crop 40..300, 95..519) ===")
c = crop(40,95,300,519)
m = PINK(c)
ys = np.nonzero(m.sum(axis=1)>6)[0]
print("pink row runs(+95):", [(a+95,d+95) for a,d in runs1d(ys,6)])
xs = np.nonzero(m.sum(axis=0)>3)[0]
print("pink col runs(+40):", [(a+40,d+40) for a,d in runs1d(xs,6)])

print("=== MATRIX panel pale green (crop 600..910, 240..519) ===")
c = crop(600,240,910,519)
m = PGREEN(c)
bbox(m, "matrix panel fill", 600, 240)
