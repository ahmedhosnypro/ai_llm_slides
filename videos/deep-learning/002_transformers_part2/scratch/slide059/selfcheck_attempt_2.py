# Closed-loop ink check for slide_059 (attempt 2 resume verification).
# 150dpi render = 2000x1125 px; slide pts -> px: *2000/960 (=150/72).
# Element ink bands (measured on the original frame, mapped to slide pts via
# slide_x=(fx-18.63)/0.96123, slide_y=fy/0.95556) vs the render's actual ink bbox.
from PIL import Image
import numpy as np

ren = np.asarray(Image.open('recreated_pptx/qa/slide059/render_2.png').convert('RGB')).astype(int)
R, G, B = ren[:,:,0], ren[:,:,1], ren[:,:,2]
S = 2000/960.0
def px(v): return v * S

def ink_bbox(x0,y0,x1,y1, pred, name, exp, tol=4):
    # search window in slide pts -> px; pred = ink predicate on (R,G,B)
    X0,Y0,X1,Y1 = int(px(x0)), int(px(y0)), int(px(x1)), int(px(y1))
    sub = pred(R[Y0:Y1,X0:X1], G[Y0:Y1,X0:X1], B[Y0:Y1,X0:X1])
    ys,xs = np.where(sub)
    if len(xs)==0:
        print(f'FAIL {name}: NO ink in window'); return
    bx0,bx1,by0,by1 = xs.min()+X0, xs.max()+X0, ys.min()+Y0, ys.max()+Y0
    dx0, dx1, dy0, dy1 = bx0-px(exp[0]), bx1-px(exp[1]), by0-px(exp[2]), by1-px(exp[3])
    ok = max(abs(dx0),abs(dx1),abs(dy0),abs(dy1)) <= tol
    print(f'{"PASS" if ok else "FAIL"} {name}: ink x {bx0}..{bx1} y {by0}..{by1} vs expected '
          f'x {px(exp[0]):.0f}..{px(exp[1]):.0f} y {px(exp[2]):.0f}..{px(exp[3]):.0f} '
          f'(deltas {dx0:+.1f}/{dx1:+.1f}/{dy0:+.1f}/{dy1:+.1f} px)')

# predicates
nonwhite  = lambda R,G,B: (R<235)|(G<235)|(B<230)
dred      = lambda R,G,B: (R>110)&(R<215)&(G<95)&(B<100)&(R-G>45)
tan       = lambda R,G,B: (R>200)&(R<250)&(G>170)&(G<225)&(B>130)&(B<200)
navyc     = lambda R,G,B: (R<110)&(G<110)&(B>90)
lblue     = lambda R,G,B: (B>230)&(R>195)&(R<235)&(G>215)
pinkc     = lambda R,G,B: (R>235)&(G>195)&(G<235)&(B>230)
peachc    = lambda R,G,B: (R>240)&(G>215)&(B>185)&(B<230)
rose      = lambda R,G,B: (R>170)&(R<225)&(G>85)&(G<135)&(B>90)&(B<140)
white_txt = lambda R,G,B: (R>230)&(G>230)&(B>230)
dark      = lambda R,G,B: (R<120)&(G<120)&(B<120)

# 1. tan softmax bar: frame x 176..864 y 88..113 -> slide (163.7..879.3, 92.1..118.2)
ink_bbox(140,80,920,135, tan, 'softmax tan bar', (163.7,879.3,92.1,118.2), tol=4)
# 2. navy circles row: frame y 84..120 c1 x 421..457 -> slide y 87.9..125.6, c1 x (419.0..456.5)
ink_bbox(400,80,480,135, navyc, 'softmax circle1', (419.0,456.5,87.9,125.6), tol=4)
# 3. GAP box black border+text: frame x 172..885 y 183..207 -> slide (159.5..901.0, 191.5..216.6)
ink_bbox(140,180,920,230, dark, 'GAP box', (159.5,901.0,191.5,216.6), tol=4)
# 4. output row blue-dashed border+fill band: frame x 168..887 y 226..258 -> (155.3..903.4, 236.5..270.0)
ink_bbox(140,225,930,285, lblue, 'output row band', (155.3,903.4,236.5,270.0), tol=5)
# 5. encoder rose container: frame x 144..877 y 274..372 -> (130.4..893.1, 286.7..389.3)
ink_bbox(110,270,930,400, rose, 'encoder container', (130.4,893.1,286.7,389.3), tol=5)
# 6. input lilac container: frame x 63..893 y 385.5..515.5 -> (46.2..909.6, 403.4..539.5)
ink_bbox(30,395,940,548, pinkc, 'input container', (46.2,909.6,403.4,539.5), tol=5)
# 7. white title text inside encoder: frame x 393..608 y 327..343 -> (388.8..612.6, 342.2..358.9)
ink_bbox(360,330,650,375, white_txt, 'encoder title', (388.8,612.6,342.2,358.9), tol=5)
# 8. pooled row: frame x 389..631 y 149..164.5 -> (385.3..637.1, 155.9..172.2)
ink_bbox(360,145,660,185, nonwhite, 'pooled row', (385.3,637.1,155.9,172.2), tol=5)
# 9. red X1 label ink: frame cx 212 y 422..430 -> slide cx 201.2, y 441.7..450.0
ink_bbox(180,430,225,465, dred, 'X1 label ink', (196.2,206.2,441.7,450.0), tol=5)
# 10. plus disc: frame x 487..509 y 446..467 -> (487.6..510.5, 466.7..488.6)
redfill = lambda R,G,B: (R>150)&(G<90)&(B<90)
ink_bbox(470,455,530,500, redfill, 'plus disc', (487.6,510.5,466.7,488.6), tol=5)
# 11. containment: no ink in the outer white margin beyond the gray panel (x<42pt or x>918pt, y<45pt)
mg = nonwhite(R[:int(px(44)),:], G[:int(px(44)),:], B[:int(px(44)),:])
print('margin-top stray ink px (y<44pt):', int(mg.sum()))
mgl = nonwhite(R[:, :int(px(41))], G[:, :int(px(41))], B[:, :int(px(41))])
print('margin-left stray ink px (x<41pt):', int(mgl.sum()))
mgr = nonwhite(R[:, int(px(919)):], G[:, int(px(919)):], B[:, int(px(919)):])
print('margin-right stray ink px (x>919pt):', int(mgr.sum()))
