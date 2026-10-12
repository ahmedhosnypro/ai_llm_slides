from PIL import Image
import numpy as np
im = Image.open('videos/deep-learning/002_transformers_part2/unique_slides/slide_046.jpg').convert('RGB')
a = np.asarray(im).astype(int)
H, W = a.shape[:2]
# red-ish mask (broad: R high, G/B low)
red = (a[:,:,0] > 120) & (a[:,:,1] < 90) & (a[:,:,2] < 90)
rcols = red.sum(axis=0); rrows = red.sum(axis=1)
print('vertical red lines (cols with >150 red px):', [int(x) for x in np.where(rcols > 150)[0]])
print('horizontal red lines (rows with >300 red px):', [int(y) for y in np.where(rrows > 300)[0]])
# badge zone: slide-pts center (893,71) -> approx frame (876,68). Crop 840..915, 30..105
crop = a[30:110, 840:915]
# purple ring
pur = (np.abs(crop[:,:,0]-0x6A)<40) & (np.abs(crop[:,:,1]-0x5A)<40) & (np.abs(crop[:,:,2]-0xCD)<40)
ys, xs = np.where(pur)
if len(xs): print('badge purple bbox in frame coords: x', xs.min()+840, xs.max()+840, ' y', ys.min()+30, ys.max()+30, ' center', (xs.min()+xs.max())/2+840, (ys.min()+ys.max())/2+30)
# yellow badge fill
yel = (crop[:,:,0]>220)&(crop[:,:,1]>220)&(crop[:,:,2]<160)
ys2, xs2 = np.where(yel)
if len(xs2): print('badge yellow bbox: x', xs2.min()+840, xs2.max()+840, ' y', ys2.min()+30, ys2.max()+30)
# check bottom red stroke rows near 538-539 slide -> frame ~514?
print('red rows 505..540 counts:', {int(y): int(rrows[y]) for y in range(505, 540) if rrows[y] > 50})
