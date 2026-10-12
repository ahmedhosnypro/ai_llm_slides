from PIL import Image
import numpy as np
im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_020.jpg').convert('RGB')
a = np.asarray(im).astype(int)
H,W,_ = a.shape
r,g,b = a[:,:,0], a[:,:,1], a[:,:,2]
red = (r>120)&(g<100)&(b<100)&((r-g)>60)

# 1) panel border check: columns 40-45, 915-920; rows 43-48
for x in [41,42,43,917,918,919]:
    col = red[:,x]
    print(f"col {x}: red rows count={col.sum()} range={np.where(col)[0].min() if col.sum() else '-'}..{np.where(col)[0].max() if col.sum() else '-'}")
for y in [44,45,46,47]:
    row = red[y,:]
    print(f"row {y}: red cols count={row.sum()} range={np.where(row)[0].min() if row.sum() else '-'}..{np.where(row)[0].max() if row.sum() else '-'}")

# 2) badge region check (893,71) d36 -> x 875..911 y 53..89
reg = a[53:90, 875:912]
med = np.median(reg.reshape(-1,3),axis=0).astype(int)
print("badge region median:", tuple(med))
# any FDFD96-ish?
ym = (np.abs(reg - np.array([253,253,150])).max(axis=2) < 40).sum()
print("FDFD96-ish px in badge region:", ym)

# 3) title text bbox: red pixels y<100
tt = red[:100,:]
ys,xs = np.where(tt)
if len(xs): print("title red text bbox: x", xs.min(), xs.max(), "y", ys.min(), ys.max())

# 4) diagram canvas border: find long red lines
colsum = red.sum(axis=0); rowsum = red.sum(axis=1)
print("long vertical red lines (colsum>150):", [(x,int(colsum[x])) for x in np.where(colsum>150)[0]])
print("long horizontal red lines (rowsum>150):", [(y,int(rowsum[y])) for y in np.where(rowsum>150)[0]])

# 5) gray panel extent: sample E8E8E8/E9E9E7 mask
gray = (np.abs(a-np.array([233,233,231])).max(axis=2)<8)
ys,xs = np.where(gray)
print("gray panel mask bbox: x", xs.min(), xs.max(), "y", ys.min(), ys.max(), "count", len(xs))
colprof = gray.sum(axis=0)
print("gray cols>400:", np.where(colprof>400)[0].min(), np.where(colprof>400)[0].max())
rowprof = gray.sum(axis=1)
print("gray rows>600:", np.where(rowprof>600)[0].min(), np.where(rowprof>600)[0].max())
