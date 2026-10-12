from PIL import Image
import numpy as np
from collections import Counter
im = Image.open('videos/deep-learning/001_introduction/unique_slides/slide_022.jpg').convert('RGB')
a = np.asarray(im).astype(int)
H, W = a.shape[:2]
r, g, b = a[:,:,0], a[:,:,1], a[:,:,2]
white = (r>235)&(g>235)&(b>235)

def colspan(x0,x1,y0,y1,minfrac=0.5):
    "contiguous column span where white count within [y0,y1] >= minfrac of span height"
    sub = white[y0:y1, x0:x1]
    cnt = sub.sum(axis=0)
    th = (y1-y0)*minfrac
    ok = cnt >= th
    xs = np.nonzero(ok)[0]
    if len(xs)==0: return None
    return (x0+int(xs.min()), x0+int(xs.max()))

def rowspan(y0,y1,x0,x1,minfrac=0.5):
    sub = white[y0:y1, x0:x1]
    cnt = sub.sum(axis=1)
    th = (x1-x0)*minfrac
    ok = cnt >= th
    ys = np.nonzero(ok)[0]
    if len(ys)==0: return None
    return (y0+int(ys.min()), y0+int(ys.max()))

print("leftbox cols:", colspan(60,460,95,240))
print("leftbox rows:", rowspan(80,250,100,420))
print("rightbox cols:", colspan(440,830,95,240))
print("rightbox rows:", rowspan(80,250,480,780))
print("decisionbox cols:", colspan(60,900,260,338))
print("decisionbox rows:", rowspan(248,350,90,760))
print("diagrambox cols:", colspan(200,700,360,500))
print("diagrambox rows:", rowspan(345,510,240,620))

# pale yellow pixels clusters
py = (r>215)&(g>215)&(b<200)&(abs(r-g)<25)
ys,xs = np.nonzero(py)
from collections import defaultdict
clusters = defaultdict(int)
for x,y in zip(xs,ys):
    clusters[(x//50*50, y//50*50)] += 1
print("\npale-yellow clusters (50px cells, n>=20):")
for k in sorted(clusters, key=lambda k:-clusters[k]):
    if clusters[k]>=20: print(k, clusters[k])

# modal colors in specific spots
def modal(x0,y0,x1,y1,exclude_white=True):
    sub = a[y0:y1, x0:x1].reshape(-1,3)
    cnt = Counter(tuple(c) for c in sub)
    return cnt.most_common(8)

print("\nmodal left box border top (x150..250,y87..92):", modal(150,87,250,93))
print("modal decision box border top (x150..250,y250..256):", modal(150,250,250,257))
print("modal decision box fill (x300..400,y265..285):", modal(300,265,400,285))
print("modal callout fill (x660..780,y400..410):", modal(660,400,780,410))
print("modal callout border? (x610..820,y396..402):", modal(610,396,820,403))
print("modal gray bg (x100..300,y470..510):", modal(100,470,300,510))
print("modal title ink (x240..700,y62..82):", modal(240,62,700,82))
