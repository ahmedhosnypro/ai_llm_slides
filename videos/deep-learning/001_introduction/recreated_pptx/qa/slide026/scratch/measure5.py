from PIL import Image
import numpy as np
im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_026.jpg').convert('RGB')
a = np.asarray(im).astype(int)
H, W = a.shape[:2]

def bands(mask, axis, min_count, gap=2):
    rows = np.where(mask.sum(axis=axis) > min_count)[0]
    out=[]
    if len(rows):
        s=rows[0]; p=rows[0]
        for r in rows[1:]:
            if r>p+gap: out.append((int(s),int(p))); s=r
            p=r
        out.append((int(s),int(p)))
    return out

# 1. Blue vertical border lines of the container: scan columns
blue = (a[:,:,2]>110)&(a[:,:,0]<110)&(a[:,:,1]<120)
colblue = blue[120:520].sum(axis=0)   # between title and container bottom
cols = np.where(colblue > 100)[0]
print('blue-heavy cols:', cols[:20], '...' if len(cols)>20 else '')
# per-column blue row extent for the found cols
for c in cols[:6]:
    ys = np.where(blue[:,c])[0]
    print('col',c,'blue rows', ys.min(), ys.max(), 'count', len(ys))

# 2. Title bands, looser
redt = (a[:,:,0]>140)&(a[:,:,1]<130)&(a[:,:,2]<130)
bluet = (a[:,:,2]>120)&(a[:,:,0]<120)
print('red title bands:', bands(redt[:130],1,20))
print('blue title bands:', bands(bluet[:135],1,20))
for nm, m, hi in [('red',redt,130),('blue',bluet,135)]:
    for (s,e) in bands(m[:hi],1,20):
        sub = m[s:e+1]
        xs = np.where(sub.sum(axis=0)>0)[0]
        print(f'  {nm} band rows {s}..{e} x {xs.min()}..{xs.max()} count={sub.sum()}')

# 3. Red rule near top?
redm = (a[:,:,0]>130)&(a[:,:,1]<140)&(a[:,:,2]<140)
print('red bands rows 0..130:', bands(redm[:130],1,30,gap=1))

# 4. Red arrow inside tan box 1 (rows 130..220, x 250..420)
sub = redm[125:220, 250:460]
ys,xs = np.where(sub)
if len(ys): print('red arrow bbox rows', 125+ys.min(), 125+ys.max(), 'x', 250+xs.min(), 250+xs.max(), 'count', len(ys))

# 5. Blue note in tan box (rows 260..300)
sub = bluet[255:300]
ys,xs = np.where(sub)
if len(ys): print('blue note bbox rows', 255+ys.min(), 255+ys.max(), 'x', xs.min(), xs.max())

# 6. Footer row profile at y=529: black runs
row = (a[529]<70).all(axis=1)
xs = np.where(row)[0]
runs=[]
if len(xs):
    s=xs[0]; p=xs[0]
    for x in xs[1:]:
        if x>p+3: runs.append((int(s),int(p))); s=x
        p=x
    runs.append((int(s),int(p)))
print('footer black runs at y=529:', runs)
# also y=522 and y=537
for yy in (520, 525, 538):
    row = (a[yy]<80).all(axis=1)
    xs = np.where(row)[0]
    print('y',yy,'black x', (xs.min(), xs.max()) if len(xs) else None, 'count', len(xs))
