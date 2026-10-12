from PIL import Image
import numpy as np
im = np.asarray(Image.open('unique_slides/slide_059.jpg').convert('RGB')).astype(int)

pts = {
 "bar1 (700,287)": (287,700), "bar2 (700,309)": (309,700), "bar3 (700,360)": (360,700),
 "mid band (700,335)": (335,700), "mid band (150,335)": (335,150),
 "rose below bars (700,375)": (375,700),
 "container edge? (80,335)": (335,80), "container edge? (70,335)": (335,70),
 "tan bar (200,94)": (94,200),
 "circle1 (437,95)": (95,437), "circle2 (513,95)": (95,513), "circle3 (585,95)": (95,585),
 "circle1 top (437,80)": (80,437),
 "output row (700,243)": (243,700), "output row edge (170,243)": (243,170),
 "pink container (700,440)": (440,700), "pink (620,440)": (440,620),
 "peach row (700,497)": (497,700),
 "plus circle (497,455)": (455,497),
 "GAP box (510,197)": (197,510),
 "pooled sq1 (400,155)": (155,400), "pooled sq2 (410,155)": (155,410), "pooled sq3 (420,155)": (155,420),
 "pooled sq4 (430,155)": (155,430),
 "left margin (40,300)": (300,40), "margin inside diagram (100,120)": (120,100),
 "below panel? (480,530)": (530,480),
}
for lbl,(y,x) in pts.items():
    print(f"{lbl}: rgb {tuple(int(v) for v in im[y,x])}")

# diagram border hunt: scan row 120 (clean white zone between C labels and tan bar? no, tan bar at 82..)
# scan row 75 x 0..200
print("\nrow75 x55..100:", [tuple(int(v) for v in im[75,x]) for x in range(55,100,3)])
print("row120 x55..100:", [tuple(int(v) for v in im[120,x]) for x in range(55,100,3)])
print("col480 y55..75:", [tuple(int(v) for v in im[y,480]) for y in range(55,76,2)])
print("row450 x880..945:", [tuple(int(v) for v in im[450,x]) for x in range(880,946,4)])
print("col480 y500..520:", [tuple(int(v) for v in im[y,480]) for y in range(500,521)])
