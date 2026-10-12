from PIL import Image
import numpy as np
p = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_015.jpg"
im = Image.open(p).convert("RGB")
W,H = im.size
print("size", W, H)
a = np.asarray(im).astype(int)

def inkmask(arr, thresh=120):
    # dark-ish ink: all channels below thresh
    return (arr[:,:,0]<thresh)&(arr[:,:,1]<thresh)&(arr[:,:,2]<thresh)

# 1. Find red border pixels (strong red: R high, G,B low)
red = (a[:,:,0]>120)&(a[:,:,1]<90)&(a[:,:,2]<90)
rows = np.where(red.sum(axis=1)>50)[0]
cols = np.where(red.sum(axis=0)>50)[0]
print("red rows span:", rows.min() if len(rows) else None, rows.max() if len(rows) else None, "count rows", len(rows))
print("red cols span:", cols.min() if len(cols) else None, cols.max() if len(cols) else None, "count cols", len(cols))
# horizontal red lines (top/bottom border)
rsum = red.sum(axis=1)
print("rows with red>400:", [ (int(r), int(rsum[r])) for r in np.where(rsum>400)[0] ])
csum = red.sum(axis=0)
print("cols with red>200:", [ (int(c), int(csum[c])) for c in np.where(csum>200)[0] ])

# 2. dark text ink inside the frame
ink = inkmask(a, 140)
# restrict to plausible title area rows 100..450
ink_r = ink[60:520,:]
rr = np.where(ink_r.sum(axis=1)>3)[0] + 60
if len(rr):
    # find contiguous bands
    bands=[]; start=rr[0]; prev=rr[0]
    for r in rr[1:]:
        if r-prev>3:
            bands.append((start,prev)); start=r
        prev=r
    bands.append((start,prev))
    print("dark-ink row bands (60..520):", bands)
    for (b0,b1) in bands:
        seg = ink[b0:b1+1,:]
        cs = np.where(seg.sum(axis=0)>0)[0]
        print(f"  band {b0}-{b1}: cols {cs.min()}-{cs.max()}, height {b1-b0+1}")
# 3. sample text color: darkest red-ish pixels in the title bands
dark = (a[:,:,0]>80)&(a[:,:,0]<200)&(a[:,:,1]<80)&(a[:,:,2]<80)
ys,xs = np.where(dark)
if len(ys):
    print("dark-red pixel count:", len(ys), "sample mean RGB:", a[ys,xs].mean(axis=0).round(1))
# 4. panel fill color sample (center, avoid text)
print("panel fill sample @(100,480):", a[480,100], "@(200,700):", a[700,200])
print("canvas sample @(5,5):", a[5,5], "@(30,300):", a[300,30])
# 5. bottom black strip
print("bottom strip sample @(535,480):", a[535,480], "rows 520..539 mean:", a[520:540,100:800].mean(axis=(0,1)).round(1))
for r in range(520,540):
    row = a[r,100:800].mean(axis=0)
    if row.mean() < 60:
        print("black-ish row:", r, row.round(1))
