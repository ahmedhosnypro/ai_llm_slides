#!/usr/bin/env python3
"""m27: non-white contiguous-stroke scan (catch light pink/blue rect strokes), ellipse fill color."""
import numpy as np
from PIL import Image

im = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_040.jpg')).astype(int)
r, g, b = im[:,:,0], im[:,:,1], im[:,:,2]
nonwhite = (np.abs(r-255)>20) | (np.abs(g-255)>20) | (np.abs(b-255)>20)

def longest_run(mask_1d):
    best=(0,0,0); cur=0; start=0
    for i,v in enumerate(mask_1d):
        if v:
            if cur==0: start=i
            cur+=1
            if cur>best[0]: best=(cur,start,i)
        else: cur=0
    return best  # (len, s, e)

def hscan(y0,y1,x0,x1,minrun,label):
    print(f"-- {label}: rows {y0}..{y1}, x {x0}..{x1}, contig nonwhite runs >={minrun}")
    for y in range(y0,y1):
        L,s,e = longest_run(nonwhite[y,x0:x1])
        if L>=minrun:
            seg = im[y, x0+s:x0+e+1]
            # exclude near-black text pixels for color: median of mid-lum pixels
            lum = seg.mean(axis=1)
            mid = seg[(lum>120)&(lum<250)]
            col = np.median(mid,axis=0).round(0) if len(mid)>3 else np.median(seg,axis=0).round(0)
            print(f"   row {y}: run {L}px x {x0+s}..{x0+e}  color {col}")

def vscan(x0,x1,y0,y1,minrun,label):
    print(f"-- {label}: cols {x0}..{x1}, y {y0}..{y1}, contig nonwhite runs >={minrun}")
    for x in range(x0,x1):
        L,s,e = longest_run(nonwhite[y0:y1,x])
        if L>=minrun:
            seg = im[y0+s:y0+e+1, x]
            lum = seg.mean(axis=1)
            mid = seg[(lum>120)&(lum<250)]
            col = np.median(mid,axis=0).round(0) if len(mid)>3 else np.median(seg,axis=0).round(0)
            print(f"   col {x}: run {L}px y {y0+s}..{y0+e}  color {col}")

print("== EQ3 region (normalize) — full nonwhite scan ==")
hscan(386,452,150,315,80,"eq3 horiz")
vscan(150,315,394,448,30,"eq3 vert")
print("== EQ4 region (scale&shift) — full nonwhite scan ==")
hscan(448,486,150,400,80,"eq4 horiz")
vscan(150,400,450,480,25,"eq4 vert")
print("== row 475 detail (is it a stroke or glyph bottoms?) ==")
y=475
row = nonwhite[y,150:400]
# gaps
idx = np.where(row)[0]
print("   nonwhite count:", len(idx), " span:", 150+idx[0], "..", 150+idx[-1] if len(idx) else None)
gaps = np.where(np.diff(idx)>1)[0]
print("   num gaps >1px:", len(gaps), " largest gap:", int(np.max(np.diff(idx))) if len(idx)>1 else 0)
print("== ELLIPSE fill color ==")
# ellipse frame[170,454,191,475]: interior pixels, exclude dark glyph ink and 2px ring boundary
y0,y1,x0,x1 = 454,476,170,192
cy, cx = (y0+y1-1)/2, (x0+x1-1)/2
ry, rx = (y1-y0)/2-1.5, (x1-x0)/2-1.5
vals=[]
for yy in range(y0,y1):
    for xx in range(x0,x1):
        if ((yy-cy)/ry)**2 + ((xx-cx)/rx)**2 < 0.55:  # well inside
            px = im[yy,xx]
            if px.mean() > 150:  # not glyph ink
                vals.append(px)
vals=np.array(vals)
print(f"   interior non-dark n={len(vals)} median {np.median(vals,axis=0).round(0)} mean {vals.mean(axis=0).round(1)}")
print("== intro gamma/beta glyph geometry (italic?) x536..546 / x583..593, rows 142..160 ==")
for (xa,xb,lab) in [(535,547,'gamma'),(582,594,'beta')]:
    tops=[];bots=[]
    for yy in range(143,152):
        roww = np.where((im[yy,xa:xb].mean(axis=1))<150)[0]
        if len(roww): tops.append(roww[0])
    for yy in range(153,161):
        roww = np.where((im[yy,xa:xb].mean(axis=1))<150)[0]
        if len(roww): bots.append(roww[0])
    if tops and bots:
        print(f"   {lab}: Ledge top {np.mean(tops):.1f} bottom {np.mean(bots):.1f} drift {np.mean(tops)-np.mean(bots):+.1f}")
