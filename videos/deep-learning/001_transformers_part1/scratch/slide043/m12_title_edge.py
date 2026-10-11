#!/usr/bin/env python3
"""Line-1 left edge; 1xd label region crops at 4x; small vector box crop."""
import numpy as np
from PIL import Image
im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_043.jpg').convert('RGB')
a = np.asarray(im).astype(int)
r,g,b = a[:,:,0], a[:,:,1], a[:,:,2]
lum = (r+g+b)/3
# line 1: y 54..73, find dark ink min x for x 400..700
band = lum[54:74, 400:700]
cols = np.where((band < 100).any(axis=0))[0]
print("line1 ink x-range:", 400+cols.min(), "..", 400+cols.max())
# line 2: y 80..100
band2 = lum[80:100, 500:850]
cols2 = np.where((band2 < 100).any(axis=0))[0]
print("line2 ink x-range:", 500+cols2.min(), "..", 500+cols2.max())
# yellow highlight on line 2
ylw = (r>230)&(g>230)&(b<120)
ys,xs = np.where(ylw[75:105, 500:850])
print("line2 highlight x:", 500+xs.min(),"..",500+xs.max(), " y:", 75+ys.min(),"..",75+ys.max())
# red ink on line1 (X2)
red = (r>150)&(g<110)&(b<110)
ys,xs = np.where(red[50:78, 500:900])
print("line1 red ink x:", (500+xs.min(), 500+xs.max()) if len(xs) else None, "y:", (50+ys.min(),50+ys.max()) if len(ys) else None)
# 1xd label near x 530..560 y 85..115? find red text around x 470..590 y 80..118
ys,xs = np.where(red[80:118, 460:620])
if len(xs): print("red ink near LT right:", 460+xs.min(),"..",460+xs.max(), " y:", 80+ys.min(),"..",80+ys.max())
# blue ink (dH sub) near LT
blue = (b>150)&(r<120)&(g<130)
ys,xs = np.where(blue[80:118, 460:620])
if len(xs): print("blue ink near LT right:", 460+xs.min(),"..",460+xs.max(), " y:", 80+ys.min(),"..",80+ys.max())
# crops at 4x
for name, box in [('crop_1xd', (470, 78, 600, 120)), ('crop_vecbox', (392, 42, 500, 84)), ('crop_ltbox', (315, 84, 560, 120))]:
    c = im.crop(box); c = c.resize((c.width*4, c.height*4), Image.LANCZOS)
    c.save(f'{name}.png'); print("saved", name, box, c.size)
