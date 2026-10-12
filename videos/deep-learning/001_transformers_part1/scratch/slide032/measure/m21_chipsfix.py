from PIL import Image
import numpy as np
fr = np.array(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_032.jpg').convert('RGB')).astype(int)

def hexc(p): return '#%02X%02X%02X' % tuple(p)

# ---- 1) OUTPUT COLUMN: vertical profile at x=431 (center) y 60..290
print("== output column vprofile x=431, y60..292 (non-pink runs) ==")
col = fr[60:292, 431]
runs = []
cur = None
for i, p in enumerate(col):
    y = 60 + i
    is_pink = abs(p[0]-247) < 12 and abs(p[1]-199) < 15 and abs(p[2]-201) < 15
    is_white = p[0] > 245 and p[1] > 245 and p[2] > 245
    tag = 'PINK' if is_pink else ('WHITE' if is_white else 'OTHER')
    if cur and cur[0] == tag: cur[2] = y
    else:
        if cur: runs.append(cur)
        cur = [tag, y, y, hexc(p)]
if cur: runs.append(cur)
for r in runs:
    if r[2]-r[1] >= 1 or r[0] == 'OTHER': print('  %s y%d..%d %s' % (r[0], r[1], r[2], r[3]))

# ---- 2) capsule border: horizontal profile at y=120, x400..465
print("== capsule hprofile y=120, x400..465 ==")
for x in range(400, 466):
    p = fr[120, x]
    if not (p[0] > 240 and p[1] > 235 and p[2] > 235):
        print('  x=%d %s' % (x, hexc(p)))
# right side
print("== capsule hprofile y=120, x455..470 right ==")
for x in range(448, 472):
    p = fr[120, x]
    if not (p[0] > 240 and p[1] > 235 and p[2] > 235):
        print('  x=%d %s' % (x, hexc(p)))

# capsule top/bottom: col x=431
print("== capsule top/bottom col x=431 y75..95 / y245..265 ==")
for y in list(range(75, 96)) + list(range(245, 266)):
    p = fr[y, 431]
    if not (p[0] > 240 and p[1] > 235 and p[2] > 235):
        print('  y=%d %s' % (y, hexc(p)))

# ---- 3) yellow chips inside capsule: scan region x412..452, y88..258 for yellow (R>230,G>230,B<215)
ys, xs = np.where((fr[80:265, 405:460, 0] > 225) & (fr[80:265, 405:460, 1] > 225) & (fr[80:265, 405:460, 2] < 215))
if len(ys):
    print("== yellow chip pixels in capsule region ==")
    # cluster by y bands
    yy = ys + 80; xx = xs + 405
    bands = []
    order = np.argsort(yy)
    yy = yy[order]; xx = xx[order]
    start = 0
    for i in range(1, len(yy)+1):
        if i == len(yy) or yy[i] - yy[i-1] > 4:
            b_y = yy[start:i]; b_x = xx[start:i]
            bands.append((b_y.min(), b_y.max(), b_x.min(), b_x.max(), len(b_y)))
            start = i
    for b in bands:
        print('  chip y%d..%d x%d..%d n=%d' % b)
    # core color of biggest chip
    for b in bands[:4]:
        cy, cx = (b[0]+b[1])//2, (b[2]+b[3])//2
        print('  chip mid sample y%d x%d %s' % (cy, cx, hexc(fr[cy, cx])))

# ---- 4) X_Q ink: darkest pixels in capsule text zone
zone = fr[85:260, 412:452]
dark = np.where(zone.sum(axis=2) < 260)
if len(dark[0]):
    vals = zone[dark]
    print("== X_Q darkest ink mean %s n=%d ==" % (hexc(vals.mean(axis=0).astype(int)), len(vals)))

# ---- 5) PILL CIRCLE interiors: sample interior away from text (corners of inner ring)
print("== pill circle interiors (ring r=11, sample r=6..8 corners, avoiding center text) ==")
for cx in [97, 122, 148, 173]:
    samples = []
    for dx, dy in [(-6,-6), (6,-6), (-6,6), (6,6), (0,-7), (0,7), (-7,0), (7,0)]:
        samples.append(fr[126 + dy, cx + dx])
    m = np.array(samples).mean(axis=0).astype(int)
    print('  c@%d interior mean %s  samples %s' % (cx, hexc(m), ' '.join(hexc(s) for s in samples)))

# yellow pixels inside pill circles?
ys2, xs2 = np.where((fr[112:142, 84:186, 0] > 225) & (fr[112:142, 84:186, 1] > 225) & (fr[112:142, 84:186, 2] < 215))
print("  yellow-ish px in pill circles zone: n=%d" % len(ys2))
# lavender-ish pixels?
ys3, xs3 = np.where((fr[112:142, 84:186, 2] > 220) & (fr[112:142, 84:186, 0] > 190) & (fr[112:142, 84:186, 0] < 235) & (fr[112:142, 84:186, 1] > 170) & (fr[112:142, 84:186, 1] < 215))
print("  lavender-ish px in pill circles zone: n=%d" % len(ys3))
if len(ys3):
    vals = fr[112+ys3, 84+xs3]
    print('  lavender mean %s' % hexc(vals.mean(axis=0).astype(int)))

# ---- 6) X_Q text vs chip: vertical structure at x=424 (text col) y 95..130 zoom
print("== capsule text zone col x=424 y92..132 ==")
for y in range(92, 133):
    p = fr[y, 424]
    print('  y=%d %s' % (y, hexc(p)))
