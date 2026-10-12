from PIL import Image
import numpy as np
from scipy import ndimage

im = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_015.jpg').convert('RGB')).astype(int)

def find(color, tol, minpx, name, region=None):
    m = (np.abs(im - np.array(color)).sum(axis=2) < tol)
    if region:
        x0,x1,y0,y1 = region
        mm = np.zeros_like(m); mm[y0:y1, x0:x1] = m[y0:y1, x0:x1]; m = mm
    lab, n = ndimage.label(m)
    blobs = []
    for i, sl in enumerate(ndimage.find_objects(lab)):
        npx = (lab[sl] == i+1).sum()
        if npx >= minpx:
            blobs.append((sl[1].start, sl[1].stop, sl[0].start, sl[0].stop, npx))
    blobs.sort(key=lambda t: -t[4])
    print(f'--- {name}  target={tuple(color)} tol={tol}')
    for b in blobs[:8]:
        print(f'    x {b[0]:4d}..{b[1]:4d}  y {b[2]:4d}..{b[3]:4d}  n={b[4]}')
    return blobs

# orange input ellipse (spec F5A050)
find((241,160,80), 90, 400, 'ORANGE input ellipse')
# green key ellipse (spec 6ABF6A)
find((106,191,106), 80, 400, 'GREEN key ellipse')
# salmon card h1 (F18B96 core) — largest blob
find((241,139,150), 45, 2000, 'SALMON h1 card')
# lavender h2 (C5C1F4 / C9A8D8)
find((201,168,216), 45, 300, 'LAVENDER h2')
# yellow h3 (EDE87F)
find((237,232,127), 50, 300, 'YELLOW h3')
# green h4 (C8E6B8)
find((200,230,184), 40, 300, 'GREEN h4 card')
# peach h5 (F5CE9A)
find((245,206,154), 40, 300, 'PEACH h5')
