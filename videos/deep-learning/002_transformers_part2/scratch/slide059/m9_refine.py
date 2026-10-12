# m9_refine.py — refined per-element measurements for slide_059
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

def sx(fx): return (fx - 18.63) / 0.96123
def sy(fy): return fy / 0.95556

print("== A. TOP BAND y 44..82: all ink (non-white, non-panel-gray) ==")
ink = (abs(r-g)>25)|(abs(g-b)>25)|(abs(r-b)>25)
band = ink[44:82, 150:920]
colcnt = band.sum(axis=0)
print("  ink col clusters:", [(a+150,c+150) for a,c in runs(colcnt>2, 4)])
rowcnt = band.sum(axis=1)
print("  ink row profile:", [(y+44,int(rowcnt[y])) for y in range(38) if rowcnt[y]>5])
# sample colors of the clusters
for (a,c) in runs(colcnt>2,4):
    xm = (a+c)//2+150
    ys, xs = np.where(band[:, a:c+1])
    if len(ys):
        ym = int(np.median(ys))+44
        print(f"  cluster x {a+150}..{c+150} sample ({xm},{ym}):", tuple(im[ym,xm]))

print("== B. ROSE container edges ==")
for row in [287, 324, 360]:
    print(f"  row {row} cols 90..170:", [(x, tuple(im[row,x])) for x in range(90, 172, 6)])
for row in [287, 324, 360]:
    print(f"  row {row} cols 845..895:", [(x, tuple(im[row,x])) for x in range(845, 896, 4)])
print("  col 150 rows 265..285:", [(y, tuple(im[y,150])) for y in range(265, 286, 3)])
print("  col 150 rows 365..385:", [(y, tuple(im[y,150])) for y in range(365, 386, 3)])
print("  col 870 rows 265..285:", [(y, tuple(im[y,870])) for y in range(265, 286, 3)])
print("  col 870 rows 365..385:", [(y, tuple(im[y,870])) for y in range(365, 386, 3)])

print("== C. ELLIPSIS band y 318..352: raw column scan ==")
whiteish = (r>225)&(g>225)&(b>225)
band = whiteish[318:352, 150:870]
colcnt = band.sum(axis=0)
cl = runs(colcnt>3, 2)
print("  white col clusters (>3px):", [(a+150,c+150) for a,c in cl])
print("  row profile of band:", [(y+318,int(band[y].sum())) for y in range(34) if band[y].sum()>10])

print("== D. GAP box: border hunt ==")
print("  col 480 rows 168..215:", [(y, tuple(im[y,480])) for y in range(168, 216, 4)])
print("  col 300 rows 168..215:", [(y, tuple(im[y,300])) for y in range(168, 216, 4)])
print("  row 190 cols 155..185:", [(x, tuple(im[190,x])) for x in range(155, 186, 4)])
print("  row 190 cols 855..900:", [(x, tuple(im[190,x])) for x in range(855, 901, 4)])
print("  row 176 cols 160..900 dark cols:", runs(((r[176]<150)&(g[176]<150)&(b[176]<150))[160:900],0), "(+160)")

print("== E. POOLED row precise ==")
print("  col 480 rows 125..165:", [(y, tuple(im[y,480])) for y in range(125, 166, 3)])
row = 139
nonwhite = (abs(r[row]-r[row-6])>18)|(abs(g[row]-g[row-6])>18)
print("  transitions row 133..145 vs 127: cols:", runs(nonwhite[300:700],0), "(+300)")

print("== F. TAN bar edges at clean cols ==")
for col in [750, 800, 850, 300, 200]:
    coltan = runs((abs(r[:,col]-245)<16)&(abs(g[:,col]-203)<18)&(abs(b[:,col]-167)<22), 1)
    print(f"  col {col} tan runs (y 60..140):", [t for t in coltan if 60 <= t[0] <= 140])

print("== G. NAVY circles per-cluster bbox ==")
navy = (b > r+35)&(b > g+30)&(b>100)&(r<120)
for (x0,x1,tag) in [(420,460,"c1"),(492,532,"c2"),(565,605,"c3")]:
    sub = navy[50:130, x0:x1]
    ys, xs = np.where(sub)
    if len(xs): print(f"  {tag}: x {xs.min()+x0}..{xs.max()+x0}  y {ys.min()+50}..{ys.max()+50}  cx={(xs.min()+xs.max())/2+x0:.1f} cy={(ys.min()+ys.max())/2+50:.1f} n={len(xs)}")
# circle interior colors
for (cx,cy,tag) in [(440,105,"c1-mid"),(512,105,"c2-mid"),(585,105,"c3-mid"),(440,75,"c1-top"),(512,75,"c2-top")]:
    print(f"  {tag} ({cx},{cy}):", tuple(im[cy,cx]))
