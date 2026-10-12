#!/usr/bin/env python3
"""Measure slide_001 original frame (960x540, 1px=1pt): ink bands, x-profiles, colors."""
from PIL import Image
import numpy as np

im = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_001.jpg').convert('RGB')).astype(int)
H, W, _ = im.shape
r, g, b = im[:,:,0], im[:,:,1], im[:,:,2]
red  = (r>120)&(g<90)&(b<90)
blue = (b>110)&(r<110)&(g<110)
dark = (r<110)&(g<110)&(b<110)

def bands(mask, axis, thresh):
    prof = mask.sum(axis=axis)
    rows = np.where(prof>thresh)[0]
    out=[]
    if len(rows)==0: return out
    s=rows[0]; p=rows[0]
    for y in rows[1:]:
        if y-p>2: out.append((s,p)); s=y
        p=y
    out.append((s,p)); return out

def xprof(mask, y0, y1, label):
    xs = np.where(mask[y0:y1+1].sum(axis=0)>0)[0]
    # print x histogram edges: contiguous x-bands
    xb=[]
    if len(xs):
        s=xs[0]; p=xs[0]
        for x in xs[1:]:
            if x-p>6: xb.append((s,p)); s=x
            p=x
        xb.append((s,p))
    print(f'  {label} y{y0}-{y1}: x-bands {xb}')
    return xb

def core_color(mask, y0, y1, x0, x1, label):
    region = im[y0:y1+1, x0:x1+1]
    m = mask[y0:y1+1, x0:x1+1]
    if m.sum()==0: print(f'  {label}: no mask px'); return
    px = region[m]
    med = np.median(px, axis=0).astype(int)
    print(f'  {label}: median core rgb {tuple(med)} n={m.sum()}')

print('== TOP RULE AREA (y38..50) ==')
for y in range(38, 51):
    row = im[y]
    dk = np.where(dark[y])[0]
    rd = np.where(red[y])[0]
    if len(dk)>10 or len(rd)>10:
        seg = row[dk] if len(dk)>10 else row[rd]
        med = np.median(seg,axis=0).astype(int)
        xs = dk if len(dk)>10 else rd
        print(f'  y={y}: {"dark" if len(dk)>10 else "red"} n={len(xs)} x {xs.min()}-{xs.max()} median {tuple(med)}')
print('== TITLE BANDS (red) ==')
for (y0,y1) in [(126,184),(198,242)]:
    xprof(red,y0,y1,'title-red')
    core_color(red,y0,y1,100,900,'title-red')
print('== PREPARED-BY / CREDIT (red y291-311) ==')
xprof(red,291,311,'prepared-red'); core_color(red,291,311,100,900,'prepared-red')
print('== CREDIT BLUE ==')
xprof(blue,317,339,'name'); core_color(blue,317,339,100,900,'name')
xprof(blue,344,358,'email'); core_color(blue,344,358,100,900,'email')
print('== INSTRUCTORS ==')
xprof(red,397,411,'instr-head'); core_color(red,397,411,50,400,'instr-head')
for (y0,y1,lab) in [(425,440,'name1'),(449,463,'email1'),(473,487,'name2'),(497,510,'email2')]:
    xprof(blue,y0,y1,lab); core_color(blue,y0,y1,100,500,lab)
print('== LOGO AREA ==')
teal = (g>140)&(b>140)&(r<120)
ys,xs = np.where(teal)
print('  teal emblem bbox x',xs.min(),xs.max(),'y',ys.min(),ys.max())
# white box: near-white pixels in logo region y430..520 x660..930
white = (r>235)&(g>235)&(b>235)
sub = white[430:520, 640:935]
ys2,xs2 = np.where(sub)
print('  white-box bbox x',640+xs2.min(),640+xs2.max(),'y',430+ys2.min(),430+ys2.max())
# maroon text inside white box
maroon = (r>100)&(r<190)&(g<70)&(b<90)
sub2 = maroon[430:520, 640:935]
ys3,xs3 = np.where(sub2)
if len(xs3): print('  maroon text bbox x',640+xs3.min(),640+xs3.max(),'y',430+ys3.min(),430+ys3.max())
xprof(dark,464,472,'arabic-row-dark'); core_color(dark,464,472,640,935,'arabic-dark')
# english line inside white box: dark-ish rows y~490-510
sub3 = (r<200)&(g<160)&(b<160)
for (y0,y1) in [(485,515)]:
    xprof(sub3,y0,y1,'eng-textish')
print('== BOTTOM STRIP ==')
for y in [516,517,518,520,539]:
    row=im[y]; med=np.median(row,axis=0).astype(int)
    print(f'  y={y}: median row rgb {tuple(med)}')
print('== FRAME EDGES / CHROME ==')
print('  corner (5,5):', tuple(im[5,5]), ' (30,30):', tuple(im[30,30]))
print('  panel sample (100,300):', tuple(im[300,100]), '(480,300):', tuple(im[300,480]))
print('  badge area (893,71):', tuple(im[71,893]), 'ring check (893,54):', tuple(im[54,893]))
print('  col x=42 (panel left border) y300:', tuple(im[300,42]), ' x=918:', tuple(im[300,918]))
print('  row y=45 x=500:', tuple(im[45,500]), ' y=44:', tuple(im[44,500]), ' y=46:', tuple(im[46,500]))
print('  bottom y537 x500:', tuple(im[537,500]), ' y538:', tuple(im[538,500]), ' y539:', tuple(im[539,500]))
