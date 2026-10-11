import numpy as np
from PIL import Image
from collections import deque

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_023.jpg').convert('RGB')
a = np.asarray(im).astype(int)
R, G, B = a[...,0], a[...,1], a[...,2]
blue = (B > R + 60) & (B > G + 60) & (B > 120)
red = (R > G + 60) & (R > B + 60) & (R > 120)

def blobs(m, x0, x1, y0, y1, min_px=5):
    sub = m[y0:y1+1, x0:x1+1].copy()
    h, w = sub.shape
    seen = np.zeros((h,w), bool)
    out = []
    for yy in range(h):
        for xx in range(w):
            if sub[yy,xx] and not seen[yy,xx]:
                q = deque([(yy,xx)]); seen[yy,xx]=True; pts=[]
                while q:
                    y,x = q.popleft(); pts.append((y,x))
                    for dy in (-2,-1,0,1,2):
                        for dx in (-2,-1,0,1,2):
                            ny,nx = y+dy,x+dx
                            if 0<=ny<h and 0<=nx<w and sub[ny,nx] and not seen[ny,nx]:
                                seen[ny,nx]=True; q.append((ny,nx))
                if len(pts)>=min_px:
                    py=[p[0] for p in pts]; px_=[p[1] for p in pts]
                    out.append((x0+min(px_),x0+max(px_),y0+min(py),y0+max(py),len(pts)))
    return sorted(out, key=lambda b:-b[4])

print('LEFT circle ALL blue blobs (x100..290, y125..372):')
for b in blobs(blue, 100, 290, 125, 372, 6): print('  ', b)
print('RIGHT circle ALL blue blobs (x560..738, y125..372):')
for b in blobs(blue, 560, 738, 125, 372, 6): print('  ', b)
print('LEFT circle ALL red blobs (x100..380, y125..372):')
for b in blobs(red, 100, 380, 125, 372, 6): print('  ', b)
print('RIGHT circle ALL red blobs (x560..790, y125..372):')
for b in blobs(red, 560, 790, 125, 372, 6): print('  ', b)
# sample the blue of the vector vs label to compare shades
print('blue px shades: line(210,230):', tuple(a[230,210]), ' label R(690,155):', tuple(a[155,690]))
print('red px shades: line(250,240):', tuple(a[240,250]), ' label L(349,207):', tuple(a[207,349]))
