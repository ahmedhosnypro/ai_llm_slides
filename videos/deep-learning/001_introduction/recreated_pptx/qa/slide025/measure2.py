#!/usr/bin/env python3
# measure2.py — slide_025 precise probes round 2
from PIL import Image

F = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_025.jpg'
im = Image.open(F).convert('RGB')
W, H = im.size
px = im.load()

def bbox(pred, x0, y0, x1, y1, step=1):
    xs, ys = [], []
    for y in range(y0, y1, step):
        for x in range(x0, x1, step):
            if pred(px[x, y]):
                xs.append(x); ys.append(y)
    if not xs: return None
    return (min(xs), min(ys), max(xs), max(ys))

def modal(x0, y0, x1, y1):
    from collections import Counter
    c = Counter()
    for y in range(y0, y1):
        for x in range(x0, x1):
            c[px[x, y]] += 1
    return c.most_common(6)

print("== title ink bbox (y55..100) ==")
print(bbox(lambda p: p[0] > 150 and p[1] < 80 and p[2] < 80, 200, 55, 760, 100))

print("== magenta/pink boxes: sample pixels ==")
print('IS box center', px[100, 112], px[95, 108], px[105, 118])
print('SL box center', px[645, 110], px[640, 105], px[650, 115])
def ispink(p): r,g,b = p; return r > 225 and 120 < g < 200 and b > 200
print('IS bbox', bbox(ispink, 40, 90, 200, 135))
print('SL bbox', bbox(ispink, 560, 90, 760, 135))
print('IS modal', modal(88, 103, 118, 120))
print('SL modal', modal(630, 100, 660, 118))

print("== dash line: rows 95..135, count magenta-dark px x140..600 ==")
def isdash(p): r,g,b = p; return 100 < r < 210 and g < 90 and 100 < b < 210 and abs(r-b) < 60
best = {}
for y in range(95, 135):
    n = sum(1 for x in range(140, 600) if isdash(px[x, y]))
    if n > 20: best[y] = n
print(best)
print("dash left extent: scan x at the dash row")
ydbest = max(best, key=best.get) if best else None
if ydbest:
    xs = [x for x in range(60, 940) if isdash(px[x, ydbest])]
    print('row', ydbest, 'x', xs[0], '..', xs[-1], 'n', len(xs))
    print('sample', px[xs[0]+2, ydbest], px[(xs[0]+xs[-1])//2, ydbest])

print("== panel bbox strict beige (200<=r<=240, 195<=g<=225, 180<=b<=215) ==")
def isb(p): r,g,b = p; return 200 <= r <= 240 and 195 <= g <= 225 and 180 <= b <= 215
rows = [y for y in range(100, 460) if sum(1 for x in range(70, 560, 3) if isb(px[x, y])) > 100]
print('panel rows', rows[0], '..', rows[-1])
midy = (rows[0] + rows[-1]) // 2
cols = [x for x in range(40, 700) if isb(px[x, midy])]
print('panel cols @y%d' % midy, cols[0], '..', cols[-1])
print('corner samples', px[66, 137], px[570, 137], px[66, 380], px[570, 380])
print('panel modal', modal(70, 150, 100, 170))

print("== dots (magenta CC00CC) x60..95, y150..400 ==")
def isdot(p): r,g,b = p; return r > 170 and g < 90 and b > 170
dotrows = runs = None
ys = [y for y in range(150, 400) if any(isdot(px[x, y]) for x in range(60, 100))]
# group
groups = []
for y in ys:
    if groups and y - groups[-1][-1] <= 2: groups[-1].append(y)
    else: groups.append([y])
print('dot y-groups', [(g[0], g[-1]) for g in groups])
for g in groups:
    ym = (g[0] + g[-1]) // 2
    xs = [x for x in range(55, 110) if isdot(px[x, ym])]
    print('  dot@y%d x %d..%d' % (ym, xs[0], xs[-1]), px[(xs[0]+xs[-1])//2, ym])

print("== neuron columns: scan for non-beige blobs on each row band ==")
# first find row centers via white circles col0
def iswhite(p): r,g,b = p; return r > 235 and g > 235 and b > 225
for band0, band1 in [(160, 210), (230, 285), (310, 365)]:
    ycents = []
    for y in range(band0, band1):
        n = sum(1 for x in range(140, 180) if iswhite(px[x, y]))
        if n > 25: ycents.append(y)
    print('col0 white rows band', band0, ycents[:3], '...', ycents[-3:] if ycents else None, 'count', len(ycents))
