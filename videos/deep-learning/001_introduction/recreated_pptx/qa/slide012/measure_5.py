from PIL import Image
import numpy as np
from collections import Counter
im = Image.open('videos/deep-learning/001_introduction/unique_slides/slide_012.jpg').convert('RGB')
a = np.asarray(im).astype(int)

# Header band rows 160..190: classify red vs black ink columns
print("== header: per-row black-only ink x-extent (x>360) ==")
for y in range(163, 190):
    blk = [x for x in range(356, 879) if a[y,x].sum() < 420]
    red = [x for x in range(100, 356) if a[y,x,0]-a[y,x,1]>70 and a[y,x,0]>130]
    print(" row", y, "red n=", len(red), ("x "+str(red[0])+".."+str(red[-1])) if red else "", "| blk n=", len(blk), (("x "+str(blk[0])+".."+str(blk[-1])) if blk else ""))

# underline check: rows 182..188, continuous dark run
print("\n== rows 182..190 any dark runs x 356..600 ==")
for y in range(182, 191):
    dk = [x for x in range(300, 700) if a[y,x].sum() < 560]
    if dk:
        runs=[]; s=dk[0]; p=dk[0]
        for x in dk[1:]:
            if x-p>3: runs.append((s,p)); s=x
            p=x
        runs.append((s,p))
        print(" row", y, "dark runs:", runs)

# bullet dots: find dark round blobs at x 100..125
print("\n== bullet dot blobs: dark px x 100..126 per band ==")
for (y0,y1) in [(230,255),(274,300),(318,342),(362,388)]:
    pts = [(y,x) for y in range(y0,y1) for x in range(100,127) if a[y,x].sum()<420]
    if pts:
        ys=[p[0] for p in pts]; xs=[p[1] for p in pts]
        print(" band", y0, ": dot y", min(ys),"..",max(ys), "x", min(xs),"..",max(xs), "n", len(pts))

# text starts: first ink col >= 128 in each bullet band
print("\n== bullet text ink (x>=127) extents and per-row detail ==")
for i,(y0,y1) in enumerate([(230,255),(274,300),(318,342),(362,388)]):
    cols = {}
    for y in range(y0,y1):
        ink = [x for x in range(127,879) if a[y,x].sum()<420]
        if ink: cols[y]=(ink[0],ink[-1],len(ink))
    xs0 = min(v[0] for v in cols.values()); xs1 = max(v[1] for v in cols.values())
    ys = sorted(cols)
    print(f" bullet{i+1}: y {ys[0]}..{ys[-1]} x {xs0}..{xs1}")
    for y in ys[:3]+ys[-3:]: print("   row",y,cols[y])

# title text ink in title box (rows 84..136, x 96..362)
print("\n== title text ink ==")
cols={}
for y in range(85, 136):
    ink=[x for x in range(98,361) if a[y,x].sum()<420]
    if ink: cols[y]=(ink[0],ink[-1],len(ink))
ys=sorted(cols)
print(" title ink y", ys[0],"..",ys[-1], "x", min(v[0] for v in cols.values()),"..",max(v[1] for v in cols.values()))
for y in ys[:4]+ys[-4:]: print("   row",y,cols[y])
