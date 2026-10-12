from PIL import Image
import numpy as np
im = Image.open('unique_slides/slide_059.jpg').convert('RGB')
a = np.asarray(im).astype(int)
R, G, B = a[:,:,0], a[:,:,1], a[:,:,2]
red = (R > 110) & (R > G + 45) & (R > B + 45)
# left/right border columns: y 150..250 (above the encoder container, below title area)
sub = red[150:250, :]
cnt = sub.sum(axis=0)
cand = [x for x in range(960) if cnt[x] > 30]
print('border cols in y150..250:', cand)
# top border rows: x 150..800
sub2 = red[:, 150:800]
cnt2 = sub2.sum(axis=1)
print('rows y<60 red counts:', {y: int(cnt2[y]) for y in range(30, 60) if cnt2[y] > 10})
print('rows y>460 red counts:', {y: int(cnt2[y]) for y in range(460, 540) if cnt2[y] > 10})
