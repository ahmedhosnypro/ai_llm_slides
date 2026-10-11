# slide 015 measurement pass 3: right-figure identity, box cores, shading edges, arrow shape
import numpy as np
from PIL import Image
from scipy import ndimage

BASE = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1'
f15 = np.asarray(Image.open(f'{BASE}/unique_slides/slide_015.jpg').convert('RGB')).astype(int)
r, g, b = f15[:, :, 0], f15[:, :, 1], f15[:, :, 2]
dark = (r < 120) & (g < 120) & (b < 120)

# ---- A. is the right figure the left figure recolored? ------------------------
# left figure ink bbox x[118,391] y[117,518]; right dark-only x[592,858] y[117,517]
L = dark[117:519, 118:392]
R = dark[117:518, 592:859]
# align by bbox tops; slide R over L for a range of dx,dy
best = None
for dy in range(-3, 4):
    for dx in range(-6, 7):
        Rs = np.roll(np.roll(R, dy, axis=0), dx, axis=1)
        # crop to common
        h = min(L.shape[0], Rs.shape[0]); w = min(L.shape[1], Rs.shape[1])
        inter = (L[:h, :w] & Rs[:h, :w]).sum(); union = (L[:h, :w] | Rs[:h, :w]).sum()
        iou = inter / union
        if best is None or iou > best[0]:
            best = (iou, dx, dy)
print(f'A. left-ink vs right-ink IoU={best[0]:.3f} at dx={best[1]} dy={best[2]}  (same-rendering test)')

# ---- B. paper figure vs right figure at proper aspect -------------------------
paper = np.asarray(Image.open(f'{BASE}/recreated_pptx/build/assets/slide014_fig1.png').convert('RGB')).astype(int)
pdark = (paper[:, :, 0] < 120) & (paper[:, :, 1] < 120) & (paper[:, :, 2] < 120)
PH, PW = pdark.shape  # 2239 x 1520

def fig_iou(fx0, fx1, fy0, fy1):
    crop = f15[fy0:fy1, fx0:fx1]
    fd = (crop[:, :, 0] < 120) & (crop[:, :, 1] < 120) & (crop[:, :, 2] < 120)
    fh, fw = fd.shape
    target_h = int(round(fh * PW / fw))  # scale keeping frame crop's own aspect -> paper aspect mapped
    # resize paper to the crop's size directly (aspect-correct: paper aspect vs crop aspect)
    pr = np.asarray(Image.fromarray((pdark * 255).astype(np.uint8)).resize((fw, fh))) > 127
    inter = (fd & pr).sum(); union = (fd | pr).sum()
    return inter / union, fd.sum(), pr.sum()

print('B. paper vs frame-right, candidate rects:')
for (x0, x1, y0, y1) in [(592, 869, 115, 522), (590, 866, 115, 522), (594, 871, 117, 524),
                          (592, 858, 117, 517), (588, 875, 112, 519), (596, 873, 117, 524)]:
    iou, fn, pn = fig_iou(x0, x1, y0, y1)
    print(f'   x[{x0},{x1}] y[{y0},{y1}] w={x1-x0} h={y1-y0}: IoU={iou:.3f} (frame n={fn}, paper n={pn})')
iou, fn, pn = fig_iou(117, 394, 115, 522)
print(f'   calib LEFT x[117,394] y[115,522]: IoU={iou:.3f}')

# ---- C. per-box color cores: map paper box components through paste transform --
# find colored components in the paper image
pm = paper.max(axis=2) - paper.min(axis=2)
psat = pm > 30
plab, pn_ = ndimage.label(psat)
sizes = ndimage.sum(psat, plab, range(1, pn_ + 1))
big = [i + 1 for i in range(pn_) if sizes[i] > 3000]
print(f'\nC. paper colored components >3000px: {len(big)}')
boxes = []
for i in big:
    yy, xx = np.where(plab == i)
    core = tuple(int(v) for v in np.median(paper[yy, xx], axis=0))
    boxes.append((len(yy), int(xx.min()), int(xx.max()), int(yy.min()), int(yy.max()), core))
boxes.sort(key=lambda t: (t[3], t[1]))
for n_, x0, x1, y0, y1, core in boxes:
    print(f'   paper comp n={n_} x[{x0},{x1}] y[{y0},{y1}] core={core}')
