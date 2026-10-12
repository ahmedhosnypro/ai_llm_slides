# m8_diagram.py — precise targeted measurements of slide_059 diagram elements
# Frame 960x540, 1px=1pt. slide_x = (fx-18.63)/0.96123, slide_y = fy/0.95556.
from PIL import Image
import numpy as np

im = np.asarray(Image.open('unique_slides/slide_059.jpg').convert('RGB')).astype(int)
H, W, _ = im.shape
r, g, b = im[:,:,0], im[:,:,1], im[:,:,2]

def bbox(mask, y0, y1, x0, x1, label):
    sub = mask[y0:y1, x0:x1]
    ys, xs = np.where(sub)
    if len(xs) == 0:
        print(f"  {label}: EMPTY in region")
        return None
    bx0, bx1, by0, by1 = xs.min()+x0, xs.max()+x0, ys.min()+y0, ys.max()+y1-1
    bx1 = xs.max()+x0; by1 = ys.max()+y0
    n = len(xs)
    print(f"  {label}: x {bx0}..{bx1}  y {by0}..{by1}  (n={n})  cx={(bx0+bx1)/2:.1f} cy={(by0+by1)/2:.1f}")
    return (bx0, bx1, by0, by1, n)

def runs(bools, min_len=2):
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
def rep(label, bx0, bx1, by0, by1):
    print(f"    -> slide pt: x {sx(bx0):.1f}..{sx(bx1):.1f}  y {sy(by0):.1f}..{sy(by1):.1f}  w {sx(bx1)-sx(bx0):.1f} h {sy(by1)-sy(by0):.1f}")

print("== 1. PINK input container (FADBD8 ~ (250,219,216)) ==")
pink = (abs(r-250)<14)&(abs(g-219)<18)&(abs(b-216)<18)
pb = bbox(pink, 370, 525, 40, 920, "pink fill")
if pb: rep("pink", *pb[:4])
# border of pink container? sample around its edges later.

print("== 2. GREEN dashed rect (word-embedding row) ==")
green = (g > r+45)&(g > b+45)&(g>110)&(g<210)
gb = bbox(green, 385, 465, 150, 920, "green stroke")
if gb: rep("green", *gb[:4])
print("  green rows at col 700:", runs(green[:,700],1))
print("  green cols at row 415:", runs(green[415,:],1)[:6], "...", runs(green[415,:],1)[-3:])

print("== 3. ORANGE dashed rect (position row) ==")
orange = (r>200)&(g>90)&(g<175)&(b<90)
ob = bbox(orange, 440, 520, 150, 920, "orange stroke")
if ob: rep("orange", *ob[:4])
print("  orange rows at col 700:", runs(orange[:,700],1))
print("  orange cols at row 460:", runs(orange[460,:],1)[:6], "...", runs(orange[460,:],1)[-3:])

print("== 4. PEACH fill (FDEBD0 ~ (253,235,208)) ==")
peach = (abs(r-253)<8)&(abs(g-235)<12)&(abs(b-208)<14)
pchb = bbox(peach, 440, 520, 150, 920, "peach fill")
if pchb: rep("peach", *pchb[:4])

print("== 5. RED + circle (C0392B ~ (192,57,43)) ==")
plusred = (r>150)&(r<225)&(g<100)&(b<100)&(r-g>70)
plb = bbox(plusred, 415, 490, 440, 560, "plus disc")
if plb: rep("plus", *plb[:4])

print("== 6. ROSE encoder container (CD5C5C ~ (205,92,92)) ==")
rose = (abs(r-205)<28)&(abs(g-92)<38)&(abs(b-92)<38)
rb = bbox(rose, 250, 400, 100, 920, "rose")
if rb: rep("rose", *rb[:4])
print("  rose rows at col 150:", runs(rose[:,150],1))
print("  rose rows at col 870:", runs(rose[:,870],1))
print("  rose cols at row 335 (mid-band):", runs(rose[335,:],2)[:4], "...", runs(rose[335,:],2)[-4:])
print("  rose cols at row 270 (above bar1):", runs(rose[270,:],2)[:4], "...", runs(rose[270,:],2)[-4:])
print("  rose cols at row 378 (below bar3):", runs(rose[378,:],2)[:4], "...", runs(rose[378,:],2)[-4:])

print("== 7. DARK-RED bars (core ~ (160,0,0)) ==")
dr = (r>=130)&(r<225)&(g<80)&(b<80)
print("  bar rows at col 200:", runs(dr[:,200],2))
print("  bar rows at col 700:", runs(dr[:,700],2))
print("  bar rows at col 830:", runs(dr[:,830],2))
for (y0,y1,tag) in [(275,300,"bar1"),(296,322,"bar2"),(348,373,"bar3")]:
    cols = np.where(dr[y0:y1,:].sum(axis=0) > (y1-y0)*0.5)[0]
    if len(cols): print(f"  {tag}: x {cols.min()}..{cols.max()} (y {y0}..{y1})")

print("== 8. WHITE ellipsis dots between bar2 and bar3 (y 320..350) ==")
whitem = (r>235)&(g>235)&(b>235)
band = whitem[320:350, 150:870]
colcnt = band.sum(axis=0)
cols = runs(colcnt > 8, 2)
print("  white col clusters:", cols)

print("== 9. LIGHT-BLUE output row (D6EAF8 ~ (214,234,248)) + blue dashed border ==")
lblu = (abs(r-214)<16)&(abs(g-234)<12)&(abs(b-248)<10)
lb = bbox(lblu, 210, 275, 150, 920, "lightblue fill")
if lb: rep("lightblue", *lb[:4])
blue = (b > r+55)&(b > g+45)&(b>130)
bb = bbox(blue, 210, 275, 150, 920, "blue border")
if bb: rep("blue-border", *bb[:4])
print("  blue rows at col 700:", runs(blue[:,700],1))
print("  blue rows at col 300:", runs(blue[:,300],1))
print("  blue cols at row 226:", runs(blue[226,:],1)[:8])
print("  blue cols at row 262:", runs(blue[262,:],1)[:8])

