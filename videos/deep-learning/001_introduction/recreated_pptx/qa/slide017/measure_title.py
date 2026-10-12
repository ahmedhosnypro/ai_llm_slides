from PIL import Image
import numpy as np
V='/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction'
a=np.asarray(Image.open(V+'/unique_slides/slide_017.jpg').convert('RGB')).astype(int)
b=np.asarray(Image.open(V+'/unique_slides/slide_016.jpg').convert('RGB')).astype(int)

# 1) title band y60..95: find BLUE ink (B >> R) in 17
band = a[55:100, :, :]
blue = (band[:,:,2] - band[:,:,0] > 60) & (band[:,:,2] > 100)
ys, xs = np.where(blue)
if len(xs): print('17 blue title ink bbox: x', xs.min(), '..', xs.max(), ' y', ys.min()+55, '..', ys.max()+55, ' npx', len(xs))
band16 = b[55:100, :, :]
blue16 = (band16[:,:,2] - band16[:,:,0] > 60) & (band16[:,:,2] > 100)
print('16 blue title ink px:', int(blue16.sum()))

# red ink bbox in 17 title band (R >> B)
red = (band[:,:,0] - band[:,:,2] > 60) & (band[:,:,0] > 120)
ys, xs = np.where(red)
print('17 red title ink bbox: x', xs.min(), '..', xs.max(), ' y', ys.min()+55, '..', ys.max()+55)
red16 = (band16[:,:,0] - band16[:,:,2] > 60) & (band16[:,:,0] > 120)
ys16, xs16 = np.where(red16)
print('16 red title ink bbox: x', xs16.min(), '..', xs16.max(), ' y', ys16.min()+55, '..', ys16.max()+55)

# 2) Apply Model callout identical? compare region (600..710, 275..330)
ra = a[270:335, 595:715]; rb = b[270:335, 595:715]
d = (np.abs(ra-rb).max(axis=2)>40)
print('apply-model region diff px:', int(d.sum()), 'of', d.size)
