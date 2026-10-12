from PIL import Image
import numpy as np

im = Image.open("videos/deep-learning/001_introduction/unique_slides/slide_031.jpg").convert("RGB")
a = np.asarray(im).astype(int)
H, W, _ = a.shape
R, G, B = a[:,:,0], a[:,:,1], a[:,:,2]
dark = (R<100) & (G<100) & (B<100)

print("=== pixel probes ===")
for (x,y,label) in [(99,300,"content-box left border"),(886,300,"right border"),
                    (480,125,"top border? y125"),(480,370,"bottom border? y370"),
                    (700,387,"matrix top border"),(700,503,"matrix bottom border"),
                    (624,450,"matrix left border"),(842,450,"matrix right border"),
                    (374,455,"label box left edge"),(604,455,"label box right edge"),
                    (490,432,"label box top edge"),(490,474,"label box bottom edge"),
                    (140,312,"bullet dot region"),(58,310,"red frame line"),
                    (200,180,"blue text px"),(300,90,"title red px"),(700,450,"matrix glyph px")]:
    print(f"  {label} ({x},{y}): {tuple(a[y,x])}")

print("\n=== vertical color strip x=480, y=115..150 and y=345..385 (find content box top/bottom borders) ===")
for y in list(range(115,150))+list(range(345,385)):
    c = a[y,480]
    if not (abs(c[0]-236)<10 and abs(c[1]-236)<10) and not all(v>246 for v in c):
        print(f"  y={y}: {tuple(c)}")

print("\n=== horizontal strip y=455, x=360..630 (label box side borders) ===")
for x in range(360,630):
    c = a[455,x]
    if not (abs(c[0]-236)<12 and abs(c[1]-236)<12) and not all(v>246 for v in c):
        print(f"  x={x}: {tuple(c)}", end="  ")
print()

print("\n=== label box top/bottom: strip x=490, y=420..490 ===")
for y in range(420,490):
    c = a[y,490]
    if not (abs(c[0]-236)<12 and abs(c[1]-236)<12) and not all(v>246 for v in c):
        print(f"  y={y}: {tuple(c)}", end="  ")
print()

print("\n=== blue text lines, full scan y 120..280 ===")
blueish = (B-R>35) & (B>140)
inner = blueish[120:280, :]
rowc = inner.sum(axis=1)
on = rowc > 3
bands=[]; s=None
for i,v in enumerate(on):
    if v and s is None: s=i
    if not v and s is not None:
        if i-s>2: bands.append((s+120, i-1+120))
        s=None
if s is not None: bands.append((s+120, 279))
for b in bands:
    m = blueish[b[0]:b[1]+1, 105:880]
    cols = np.where(m.any(axis=0))[0]
    print(f"  blue band y {b[0]}..{b[1]} (h={b[1]-b[0]+1})  x {105+cols[0]}..{105+cols[-1]}")

print("\n=== red bullets x-profile (y 302..323) to find bullet dot vs text ===")
reddish = (R-B>50) & (R-G>50) & (R>90)
band = reddish[302:324, :]
colc = band.sum(axis=0)
runs=[]; s=None
for x,v in enumerate(colc>0):
    if v and s is None: s=x
    if not v and s is not None:
        runs.append((s,x-1)); s=None
print("  ink column runs:", runs[:12])

print("\n=== matrix dark ink inside box x 628..838, y 390..502 ===")
inner = dark[390:502, 628:838]
rows = np.where(inner.any(axis=1))[0]; cols = np.where(inner.any(axis=0))[0]
print(f"  ink bbox x {628+cols[0]}..{628+cols[-1]}  y {390+rows[0]}..{390+rows[-1]}  (w={cols[-1]-cols[0]+1}, h={rows[-1]-rows[0]+1})")
# row profile to see the 3 matrix rows
rowc = inner.sum(axis=1)
on = rowc>1
bands=[]; s=None
for i,v in enumerate(on):
    if v and s is None: s=i
    if not v and s is not None:
        bands.append((s+390,i-1+390)); s=None
if s is not None: bands.append((s+390,501))
print("  matrix ink row bands:", bands)

print("\n=== matrix bracket columns: ink columns profile ===")
colc = inner.sum(axis=0)
runs=[]; s=None
for x,v in enumerate(colc>0):
    if v and s is None: s=x
    if not v and s is not None:
        runs.append((628+s,628+x-1)); s=None
if s is not None: runs.append((628+s,628+837))
print("  ink col runs (first/last 8):", runs[:8], "...", runs[-8:])

print("\n=== title: exact red ink bbox with looser mask ===")
tl = (R-G>60) & (R-B>60) & (R>120)
inner = tl[60:140, 100:900]
rows = np.where(inner.any(axis=1))[0]; cols = np.where(inner.any(axis=0))[0]
print(f"  title ink x {100+cols[0]}..{100+cols[-1]}  y {60+rows[0]}..{60+rows[-1]}  (w={cols[-1]-cols[0]+1}, h={rows[-1]-rows[0]+1})")

print("\n=== content box borders: light-periwinkle mask ===")
lp = (B-R>10) & (B-G>10) & (B>170) & (R<235)
print("  rows y115..390 with long horizontal lp runs:")
for y in range(115,395):
    row = lp[y, 90:900]
    if row.sum() > 400: print(f"    y={y} count={row.sum()}")
print("  cols x90..900 with long vertical lp runs (y115..390):")
for x in range(90,900):
    col = lp[115:395, x]
    if col.sum() > 150: print(f"    x={x} count={col.sum()}")
