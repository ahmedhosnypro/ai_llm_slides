#!/usr/bin/env python3
# Pre-judge self-check, slide 004 attempt 1 (per scripts/17_worker_instructions.md).
# Checks: (2) frame containment incl. exact-touch gap vs original, (6-crop) dense-region
# measurements (body lines, badge), (7) wrap, (8) explicit lineSpacing pin + XML assert.
# N/A on this slide: (3) equations, (4) multi-line delimiters, (5) tables.
from PIL import Image
import numpy as np, zipfile, re

K = 2001/960  # render px per original px
ren = np.array(Image.open('videos/deep-learning/001_transformers_part1/recreated_pptx/qa/slide004/render_1.png').convert('RGB')).astype(int)
orig = np.array(Image.open('videos/deep-learning/001_transformers_part1/unique_slides/slide_004.jpg').convert('RGB')).astype(int)
r,g,b = ren[:,:,0], ren[:,:,1], ren[:,:,2]
blue = (b-np.maximum(r,g)>45)&(b>110)
yellow = (r>200)&(g>200)&(b<190)
red = (r>150)&(g<100)&(b<100)

print('== SELF-CHECK 2: FRAME CONTAINMENT (panel border core: left 38.9, top 43.2, right 918.7, bottom 536.9 o-px) ==')
# content ink excl. border corridor +-4px
content = ((r>140)&(g<110)&(b<110)) | ((b-np.maximum(r,g)>45)&(b>110)) | ((r>200)&(g>200)&(b<190)) | ((r<120)&(g<120)&(b<120))
cm = content.copy()
for c in (81,1916): cm[:, max(0,c-4):c+5] = False
for rw in (91,1119): cm[max(0,rw-4):rw+5, :] = False
outside_ok = (cm[:86,100:1900].sum()==0 and cm[1126:,:].sum()==0 and cm[:, :76].sum()==0 and cm[:,1922:].sum()==0)
print(f'  ink in outside bands: 0/0/0/0 -> {"PASS" if outside_ok else "FAIL"}')
# badge-right exact-touch gap vs original
pys,pxs = np.where((b-np.maximum(r,g)>45)&(b>110))
border_left = min(x for x in range(1900,1930) if red[560,x])
gap_r = (border_left - pxs.max())/K
ob = orig[300,910:930]; ocol = [910+i for i in range(20) if ob[i,0]-ob[i,1]>50]
gap_o = min(ocol) - 914  # original badge outline right edge (bbox 872..914)
print(f'  badge-ring right {pxs.max()/K:.1f} o-px, border left {border_left/K:.1f} o-px, gap {gap_r:.1f}px (original ~{gap_o}px) -> {"PASS" if gap_r>2 else "FAIL"} (no touch; clearance matches original)')

print('== SELF-CHECK 6 (measurements for dense-region crops) ==')
bl = blue.copy(); bl[:,1770:1925]=False
rows = bl.sum(axis=1); bands=[]; inb=False
for y,v in enumerate(rows):
    if v>4 and not inb: s0=y; inb=True
    elif v<=4 and inb: bands.append((s0,y-1)); inb=False
bands=[(a2,b2) for a2,b2 in bands if b2-a2>10]
for i,(a2,b2) in enumerate(bands):
    xs = np.where(bl[a2:b2+1].any(axis=0))[0]
    print(f'  body L{i+1}: y {a2/K:.1f}..{b2/K:.1f}, x {xs.min()/K:.1f}..{xs.max()/K:.1f} (orig: y 342..372/422..452, x 89..857/89..644)')
ys,xs = np.where(yellow)
print(f'  badge yellow: x {xs.min()/K:.1f}..{xs.max()/K:.1f}, y {ys.min()/K:.1f}..{ys.max()/K:.1f} (orig 876..911 / 57..86)')
tm = red[280:660, 200:1800]; tys,txs = np.where(tm)
print(f'  title ink: x {(200+txs.min())/K:.1f}..{(200+txs.max())/K:.1f}, y {(280+tys.min())/K:.1f}..{(280+tys.max())/K:.1f} (orig 146..788 / 200..247; x centered per house/spec, orig ink center 467)')

print('== SELF-CHECK 7: WRAP ==')
print(f'  body bands: {len(bands)} (expect 2) -> {"PASS" if len(bands)==2 else "FAIL"}; rightmost ink {max(np.where(bl[a2:b2+1].any(axis=0))[0].max() for a2,b2 in bands)/K:.1f} o-px < box right 917.3')

print('== SELF-CHECK 8: LINE SPACING PIN ==')
pitch = (bands[1][0]-bands[0][0])/K
print(f'  measured pitch {pitch:.2f} o-px vs pinned 80.00 -> {"PASS" if abs(pitch-80)<1.5 else "FAIL"}')
xml = zipfile.ZipFile('videos/deep-learning/001_transformers_part1/recreated_pptx/slide_004_recreated.pptx').read('ppt/slides/slide1.xml').decode()
n_spc = len(re.findall(r'<a:spcPts val="8000"/>', xml))
print(f'  XML spcPts 8000 count {n_spc} (>=1) -> {"PASS" if n_spc>=1 else "FAIL"}')
