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
    if len(rows)==0: print(f"{label}: EMPTY"); return
    ry0, ry1, rx0, rx1 = y0+rows.min(), y0+rows.max(), x0+cols.min(), x0+cols.max()
    line = f"{label}: y {ry0}..{ry1} x {rx0}..{rx1} (w {rx1-rx0+1}, h {ry1-ry0+1})"
    if tgt:
        tt = [v for v in tgt if v is not None]
        tv = [px(v) for v in tt]
        line += "  TARGET " + " ".join(f"{v:.0f}" for v in tv)
        d = []
        names = ["y0","y1","x0","x1"]
        for i, v in enumerate(tgt):
            if v is None: d.append("  ----")
            else:
                mv = [ry0,ry1,rx0,rx1][i]; d.append(f"{names[i]} {mv - px(v):+.0f}")
        line += "  DELTA " + " ".join(d)
    print(line)

meas(96, 112, 40, 145,  "R1 label L1", tgt=(119.2, 131.8, 53.4, None))
meas(111, 125, 40, 145, "R1 label L2", tgt=(134.9, 145.4, 53.4, None))
meas(126, 140, 40, 145, "R1 label L3", tgt=(151.6, 165.2, 53.4, None))
meas(165, 180, 40, 145, "R2 label L1", tgt=(200.8, 211.2, 52.4, None))
meas(180, 195, 40, 145, "R2 label L2", tgt=(216.4, 230.0, 52.4, None))
meas(238, 253, 40, 145, "R3 label L1", tgt=(275.0, 286.5, 49.3, None))
meas(254, 268, 40, 145, "R3 label L2", tgt=(291.7, 302.2, 49.3, None))
meas(300, 326, 195, 240, "+d label 1", tgt=(327.3, 342.9, 208.5, 226.1))
meas(300, 313, 250, 272, "shaft1", tgt=(306.9, 317.5, 257.5, 263.5))
meas(300, 326, 275, 305, "+d label 2", tgt=(327.3, 342.9, 281.3, 297.9))
meas(300, 326, 780, 825, "+d label 6", tgt=(327.3, 342.9, 797.3, 817.0))
meas(134, 150, 165, 220, "R1 box1 text", tgt=(f2s_y(131), f2s_y(142), f2s_x(184), f2s_x(226)))
meas(134, 150, 742, 804, "R1 box7 text", tgt=(f2s_y(131), f2s_y(142), f2s_x(736), f2s_x(786)))
meas(205, 222, 160, 218, "R2 box1 text", tgt=(f2s_y(198), f2s_y(212), f2s_x(180), f2s_x(221)))
meas(286, 304, 158, 216, "R3 box1 text", tgt=(f2s_y(277), f2s_y(290), f2s_x(196), f2s_x(204)))
meas(286, 304, 330, 370, "R3 box3 text", tgt=(f2s_y(277), f2s_y(288), f2s_x(336), f2s_x(354)))
meas(136, 152, 620, 725, "R1 dots", tgt=(f2s_y(134), f2s_y(142), f2s_x(624), f2s_x(701)))
meas(209, 226, 620, 725, "R2 dots", tgt=(f2s_y(203), f2s_y(212), f2s_x(624), f2s_x(703)))
meas(360, 370, 50, 912, "hl top border", tgt=(363.9, 366.5, 54.5, 907.6))
meas(518, 532, 50, 912, "hl bottom border", tgt=(523.3, 525.9, 54.5, 907.6))
meas(396, 416, 55, 900, "lead", tgt=(384.8, 398.3, 64.9, 890.9))
meas(418, 432, 55, 210, "problems", tgt=(408.8, 421.3, 63.8, 142.9))
meas(434, 450, 75, 790, "b1", tgt=(431.8, 444.3, 82.4, 773.4))
meas(452, 470, 75, 910, "b2L1", tgt=(453.8, 466.3, 82.4, 896.2))
meas(474, 492, 75, 360, "b2L2", tgt=(476.8, 489.3, 84.7, 338.5))
meas(496, 514, 75, 780, "b3", tgt=(499.8, 512.3, 82.4, 754.6))
meas(430, 446, 78, 98, "b1 dot", tgt=(432.0, 443.0, 82.4, 93.3))
# color samples
def cs(ypt, xpt, label):
    print(f"{label}: {tuple(im[int(px(ypt)), int(px(xpt))])}")
cs(500, 300, "hl fill")
cs(140, 700, "R1 container interior (gap)")
cs(210, 700, "R2 container interior")
cs(295, 700, "R3 container interior (gap)")
cs(300, 262, "shaft1 fill")
