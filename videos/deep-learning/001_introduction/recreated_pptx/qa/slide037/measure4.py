#!/usr/bin/env python3
"""Measure slide_037.jpg pass 4 — diagram blocks: slab, filters, cube, labels, question, equation."""
from PIL import Image
import numpy as np
from collections import Counter

SRC = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_037.jpg'
im = Image.open(SRC).convert('RGB')
a = np.asarray(im).astype(int)

def runs(mask, min_gap=2):
    idx = np.where(mask)[0]
    if len(idx) == 0:
        return []
    out = []
    s = p = idx[0]
    for v in idx[1:]:
        if v - p > min_gap:
            out.append((s, p))
            s = v
        p = v
    out.append((s, p))
    return out

def bbox(mask, label):
    ys, xs = np.where(mask)
    if len(ys) == 0:
        print(f"{label}: EMPTY")
        return None
    print(f"{label}: x{xs.min()}..{xs.max()} y{ys.min()}..{ys.max()}  n={len(ys)}")
    return xs.min(), xs.max(), ys.min(), ys.max()

P = (265, 510, 60, 900)  # panel inner band y0,y1,x0,x1
def sub(y0=265, y1=510, x0=60, x1=900):
    return a[y0:y1, x0:x1], y0, x0

# ---- orange slab (input): brownish-orange
s, oy, ox = sub()
orange = (s[:, :, 0] > 140) & (s[:, :, 0] < 230) & (s[:, :, 1] > 60) & (s[:, :, 1] < 160) & (s[:, :, 2] < 80)
ys, xs = np.where(orange)
print("orange slab pixels bbox:", f"x{ox+xs.min()}..{ox+xs.max()} y{oy+ys.min()}..{oy+ys.max()} n={len(ys)}")
# column profile of orange to find slab extent
cp = orange.sum(axis=0)
print("orange col runs:", [(ox+s0, ox+e0) for s0, e0 in runs(cp > 2, min_gap=8)])
rp = orange.sum(axis=1)
print("orange row runs:", [(oy+s0, oy+e0) for s0, e0 in runs(rp > 2, min_gap=8)])
print("modal orange:", Counter(map(tuple, s[orange])).most_common(4))

# ---- black dashed lines: dark pixels right of slab, left of filter stack
dash = (s.sum(axis=-1) < 260)
# dashes zone: x 250..330 approx — measure in frame coords
dz = dash[:, 250-60:345-60]
rp2 = dz.sum(axis=1)
print("\ndash rows (y, count) in x250..345:")
print([(oy+i, int(c)) for i, c in enumerate(rp2) if c > 8])

# ---- filter stack: saturated colors region x300..470
st = s[:, 300-60:470-60]
sat = (st.max(axis=-1) - st.min(axis=-1) > 60) & (st.sum(axis=-1) > 200) & (st.sum(axis=-1) < 700)
rp3 = sat.sum(axis=1)
print("\nfilter stack rows:", [(oy+s0, oy+e0) for s0, e0 in runs(rp3 > 3, min_gap=4)])
cp3 = sat.sum(axis=0)
print("filter stack cols:", [(300+s0, 300+e0) for s0, e0 in runs(cp3 > 2, min_gap=4)])

# front-row filter colors: sample the 5 front slabs
print("\nfilter color samples (front row y~400):")
for x in [320, 345, 370, 395, 420]:
    print(f"  x={x} y=395..405:", [tuple(a[y, x]) for y in range(395, 406, 2)])

# ---- '=' sign: blue/cyan between stack and cube
eq = (s[:, :, 2] > 150) & (s[:, :, 0] < 120) & (s[:, :, 1] > 100)
eqz = eq[:, 470-60:520-60]
rp4 = eqz.sum(axis=1)
print("\n'=' rows:", [(oy+s0, oy+e0) for s0, e0 in runs(rp4 > 1, min_gap=2)])
print("modal '=' color:", Counter(map(tuple, s[470-60:520-60][eqz])).most_common(2))

# ---- cube: tan region x500..800
tan = (s[:, :, 0] > 200) & (s[:, :, 1] > 150) & (s[:, :, 1] < 215) & (s[:, :, 2] > 100) & (s[:, :, 2] < 180)
rp5 = tan.sum(axis=1)
cp5 = tan.sum(axis=0)
print("\ncube rows:", [(oy+s0, oy+e0) for s0, e0 in runs(rp5 > 10, min_gap=6)])
print("cube cols:", [(ox+s0, ox+e0) for s0, e0 in runs(cp5 > 10, min_gap=6)])
print("modal tan:", Counter(map(tuple, s[tan])).most_common(3))

