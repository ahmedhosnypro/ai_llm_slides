from PIL import Image
import numpy as np
from scipy import ndimage

im = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_015.jpg').convert('RGB')).astype(int)
par = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_043.jpg').convert('RGB')).astype(int)

def find(img, color, tol, minpx=200, name=''):
    m = (np.abs(img - np.array(color)).sum(axis=2) < tol)
    lab, n = ndimage.label(m)
    out = []
    for i, sl in enumerate(ndimage.find_objects(lab)):
        npx = (lab[sl] == i+1).sum()
        if npx >= minpx:
            out.append((sl[1].start, sl[1].stop, sl[0].start, sl[0].stop, npx))
    out.sort(key=lambda t: -t[4])
    print(f'--- {name} target={color} tol={tol}')
    for o in out[:6]:
        print(f'    x {o[0]:4d}..{o[1]:4d}  y {o[2]:4d}..{o[3]:4d}  n={o[4]}')
    return out

# anchors (parent geometry from component):
# q1 red bar       x205..251 y467..479   fill pure red C00000-ish
find(im,  (200, 30, 40), 130, 300, 'q1 red bar  CHILD')
find(par, (200, 30, 40), 130, 300, 'q1 red bar  PARENT')
# tan Dot Product  x195..253 y301..441  D8C0A8
find(im,  (216, 192, 168), 60, 800, 'DotProduct tan  CHILD')
find(par, (216, 192, 168), 60, 800, 'DotProduct tan  PARENT')
# scaling pill FBD8E8 x278..300 y301..441
find(im,  (251, 216, 232), 40, 500, 'Scaling pill  CHILD')
find(par, (251, 216, 232), 40, 500, 'Scaling pill  PARENT')
# softmax pill E4D8F4 x332..355 y301..441
find(im,  (228, 216, 244), 40, 400, 'Softmax pill  CHILD')
find(par, (228, 216, 244), 40, 400, 'Softmax pill  PARENT')
