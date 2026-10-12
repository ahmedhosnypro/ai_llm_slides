# m13_bands.py — disambiguate encoder band, bar edges, dots vs text, probes
from PIL import Image
import numpy as np

im = np.asarray(Image.open('unique_slides/slide_059.jpg').convert('RGB')).astype(int)
r, g, b = im[:,:,0], im[:,:,1], im[:,:,2]

def runs(bools, min_len=1):
    out, s = [], None
    for i, v in enumerate(bools):
        if v and s is None: s = i
        if not v and s is not None:
            if i - s >= min_len: out.append((s, i-1))
            s = None
    if s is not None: out.append((s, len(bools)-1))
    return out

def px(x, y): return tuple(int(v) for v in im[y, x])

print("== 1. band y 319..351: white clusters and dark-red clusters ==")
white = (r>215)&(g>215)&(b>215)
drk = (r>=130)&(r<225)&(g<80)&(b<80)
wc = runs(white[319:352,:].sum(axis=0)>0, 1)
rc = runs(drk[319:352,:].sum(axis=0)>0, 1)
print("  white col clusters:", wc)
print("  darkred col clusters:", rc)
print("  white row profile:", [(y+319,int(white[y,150:870].sum())) for y in range(33) if white[y,150:870].sum()>3])
print("  darkred row profile:", [(y+319,int(drk[y,150:870].sum())) for y in range(33) if drk[y,150:870].sum()>3])

print("== 2. bar edge rows: dash patterns? ==")
for y in [295, 296, 297, 298, 317, 318, 319, 366, 367, 368, 369, 370]:
    rr = runs(drk[y, 160:860], 1)
    print(f"  y{y}: darkred runs n={len(rr)} first5={rr[:5]} last3={rr[-3:]}")

print("== 3. probes ==")
pts = [(200,296),(200,298),(500,296),(200,303),(200,318),(200,320),(350,86),(350,88),(350,90),
       (441,76),(441,78),(441,80),(438,75),(445,80),(440,95),(440,98),(440,102),(430,86),(450,86),
       (430,116),(450,116),(440,110),(440,118),(441,124)]
for p in pts: print(f"  {p}: {px(*p)}")

print("== 4. circle1 exact vertical scan x=440 y 78..130 ==")
for y in range(78, 131): print(f"  y{y}: {px(440,y)}", end="")
print()
print("== 4b. circle1 horizontal scan y=100 x 420..462 ==")
for x in range(420, 463): print(f"  x{x}: {px(x,100)}", end="")
print()

print("== 5. Softmax text color in circle: modal colors y 82..92 x 428..453 ==")
from collections import Counter
blk = im[82:93, 428:454].reshape(-1,3)
print("  ", Counter((int(a)//32*32,int(bb)//32*32,int(c)//32*32) for a,bb,c in blk).most_common(5))
print("== 5b. Sigma zone y 98..120 x 428..453 ==")
blk = im[98:121, 428:454].reshape(-1,3)
print("  ", Counter((int(a)//32*32,int(bb)//32*32,int(c)//32*32) for a,bb,c in blk).most_common(5))

print("== 6. left annotations x-extents (exclude border x<62) ==")
ink = (abs(r-g)>30)|(abs(g-b)>30)|(abs(r-b)>30)
for (y0,y1,tag) in [(138,168,"pooled-note"),(298,346,"output-seq"),(384,404,"input-seq"),
                    (404,450,"word-emb"),(456,506,"position")]:
    sub = ink[y0:y1, 62:140]
    ys, xs = np.where(sub)
    if len(xs):
        print(f"  {tag}: x {xs.min()+62}..{xs.max()+62} y {ys.min()+y0}..{ys.max()+y0} n={len(xs)}")
        # line structure
        rowc = sub.sum(axis=1)
        print(f"    lines:", runs(rowc>2, 2), f"(+{y0})")

print("== 7. X-row text/cells: dark-red text clusters y 414..442 ==")
dtxt = (r<210)&(r-g>55)&(r-b>45)&(r>80)
sub = dtxt[414:443, 155:910]
colc = sub.sum(axis=0)
print("  dark-red text col clusters:", runs(colc>0, 2), "(+155)")
print("== 7b. Y-row blue text clusters y 226..258 ==")
btxt = (b-r>35)&(b-g>25)&(b>90)&(r<160)
sub = btxt[226:259, 155:910]
print("  blue text col clusters:", runs(sub.sum(axis=0)>0, 2), "(+155)")
print("== 7c. Vector-row navy text clusters y 470..505 ==")
sub = btxt[470:506, 155:910]
print("  navy text col clusters:", runs(sub.sum(axis=0)>0, 2), "(+155)")

print("== 8. colored cells per row: yellow/green/pink/lavender clusters ==")
yel = (r>235)&(g>235)&(b<215)&(r-b>30)
grn = (g-r>20)&(g-b>20)&(g>200)
pnk = (r>230)&(r-g>28)&(r-b>28)
lav = (b-r>15)&(b-g>10)&(b>225)&(r>190)
for (y0,y1,tag) in [(414,443,"X"),(226,259,"Y"),(470,506,"V")]:
    for (m,tag2) in [(yel,"yel"),(grn,"grn"),(pnk,"pnk"),(lav,"lav")]:
        cl = runs(m[y0:y1,155:910].sum(axis=0)>1, 2)
        print(f"  {tag}-row {tag2}: {cl} (+155)")

print("== 9. row band vertical extents at col 650 (dots zone) ==")
for y in range(405, 450): print(f"  {px(650,y)}", end="")
print("  <- X row col650")
for y in range(218, 265): print(f"  {px(650,y)}", end="")
print("  <- Y row col650")
