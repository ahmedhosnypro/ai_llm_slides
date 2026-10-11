#!/usr/bin/env python3
"""Measure slide_045.jpg (960x540, 1px=1pt=1/72in): delta regions vs slide 43 parent.
Sections: title/subtitle, ltbox absence, vecbox+label, bar->vecbox arrow, concat bar,
top-right equation box, bottom-right additions (Input Sequence ellipse, X chips,
Split caption, chunk table, To Head labels, colored arrows)."""
import numpy as np
from PIL import Image
import json

IM = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_045.jpg').convert('RGB')).astype(int)
H, W = IM.shape[:2]
r, g, b = IM[:,:,0], IM[:,:,1], IM[:,:,2]
lum = IM.mean(axis=2)

def bbox(mask, name):
    ys, xs = np.where(mask)
    if not len(ys):
        print(f"{name}: NOT FOUND"); return None
    print(f"{name}: x {xs.min()}..{xs.max()} y {ys.min()}..{ys.max()}  (n={len(ys)})")
    return dict(x0=int(xs.min()), x1=int(xs.max()), y0=int(ys.min()), y1=int(ys.max()), n=int(len(ys)))

def near(c, tol=18):
    return (abs(r-c[0])<tol) & (abs(g-c[1])<tol) & (abs(b-c[2])<tol)

def rowscan(y0,y1,x0,x1,mask,name):
    """per-row ink counts of mask inside a window"""
    m = np.zeros_like(mask); m[y0:y1, x0:x1] = mask[y0:y1, x0:x1]
    ys, xs = np.where(m)
    if not len(ys): print(name, "EMPTY"); return
    for y in range(y0,y1):
        cnt = m[y].sum()
        if cnt:
            xr = np.where(m[y])[0]
            print(f"  {name} y={y}: n={cnt} x {xr.min()}..{xr.max()}")

def colscan(y0,y1,x0,x1,mask,name):
    m = np.zeros_like(mask); m[y0:y1, x0:x1] = mask[y0:y1, x0:x1]
    for x in range(x0,x1):
        cnt = m[:,x].sum()
        if cnt>1:
            yr = np.where(m[:,x])[0]
            print(f"  {name} x={x}: n={cnt} y {yr.min()}..{yr.max()}")

print("=== 1. TITLE / SUBTITLE ===")
dark = lum < 140
bbox(dark[44:104, 500:925], "title ink (y44..104,x500..925)")
rowscan(44,110,500,925,dark,"title")
print("--- subtitle colors: sample runs in y78..100, x560..820")
for y in range(78, 102, 2):
    row = IM[y, 560:830]
    dk = np.where(row.mean(axis=1)<170)[0]
    if len(dk):
        x0 = 560+dk.min(); x1=560+dk.max()
        px = IM[y, x0:x1+1]
        dkk = px[px.mean(axis=1)<170]
        med = np.median(dkk, axis=0).astype(int)
        print(f"  y={y}: ink x {x0}..{x1} medcolor {tuple(med)} n={len(dkk)}")
print("--- blue check (blue bold italic Narrow): blue pixels y75..105 x560..830")
blue = (b>120)&(b-r>40)&(b-g>30)
bbox(blue[75:105,560:830],"blue ink in subtitle zone")
print("--- yellow highlight check y75..105 x560..830 (parent Wide had FFFF00)")
yel = (r>200)&(g>200)&(b<120)
bbox(yel[70:110,540:840],"yellow highlight in subtitle zone")

print("=== 2. LTBOX ABSENCE (parent: fill F6FAD5 edge D26900 x314..554 y90..114) ===")
ltfill = near((246,250,213),12)
bbox(ltfill[85:120,300:570],"lt fill F6FAD5 in 45?")
ltedge = near((210,105,0),30)
bbox(ltedge[85:120,300:570],"lt edge D26900 in 45?")
print("--- mean color of parent ltbox interior x330..540 y95..110:")
print("   43:", IM[95:110,330:540].reshape(-1,3).mean(axis=0).round(0))
a43 = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_043.jpg').convert('RGB')).astype(int)
print("   43-frame same region:", a43[95:110,330:540].reshape(-1,3).mean(axis=0).round(0))