print("== 10. GAP box (white + black thin border), y 165..215 ==")
black = (r<110)&(g<110)&(b<110)
gpb = bbox(black, 160, 220, 150, 920, "black ink (GAP border+text)")
print("  black rows at col 200:", runs(black[:,200],1))
print("  black cols at row 178:", runs(black[178,:],1)[:4], "...", runs(black[178,:],1)[-4:])
print("  black cols at row 207:", runs(black[207,:],1)[:4], "...", runs(black[207,:],1)[-4:])
print("  black rows at col 165:", runs(black[:,165],1))
print("  black rows at col 880:", runs(black[:,880],1))

print("== 11. POOLED row (y 130..170): colored squares ==")
ysq = (r>215)&(g>190)&(b<130)&(r-b>90)
gsq = (g > r+30)&(g > b+30)&(g>150)&(g<230)
psq = (r>200)&(r-g>45)&(r-b>45)
print("  yellow bbox:", end=" "); bbox(ysq, 130, 172, 300, 700, "yellow sq")
print("  green bbox:", end=" "); bbox(gsq, 130, 172, 300, 700, "green sq")
print("  pink bbox:", end=" "); bbox(psq, 130, 172, 300, 700, "pink sq")
rowc = 155
ymid = runs(ysq[rowc,300:700]|gsq[rowc,300:700]|psq[rowc,300:700], 1)
print(f"  colored runs at row {rowc} (offset+300):", [(a+300,c+300) for a,c in ymid])

print("== 12. TAN softmax bar (F5CBA7 ~ (245,203,167)) ==")
tan = (abs(r-245)<14)&(abs(g-203)<16)&(abs(b-167)<20)
tb = bbox(tan, 55, 140, 100, 920, "tan")
if tb: rep("tan", *tb[:4])
print("  tan rows at col 250:", runs(tan[:,250],1))
print("  tan rows at col 700:", runs(tan[:,700],1))
print("  tan cols at row 92:", runs(tan[92,:],1)[:5], "...", runs(tan[92,:],1)[-3:])

print("== 13. NAVY circles (dark blue) in y 50..140 ==")
navy = (b > r+35)&(b > g+30)&(b>100)&(r<120)
nb = bbox(navy, 50, 140, 150, 920, "navy all")
# connected-ish: col profile
colcnt = navy[50:140,:].sum(axis=0)
print("  navy col clusters (x, count>4):", runs(colcnt>4, 4))
rowcnt = navy[50:140,150:920].sum(axis=1)
print("  navy row profile peaks:", [(y+50,int(rowcnt[y])) for y in range(90) if rowcnt[y]>30])
for cx in [437, 513, 585]:
    print(f"  navy rows at col {cx}:", runs(navy[:,cx],1))

print("== 14. RED base nodes under circles (C0392B) ==")
print("  plus-red in y 105..135:", end=" "); bbox(plusred, 105, 135, 150, 920, "red base")

print("== 15. FAN lines (dark red thin) y 165..230 ==")
fan = (r>120)&(r<225)&(g<85)&(b<85)&(r-g>60)
print("  fan col clusters at row 200:", runs(fan[200,:],0))
print("  fan col clusters at row 215:", runs(fan[215,:],0))
print("  fan col clusters at row 180:", runs(fan[180,:],0))

print("== 16. C1/C2/C3 + Output Classes (blue text, y 5..55) ==")
bluetxt = (b > r+40)&(b > g+30)&(b>120)
cb = bbox(bluetxt, 5, 58, 250, 920, "blue text top")
print("  blue col clusters y 5..58:", runs(bluetxt[5:58,:].sum(axis=0)>2, 6))

print("== 17. LEFT annotations (x 40..270) ==")
redtxt = (r>130)&(r<230)&(g<90)&(b<90)&(r-g>60)
greentxt = green
bluetxt2 = bluetxt
print("  red ann y 90..130:", end=" "); bbox(redtxt, 90, 130, 40, 280, "red ann softmax")
print("  red ann y 165..215:", end=" "); bbox(redtxt, 165, 215, 40, 280, "red ann pooled")
print("  red ann y 275..320:", end=" "); bbox(redtxt, 275, 320, 40, 280, "red ann output")
print("  red ann y 375..400:", end=" "); bbox(redtxt, 375, 400, 40, 280, "red ann input")
print("  green ann y 400..465:", end=" "); bbox(greentxt, 400, 465, 40, 280, "green ann")
print("  blue ann y 460..515:", end=" "); bbox(bluetxt2, 460, 515, 40, 280, "blue ann")

print("== 18. BLOCK ARROWS (blue outline) four bands, x 430..570 ==")
print("  arrow1 y 368..392:", end=" "); bbox(blue, 368, 392, 430, 570, "arrow1")
print("  arrow2 y 255..272:", end=" "); bbox(blue, 255, 272, 430, 570, "arrow2")
print("  arrow3 y 205..222:", end=" "); bbox(blue, 205, 222, 430, 570, "arrow3")
print("  arrow4 y 160..178:", end=" "); bbox(blue, 160, 178, 430, 570, "arrow4")
print("  arrow1 rows at col 500:", runs(blue[368:392,500],0), "(rel)")
print("  arrow2 rows at col 500:", runs(blue[255:272,500],0), "(rel)")
