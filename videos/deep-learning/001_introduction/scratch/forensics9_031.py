from PIL import Image
import numpy as np
from collections import Counter

# --- Part A: the banked eq_031_matrix_test.png ---
p = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/build/assets/eq_031_matrix_test.png"
im = Image.open(p)
print("eq PNG:", im.size, im.mode)
a = np.asarray(im.convert("RGBA")).astype(int)
alpha = a[:, :, 3]
ink = alpha > 40
rows = np.where(ink.any(axis=1))[0]
cols = np.where(ink.any(axis=0))[0]
print("ink bbox: x", cols[0], "..", cols[-1], " y", rows[0], "..", rows[-1],
      f" (w={cols[-1]-cols[0]+1}, h={rows[-1]-rows[0]+1})")
# col profile runs (brackets vs entries)
colc = ink.sum(axis=0)
on = colc > 0
runs = []
s = None
for x, v in enumerate(on):
    if v and s is None: s = x
    if not v and s is not None:
        runs.append((s, x - 1)); s = None
if s is not None: runs.append((s, len(on) - 1))
print("col runs (n=%d):" % len(runs), runs[:20])
# row bands
rowc = ink.sum(axis=1)
onr = rowc > 0
bands = []
s = None
for y, v in enumerate(onr):
    if v and s is None: s = y
    if not v and s is not None:
        bands.append((s, y - 1)); s = None
if s is not None: bands.append((s, len(onr) - 1))
print("row bands:", bands)
# ink color
rgb = a[:, :, :3][ink]
c = Counter(map(tuple, rgb))
print("ink color modal:", c.most_common(5))

# --- Part B: original frame open questions ---
im2 = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_031.jpg").convert("RGB")
b = np.asarray(im2).astype(int)
H, W, _ = b.shape
R, G, B = b[:, :, 0], b[:, :, 1], b[:, :, 2]
darkred = (R > 100) & (R - G > 50) & (R - B > 40)

# vertical red line near x 50..70: full y extent
for x in range(50, 70):
    col = darkred[:, x]
    rr = np.where(col)[0]
    if len(rr) > 50:
        # longest contiguous run
        d = np.diff(rr)
        splits = np.where(d > 3)[0]
        segs = np.split(rr, splits + 1)
        longest = max(segs, key=len)
        print(f"red vline x={x}: longest run y {longest[0]}..{longest[-1]} (len {len(longest)}), total {len(rr)}")

# horizontal red line near y 30..50
for y in range(28, 55):
    row = darkred[y, :]
    rr = np.where(row)[0]
    if len(rr) > 300:
        print(f"red hline y={y}: x {rr[0]}..{rr[-1]} n={len(rr)}")

# darkest px of content box top border rows 132..136, x 150..850
band = b[132:137, 150:850].reshape(-1, 3)
lum = band.sum(axis=1)
i = lum.argmin()
print("content-box top border darkest px:", tuple(band.reshape(-1, 3)[i]))
band = b[365:369, 150:850].reshape(-1, 3)
lum = band.sum(axis=1); i = lum.argmin()
print("content-box bottom border darkest px:", tuple(band.reshape(-1, 3)[i]))
band = b[200:300, 97:102].reshape(-1, 3)
lum = band.sum(axis=1); i = lum.argmin()
print("content-box left border darkest px:", tuple(band.reshape(-1, 3)[i]))

# matrix box border geometry: rows/cols with red runs
for y in range(380, 512):
    row = darkred[y, 600:860]
    if row.sum() > 150:
        rr = np.where(row)[0]
        print(f"matrix box h-red y={y}: x {600+rr[0]}..{600+rr[-1]} n={len(rr)}")
for x in range(615, 855):
    colv = darkred[380:512, x]
    if colv.sum() > 90:
        rr = np.where(colv)[0]
        print(f"matrix box v-red x={x}: y {380+rr[0]}..{380+rr[-1]} n={len(rr)}")

# label box border rows/cols (periwinkle) exact extent
lp = (B - R > 10) & (B - G > 10) & (B > 150) & (R < 235)
print("label box h-borders (y 425..485, x 360..630, count>150):")
for y in range(425, 486):
    if lp[y, 360:630].sum() > 150:
        rr = np.where(lp[y, 360:630])[0]
        print(f"  y={y}: x {360+rr[0]}..{360+rr[-1]} n={lp[y,360:630].sum()}")
print("label box v-borders (x 360..630, y 425..485, count>30):")
for x in range(360, 631):
    if lp[425:486, x].sum() > 30:
        rr = np.where(lp[425:486, x])[0]
        print(f"  x={x}: y {425+rr[0]}..{425+rr[-1]} n={lp[425:486,x].sum()}")

# content box borders exact (lp mask, long runs)
print("content box h-borders y 125..140 / y 360..375 (x 90..900, count>600):")
for y in list(range(125, 141)) + list(range(358, 375)):
    if lp[y, 90:900].sum() > 600:
        rr = np.where(lp[y, 90:900])[0]
        print(f"  y={y}: x {90+rr[0]}..{90+rr[-1]} n={lp[y,90:900].sum()}")
print("content box v-borders x 90..110 / x 880..895 (y 130..370, count>200):")
for x in list(range(90, 111)) + list(range(880, 896)):
    if lp[130:370, x].sum() > 200:
        rr = np.where(lp[130:370, x])[0]
        print(f"  x={x}: y {130+rr[0]}..{130+rr[-1]} n={lp[130:370,x].sum()}")
