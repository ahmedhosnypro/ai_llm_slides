# m10_final.py — resolve remaining structure: top labels, encoder text, row box
# structure, pooled squares, edges.
from PIL import Image
import numpy as np
from collections import Counter

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

print("== 1. TOP BAND per-cluster y-extents (lavender-blue text) ==")
lav = (b > r+20)&(b > 200)&(r>120)
for (x0,x1,tag) in [(315,420,"OutputClasses?"),(435,460,"C1"),(508,532,"C2"),(579,605,"C3")]:
    sub = lav[44:95, x0:x1]
    ys, xs = np.where(sub)
    if len(xs):
        print(f"  {tag}: x {xs.min()+x0}..{xs.max()+x0} y {ys.min()+44}..{ys.max()+44} n={len(xs)}")
# arrows from circles up: dark-blue thin at circle cx, y 62..92
darkblue = (b > r+40)&(b > g+30)&(b>110)&(r<130)
for cx in [440, 512, 585]:
    rr = runs(darkblue[55:95, cx-2:cx+3].any(axis=1), 0)
    print(f"  darkblue rows near cx={cx} (y+55):", rr)

print("== 2. col 700 rows 366..400 (pink top edge) ==")
for y in range(366, 401, 2): print(f"  y{y}: {px(700,y)}", end="")
print()
print("== 2b. col 200 rows 366..400 ==")
for y in range(366, 401, 2): print(f"  y{y}: {px(200,y)}", end="")
print()

print("== 3. WHITE text inside rose container (y 275..373, x 141..878) ==")
white = (r>228)&(g>228)&(b>228)
sub = white[275:374, 141:879]
colcnt = sub.sum(axis=0)
cl = runs(colcnt>1, 3)
print("  white col clusters:", [(a+141,c+141) for a,c in cl])
rowcnt = sub.sum(axis=1)
print("  white row profile:", [(y+275,int(rowcnt[y])) for y in range(99) if rowcnt[y]>8])

print("== 4. GAP box edges ==")
print("  row 190 x 875..905:", [(x, px(x,190)) for x in range(875, 906, 2)])
print("  row 196 dark text runs:", runs(((r[196]<120)&(g[196]<120)&(b[196]<120))[160:900],1), "(+160)")
print("  col 480 rows 182..212 1px:", [(y, px(480,y)) for y in range(182, 213)])

print("== 5. POOLED row: transitions + square colors ==")
band = im[146:166, 340:660]
nonwhite = (abs(band[:,:,0].astype(int)-band[:1,:,:].repeat(20,0)[:,:,0])>0)
# simpler: color-change transitions along row 156
row = im[156, 340:660].astype(int)
diffs = np.abs(np.diff(row, axis=0)).sum(axis=1)
tr = [i+340 for i in np.where(diffs>60)[0]]
print("  strong transitions row 156:", tr)
# modal colors per 9px cell from x 365
cells = []
for x0 in range(365, 625, 9):
    block = im[150:162, x0:x0+8].reshape(-1,3)
    med = tuple(int(v) for v in np.median(block, axis=0))
    cells.append((x0, med))
print("  cell medians:", cells)

