from PIL import Image
import numpy as np
im = np.asarray(Image.open('slide-1.png').convert('RGB')).astype(int)
r, g, b = im[:,:,0], im[:,:,1], im[:,:,2]
luma = (0.299*r+0.587*g+0.114*b)
S = 150/72.0
def px(pt): return pt * S
ink = luma < 200

def capline(y0pt, y1pt, x0pt, x1pt, label, tgt_cap):
    y0,y1,x0,x1 = int(px(y0pt)), int(px(y1pt)), int(px(x0pt)), int(px(x1pt))
    m = ink[y0:y1, x0:x1]
    prof = m.sum(axis=1)
    rows = np.where(prof >= 3)[0]
    if len(rows)==0: print(f"{label}: EMPTY"); return
    cap = y0+rows.min(); base_approx = y0+rows.max()
    print(f"{label}: cap {cap} ({cap/S:.1f}pt) vs target {tgt_cap}pt ({px(tgt_cap):.0f})  delta {cap-px(tgt_cap):+.0f}px  band-bottom {base_approx} ({base_approx/S:.1f}pt)")
    return cap

capline(378, 401, 70, 890, "lead cap", 384.8)
capline(404.5, 424, 70, 200, "problems cap", 408.8)
capline(426, 447, 110, 780, "b1 cap", 431.8)
capline(448.5, 469, 110, 890, "b2L1 cap", 453.8)
capline(471, 491.5, 90, 350, "b2L2 cap", 476.8)
capline(494, 514, 110, 760, "b3 cap", 499.8)
# problems width only (x extent of its own band)
y0,y1,x0,x1 = int(px(406)), int(px(422)), int(px(58)), int(px(220))
m = ink[y0:y1, x0:x1]
cols = np.where(m.any(axis=0))[0]
print("problems x:", x0+cols.min(), "..", x0+cols.max(), " target 133..298")
# b2L2 width
y0,y1,x0,x1 = int(px(478)), int(px(490)), int(px(80)), int(px(400))
m = ink[y0:y1, x0:x1]
cols = np.where(m.any(axis=0))[0]
print("b2L2 x:", x0+cols.min(), "..", x0+cols.max(), " target 176..705")
# lead width excluding hl border
y0,y1,x0,x1 = int(px(386)), int(px(398)), int(px(60)), int(px(900))
m = ink[y0:y1, x0:x1]
cols = np.where(m.any(axis=0))[0]
print("lead x:", x0+cols.min(), "..", x0+cols.max(), " target 135..1856")
# b1 width
y0,y1,x0,x1 = int(px(433)), int(px(445)), int(px(95)), int(px(800))
m = ink[y0:y1, x0:x1]
cols = np.where(m.any(axis=0))[0]
print("b1 x:", x0+cols.min(), "..", x0+cols.max(), " target 207..1611")
# shaft color
print("shaft px (312pt, 260.5pt):", tuple(im[int(px(312)), int(px(260.5))]))
print("head px (319pt, 260.5pt):", tuple(im[int(px(319)), int(px(260.5))]))
