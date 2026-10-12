from PIL import Image
import numpy as np
im = np.asarray(Image.open('slide2-1.png').convert('RGB')).astype(int)
r, g, b = im[:,:,0], im[:,:,1], im[:,:,2]
luma = (0.299*r+0.587*g+0.114*b)
S = 150/72.0
def px(pt): return int(pt * S)

m1 = (luma[:, :px(41.0)] < 180).sum()
m2 = (luma[:, px(920.0):] < 180).sum()
m3 = (luma[:px(43.5), px(41.0):px(920.0)] < 180).sum()
m4 = (luma[px(517.5):, px(41.0):px(920.0)] < 180).sum()
print("containment: ink left", int(m1), "right", int(m2), "above-panel", int(m3), "letterbox-zone", int(m4))

def gap(y0pt, y1pt, x0pt, x1pt, label):
    n = int((luma[px(y0pt):px(y1pt), px(x0pt):px(x1pt)] < 200).sum())
    print(f"gap {label}: {n} {'OK' if n==0 else 'CHECK'}")
gap(470.5, 475.5, 100, 890, "b2L1-desc/b2L2-cap")
gap(493.5, 497.5, 100, 890, "b2L2-desc/b3-cap")
gap(120.0, 126.0, 46, 140, "R1label above-L1")

sub = (luma[px(53):px(89), px(875):px(911)] < 150)
print("badge numeral ink px:", int(sub.sum()))

cnt = 0
for cx in (217.3, 289.6, 373.9, 452.4, 527.8, 807.2):
    n = int((luma[px(326):px(344), px(cx-12):px(cx+12)] < 200).sum())
    cnt += 1 if n > 20 else 0
print("+delta labels with ink:", cnt, "/6")

cnt = 0
for cx in (260.5, 339.5, 416.0, 493.5, 570.0, 844.1):
    n1 = int((luma[px(308):px(315), px(cx-3):px(cx+3)] < 210).sum())
    n2 = int((luma[px(317):px(321), px(cx-8):px(cx+8)] < 210).sum())
    cnt += 1 if (n1 > 10 and n2 > 10) else 0
print("arrows with shaft+head ink:", cnt, "/6")

rows = [
  [132.3, 154.2, [[161.6,223.5],[238.1,300.5],[315.1,376.5],[392.1,453.5],[468.0,529.4],[545.0,606.4],[739.5,806.1],[817.6,885.2]]],
  [203.9, 226.7, [[157.2,219.4],[233.9,295.8],[310.9,372.3],[387.4,448.8],[463.9,525.8],[540.8,602.2],[734.6,802.0],[812.9,882.1]]],
  [284.9, 307.4, [[156.4,217.3],[231.9,292.7],[309.9,371.3],[385.3,447.2],[463.9,525.2],[539.3,601.2],[733.8,800.9],[812.4,880.0]]],
]
ok = 0; total = 0; misses=[]
for yt, yb, boxes in rows:
    for (bx0, bx1) in boxes:
        total += 1
        n = int((luma[px(yt+4):px(yb-4), px(bx0+5):px(bx1-5)] < 190).sum())
        if n > 15: ok += 1
        else: misses.append((yt, bx0, bx1, n))
print(f"box texts with ink: {ok}/{total}", misses if misses else "")
