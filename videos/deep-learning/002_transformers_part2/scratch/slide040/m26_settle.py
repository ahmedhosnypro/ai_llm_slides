#!/usr/bin/env python3
"""m26: settle every crop-judge contested element against the ORIGINAL frame (law)."""
import numpy as np
from PIL import Image

im = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_040.jpg')).astype(int)
H, W, _ = im.shape
r, g, b = im[:,:,0], im[:,:,1], im[:,:,2]
lum = (r+g+b)/3.0

def core(y0,y1,x0,x1,frac=0.3):
    reg = im[y0:y1, x0:x1].reshape(-1,3)
    l = reg.mean(axis=1)
    idx = np.argsort(l)[:max(int(len(l)*frac), 4)]
    med = np.median(reg[idx], axis=0)
    return f"#{int(med[0]):02X}{int(med[1]):02X}{int(med[2]):02X} n={len(idx)}"

def ink_mask(y0,y1,x0,x1, thr=140):
    return lum[y0:y1, x0:x1] < thr

def left_edge_per_row(y0,y1,x0,x1, thr=140):
    """x of first ink pixel per row (relative to x0)."""
    out=[]
    for y in range(y0,y1):
        row = np.where(lum[y, x0:x1] < thr)[0]
        out.append((y, int(row[0]) if len(row) else None))
    return out

def hstroke(y0,y1,x0,x1, minfrac=0.6, thr=170):
    """rows whose ink run spans >minfrac of the x-range (candidate horizontal strokes)."""
    res=[]
    for y in range(y0,y1):
        row = lum[y, x0:x1] < thr
        n = row.sum()
        if n > minfrac*(x1-x0):
            res.append((y, int(n)))
    return res

def vstroke(x0,x1,y0,y1, minfrac=0.6, thr=170):
    res=[]
    for x in range(x0,x1):
        col = lum[y0:y1, x] < thr
        n = col.sum()
        if n > minfrac*(y1-y0):
            res.append((x, int(n)))
    return res

print("== 1. INTRO L2 glyph cores (frame rows 142..160) ==")
print("  green 'learn parameters' core:", core(142,160,390,531))
print("  glyph A x535..546:", core(142,160,535,546))
print("  glyph B x549..578:", core(142,160,549,578))
print("  glyph C x582..593:", core(142,160,582,593))
# hue classification per 1px column across x 530..600: dominant class of dark pixels
print("  per-column hue x530..600 (R=red-dom G=green-dom .=none):")
line=""
for x in range(530,601):
    col = im[142:160, x]
    l = col.mean(axis=1)
    dk = col[l<150]
    if len(dk)<2: line+="."; continue
    m = dk.mean(axis=0)
    if m[1] > m[0]+15: line+="G"
    elif m[0] > m[1]+15: line+="R"
    else: line+="k"
print("   ", line)
print("== 2. red L2 'convert the mean and' (x663..828 rows 142..160): italic slant ==")
for (y,xe) in left_edge_per_row(143,159,655,700): print(f"   row {y} first-ink x+{xe}")
print("   red L2 underline? rows 160..172 x663..828 hstroke:", hstroke(160,172,663,828,0.5))
print("   red L2 underline strict rows 160..170, dark-red mask:")
for y in range(160,171):
    row = (r[y,663:828]>100)&(r[y,663:828]<220)&(g[y,663:828]<90)&(b[y,663:828]<90)
    if row.sum()>10: print(f"    row {y}: n={int(row.sum())} x {663+int(np.where(row)[0][0])}..{663+int(np.where(row)[0][-1])}")
print("== 3. red L3 (x105..436 rows 167..182): italic slant ==")
for (y,xe) in left_edge_per_row(168,182,100,180): print(f"   row {y} first-ink x+{xe}")
print("   red L3 underline rows 176..190 x105..436:")
for y in range(176,191):
    row = (r[y,105:436]>100)&(r[y,105:436]<220)&(g[y,105:436]<90)&(b[y,105:436]<90)
    if row.sum()>30: print(f"    row {y}: n={int(row.sum())} x {105+int(np.where(row)[0][0])}..{105+int(np.where(row)[0][-1])}")
