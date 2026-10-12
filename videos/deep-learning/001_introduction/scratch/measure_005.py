from PIL import Image
import numpy as np
im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_005.jpg').convert('RGB')
a = np.asarray(im).astype(int)
H, W, _ = a.shape
print("size", W, H)

def modal(region):
    px = region.reshape(-1,3)
    vals, counts = np.unique(px, axis=0, return_counts=True)
    return vals[counts.argmax()], counts.max()

# corners / backdrop samples
print("corner(5,5)", a[5,5], "top-mid(5,480)", a[5,480], "left-mid(270,20)", a[270,20], "right-mid(270,940)", a[270,940])
print("bottom bar rows:", [(y, tuple(a[y,480])) for y in (515,520,525,530,535,538,539)])

# black bar top edge: scan column 480 from bottom for near-black run
col = a[:,480,:]
dark = np.where(col.sum(axis=1) < 150)[0]
print("dark rows col480:", dark.min() if len(dark) else None, dark.max() if len(dark) else None, len(dark))

# white surface bounds: near-white mask
white = (a.min(axis=2) > 235)
rows = np.where(white.sum(axis=1) > 100)[0]
cols = np.where(white.sum(axis=0) > 30)[0]
print("white rows", rows.min(), rows.max(), "cols", cols.min(), cols.max())

# red mask (title, header, border, lead-ins)
r, g, b = a[:,:,0], a[:,:,1], a[:,:,2]
red = (r > 130) & (g < 90) & (b < 90)
red_rows = np.where(red.sum(axis=1) > 3)[0]
print("red row bands:", red_rows.min(), red_rows.max())
# find red bands (runs of rows with red)
bands = []
prev = -10; start=None
for y in red_rows:
    if y - prev > 3:
        if start is not None: bands.append((start, prev))
        start = y
    prev = y
bands.append((start, prev))
for (y0,y1) in bands:
    band = red[y0:y1+1,:]
    xs = np.where(band.sum(axis=0) > 0)[0]
    print(f"red band y {y0}..{y1} h={y1-y0+1} x {xs.min()}..{xs.max()} count={band.sum()}")

# black ink (bullets) inside content area
ink = (a.max(axis=2) < 110)
sub = ink[100:520, 60:900]
rr = np.where(sub.sum(axis=1) > 2)[0]
bands = []
prev=-10; start=None
for y in rr:
    if y - prev > 4:
        if start is not None: bands.append((start+100, prev+100))
        start = y
    prev = y
if start is not None: bands.append((start+100, prev+100))
print("black ink bands (y, x-extent):")
for (y0,y1) in bands:
    band = ink[y0:y1+1, 60:900]
    xs = np.where(band.sum(axis=0)>0)[0]
    print(f"  y {y0}..{y1} h={y1-y0+1} x {xs.min()+60}..{xs.max()+60} count={band.sum()}")

# blue mask
blue = (b > 120) & (r < 100) & (g < 100)
brs = np.where(blue.sum(axis=1) > 2)[0]
print("blue rows:", (brs.min(), brs.max()) if len(brs) else None, "count", blue.sum())

# color samples
tt = red[60:110, 200:760]
print("modal title red px:", modal(a[60:110,200:760][tt]) if tt.sum() else None)
hb = red[150:200, 80:880]
print("modal header red px:", modal(a[150:200,80:880][hb]) if hb.sum() else None)
print("modal backdrop:", modal(a[0:30, 0:80]))
print("modal surface:", modal(a[420:470, 300:600]))
print("modal bar:", modal(a[528:538, 300:600]))
bl = blue[100:520, 60:900]
if bl.sum():
    ys, xs = np.where(bl)
    print("blue px bbox: y", ys.min()+100, ys.max()+100, "x", xs.min()+60, xs.max()+60)
    print("modal blue:", modal(a[100:520,60:900][bl]))
bb = (r>130)&(g<90)&(b<90)
print("modal content-box border red sample y135-140 x100-900:", modal(a[133:142,100:900][bb[133:142,100:900]]) if bb[133:142,100:900].sum() else None)
