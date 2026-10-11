# Pass 6: per-edge red coverage + icon crop maps + border scans.
from PIL import Image
import numpy as np

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_024.jpg').convert('RGB')
a = np.asarray(im).astype(int)
r, g, b = a[..., 0], a[..., 1], a[..., 2]
red = (r > 140) & (g < 120) & (b < 120)

NODES = {'in': (202, 144, 46), 'garden': (360, 163, 46), 'the': (119, 294, 46),
         'Boy': (268, 288, 48), 'tree': (432, 366, 47), 'climbs': (253, 450, 46),
         'Boy_out': (743, 290, 50), 'Boy_in2': (608, 445, 48)}

def boundary(p, q, rp, rq):
    # point on circle p toward q, and on q toward p
    import math
    px, py, _ = p; qx, qy, _ = q
    dx, dy = qx - px, qy - py
    d = math.hypot(dx, dy)
    ux, uy = dx / d, dy / d
    return (px + ux * rp, py + uy * rp), (qx - ux * rq, qy - uy * rq)

def edge_report(name1, name2):
    p = NODES[name1]; q = NODES[name2]
    (x1, y1), (x2, y2) = boundary(p, q, p[2] + 3, q[2] + 3)
    n = 60
    hit = 0; widths = []
    for i in range(n + 1):
        t = i / n
        x, y = x1 + (x2 - x1) * t, y1 + (y2 - y1) * t
        xi, yi = int(round(x)), int(round(y))
        # perpendicular width of red run
        dx, dy = x2 - x1, y2 - y1
        L = (dx * dx + dy * dy) ** 0.5
        px_, py_ = -dy / L, dx / L
        w = 0
        for s in range(-8, 9):
            xx, yy = int(round(x + px_ * s)), int(round(y + py_ * s))
            if 0 <= yy < 540 and 0 <= xx < 960 and red[yy, xx]:
                w += 1
        if w > 0:
            hit += 1; widths.append(w)
    avgw = sum(widths) / len(widths) if widths else 0
    print(f"edge {name1:7s}<->{name2:7s}: coverage={hit}/{n+1} ({100*hit/(n+1):.0f}%)  avg_perp_width={avgw:.1f}px = {avgw:.2f}pt")

pairs = [('in','garden'),('in','the'),('in','Boy'),('the','garden'),('the','Boy'),
         ('the','tree'),('Boy','garden'),('Boy','tree'),('Boy','climbs'),
         ('climbs','tree'),('garden','tree')]
for p in pairs:
    edge_report(*p)

# dashed red link: input-Boy blue icon -> orange icon
import math
def line_report(x1, y1, x2, y2, label):
    n = 50; hit = 0
    for i in range(n + 1):
        t = i / n
        x, y = x1 + (x2 - x1) * t, y1 + (y2 - y1) * t
        xi, yi = int(round(x)), int(round(y))
        if red[max(0,yi-3):yi+4, max(0,xi-3):xi+4].any(): hit += 1
    print(f"{label}: dashed coverage {hit}/{n+1}")
line_report(660, 495, 790, 390, 'dashed link blue->orange')

def amap(x0, y0, x1, y1, label):
    print(f"== {label} x[{x0},{x1}] y[{y0},{y1}]")
    for yy in range(y0, y1):
        row = []
        for xx in range(x0, x1):
            p = a[yy, xx]
            if b[yy, xx] > 120 and b[yy, xx] - p[0] > 40 and p[1] < b[yy, xx]: c = 'B'
            elif p[0] > 190 and 60 < p[1] < 190 and p[2] < 110: c = 'O'
            elif p[0] > 140 and p[1] < 120 and p[2] < 120: c = 'R'
            elif p[0] > 228 and p[1] > 228 and p[2] > 228: c = 'w'
            elif p[0] < 90 and p[1] < 90 and p[2] < 90: c = '#'
            else: c = '.'
            row.append(c)
        print(''.join(row))

amap(95, 142, 140, 200, "'in' icon")
amap(780, 322, 836, 428, "orange icon")

def scanv(x, y0, y1, label):
    print(f"-- vscan x={x} {label}:")
    for y in range(y0, y1):
        p = a[y, x]
        print(f"   y={y} ({p[0]:3d},{p[1]:3d},{p[2]:3d})")

scanv(268, 236, 246, "Boy(in) top edge")
scanv(202, 94, 102, "'in' top edge")