print("=== 3. VECBOX (parent x400..470 y50..72) + right label ===")
white = (r>246)&(g>246)&(b>246)
bbox(white[44:80,395:480],"white vecbox area")
bbox(dark[44:80,472:540],"ink right of vecbox (label 1xd)")
for y in range(48,80,2):
    row = IM[y, 472:545]
    dk = np.where(row.mean(axis=1)<170)[0]
    if len(dk):
        px = IM[y, 472+dk.min():472+dk.max()+1]
        dkk = px[px.mean(axis=1)<170]
        med = np.median(dkk, axis=0).astype(int)
        print(f"  label y={y}: x {472+dk.min()}..{472+dk.max()} med {tuple(med)}")

print("=== 4. RED ARROW bar->vecbox (window x420..500 y70..130) ===")
red = (r>150)&(g<90)&(b<90)
rowscan(68,132,420,505,red,"redarrow")

print("=== 5. CONCAT BAR (parent x185..684 y128..151.5) ===")
barlbl = near((249,251,189),14)
bbox(barlbl[120:160,170:700],"bar base F9FBBD")
for c,nm in [((187,79,7),'seg1'),((119,124,92),'seg2'),((242,242,8),'seg3'),((170,255,113),'seg4'),((243,222,188),'seg5')]:
    bbox(near(c,20)[124:156,170:700], f"concat seg {nm}")
print("--- Concatenated Vector label ink (red) y128..150 x185..310:")
rowscan(126,152,183,315,red,"conlabel")

print("=== 6. TOP-RIGHT EQUATION BOX (green dashed) ===")
grn = (g>130)&(g-r>50)&(g-b>40)
bbox(grn[100:200,700:940],"green border top-right zone")
bbox(dark[100:200,730:930],"dark ink top-right zone")
print("--- caption under box (blue): y150..200 x730..930")
blu = (b>120)&(b-r>40)&(b-g>30)
rowscan(150,205,720,940,blu,"cap-blue")

print("=== 7. BOTTOM-RIGHT ADDITIONS ===")
# red ellipse Input Sequence
bbox(near((204,0,0),45)[350:430,720:940],"red ellipse Input Sequence zone (y350..430)")
bbox(white[355:425,730:930],"white text inside ellipse zone")
# dark blue X chips
dblu = near((31,63,191),45)
bbox(dblu[350:440,720:940],"darkblue X chips (y350..440)")
# black caption Split vectors
bbox(dark[430:460,700:940],"dark ink caption zone y430..460")
# chunk table rows: colored subchunks green/yellow/purple/pink/red
for c,nm in [((124,196,124),'grn'),((230,230,92),'yel'),((181,126,220),'pur'),((240,160,176),'pnk'),((224,112,112),'red')]:
    bbox(near(c,32)[450:540,700:945], f"chunk row {nm}")
print("--- To Head labels (right of table): dark ink x870..945 y440..540")
rowscan(430,540,860,950,dark,"tohead")
print("--- colored arrows W-cols to table (x600..780 y400..540):")
for c,nm in [((124,196,124),'grn'),((230,230,92),'yel'),((181,126,220),'pur'),((240,160,176),'pnk'),((224,112,112),'red'),((0,170,0),'dgrn')]:
    bbox(near(c,36)[390:540,590:800], f"arrow {nm}")

print("=== 8. PARENT LEGEND ZONE NOW EMPTY? (parent legend x736..906 y468..532) ===")
leg = near((230,252,230),16)
bbox(leg[455:540,720:920],"parent legend fill in 45 (should be gone)")

print("=== 9. INHERITED SANITY: cards, swoosh, tan box, queryrow ===")
out = {}
out['card_h1'] = bbox(near((238,140,150),22)[180:440,40:240],"h1 card")
out['card_h5'] = bbox(near((247,226,205),20)[180:340,220:420],"h5 card")
out['tan'] = bbox(near((216,192,168),20)[280:460,180:270],"tan dot product")
out['swoosh'] = bbox(near((139,26,16),40)[300:540,480:700],"swoosh darkred")
out['q1bar'] = bbox(near((204,0,0),40)[455:485,190:260],"q1 red bar")
out['badge'] = bbox(near((253,253,150),30)[40:110,860:930],"badge yellow")