# ---- question text: black ink y445..485 x60..600
q = (s.sum(axis=-1) < 300)
qz = q[440-265:490-265, 60-60:620-60]
rp6 = qz.sum(axis=1)
print("\nquestion rows:", [(440+s0, 440+e0) for s0, e0 in runs(rp6 > 2, min_gap=4)])
for s0, e0 in runs(rp6 > 2, min_gap=4):
    xs6 = np.where(qz[s0:e0+1].sum(axis=0) > 0)[0]
    print(f"  q line y{440+s0}..{440+e0} x{60+xs6[0]}..{60+xs6[-1]}")

# ---- equation: red ink y480..515
r = (s[:, :, 0] > 140) & (s[:, :, 0] - s[:, :, 1] > 60) & (s[:, :, 0] - s[:, :, 2] > 60)
rz = r[475-265:515-265, 150-60:450-60]
rp7 = rz.sum(axis=1)
print("\nequation rows:", [(475+s0, 475+e0) for s0, e0 in runs(rp7 > 1, min_gap=3)])
for s0, e0 in runs(rp7 > 1, min_gap=3):
    xs7 = np.where(rz[s0:e0+1].sum(axis=0) > 0)[0]
    print(f"  eq line y{475+s0}..{475+e0} x{150+xs7[0]}..{150+xs7[-1]}")
print("modal eq red:", Counter(map(tuple, s[475-265:515-265, 150-60:450-60][rz])).most_common(3))

# ---- 'Depth=5 dims' label: black ink top right of cube
dz2 = q[285-265:315-265, 720-60:900-60]
rp8 = dz2.sum(axis=1)
print("\nDepth label rows:", [(285+s0, 285+e0) for s0, e0 in runs(rp8 > 1, min_gap=3)])
for s0, e0 in runs(rp8 > 1, min_gap=3):
    xs8 = np.where(dz2[s0:e0+1].sum(axis=0) > 0)[0]
    print(f"  y{285+s0}..{285+e0} x{720+xs8[0]}..{720+xs8[-1]}")

# ---- 'RGB' label above slab
rgb = q[263-265:295-265, 200-60:320-60]
rp9 = rgb.sum(axis=1)
print("\nRGB label rows:", [(263+s0, 263+e0) for s0, e0 in runs(rp9 > 1, min_gap=3)])
for s0, e0 in runs(rp9 > 1, min_gap=3):
    xs9 = np.where(rgb[s0:e0+1].sum(axis=0) > 0)[0]
    print(f"  y{263+s0}..{263+e0} x{200+xs9[0]}..{200+xs9[-1]}")

# ---- '3 dims' label left
d3 = q[310-265:340-265, 50-60:130-60]
rp10 = d3.sum(axis=1)
print("\n'3 dims' rows:", [(310+s0, 310+e0) for s0, e0 in runs(rp10 > 0, min_gap=3)])
for s0, e0 in runs(rp10 > 0, min_gap=3):
    xs10 = np.where(d3[s0:e0+1].sum(axis=0) > 0)[0]
    print(f"  y{310+s0}..{310+e0} x{50+xs10[0]}..{50+xs10[-1]}")

# ---- '5' label above stack + '3' label below stack (small black marks)
f5 = q[315-265:340-265, 315-60:345-60]
print("\n'5' above stack ink px:", int(f5.sum()))
f3 = q[390-265:415-265, 310-60:335-60]
print("'3' below stack ink px:", int(f3.sum()))
for nm, (yy0, yy1, xx0, xx1) in {
    "'5' zone": (315, 340, 315, 345),
    "'3' zone": (390, 415, 310, 335),
    "7-top zone": (330, 355, 280, 305),
    "7-left zone": (370, 400, 170, 200),
}.items():
    zz = q[yy0-265:yy1-265, xx0-60:xx1-60]
    ys2, xs2 = np.where(zz)
    if len(ys2):
        print(f"{nm}: x{xx0+xs2.min()}..{xx0+xs2.max()} y{yy0+ys2.min()}..{yy0+ys2.max()} n={len(ys2)}")
    else:
        print(f"{nm}: empty")
