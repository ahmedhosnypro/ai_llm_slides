from PIL import Image
import numpy as np
im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_048.jpg').convert('RGB')
W,H = im.size
a = np.asarray(im).astype(int)
R,G,B = a[...,0],a[...,1],a[...,2]
# loose washed-red: pinkish over white/gray
loose = ((R-G)>28)&((R-B)>28)&(R>150)
rc = loose.sum(axis=1)
print('rows with >300 loose-red px:')
for r in range(H):
    if rc[r]>300:
        xs=np.nonzero(loose[r,:])[0]; print(f'  row {r}: n={rc[r]} x {xs.min()}..{xs.max()}')
cc = loose.sum(axis=0)
print('cols with >300 loose-red px:')
for c in range(W):
    if cc[c]>300:
        ys=np.nonzero(loose[:,c])[0]; print(f'  col {c}: n={cc[c]} y {ys.min()}..{ys.max()}')
# gray panel extent: modal gray ~231-234
gray = (abs(R-232)<8)&(abs(G-233)<8)&(abs(B-231)<8)
print('gray panel: rows where gray spans wide:')
for r in [44,46,50,300,510,515,517,518]:
    xs=np.nonzero(gray[r,:])[0]
    print(f'  row {r}: n={len(xs)}', f'x {xs.min()}..{xs.max()}' if len(xs) else '')
for c in [30,40,44,46,48,52,58,900,910,915,918,920,925]:
    ys=np.nonzero(gray[:,c])[0]
    print(f'  col {c}: n={len(ys)}', f'y {ys.min()}..{ys.max()}' if len(ys) else '')
