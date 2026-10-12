from PIL import Image
import numpy as np
im = np.asarray(Image.open('slide-1.png').convert('RGB')).astype(int)
r, g, b = im[:,:,0], im[:,:,1], im[:,:,2]
luma = (0.299*r+0.587*g+0.114*b)
S = 150/72.0
def px(pt): return pt * S
ink = luma < 200
f2s_x = lambda fx: (fx-17.628)/0.961230
f2s_y = lambda fy: (fy+0.045)/0.956566

def meas(y0pt, y1pt, x0pt, x1pt, label, tgt=None):
    y0,y1,x0,x1 = int(px(y0pt)), int(px(y1pt)), int(px(x0pt)), int(px(x1pt))
    m = ink[y0:y1, x0:x1]
    rows = np.where(m.any(axis=1))[0]; cols = np.where(m.any(axis=0))[0]
    if len(rows)==0: print(f"{label}: EMPTY"); return None
    ry0, ry1, rx0, rx1 = y0+rows.min(), y0+rows.max(), x0+cols.min(), x0+cols.max()
    line = f"{label}: y {ry0}..{ry1} x {rx0}..{rx1} (w {rx1-rx0+1}, h {ry1-ry0+1})"
    if tgt:
        names = ["y0","y1","x0","x1"]
        line += "  DELTA " + " ".join((f"{names[i]} {[ry0,ry1,rx0,rx1][i]-px(v):+.0f}" if v is not None else f"{names[i]} ----") for i,v in enumerate(tgt))
    print(line)
    return (ry0,ry1,rx0,rx1)

meas(112, 140, 46, 145, "R1 label L1", tgt=(119.2, 131.8, 53.4, None))
meas(140, 152, 46, 145, "R1 label L2 mid", tgt=(134.9, 145.4, 53.4, None))
meas(148, 170, 46, 145, "R1 label L3", tgt=(151.6, 165.2, 53.4, None))
meas(195, 215, 46, 145, "R2 label L1", tgt=(200.8, 211.2, 52.4, None))
meas(213, 236, 46, 145, "R2 label L2", tgt=(216.4, 230.0, 52.4, None))
meas(270, 290, 46, 145, "R3 label L1", tgt=(275.0, 286.5, 49.3, None))
meas(288, 308, 46, 145, "R3 label L2", tgt=(291.7, 302.2, 49.3, None))
meas(324, 348, 196, 240, "+d label 1", tgt=(327.3, 342.9, 208.5, 226.1))
meas(324, 348, 270, 310, "+d label 2", tgt=(327.3, 342.9, 281.3, 297.9))
meas(324, 348, 352, 396, "+d label 3", tgt=(327.3, 342.9, 364.5, 383.2))
meas(324, 348, 780, 826, "+d label 6", tgt=(327.3, 342.9, 797.3, 817.0))
meas(308, 315.5, 256, 265, "shaft1 mid", tgt=(306.9, None, 257.5, 263.5))
meas(318, 324, 250, 271, "head1", tgt=(316.5, 321.0, 253.2, 267.8))
meas(378, 404, 58, 898, "lead", tgt=(384.8, 398.3, 64.9, 890.9))
meas(402, 428, 58, 210, "problems", tgt=(408.8, 421.3, 63.8, 142.9))
meas(425, 452, 95, 790, "b1 text-only", tgt=(431.8, 444.3, 99.2, 773.4))
meas(447, 476, 95, 898, "b2L1", tgt=(453.8, 466.3, 99.2, 896.2))
meas(470, 496, 75, 360, "b2L2", tgt=(476.8, 489.3, 84.7, 338.5))
meas(493, 520, 95, 780, "b3", tgt=(499.8, 512.3, 99.2, 754.6))
# wrap check: no ink between lines (bands that must be EMPTY)
def empty(y0pt, y1pt, x0pt, x1pt, label):
    y0,y1,x0,x1 = int(px(y0pt)), int(px(y1pt)), int(px(x0pt)), int(px(x1pt))
    m = ink[y0:y1, x0:x1]
    n = int(m.sum())
    print(f"{label}: ink px {n} {'OK' if n==0 else 'VIOLATION'}")
empty(468, 472, 100, 890, "gap b2L1/b2L2")
empty(492, 496, 100, 890, "gap b2L2/b3")
empty(520, 528, 60, 890, "gap b3/hl-bottom")
empty(112, 116, 300, 700, "gap title/subtitle-ish top")
