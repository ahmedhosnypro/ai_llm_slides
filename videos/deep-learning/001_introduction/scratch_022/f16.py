from PIL import Image
import numpy as np
from collections import Counter
im = np.asarray(Image.open('unique_slides/slide_022.jpg').convert('RGB')).astype(int)
lum = (im[:,:,0]+im[:,:,1]+im[:,:,2])/3
def modal_ink(x0,y0,x1,y1,label,maxlum=150):
    reg = im[y0:y1, x0:x1].reshape(-1,3)
    ink = reg[reg.mean(axis=1) < maxlum]
    if not len(ink): print(label, 'no ink'); return
    c = Counter(map(tuple, (ink//8*8)))
    top = c.most_common(3)
    s = ' | '.join('%02X%02X%02X x%d' % (t[0][0],t[0][1],t[0][2],t[1]) for t in top)
    print(f'{label}: {s}')
modal_ink(88,158,102,174, 'aug X')
modal_ink(104,160,118,171, 'aug =')
modal_ink(118,110,142,230, 'aug vector1 ink (entries+parens)')
modal_ink(178,160,196,171, 'aug red arrow')
modal_ink(258,105,275,121, 'aug red 1')
modal_ink(220,157,252,175, 'aug X2 =')
modal_ink(559,157,580,175, 'weights W')
modal_ink(580,158,598,171, 'weights =')
modal_ink(598,104,616,122, 'weights b')
modal_ink(598,130,616,146, 'weights w1')
modal_ink(86,58,720,90, 'title')
modal_ink(88,265,525,306, 'decision eq ink (all)')
modal_ink(108,286,124,302, 'decision d(')
modal_ink(425,286,456,302, 'decision b*1')
modal_ink(500,285,524,300, 'decision big arrow')
modal_ink(555,265,745,328, 'decision cases ink', 200)
modal_ink(630,402,817,444, 'callout text', 200)
modal_ink(232,352,612,508, 'diagram box ink(all)', 200)
