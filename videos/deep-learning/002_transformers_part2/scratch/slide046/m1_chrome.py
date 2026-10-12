from PIL import Image
import numpy as np
im = Image.open('videos/deep-learning/002_transformers_part2/unique_slides/slide_046.jpg').convert('RGB')
a = np.asarray(im).astype(int)
H, W = a.shape[:2]
print('frame size', W, H)
# gray panel E9E9E7
def mask(c, tol=12):
    return (np.abs(a - np.array(c)).max(axis=2) <= tol)
g = mask((0xE9,0xE9,0xE7), 10)
cols = g.sum(axis=0); rows = g.sum(axis=1)
xs = np.where(cols > H*0.3)[0]; ys = np.where(rows > W*0.3)[0]
print('panel gray cols span', xs.min() if len(xs) else None, xs.max() if len(xs) else None)
print('panel gray rows span', ys.min() if len(ys) else None, ys.max() if len(ys) else None)
# red border C00000 strokes (long vertical/horizontal runs)
r = mask((0xC0,0,0), 60)
rcols = r.sum(axis=0); rrows = r.sum(axis=1)
print('red col peaks (>=200):', [int(x) for x in np.where(rcols>200)[0]][:8], '...', [int(x) for x in np.where(rcols>200)[0]][-8:] if (rcols>200).any() else '')
print('red row peaks (>=300):', [int(y) for y in np.where(rrows>300)[0]][:8])
# badge: FDFD96 fill near top-right
b = mask((0xFD,0xFD,0x96), 40)
bx = np.where(b.sum(axis=0) > 5)[0]; by = np.where(b.sum(axis=1) > 5)[0]
if len(bx): print('badge-ish yellow span x', bx.min(), bx.max(), 'y', by.min(), by.max())
# purple ring 6A5ACD
p = mask((0x6A,0x5A,0xCD), 45)
px_ = np.where(p.sum(axis=0) > 2)[0]; py = np.where(p.sum(axis=1) > 2)[0]
if len(px_): print('purple ring span x', px_.min(), px_.max(), 'y', py.min(), py.max())
