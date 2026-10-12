#!/usr/bin/env python3
"""Blue ink histogram: all near-pure blue px in the six agenda bands, bucket by (R,G,B)."""
from PIL import Image
import numpy as np
from collections import Counter

p = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_006.jpg"
a = np.asarray(Image.open(p).convert("RGB")).astype(int)
R, G, B = a[:,:,0], a[:,:,1], a[:,:,2]

pure = (B - R > 70) & (B - G > 70) & (B > 100)
ys, xs = np.where(pure)
# restrict to agenda bands
mask = ((ys>=147)&(ys<=161))|((ys>=187)&(ys<=201))|((ys>=229)&(ys<=247))|((ys>=269)&(ys<=283))|((ys>=309)&(ys<=323))|((ys>=353)&(ys<=367))
ys, xs = ys[mask], xs[mask]
print("near-pure blue px:", len(ys))
# bucket R//8, G//8, B//16
cnt = Counter()
for r,g,b in zip(R[ys,xs], G[ys,xs], B[ys,xs]):
    cnt[(int(r)//8*8, int(g)//8*8, int(b)//16*16)] += 1
for k, v in sorted(cnt.items(), key=lambda kv: (kv[0][2], kv[0][0])):
    if v >= 10: print(f"  R~{k[0]:3d} G~{k[1]:3d} B~{k[2]:3d}  n={v}")
# darkest quartile mean
order = np.argsort(B[ys, xs])
n = len(order)
dark = order[:max(1, n//8)]
print("darkest-1/8 mean RGB:", R[ys[dark], xs[dark]].mean(), G[ys[dark], xs[dark]].mean(), B[ys[dark], xs[dark]].mean())
q = order[:max(1, n//4)]
print("darkest-1/4 mean RGB:", R[ys[q], xs[q]].mean(), G[ys[q], xs[q]].mean(), B[ys[q], xs[q]].mean())
print("overall mean RGB:", R[ys,xs].mean(), G[ys,xs].mean(), B[ys,xs].mean())
# title red census same way
redm = (R - G > 60) & (R - B > 60) & (R > 120)
rys, rxs = np.where(redm)
rmask = (rys>=68)&(rys<=96)&(rxs>=233)&(rxs<=625)
print("\ntitle red px:", rmask.sum(), "mean RGB:", R[rys[rmask],rxs[rmask]].mean(), G[rys[rmask],rxs[rmask]].mean(), B[rys[rmask],rxs[rmask]].mean())
top = Counter()
for r,g,b in zip(R[rys[rmask],rxs[rmask]], G[rys[rmask],rxs[rmask]], B[rys[rmask],rxs[rmask]]):
    top[(int(r)//8*8, int(g)//8*8, int(b)//8*8)] += 1
print("title red buckets:", top.most_common(8))
