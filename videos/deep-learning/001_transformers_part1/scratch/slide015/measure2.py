# slide 015 measurement pass 2: figure bbox, structural check, color cores
import numpy as np
from PIL import Image
from scipy import ndimage

BASE = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1'
f15 = np.asarray(Image.open(f'{BASE}/unique_slides/slide_015.jpg').convert('RGB')).astype(int)
r, g, b = f15[:, :, 0], f15[:, :, 1], f15[:, :, 2]
H, W = 540, 960

# ---- 1. left figure bbox (verify parent inheritance) --------------------------
dark = (r < 120) & (g < 120) & (b < 120)
sat = (np.max(f15, axis=2) - np.min(f15, axis=2)) > 40
ink = dark | sat
ys, xs = np.where(ink[100:530, 100:410])
print('LEFT figure ink bbox: x[%d,%d] y[%d,%d]  (parent certified: x[117,394] y[115,522])'
      % (xs.min() + 100, xs.max() + 100, ys.min() + 100, ys.max() + 100))

# ---- 2. right panel interior: figure ink bbox ---------------------------------
# panel x[572,895] y[104,525]; exclude the green border ring (2px) and headers zone
ys, xs = np.where(ink[110:522, 578:890])
print('RIGHT figure ink bbox (dark|sat, interior): x[%d,%d] y[%d,%d]'
      % (xs.min() + 578, xs.max() + 578, ys.min() + 110, ys.max() + 110))
# dark-only (lines/text) within right panel
ys, xs = np.where(dark[110:522, 578:890])
print('RIGHT figure dark-only bbox: x[%d,%d] y[%d,%d] n=%d'
      % (xs.min() + 578, xs.max() + 578, ys.min() + 110, ys.max() + 110, len(ys)))

# ---- 3. structural check: paper figure vs frame right region ------------------
paper = np.asarray(Image.open(f'{BASE}/recreated_pptx/build/assets/slide014_fig1.png').convert('RGB')).astype(int)
print('paper image size:', paper.shape[1], 'x', paper.shape[0])
pdark = (paper[:, :, 0] < 120) & (paper[:, :, 1] < 120) & (paper[:, :, 2] < 120)
print('paper dark px:', pdark.sum(), 'fraction', pdark.mean())

def iou_check(fx0, fx1, fy0, fy1, tag):
    fw, fh = fx1 - fx0 + 1, fy1 - fy0 + 1
    fr = np.asarray(Image.fromarray(f15[fy0:fy1 + 1, fx0:fx1 + 1].astype(np.uint8)).resize((200, 295)))
    fdark = (fr[:, :, 0] < 120) & (fr[:, :, 1] < 120) & (fr[:, :, 2] < 120)
    pr = np.asarray(Image.fromarray(pdark.astype(np.uint8) * 255).resize((200, 295))) > 127
    inter = (fdark & pr).sum(); union = (fdark | pr).sum()
    print(f'{tag}: frame ink n={fdark.sum()} paper ink n={pr.sum()} IoU={inter/union:.3f}')
    return inter / union

# left figure rect (parent) as calibration of the method
iou_check(117, 394, 115, 522, 'calib LEFT fig vs paper')
# candidate right figure rects
iou_check(578, 890, 110, 522, 'RIGHT fig candidate A (panel interior)')

