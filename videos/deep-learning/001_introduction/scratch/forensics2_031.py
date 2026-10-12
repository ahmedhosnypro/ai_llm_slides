from PIL import Image
import numpy as np

im = Image.open("videos/deep-learning/001_introduction/unique_slides/slide_031.jpg").convert("RGB")
a = np.asarray(im).astype(int)
H, W, _ = a.shape
R, G, B = a[:,:,0], a[:,:,1], a[:,:,2]

blueish = (B-R>40) & (B-G>40) & (B>90)
reddish = (R-B>50) & (R-G>50) & (R>90)
dark    = (R<100) & (G<100) & (B<100)

print("=== content box border detection: horizontal runs ===")
# find rows where a contiguous blue run > 400 px exists
def longest_run(row):
    best=0; cur=0; s=0; bs=0
    for i,v in enumerate(row):
        if v:
            if cur==0: s=i
            cur+=1
            if cur>best: best=cur; bs=s
        else: cur=0
    return best, bs

for name, mask, yr in [("blue", blueish, range(110, 400)), ("red", reddish, range(360, 530))]:
    print(f"--- {name} rows with run>350 ---")
    for y in yr:
        run, s = longest_run(mask[y])
        if run > 350:
            print(f"  y={y} run={run} xstart={s} xend={s+run-1}")

print("\n=== vertical blue runs (content box side borders), x scan ===")
for x in range(80, 920):
    col = blueish[130:380, x]
    run, s = longest_run(col)
    if run > 100:
        print(f"  x={x} run={run} ystart={130+s} yend={130+s+run-1}")

print("\n=== red box (matrix) vertical runs, x scan 560..900, y 360..530 ===")
for x in range(560, 900):
    col = reddish[360:530, x]
    run, s = longest_run(col)
    if run > 80:
        print(f"  x={x} run={run} ystart={360+s} yend={360+s+run-1}")

print("\n=== blue label box (x 350..630, y 420..500): vertical runs ===")
for x in range(350, 630):
    col = blueish[420:500, x]
    run, s = longest_run(col)
    if run > 30:
        print(f"  x={x} run={run} ystart={420+s} yend={420+s+run-1}")

print("\n=== blue text lines inside content box (x 120..800, y 155..270) ===")
inner = blueish[155:270, 120:800]
rowc = inner.sum(axis=1)
on = rowc > 3
bands=[]; s=None
for i,v in enumerate(on):
    if v and s is None: s=i
    if not v and s is not None:
        if i-s>2: bands.append((s+155, i-1+155))
        s=None
if s is not None: bands.append((s+155, 269))
for b in bands:
    m = blueish[b[0]:b[1]+1, :]
    cols = np.where(m.any(axis=0))[0]
    print(f"  blue band y {b[0]}..{b[1]} (h={b[1]-b[0]+1})  x {cols[0]}..{cols[-1]}")

print("\n=== red bullet lines (y 290..370) ===")
inner = reddish[290:370, 100:700]
rowc = inner.sum(axis=1)
on = rowc > 2
bands=[]; s=None
for i,v in enumerate(on):
    if v and s is None: s=i
    if not v and s is not None:
        if i-s>2: bands.append((s+290, i-1+290))
        s=None
if s is not None: bands.append((s+290, 369))
for b in bands:
    m = reddish[b[0]:b[1]+1, :]
    cols = np.where(m.any(axis=0))[0]
    print(f"  red band y {b[0]}..{b[1]} (h={b[1]-b[0]+1})  x {cols[0]}..{cols[-1]}")

print("\n=== matrix dark ink (x 610..870, y 370..520) ===")
inner = dark[370:520, 610:870]
rows = np.where(inner.any(axis=1))[0]; cols = np.where(inner.any(axis=0))[0]
if len(rows): print(f"  dark ink bbox x {610+cols[0]}..{610+cols[-1]}  y {370+rows[0]}..{370+rows[-1]}  (w={cols[-1]-cols[0]+1}, h={rows[-1]-rows[0]+1})")
else: print("  EMPTY")

print("\n=== label text 'Filter Parameters' bbox ===")
inner = blueish[440:470, 350:630]
rows = np.where(inner.any(axis=1))[0]; cols = np.where(inner.any(axis=0))[0]
print(f"  text ink x {350+cols[0]}..{350+cols[-1]}  y {440+rows[0]}..{440+rows[-1]}")

print("\n=== gray field vs white: column profile at y=300 ===")
row = a[300]
# find transitions white->gray
prev=None
for x in range(0, W):
    c = tuple(row[x])
    cat = 'white' if all(v>245 for v in c) else ('gray' if abs(c[0]-236)<16 and abs(c[1]-236)<16 else 'other')
    if cat != prev:
        print(f"  x={x}: {prev} -> {cat} {c}")
        prev = cat
