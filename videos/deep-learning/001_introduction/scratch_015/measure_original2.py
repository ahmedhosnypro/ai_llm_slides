from PIL import Image
import numpy as np
p = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_015.jpg"
im = Image.open(p).convert("RGB")
a = np.asarray(im).astype(int)
H,W = a.shape[:2]

# red-ish (border + text): R much greater than G,B
redish = (a[:,:,0]-a[:,:,1]>60)&(a[:,:,0]-a[:,:,2]>50)
rsum = redish.sum(axis=1); csum = redish.sum(axis=0)
rows = np.where(rsum>100)[0]; cols = np.where(csum>100)[0]
print("redish rows(>100):", rows.min(), rows.max(), "| rowprofile>100:", rows.tolist()[:10], "...")
print("redish cols(>100):", [(int(c), int(csum[c])) for c in cols])
print("rows with redish>400:", [int(r) for r in np.where(rsum>400)[0]])
# top border row?
top_candidates = np.where(rsum>300)[0]
print("rows redish>300:", top_candidates.tolist())

# interior (exclude border margins col<70 or col>890, rows<70)
inner = np.zeros_like(redish)
inner[75:500, 75:885] = redish[75:500, 75:885]
irsum = inner.sum(axis=1)
bands = []
rr = np.where(irsum>2)[0]
if len(rr):
    start=rr[0]; prev=rr[0]
    for r in rr[1:]:
        if r-prev>4: bands.append((int(start),int(prev))); start=r
        prev=r
    bands.append((int(start),int(prev)))
print("TEXT bands (interior redish):", bands)
for (b0,b1) in bands:
    seg = inner[b0:b1+1,:]
    cs = np.where(seg.sum(axis=0)>0)[0]
    print(f"  band {b0}-{b1} h={b1-b0+1}: col {cs.min()}..{cs.max()}, ink px={int(seg.sum())}")

# text color: strongly red pixels in the title band only (line1)
l1 = a[190:242, 75:885]
l1red = (l1[:,:,0]-l1[:,:,1]>60)&(l1[:,:,0]-l1[:,:,2]>50)
px = l1[l1red]
print("line1 red text px count", len(px), "mean", px.mean(axis=0).round(1), "p25", np.percentile(px,25,axis=0).round(1))

# panel fill: rows 100..180 (between panel top and line1), away from border
fill = a[100:180, 150:800]
print("panel fill mean:", fill.mean(axis=(0,1)).round(1))
# canvas outside panel: left of col 42?
print("canvas @(row300,col10:35):", a[300,10:35].mean(axis=0).round(1), "@(row20, col400:600):", a[20,400:600].mean(axis=0).round(1))
# where does the gray panel start? scan col profile of "not white" at row 300
row300 = a[300]
nonwhite = np.where(row300.sum(axis=1) < 720)[0]
print("row300 nonwhite cols first/last:", nonwhite.min(), nonwhite.max())
# vertical: scan rows at col 480
col480 = a[:,480]
nw = np.where(col480.sum(axis=1) < 720)[0]
print("col480 nonwhite rows first/last:", nw.min(), nw.max())
# black strip
strip = a[515:540, 200:700]
print("strip 515-539 mean:", strip.mean(axis=(0,1)).round(1))
for r in range(500,540):
    m = a[r,200:700].mean(axis=0)
    if m.mean()<100: print("dark row:", r, m.round(1))
