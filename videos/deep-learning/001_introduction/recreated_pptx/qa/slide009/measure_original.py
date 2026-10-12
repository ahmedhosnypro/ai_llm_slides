# measure_original.py — slide 009 forensics, stage 1: panel, title, colored regions.
from PIL import Image
import numpy as np
from collections import Counter

im = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_009.jpg").convert("RGB")
a = np.asarray(im).astype(int)
H, W, _ = a.shape
print("size", W, H)

def near(px, target, tol):
    return (abs(px[...,0]-target[0])<=tol) & (abs(px[...,1]-target[1])<=tol) & (abs(px[...,2]-target[2])<=tol)

def bbox(mask):
    ys, xs = np.nonzero(mask)
    if len(xs)==0: return None
    return (int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max()), int(mask.sum()))

# global census of quantized colors
q = (a//16*16)
cnt = Counter(map(tuple, q.reshape(-1,3)))
print("\n-- top 24 quantized colors (r,g,b //16) --")
for c, n in cnt.most_common(24):
    print(c, n)

# Title red ink: strong red pixels in top band
r, g, b = a[...,0], a[...,1], a[...,2]
redmask = (r>120)&(g<90)&(b<90)
print("\ntitle band red bbox y<80:", bbox(redmask & (np.arange(H)[:,None]<80)))
# column profile of title band red
tm = redmask & (np.arange(H)[:,None]<80)
cols = tm.any(axis=0)
xs = np.nonzero(cols)[0]
print("title x-range:", xs.min(), xs.max(), "n cols", len(xs))
rows = np.nonzero(tm.any(axis=1))[0]
print("title y-range:", rows.min(), rows.max())
# title core color
tp = a[tm]
print("title red modal:", Counter(map(tuple, (tp//8*8))).most_common(5))

# White panel: near-white mask
white = (r>240)&(g>240)&(b>240)
# find rows where a long white run exists
roww = white.sum(axis=1)
print("\nwhite row counts sample (rows 40..120 step 5):", [(y, int(roww[y])) for y in range(40,121,5)])
print("white rows 450..540:", [(y, int(roww[y])) for y in range(450,540,5)])

# red border of panel: strong red rows/cols in mid slide
redb = (r>140)&(g<60)&(b<60)
# vertical red lines: columns with many red pixels between y 60 and 460
redband = redb[60:460,:]
colc = redband.sum(axis=0)
strong = np.nonzero(colc>200)[0]
print("\nvertical red lines cols>200:", strong)
rowc = redband.sum(axis=1)
strongy = np.nonzero(rowc>300)[0]+60
print("horizontal red lines rows>300:", strongy)

# colored region masks (spec colors)
targets = {
 "peach F5CBA7": (245,203,167),
 "paleyellow FFFFCC": (255,255,204),
 "palecyan CCFFFF": (204,255,255),
 "palegreen E5FFE5": (229,255,229),
 "darkred B02020": (176,32,32),
 "lavender E0CCF0": (224,204,240),
 "yellow FFFF00": (255,255,0),
 "gray D9D9D9": (217,217,217),
}
for name, t in targets.items():
    m = near(a, t, 20)
    print(f"\n{name}: bbox", bbox(m), "count", int(m.sum()))

