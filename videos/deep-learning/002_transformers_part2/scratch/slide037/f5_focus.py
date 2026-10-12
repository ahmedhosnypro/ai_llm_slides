# f5: focused pass — pin shape, disc, dashed box edges, funnel lines, title metrics.
from PIL import Image
import numpy as np
img = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_037.jpg').convert('RGB')).astype(int)
H, W, _ = img.shape
A, B, C, D = 21.15, 0.95635, 2.00, 0.95695
def tb(fx, fy): return (round((fx-A)/B,1), round((fy-C)/D,1))

r, g, b = img[...,0], img[...,1], img[...,2]

# (a) what is strong red at y115-185, x660-790?
strong = (r > 150) & (g < 70) & (b < 80)
ys, xs = np.where(strong[110:190, 655:795])
print("strong red y110-190 x655-795:", len(xs), "px; bbox:",
      (int(xs.min()+655), int(ys.min()+110), int(xs.max()+655), int(ys.max()+110)) if len(xs) else None)
# cluster by row
for y in range(110, 190):
    xr = np.where(strong[y, 655:795])[0]
    if len(xr): print(f"  y={y}: x {xr.min()+655}-{xr.max()+655} n={len(xr)}")

# (b) pin white text, threshold 200
wt = (r > 200) & (g > 200) & (b > 200)
ys, xs = np.where(wt[150:250, 580:730])
print("white>200 in pin zone:", len(xs), "px; bbox:",
      (int(xs.min()+580), int(ys.min()+150), int(xs.max()+580), int(ys.max()+150)) if len(xs) else None,
      "-> build", tb(int(xs.min()+580), int(ys.min()+150)) if len(xs) else None)
if len(xs):
    rows = {}
    for y in range(150, 250):
        xr = np.where(wt[y, 580:730])[0]
        if len(xr) >= 2: rows[y] = (int(xr.min()+580), int(xr.max()+580))
    print("  white rows:", rows)

# (c) funnel: LOOSE red (thin dashes on gray/white/peach)
loose = (r > 130) & (r - g > 45) & (r - b > 35) & (g < 150)
print("LOOSE red funnel scan x180-570 y270-440:")
seg = {}
for y in range(270, 440):
    xr = np.where(loose[y, 180:570])[0]
    if len(xr) >= 2: seg[y] = (int(xr.min()+180), int(xr.max()+180), int(len(xr)))
print(seg)
# also x505-570 (between inset B right edge and arch border)
seg2 = {}
for y in range(200, 470):
    xr = np.where(loose[y, 509:568])[0]
    if len(xr) >= 1: seg2[y] = (int(xr.min()+509), int(xr.max()+509), int(len(xr)))
print("LOOSE red x509-568:", seg2)

# (d) dashed box edges: red px in x600-740 y230-420 excluding disc (x641-712 y320-388) & pin (y<300 x582-700)
box = loose.copy()
box[:232, :] = False; box[420:, :] = False
box[:, :600] = False; box[:, 745:] = False
box[300:395, 630:725] = False   # disc zone
ys, xs = np.where(box)
print("dashed-box candidate px:", len(xs))
colhist = {}
for x, y in zip(xs, ys):
    colhist.setdefault(x, []).append(y)
cols = sorted(colhist)
print("box red columns:", [(x, len(colhist[x]), min(colhist[x]), max(colhist[x])) for x in cols if len(colhist[x]) >= 3])

# (e) title 'T' cap height: red rows in x110-140
tit = (r > 140) & (g < 95) & (b < 95)
for x0, x1, lbl in [(110, 140, "'T'"), (319, 345, "'B' of Blocks"), (586, 610, "'o' of over")]:
    ys2 = np.where(tit[40:100, x0:x1].sum(axis=1) > 0)[0]
    if len(ys2): print(f"title {lbl} x{x0}-{x1}: rows {ys2.min()+40}-{ys2.max()+40} (h={ys2.max()-ys2.min()+1})")

# (f) save visualization overlays (red mask + strong mask) for the record
vis = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_037.jpg')).copy()
vis[loose] = [255, 0, 255]
Image.fromarray(vis).save('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide037/f5_loose_red_overlay.png')
vis2 = vis.copy(); vis2[strong] = [0, 255, 255]
Image.fromarray(vis2).save('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide037/f5_strong_overlay.png')
print("overlays saved")