# ---- 4. paper palette (cluster) ------------------------------------------------
q = (paper.reshape(-1, 3) // 24) * 24
uq, cnt = np.unique(q, axis=0, return_counts=True)
order = np.argsort(-cnt)
print('\nPAPER dominant colors:')
for i in order[:14]:
    c = uq[i]
    print(f'  ~({c[0]},{c[1]},{c[2]}) n={cnt[i]}')

# ---- 5. frame right-panel box fill cores by column ------------------------------
print('\nFRAME right-panel saturated colors (encoder col x 578..734 / decoder col x 736..890):')
zone = f15[115:515, 578:890]
zone_r, zone_g, zone_b = zone[:, :, 0], zone[:, :, 1], zone[:, :, 2]
enc = zone[:, :734 - 578 + 1].reshape(-1, 3)
dec = zone[:, 736 - 578:].reshape(-1, 3)
for tag, arr in (('ENC', enc), ('DEC', dec)):
    qs = (arr // 16) * 16
    uq, cnt = np.unique(qs, axis=0, return_counts=True)
    order = np.argsort(-cnt)
    print(f' {tag}:')
    for i in order[:12]:
        c = uq[i]
        if c[0] > 240 and c[1] > 240 and c[2] > 240:
            continue
        print(f'   ~({c[0]},{c[1]},{c[2]}) n={cnt[i]}')

# ---- 6. shading rect edges precise ---------------------------------------------
peach = (r > 240) & (g > 215) & (g < 250) & (b > 195) & (b < 240) & (r - b > 18)
peach_r = peach[:, 560:900]
rows = np.where(peach_r.sum(axis=1) > 80)[0]
cols = np.where(peach_r.sum(axis=0) > 200)[0] + 560
print('\nPEACH rect rows', rows.min(), rows.max(), 'cols', cols.min(), cols.max())
lgreen = (r > 195) & (r < 240) & (g > 228) & (b > 195) & (b < 235) & (g - b > 14)
lg_r = lgreen[:, 560:900]
rows2 = np.where(lg_r.sum(axis=1) > 80)[0]
cols2 = np.where(lg_r.sum(axis=0) > 200)[0] + 560
print('LGREEN rect rows', rows2.min(), rows2.max(), 'cols', cols2.min(), cols2.max())
# color cores away from ink: sample the middle of each shading rect's top area
print('peach core sample (y=130,x=600):', f15[130, 600], ' (y=460,x=700):', f15[460, 700])
print('lgreen core sample (y=130,x=860):', f15[130, 860], ' (y=460,x=860):', f15[460, 860])

# ---- 7. panel green border precise ----------------------------------------------
gstrong = (g > 110) & (g - r > 55) & (g - b > 35) & (r < 120)
# vertical border lines: columns with long runs
colsum = gstrong[100:530, :].sum(axis=0)
cand = np.where(colsum > 200)[0]
print('\ngreen vertical border cols:', cand)
rowsum = gstrong[:, 560:910].sum(axis=1)
candr = np.where(rowsum > 200)[0]
print('green horizontal border rows:', candr)
# border stroke color: sample on the left border col
if len(cand):
    c0 = cand.min()
    print('border color samples col', c0, ':', f15[200, c0], f15[300, c0], f15[400, c0])

# ---- 8. block arrow precise (looser red) ----------------------------------------
red = (r > 130) & (g < 110) & (b < 110) & (r - g > 60)
sub = red[270:350, 430:560]
ys, xs = np.where(sub)
print('\nBLOCK ARROW bbox: x[%d,%d] y[%d,%d] n=%d' % (xs.min() + 430, xs.max() + 430, ys.min() + 270, ys.max() + 270, len(ys)))
print('arrow core:', f15[307, 490], f15[300, 470], f15[315, 510])
# per-row extent to see the shape (shaft vs head)
for yy in range(ys.min(), ys.max() + 1, 4):
    xr = np.where(sub[yy])[0]
    if len(xr):
        print(f'  row y={yy+270}: x {xr.min()+430}..{xr.max()+430} (w={xr.max()-xr.min()+1})')

# ---- 9. up arrows (looser red) ---------------------------------------------------
for tag, (x0, x1, y0, y1) in {'up1': (640, 690, 470, 530), 'up2': (725, 775, 100, 160)}.items():
    sub = red[y0:y1, x0:x1]
    ys, xs = np.where(sub)
    if len(ys):
        print(f'{tag}: x[{xs.min()+x0},{xs.max()+x0}] y[{ys.min()+y0},{ys.max()+y0}] n={len(ys)} core:', f15[(ys.min()+ys.max())//2+y0, (xs.min()+xs.max())//2+x0])
        for yy in range(ys.min(), ys.max() + 1, 3):
            xr = np.where(sub[yy])[0]
            if len(xr):
                print(f'   row y={yy+y0}: x {xr.min()+x0}..{xr.max()+x0} (w={xr.max()-xr.min()+1})')

# ---- 10. headers ------------------------------------------------------------------
redtxt = (r > 140) & (r - g > 60) & (r - b > 60)
sub = redtxt[105:145, 578:770]
ys, xs = np.where(sub)
print('\nENCODER header red ink: x[%d,%d] y[%d,%d] n=%d' % (xs.min() + 578, xs.max() + 578, ys.min() + 105, ys.max() + 105, len(ys)))
gtxt = (g > 110) & (g - r > 55) & (g - b > 35) & (r < 120)
sub = gtxt[105:145, 770:900]
ys, xs = np.where(sub)
print('DECODER header green ink: x[%d,%d] y[%d,%d] n=%d' % (xs.min() + 770, xs.max() + 770, ys.min() + 105, ys.max() + 105, len(ys)))

# ---- 11. left-vs-right figure mean abs diff (inheritance sanity) ------------------
f14 = np.asarray(Image.open(f'{BASE}/unique_slides/slide_014.jpg').convert('RGB')).astype(int)
dl = np.abs(f15[115:523, 117:395] - f14[115:523, 117:395]).mean()
print('\nleft figure region mean|diff| vs slide014 frame:', round(dl, 2))
