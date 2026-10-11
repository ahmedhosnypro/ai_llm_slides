#!/usr/bin/env python3
# Pre-judge self-check, slide 004 attempt 2 (chrome rebuilt to playlist law; shared module).
# Checks: house_chrome_check.py (run separately: PASS), (2) containment, (6) crop measurements,
# (7) wrap, (8) lineSpacing pin + XML. N/A: (3) equations, (4) multi-line delimiters, (5) tables.
from PIL import Image
import numpy as np, zipfile, re
K = 2001/960
ren = np.array(Image.open('videos/deep-learning/001_transformers_part1/recreated_pptx/qa/slide004/render_2.png').convert('RGB')).astype(int)
orig = np.array(Image.open('videos/deep-learning/001_transformers_part1/unique_slides/slide_004.jpg').convert('RGB')).astype(int)
r,g,b = ren[:,:,0], ren[:,:,1], ren[:,:,2]
blue = (b-np.maximum(r,g)>45)&(b>110); yellow = (r>200)&(g>200)&(b<190); red = (r>150)&(g<100)&(b<100)

# border positions per law: x 42..918px, y 45px..bottom (72dpi)
print('== CHROME positions (law: panel x42..918, y45..bottom; badge circle d36 @ (893,71)) ==')
print(f'  left border col: {np.where(red[560,:])[0].min()/K:.1f} (law ~42)')
print(f'  right border col: {np.where(red[560,:])[0].max()/K:.1f} (law ~918)')
print(f'  top border row: {np.where(red[:,1000])[0].min()/K:.1f} (law ~45)')
print(f'  bottom border row: {np.where(red[:,1000])[0].max()/K:.1f} (law ~538-539, half-visible)')
pys,pxs = np.where(yellow)
print(f'  badge fill bbox: x {pxs.min()/K:.1f}..{pxs.max()/K:.1f} y {pys.min()/K:.1f}..{pys.max()/K:.1f} (law circle x875..911 y53..89)')

print('== SELF-CHECK 2: FRAME CONTAINMENT ==')
content = ((r>140)&(g<110)&(b<110)) | ((b-np.maximum(r,g)>45)&(b>110)) | ((r>200)&(g>200)&(b<190)) | ((r<130)&(g<130)&(b<130))
cm = content.copy()
for c in (89,1913): cm[:, max(0,c-4):c+5] = False
for rw in (95,1121): cm[max(0,rw-4):rw+5, :] = False
outside_ok = (cm[:90,110:1900].sum()==0 and cm[1126:,:].sum()==0 and cm[:, :84].sum()==0 and cm[:,1920:].sum()==0)
print(f'  ink in outside bands -> {"PASS" if outside_ok else "FAIL"}')
border_left = min(x for x in range(1890,1930) if red[560,x])
gap_r = (border_left - pxs.max())/K
print(f'  badge right {pxs.max()/K:.1f} vs border left {border_left/K:.1f}: gap {gap_r:.1f}px -> {"PASS" if gap_r>2 else "FAIL"}')

print('== SELF-CHECK 6: dense-region crop measurements (crops re-made below) ==')
bl = blue.copy(); bl[:,1770:1925]=False
rows = bl.sum(axis=1); bands=[]; inb=False
for y,v in enumerate(rows):
    if v>4 and not inb: s0=y; inb=True
    elif v<=4 and inb: bands.append((s0,y-1)); inb=False
bands=[(a2,b2) for a2,b2 in bands if b2-a2>10]
for i,(a2,b2) in enumerate(bands):
    xs = np.where(bl[a2:b2+1].any(axis=0))[0]
    print(f'  body L{i+1}: y {a2/K:.1f}..{b2/K:.1f}, x {xs.min()/K:.1f}..{xs.max()/K:.1f} (orig 342..372 / 422..452, x 89..857 / 89..644)')
sub = ren[pys.min():pys.max()+1, pxs.min():pxs.max()+1]
dark = sub[:,:,0]<160
dys,dxs = np.where(dark)
print(f'  numeral: x {(pxs.min()+dxs.min())/K:.1f}..{(pxs.min()+dxs.max())/K:.1f} y {(pys.min()+dys.min())/K:.1f}..{(pys.min()+dys.max())/K:.1f} (orig ink x885..897 y68..78; law: 18pt bold 333333 in d36 circle)')
tm = red[280:660, 200:1800]; tys,txs = np.where(tm)
print(f'  title ink: x {(200+txs.min())/K:.1f}..{(200+txs.max())/K:.1f}, y {(280+tys.min())/K:.1f}..{(280+tys.max())/K:.1f} (orig 146..788 / 200..247; x centered per spec, orig ink center 467)')

print('== SELF-CHECK 7: WRAP ==')
print(f'  body bands {len(bands)} (expect 2) -> {"PASS" if len(bands)==2 else "FAIL"}')

print('== SELF-CHECK 8: LINE SPACING PIN ==')
pitch = (bands[1][0]-bands[0][0])/K
print(f'  pitch {pitch:.2f} vs pinned 80 -> {"PASS" if abs(pitch-80)<1.5 else "FAIL"}')
xml = zipfile.ZipFile('videos/deep-learning/001_transformers_part1/recreated_pptx/slide_004_recreated.pptx').read('ppt/slides/slide1.xml').decode()
n_spc = len(re.findall(r'<a:spcPts val="8000"/>', xml))
print(f'  XML spcPts 8000 count {n_spc} -> {"PASS" if n_spc>=1 else "FAIL"}')
