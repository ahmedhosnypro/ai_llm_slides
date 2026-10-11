import numpy as np
from PIL import Image

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_023.jpg').convert('RGB')
a = np.asarray(im).astype(int)
R, G, B = a[...,0], a[...,1], a[...,2]
lum = 0.3*R + 0.6*G + 0.1*B

blue = (B > R + 60) & (B > G + 60) & (B > 120)
red = (R > G + 60) & (R > B + 60) & (R > 120)
greenl = (G > R + 25) & (G > B + 25) & (G > 110)

def bbox(m, x0, x1, y0, y1):
    sub = m[y0:y1+1, x0:x1+1]
    ys, xs = np.nonzero(sub)
    if len(ys) == 0: return None
    return (x0+int(xs.min()), x0+int(xs.max()), y0+int(ys.min()), y0+int(ys.max()), len(ys))

def blobs(m, x0, x1, y0, y1, min_px=6):
    from collections import deque
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

print('== AXES (lum<175, excluding colored) ==')
axisink = (lum < 175) & ~blue & ~red & ~greenl
print(' left horiz y246..254:', bbox(axisink, 40, 345, 246, 254))
print(' left vert  x186..205:', bbox(axisink, 186, 205, 110, 395))
print(' right horiz y246..254:', bbox(axisink, 470, 800, 246, 254))
print(' right vert  x628..648:', bbox(axisink, 628, 648, 110, 395))
print(' left axis arrowhead probe: dark rows at x60..80 (y240..260):', bbox(axisink, 55, 85, 235, 265))
print(' left vert top arrowhead x186..205 y110..135:', bbox(axisink, 186, 205, 110, 135))

print('== GREEN blobs (loose) ==')
print(' left circle x195..265 y210..255:', blobs(greenl, 195, 265, 210, 255, 5))
print(' right circle x637..710 y210..255:', blobs(greenl, 637, 710, 210, 255, 5))

print('== VECTOR LABELS ==')
print(' left b label x232..270 y145..200:', blobs(blue, 232, 270, 145, 200, 5))
print(' left a label x292..340 y195..245:', blobs(red, 292, 340, 195, 245, 5))
print(' right b label x685..730 y140..195:', blobs(blue, 685, 730, 140, 195, 5))
print(' right a label x752..800 y195..245:', blobs(red, 752, 800, 195, 245, 5))
print(' right a line end probe x720..760 y215..250:', bbox(red, 720, 760, 215, 250))
print(' left a line end probe x280..300 y210..250:', bbox(red, 280, 300, 210, 250))

print('== RED COS in bceq line2 (x298..525 y366..416) ==')
print(' red bbox:', bbox(red, 298, 525, 366, 416))
print(' red blobs:', blobs(red, 298, 525, 366, 416, 5))

print('== PANEL/CANVAS SAMPLES ==')
for x,y in [(250,415),(480,55),(700,415),(480,300),(20,20),(940,300),(480,520)]:
    print(f'  ({x},{y}):', tuple(a[y,x]))

print('== ARROW (Normalize) ==')
print(' red outline bbox x385..495 y225..280:', bbox(red, 385, 495, 225, 280))
# arrow interior rows: white fill between outline rows at x400..440
print(' red cols y229..273:', bbox(red, 385, 495, 229, 273))
print(' text (red) rows inside x395..465 y233..265:', bbox(red, 395, 465, 233, 265))
print(' arrowhead probe x455..495 y235..270:', bbox(red, 455, 495, 235, 270))

print('== TITLE ==')
redt = red.copy()
print(' title band rows x240..610 y60..100:', bbox(redt, 240, 610, 60, 100))
print(' cap R x248..268 y60..100:', bbox(redt, 248, 268, 60, 100))
