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

def colprof(m, x0, x1, y0, y1):
    proj = m[y0:y1+1, x0:x1+1].sum(axis=0)
    return ''.join(str(min(9,int(v))) for v in proj)

print('LEFT red line-end: col profile y200..235, x285..395:')
print(' ', colprof(red, 285, 395, 200, 235))
print('LEFT red blobs x330..400 y180..245:', blobs(red, 330, 400, 180, 245, 4))
print('LEFT blue label: blobs x196..293 y120..200:', blobs(blue, 196, 293, 120, 200, 4))
print('LEFT blue col profile y150..200 x196..293:')
print(' ', colprof(blue, 196, 293, 150, 200))
print('RIGHT red: col profile y200..235 x735..800:')
print(' ', colprof(red, 735, 800, 200, 235))
print('RIGHT red blobs x735..810 y180..245:', blobs(red, 735, 810, 180, 245, 4))
print('RIGHT red blobs above-line x690..790 y175..215:', blobs(red, 690, 790, 175, 215, 4))
print('RIGHT blue label blobs x670..740 y130..200:', blobs(blue, 670, 740, 130, 200, 4))
print()
print('RIGHT red full line col profile y210..250 x630..770 (per-8px):')
proj = red[210:251, 630:770].sum(axis=0)
print(' ', [int(proj[i:i+10].sum()) for i in range(0, 140, 10)])
print('LEFT red full line col profile y200..252 x190..360 (per-10px):')
proj = red[200:253, 190:360].sum(axis=0)
print(' ', [int(proj[i:i+10].sum()) for i in range(0, 170, 10)])
print()
print('LEFT blue full vector col profile y165..255 x190..250 (per-5px):')
proj = blue[165:256, 190:250].sum(axis=0)
print(' ', [int(proj[i:i+5].sum()) for i in range(0, 60, 5)])
print('LEFT blue row profile x196..240 y165..255 (per-5px):')
proj = blue[165:256, 196:241].sum(axis=1)
print(' ', [int(proj[i:i+5].sum()) for i in range(0, 91, 5)])