# yellow Softmax text in circles
ytxt = (r>200)&(g>170)&(b<140)&(r-b>80)
for (x0,x1,tag) in [(420,460,"c1"),(492,532,"c2"),(565,605,"c3")]:
    sub = ytxt[55:125, x0:x1]
    ys, xs = np.where(sub)
    if len(xs): print(f"  {tag} yellow text: x {xs.min()+x0}..{xs.max()+x0} y {ys.min()+55}..{ys.max()+55} n={len(xs)}")

print("== H. RED base nodes per circle ==")
plusred = (r>150)&(r<225)&(g<100)&(b<100)&(r-g>70)
for (x0,x1,tag) in [(425,460,"c1"),(495,532,"c2"),(565,605,"c3")]:
    sub = plusred[110:135, x0:x1]
    ys, xs = np.where(sub)
    if len(xs): print(f"  {tag} red base: x {xs.min()+x0}..{xs.max()+x0} y {ys.min()+110}..{ys.max()+110} n={len(xs)}")

print("== I. FAN lines raw scan rows 130..165, x 380..660 ==")
reddish = (r-g>22)&(r-b>15)&(r>130)
for row in [135, 145, 155, 162, 168, 175]:
    print(f"  row {row} reddish cols:", runs(reddish[row,380:660],0), "(+380)")

print("== J. + circle precise ==")
print("  col 500 rows 415..475:", [(y, tuple(im[y,500])) for y in range(415, 476, 4)])
print("  row 445 cols 480..525:", [(x, tuple(im[445,x])) for x in range(480, 526, 3)])

print("== K. GREEN/ORANGE dashed rects: looser masks ==")
grn = (g > r+22)&(g > b+22)&(g>95)
print("  green rows at col 700:", runs(grn[:,700],0))
print("  green rows at col 300:", runs(grn[:,300],0))
print("  green cols at row 421:", runs(grn[421,:],0)[:8], "...")
org = (r>190)&(g>80)&(g<190)&(b<120)&(r-b>80)
print("  orange rows at col 700:", runs(org[:,700],0))
print("  orange rows at col 300:", runs(org[:,300],0))
print("  orange cols at row 462:", runs(org[462,:],0)[:8], "...")

print("== L. ROWS: white X/Y boxes + cells (word-embedding row y 400..450) ==")
print("  col 250 rows 395..460:", [(y, tuple(im[y,250])) for y in range(395, 461, 5)])
print("  row 425 cols 165..900 white-box runs:")
whiterow = (r>238)&(g>238)&(b>238)
print("   ", [(a+165,c+165) for a,c in runs(whiterow[425,165:900],3)])

print("== M. OUTPUT row boxes ==")
print("  row 242 white-box runs:")
print("   ", [(a+165,c+165) for a,c in runs(whiterow[242,165:900],3)])
print("  col 250 rows 215..270:", [(y, tuple(im[y,250])) for y in range(215, 271, 5)])

print("== N. POSITION row boxes ==")
print("  row 487 white-box runs:")
print("   ", [(a+165,c+165) for a,c in runs(whiterow[487,165:900],3)])
print("  col 250 rows 465..515:", [(y, tuple(im[y,250])) for y in range(465, 516, 5)])

print("== O. LEFT annotations precise (x<160) ==")
ink2 = (abs(r-g)>30)|(abs(g-b)>30)|(abs(r-b)>30)
for (y0,y1,tag) in [(145,200,"pooled-note"),(300,345,"output-seq"),(378,402,"input-seq"),(405,450,"word-emb"),(458,505,"position"),(85,115,"softmax-left")]:
    sub = ink2[y0:y1, 45:165]
    ys, xs = np.where(sub)
    if len(xs):
        print(f"  {tag}: x {xs.min()+45}..{xs.max()+45} y {ys.min()+y0}..{ys.max()+y0} n={len(xs)}", end=" ")
        xm = int(np.median(xs))+45; ym=int(np.median(ys))+y0
        print("color@med:", tuple(im[ym,xm]))
    else:
        print(f"  {tag}: EMPTY")

print("== P. ARROWS precise (x 470..550) ==")
blue = (b > r+45)&(b > g+35)&(b>120)
for (y0,y1,tag) in [(160,180,"arrow4"),(200,224,"arrow3"),(250,275,"arrow2"),(365,395,"arrow1")]:
    sub = blue[y0:y1, 470:550]
    ys, xs = np.where(sub)
    if len(xs):
        print(f"  {tag}: x {xs.min()+470}..{xs.max()+470} y {ys.min()+y0}..{ys.max()+y0} n={len(xs)}")
print("  arrow1 col 510 rows 360..400:", [(y, tuple(im[y,510])) for y in range(360, 401, 4)])
print("  arrow2 col 510 rows 245..285:", [(y, tuple(im[y,510])) for y in range(245, 286, 4)])
