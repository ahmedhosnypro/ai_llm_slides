import numpy as np
from PIL import Image

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_023.jpg').convert('RGB')
a = np.asarray(im).astype(int)
H, W = a.shape[:2]
R, G, B = a[...,0], a[...,1], a[...,2]

red = (R > G + 60) & (R > B + 60) & (R > 120)
blue = (B > R + 60) & (B > G + 60) & (B > 120)
green = (G > R + 50) & (G > B + 50) & (G > 100)
dark = (R < 130) & (G < 130) & (B < 130)

def runs_of(idx):
    idx = list(idx)
    if not idx: return []
    out=[]; s=idx[0]; p=idx[0]
    for i in idx[1:]:
        if i > p+1: out.append((int(s),int(p))); s=i
        p=i
    out.append((int(s),int(p)))
    return out
def bands_y(m,x0,x1,mino=1):
    proj = m[:, x0:x1+1].sum(axis=1); return runs_of(np.nonzero(proj>mino)[0])
def bands_x(m,y0,y1,mino=1):
    proj = m[y0:y1+1, :].sum(axis=0); return runs_of(np.nonzero(proj>mino)[0])

def px(x,y): return tuple(a[y,x])

print('== badge pixel probe (around 893,71):')
for y in (50,55,60,65,70,75,80,85,88):
    print('  row',y, [px(x,y) for x in (875,885,893,900,910)])

print('== title cols (y67..94):', bands_x(red,67,94,1))
print('== maxbox border probe: col scan x110..115, rows 495..535')
for x in (110,112,114,116):
    print('  x',x,[px(x,y) for y in (497,500,505,515,525,530,533)])
print('   row scan y496..500 at x300:', [px(300,y) for y in range(494,502)])
print('== lossbox border probe x566..572 y500..532:', [px(567,y) for y in (500,510,520,530)])

print('== CIRCLES: pale-yellow fill mask')
yel = (R>240)&(G>240)&(B>170)&(B<225)
# left circle bbox
m = yel.copy(); m[:, 340:] = False
ys,xs = np.nonzero(m)
print('  left circle bbox x%d..%d y%d..%d'%(xs.min(),xs.max(),ys.min(),ys.max()))
m2 = yel.copy(); m2[:, :450] = False
ys2,xs2 = np.nonzero(m2)
print('  right circle bbox x%d..%d y%d..%d'%(xs2.min(),xs2.max(),ys2.min(),ys2.max()))

print('== left circle inks (window x60..330, y120..380):')
win = (slice(120,380), slice(60,330))
print('  blue rows:', bands_y(blue[win[0],win[1]],0,269,2), 'cols:', bands_x(blue[win[0],win[1]],0,259,2))
print('  red rows:', bands_y(red[win[0],win[1]],0,269,2), 'cols:', bands_x(red[win[0],win[1]],0,259,2))
print('  green rows:', bands_y(green[win[0],win[1]],0,269,2), 'cols:', bands_x(green[win[0],win[1]],0,259,2))
print('  dark rows:', bands_y(dark[win[0],win[1]],0,269,3), 'cols:', bands_x(dark[win[0],win[1]],0,259,3))

print('== right circle inks (window x500..770, y120..380):')
win2 = (slice(120,380), slice(500,770))
print('  blue rows:', bands_y(blue[win2[0],win2[1]],0,269,2), 'cols:', bands_x(blue[win2[0],win2[1]],0,269,2))
print('  red rows:', bands_y(red[win2[0],win2[1]],0,269,2), 'cols:', bands_x(red[win2[0],win2[1]],0,269,2))
print('  green rows:', bands_y(green[win2[0],win2[1]],0,269,2), 'cols:', bands_x(green[win2[0],win2[1]],0,269,2))
print('  dark rows:', bands_y(dark[win2[0],win2[1]],0,269,3), 'cols:', bands_x(dark[win2[0],win2[1]],0,269,3))

print('== normalize arrow (red outline) x380..500 y225..280:')
print('  red rows:', bands_y(red,380,500,3))
print('  red cols:', bands_x(red,228,278,3))

print('== equation ink bands (dark ink) inside boxes:')
dk = (R<150)&(G<150)&(B<150)
print('  treq box x742..914 y82..185: dark rows', bands_y(dk,744,912,3))
print('  bceq box x296..527 y324..425: dark rows', bands_y(dk,298,525,3))
print('  aftnorm box x750..907 y316..378: dark rows', bands_y(dk,752,905,3))
print('  cyanbar x58..860 y436..486: dark rows', bands_y(dk,60,858,3))
print('  cyanbar blue rows:', bands_y(blue,60,858,3))
print('  maxbox x114..523 y500..530: dark rows', bands_y(dk,116,521,3))
print('  lossbox x571..761 y501..530: dark rows', bands_y(dk,573,759,3))
