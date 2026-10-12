from PIL import Image
import numpy as np

im = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_017.jpg").convert("RGB")
a = np.asarray(im).astype(int)
H, W = a.shape[:2]
r, g, b = a[:,:,0], a[:,:,1], a[:,:,2]

# red-ish mask (border C00000 / dark red variants): strong red dominance
red = (r > 100) & (g < 90) & (b < 90) & (r - g > 60) & (r - b > 60)

# vertical borders: for each column count red pixels in y range 60..500
colcount = red[60:500, :].sum(axis=0)
cands = np.where(colcount > 200)[0]
print("vertical border columns (count>200):", cands)

# horizontal borders: rows with many red px in x 100..900
rowcount = red[:, 100:900].sum(axis=1)
cands = np.where(rowcount > 400)[0]
print("horizontal border rows (count>400):", cands)

# badge: yellow FDFD96-ish fill near top right: r>230,g>230,b<190
yel = (r>230)&(g>228)&(b<200)&(b>140)
# restrict to top-right quadrant
mask = np.zeros_like(yel); mask[0:150, 800:960] = yel[0:150, 800:960]
ys, xs = np.where(mask)
if len(xs):
    print("badge yellow bbox: x %d..%d  y %d..%d  cx %.1f cy %.1f n=%d" % (xs.min(), xs.max(), ys.min(), ys.max(), xs.mean(), ys.mean(), len(xs)))
else:
    print("no yellow badge found in top-right")

# purple ring 6A5ACD
pur = (np.abs(r-106)<45)&(np.abs(g-90)<45)&(np.abs(b-205)<55)
mask = np.zeros_like(pur); mask[0:150, 800:960] = pur[0:150, 800:960]
ys, xs = np.where(mask)
if len(xs):
    print("badge purple-ring bbox: x %d..%d y %d..%d n=%d" % (xs.min(), xs.max(), ys.min(), ys.max(), len(xs)))

# gray panel E9E9E7 extent: sample row y=200 and column x=W//2
def classify(px):
    rr,gg,bb = px
    if abs(rr-233)<8 and abs(gg-233)<8 and abs(bb-231)<8: return "panel"
    return None
row = a[250]
xs = [x for x in range(W) if classify(row[x])]
print("row250 panel-gray run:", (min(xs), max(xs)) if xs else None, "n=", len(xs))
col = a[:, 470]
ys = [y for y in range(H) if classify(col[y])]
print("col470 panel-gray run:", (min(ys), max(ys)) if ys else None, "n=", len(ys))

# bottom dark strip (letterbox) height
dark = (r<70)&(g<70)&(b<70)
for y in range(H-1, H-40, -1):
    frac = dark[y, :].mean()
    if frac < 0.5:
        print("last non-dark row:", y); break
