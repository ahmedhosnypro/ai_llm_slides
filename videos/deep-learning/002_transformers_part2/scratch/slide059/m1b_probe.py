from PIL import Image
import numpy as np
im = Image.open('unique_slides/slide_059.jpg').convert('RGB')
a = np.asarray(im).astype(int)
R, G, B = a[:,:,0], a[:,:,1], a[:,:,2]
red = (R > 120) & (R > G + 60) & (R > B + 60)
counts = red[100:450, :].sum(axis=0)
cols = [x for x in range(960) if counts[x] > 50]
print('cols with >50 red px:', cols[:20], '...', cols[-20:] if len(cols) > 20 else '')
rows = red[:, 200:700].sum(axis=1)
rws = [y for y in range(540) if rows[y] > 100]
print('rows with >100 red px:', rws[:10], '...', rws[-10:] if len(rws) > 10 else '')
