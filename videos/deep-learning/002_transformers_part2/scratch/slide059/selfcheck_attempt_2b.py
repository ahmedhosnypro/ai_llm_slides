# Refined closed-loop edge checks (profile-based, immune to neighboring ink).
from PIL import Image
import numpy as np
ren = np.asarray(Image.open('recreated_pptx/qa/slide059/render_2.png').convert('RGB')).astype(int)
R, G, B = ren[:,:,0], ren[:,:,1], ren[:,:,2]
S = 2000/960.0
def px(v): return int(round(v * S))

def edges(pred, x0,y0,x1,y1, exp, name, tol=5, frac=0.5):
    X0,Y0,X1,Y1 = px(x0),px(y0),px(x1),px(y1)
    sub = pred(R[Y0:Y1,X0:X1], G[Y0:Y1,X0:X1], B[Y0:Y1,X0:X1])
    h, w = sub.shape
    cols = sub.sum(axis=0); rows = sub.sum(axis=1)
    cth, rth = frac*h, frac*w
    cx = [i for i in range(w) if cols[i]>cth]; ry = [i for i in range(h) if rows[i]>rth]
    if not cx or not ry:
        print(f'FAIL {name}: no solid ink'); return
    L,Rt,T,Bt = cx[0]+X0, cx[-1]+X0, ry[0]+Y0, ry[-1]+Y0
    e = [px(exp[0]), px(exp[1]), px(exp[2]), px(exp[3])]
    d = [L-e[0], Rt-e[1], T-e[2], Bt-e[3]]
    ok = max(abs(v) for v in d) <= tol
    print(f'{"PASS" if ok else "FAIL"} {name}: L{L} R{Rt} T{T} B{Bt} vs {e}  d={d}')

tan    = lambda R,G,B: (R>200)&(R<252)&(G>170)&(G<228)&(B>120)&(B<205)&(R-B>30)
navy   = lambda R,G,B: (R<100)&(G<100)&(B>85)
lblue  = lambda R,G,B: (B>238)&(R>195)&(R<235)&(G>218)&(G<245)
pinkf  = lambda R,G,B: (R>240)&(G>200)&(G<235)&(B>235)
white  = lambda R,G,B: (R>235)&(G>235)&(B>235)
nonwht = lambda R,G,B: (R<238)|(G<238)|(B<232)
redfl  = lambda R,G,B: (R>150)&(G<90)&(B<90)

# 1. tan bar edges (window = bar neighborhood only)
edges(tan, 150,86,900,124, (163.7,879.3,92.1,118.2), 'tan bar', tol=5)
# 2. circle1 navy (window tight around circle, excluding arrow above: y 90..128)
edges(navy, 405,90,470,128, (419.0,456.5,89.9,125.6), 'circle1 navy', tol=5)
# 3. output row LBLUE fill (center band of the fill)
edges(lblue, 140,240,930,268, (155.3,903.4,236.5,270.0), 'output row fill', tol=6, frac=0.4)
# 4. input lilac container (center band)
edges(pinkf, 30,410,945,535, (46.2,909.6,403.4,539.5), 'input container fill', tol=8, frac=0.4)
# 5. encoder title white text only (y 336..363, excludes bar3 text below)
edges(white, 360,336,650,363, (388.8,612.6,342.2,358.9), 'encoder title', tol=6, frac=0.15)
# 6. pooled row cells (y band between fan lines and arrow4)
edges(nonwht, 370,157,650,171, (385.3,637.1,157.5,171.0), 'pooled row cells', tol=6, frac=0.5)
# 7. plus disc (window below word-row labels)
edges(redfl, 475,458,525,497, (487.6,510.5,466.7,488.6), 'plus disc', tol=5)
# 8. bar1 dark-red edges (window at bar1 only)
barr = lambda R,G,B: (R>120)&(R<200)&(G<60)&(B<70)
edges(barr, 130,288,900,312, (147.0,870.1,292.0,310.3), 'encoder bar1', tol=5)
