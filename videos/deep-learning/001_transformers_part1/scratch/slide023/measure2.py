import numpy as np
from PIL import Image

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_023.jpg').convert('RGB')
a = np.asarray(im).astype(int)
H, W = a.shape[:2]
R, G, B = a[...,0], a[...,1], a[...,2]

red = (R > G + 60) & (R > B + 60) & (R > 120)
blue = (B > R + 60) & (B > G + 60) & (B > 120)
green = (G > R + 50) & (G > B + 50) & (G > 100)
dark = (R < 120) & (G < 120) & (B < 120)

def runs_of(idx):
    idx = list(idx)
    if not idx: return []
    out = []; s = idx[0]; p = idx[0]
    for i in idx[1:]:
        if i > p + 1:
            out.append((int(s), int(p))); s = i
        p = i
    out.append((int(s), int(p)))
    return out

def bands_y(m, x0, x1, min_run=2):
    proj = m[:, x0:x1+1].sum(axis=1)
    return [r for r in runs_of(np.nonzero(proj >= min_run)[0])]

def bands_x(m, y0, y1, min_run=2):
    proj = m[y0:y1+1, :].sum(axis=0)
    return [r for r in runs_of(np.nonzero(proj >= min_run)[0])]

print('== TITLE (red ink, y 40..110):')
print('  rows:', bands_y(red, 200, 640, 2))
ty = bands_y(red, 200, 640, 2)
if ty:
    print('  cols:', bands_x(red, ty[0][0], ty[-1][1], 1))

print('== BADGE (yellowish x 850..940):')
yel = (R > 220) & (G > 220) & (B < 190)
print('  rows:', bands_y(yel, 850, 940, 3))
print('  cols:', bands_x(yel, 40, 110, 2))

print('== WHITE BOXES borders (blue):')
print('  callout rows y90..190 x300..530:', bands_y(blue, 300, 530, 30))
print('  callout cols x280..545 y110..170:', bands_x(blue, 110, 170, 20))
print('  treq rows y70..195 x750..900:', bands_y(blue, 750, 900, 30))
print('  treq cols x730..930 y90..180:', bands_x(blue, 90, 180, 20))
print('  bceq rows y310..440 x300..520:', bands_y(blue, 300, 520, 30))
print('  bceq cols x280..545 y330..425:', bands_x(blue, 330, 425, 20))
print('  aftnorm rows y300..395 x750..900:', bands_y(blue, 750, 900, 30))
print('  aftnorm cols x730..930 y320..380:', bands_x(blue, 320, 380, 20))
print('  cyanbar rows y420..500 x60..860:', bands_y(blue, 60, 860, 30))
print('  cyanbar cols x40..880 y445..485:', bands_x(blue, 445, 485, 20))

print('== RED BOX BORDERS (maximize/loss):')
print('  rows y490..540 x120..510:', bands_y(red, 120, 510, 30))
print('  cols x100..540 y505..530:', bands_x(red, 505, 530, 20))
print('  loss rows y490..540 x580..750:', bands_y(red, 580, 750, 30))
print('  loss cols x555..790 y505..530:', bands_x(red, 505, 530, 20))