print("== 4. blue words italic? L1 'mean'(x~640) 'variance,'(x~790) vs 'Zero'(bold x~560) ==")
print("   blue word spans: scan x536..830 for blue-dominant dark cols:")
prev=None; spans=[]
for x in range(530,835):
    col = im[115:137, x]
    l = col.mean(axis=1)
    dk = col[l<160]
    isblue = len(dk)>1 and dk[:,2].mean() > dk[:,0].mean()+30
    if isblue and prev is None: prev=x
    if not isblue and prev is not None:
        if x-prev>3: spans.append((prev,x))
        prev=None
print("   blue spans:", spans)
def slant(x0,x1,label):
    # left edge of ink at top half vs bottom half of x-height band rows 118..134
    tops=[]; bots=[]
    for y in range(118,127):
        row = np.where(lum[y,x0:x1]<150)[0]
        if len(row): tops.append(row[0])
    for y in range(128,136):
        row = np.where(lum[y,x0:x1]<150)[0]
        if len(row): bots.append(row[0])
    if tops and bots:
        print(f"   {label}: meanLedge top {np.mean(tops):.1f} bottom {np.mean(bots):.1f} drift {np.mean(tops)-np.mean(bots):+.1f}")
for (a,bnd) in spans:
    slant(a,bnd,f"blue span x{a}..{bnd}")
print("   ('strictly' italic control x536..585ish handled above)")
print("== 5. 'learn parameters' highlight vs underline (x390..531, rows 142..168) ==")
reg = im[145:157, 400:420].reshape(-1,3)
print("   interior sample x400..420 rows145..157 mean:", reg.mean(axis=0).round(1))
reg2 = im[145:157, 500:528].reshape(-1,3)
print("   interior sample x500..528:", reg2.mean(axis=0).round(1))
print("   green underline stroke? rows 158..168 x390..531 dark-green:")
for y in range(158,169):
    row = (g[y,390:531]>60)&(g[y,390:531]<160)&(r[y,390:531]<g[y,390:531]-30)
    if row.sum()>30: print(f"    row {y}: n={int(row.sum())} x {390+int(np.where(row)[0][0])}..{390+int(np.where(row)[0][-1])}")
print("== 6. eq3 rect? scan x150..310, rows 388..452 ==")
print("   horizontal strokes (rows, thr170):", hstroke(388,452,150,310,0.55))
print("   vertical strokes (cols, thr170):", vstroke(150,310,396,448,0.55))
print("   row-446 line color/extent recheck:", core(445,448,164,287))
print("   candidate top stroke rows 392..400 ink runs:")
for y in range(392,401):
    row = np.where(lum[y,150:310]<180)[0]
    if len(row)>40: print(f"    row {y}: n={len(row)} x {150+row[0]}..{150+row[-1]}")
print("== 7. eq4 red rect? scan x150..400, rows 448..484 ==")
print("   horizontal strokes:", hstroke(448,484,150,400,0.55,175))
print("   vertical strokes:", vstroke(150,400,450,480,0.55,175))
print("   red-dominant strokes rows 448..484 x150..400:")
for y in range(448,485):
    row = (r[y,150:400]>130)&(g[y,150:400]<120)&(b[y,150:400]<120)
    if row.sum()>40: print(f"    row {y}: n={int(row.sum())} x {150+int(np.where(row)[0][0])}..{150+int(np.where(row)[0][-1])}")
for x in range(150,400):
    col = (r[448:484,x]>130)&(g[448:484,x]<120)&(b[448:484,x]<120)
    if col.sum()>15: print(f"    col {x}: n={int(col.sum())} y {448+int(np.where(col)[0][0])}..{448+int(np.where(col)[0][-1])}")
print("== 8. y_i ellipse interior (frame 170..191 x, 454..475 y) ==")
for (x0,x1,y0,y1,lab) in [(173,179,456,461,'upper-left inside'),(182,189,456,461,'upper-right inside'),(173,179,468,473,'lower-left inside'),(182,189,468,473,'lower-right inside')]:
    reg = im[y0:y1, x0:x1].reshape(-1,3)
    print(f"   {lab}: mean {reg.mean(axis=0).round(1)}")
print("== 9. blue L1 word 'mean' exact italic? full-word slant x~634..670 ==")
slant(630,672,'blue mean')
slant(780,825,'blue variance,')
