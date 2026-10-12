from PIL import Image
import numpy as np
V='/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction'
a=np.asarray(Image.open(V+'/unique_slides/slide_017.jpg').convert('RGB')).astype(int)
b=np.asarray(Image.open(V+'/unique_slides/slide_016.jpg').convert('RGB')).astype(int)

def edge_profile(img, tag):
    # border ink C2C4C2 (~194,196,194): darker than fill E6E8E6 (230)
    reg = img[275:335, 600:720]
    dark = reg.sum(axis=2) < 640   # border+text ink
    colsum = dark.sum(axis=0); rowsum = dark.sum(axis=1)
    cols = [600+x for x,c in enumerate(colsum) if c>18]
    rows = [275+y for y,c in enumerate(rowsum) if c>28]
    print(tag, 'border cols:', cols[:6], '...', cols[-6:] if len(cols)>6 else '')
    print(tag, 'border rows:', rows[:6], '...', rows[-6:] if len(rows)>6 else '')
edge_profile(a, '17')
edge_profile(b, '16')
# text ink bands inside apply box (y282..323, x613..700)
def textband(img, tag, y0,y1,x0,x1):
    reg = img[y0:y1, x0:x1]
    ink = reg.sum(axis=2) < 300
    rows = ink.sum(axis=1)
    bands=[]; inr=False
    for y,c in enumerate(rows):
        if c>2 and not inr: s=y; inr=True
        if c<=2 and inr: bands.append((y0+s, y0+y-1)); inr=False
    if inr: bands.append((y0+s, y0+len(rows)-1))
    print(tag, 'text bands:', bands)
textband(a, '17', 282, 330, 613, 701)
textband(b, '16', 282, 330, 613, 701)
