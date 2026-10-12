from PIL import Image
import numpy as np
from collections import Counter
im = Image.open('videos/deep-learning/002_transformers_part2/unique_slides/slide_014.jpg').convert('RGB')
A = np.asarray(im).astype(int)
def dom(x0,y0,x1,y1,label,n=6):
    p = A[y0:y1, x0:x1].reshape(-1,3)
    q = (p//16*16)
    c = Counter(map(tuple, q))
    tot = len(q)
    top = c.most_common(n)
    print(f"{label} [{x0},{y0} - {x1},{y1}]: " + ", ".join(f"{t} {cnt*100//tot}%" for t,cnt in top))
def edge_scan_h(y, x0, x1, label):
    prev=None; out=[]
    for x in range(x0,x1):
        c=tuple(A[y,x]); key=(c[0]//20,c[1]//20,c[2]//20)
        if key!=prev: out.append(f"x{x}{c}"); prev=key
    print(f"{label} y={y}: "+" | ".join(out))
def edge_scan_v(x, y0, y1, label):
    prev=None; out=[]
    for y in range(y0,y1):
        c=tuple(A[y,x]); key=(c[0]//20,c[1]//20,c[2]//20)
        if key!=prev: out.append(f"y{y}{c}"); prev=key
    print(f"{label} x={x}: "+" | ".join(out))

dom(320,255,450,265,"Y1 box top strip (inside, above squares)")
dom(320,460,450,468,"Y5 box strip")
dom(300,250,470,300,"Y1 box full")
dom(620,300,670,320,"matrix area left edge")
dom(640,300,820,330,"matrix row1 band")
dom(640,340,820,370,"matrix row2 band")
dom(640,380,820,410,"matrix row3 band")
dom(640,420,820,450,"matrix row4 band")
dom(840,300,880,330,"zero col box1")
dom(840,340,880,365,"zero col box2")
dom(60,255,300,265,"left panel mid strip")
dom(70,105,160,160,"fanned label area")
dom(230,140,300,180,"cluster1 + Sigma1 area")
dom(320,140,890,235,"design box")
dom(680,60,915,95,"badge area")
dom(190,52,815,95,"title band")
dom(80,72,860,95,"subtitle band")
print()
edge_scan_h(255, 295, 470, "Y1 top edge scan")
edge_scan_h(258, 295, 470, "Y1 top edge scan2")
edge_scan_v(330, 245, 310, "Y1 left part col x=330")
edge_scan_v(455, 245, 310, "col x=455 (Y right edge?)")
edge_scan_h(180, 296, 330, "design box left border y=180")
edge_scan_h(180, 885, 915, "design box right border y=180")
edge_scan_v(500, 130, 148, "design box top border x=500")
edge_scan_v(500, 230, 250, "design box bottom border x=500")