print("== 6. CIRCLE modal colors ==")
for (x0,x1,y0,y1,tag) in [(423,458,58,122,"c1"),(495,530,58,122,"c2"),(567,603,58,122,"c3")]:
    block = im[y0:y1, x0:x1].reshape(-1,3)
    cnt = Counter((int(rr)//24*24, int(gg)//24*24, int(bb)//24*24) for rr,gg,bb in block)
    print(f"  {tag} top colors:", cnt.most_common(6))

print("== 7. ROW STRUCTURE: X row (y 413..443) ==")
print("  row 428 x 155..265 1px:", [(x, px(x,428)) for x in range(155, 266, 3)])
print("  row 428 white runs:", runs(((r[428]>240)&(g[428]>240)&(b[428]>240))[150:910],2), "(+150)")
print("  row 428 greenish runs:", runs(((g[428]-r[428]>8)&(g[428]>235))[150:910],2), "(+150)")
print("  col 200 rows 410..448 1px:", [(y, px(200,y)) for y in range(410, 449)])
print("== 7b. green dashed rect edges ==")
grn = (g-r>25)&(g-b>25)&(g>110)
print("  green rows at col 500:", runs(grn[:,500],0))
print("  green rows at col 800:", runs(grn[:,800],0))
print("  green cols at row 416:", runs(grn[416,:],0)[:10], "...")
print("  green cols at row 440:", runs(grn[440,:],0)[:10], "...")

print("== 8. ROW STRUCTURE: Y row (y 222..262) ==")
print("  row 242 x 165..270 1px:", [(x, px(x,242)) for x in range(165, 271, 3)])
blueb = (b-r>50)&(b>140)
print("  row 242 blue runs:", runs(blueb[242,150:910],0), "(+150)")
print("  blue cols dense y 224..258:", [ (x, int(blueb[224:258,x].sum())) for x in range(150, 910) if blueb[224:258,x].sum() > 18 ][:40])
print("  col 175 rows 208..278 1px:", [(y, px(175,y)) for y in range(208, 279, 2)])

print("== 9. ROW STRUCTURE: Vector row (y 466..508) ==")
print("  row 487 x 165..270 1px:", [(x, px(x,487)) for x in range(165, 271, 3)])
org = (r>195)&(g>100)&(g<180)&(b<105)&(r-b>115)
print("  orange rows at col 500:", runs(org[:,500],0))
print("  orange rows at col 750:", runs(org[:,750],0))
print("  orange cols at row 468:", runs(org[468,:],0)[:10], "...")
print("  orange cols at row 505:", runs(org[505,:],0)[:10], "...")
print("  peach fill rows at col 750:", runs((abs(r[:,750]-252)<8)&(abs(g[:,750]-229)<12)&(abs(b[:,750]-203)<14),0))

print("== 10. TAN bar full runs row 100 ==")
tan = (abs(r-245)<16)&(abs(g-203)<18)&(abs(b-167)<22)
print("  row 100 tan runs:", runs(tan[100,:],1))

print("== 11. annotation y-profiles (x 45..140) ==")
ink2 = (abs(r-g)>30)|(abs(g-b)>30)|(abs(r-b)>30)
for (y0,y1,tag) in [(140,205,"pooled-note"),(370,405,"input-seq")]:
    rowc = ink2[y0:y1, 45:140].sum(axis=1)
    print(f"  {tag}:", [(y+y0,int(rowc[y])) for y in range(y1-y0) if rowc[y]>2])

print("== 12. pink container edges ==")
print("  row 450 x 50..80:", [(x, px(x,450)) for x in range(50, 81, 3)])
print("  row 450 x 890..915:", [(x, px(x,450)) for x in range(890, 916, 3)])
print("  col 300 rows 505..520:", [(y, px(300,y)) for y in range(505, 521)])

print("== 13. cells in X row (tiny colored) ==")
ycell = (r>210)&(g>190)&(b<160)&(r-b>60)
gcell = (g-r>25)&(g-b>25)&(g>170)&(g<240)
pcell = (r>215)&(r-g>40)&(r-b>40)
for (mask,tag) in [(ycell,"yellow"),(gcell,"green"),(pcell,"pink")]:
    sub = mask[413:443, 150:910]
    colc = sub.sum(axis=0)
    print(f"  X-row {tag} col clusters:", runs(colc>1,1), "(+150)")

print("== 14. cells in Y row ==")
for (mask,tag) in [(ycell,"yellow"),(gcell,"green"),(pcell,"pink")]:
    sub = mask[222:262, 150:910]
    colc = sub.sum(axis=0)
    print(f"  Y-row {tag} col clusters:", runs(colc>1,1), "(+150)")

print("== 15. dots in rows ==")
for (mask,tag,(y0,y1)) in [(gcell,"green dots X-row",(413,443)),(gcell,"green dots V-row",(466,508))]:
    sub = mask[y0:y1, 480:680]
    colc = sub.sum(axis=0)
    print(f"  {tag} clusters x480..680:", runs(colc>0,1), "(+480)")
bluedot = (b-r>40)&(b-g>25)&(b>150)
sub = bluedot[222:262, 480:680]
print("  Y-row blue dots:", runs(sub.sum(axis=0)>0,1), "(+480)")
