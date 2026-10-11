# slide 015 measurement pass 4: paste-rect optimization, arrow shapes, tint cores, headers
import numpy as np
from PIL import Image

BASE = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1'
f15 = np.asarray(Image.open(f'{BASE}/unique_slides/slide_015.jpg').convert('RGB')).astype(int)
r, g, b = f15[:, :, 0], f15[:, :, 1], f15[:, :, 2]
dark = (r < 120) & (g < 120) & (b < 120)
paper = np.asarray(Image.open(f'{BASE}/recreated_pptx/build/assets/slide014_fig1.png').convert('RGB')).astype(int)
pdark = (paper[:, :, 0] < 120) & (paper[:, :, 1] < 120) & (paper[:, :, 2] < 120)

# ---- A. IoU-optimize figure paste rect (fixed 277x407, grid over x0,y0) --------
FW, FH = 277, 407
pr = np.asarray(Image.fromarray((pdark * 255).astype(np.uint8)).resize((FW, FH))) > 127
zone = dark[100:530, 570:900]  # panel interior
best = None
for x0 in range(582, 598):
    for y0 in range(110, 121):
        x1, y1 = x0 + FW - 1, y0 + FH - 1
        if y1 > 529 or x1 > 899:
            continue
        fd = dark[y0:y1 + 1, x0:x1 + 1]
        inter = (fd & pr).sum(); union = (fd | pr).sum()
        iou = inter / union
        if best is None or iou > best[0]:
            best = (iou, x0, y0)
print(f'A. best paste rect 277x407: IoU={best[0]:.3f} at x0={best[1]} y0={best[2]} -> x[{best[1]},{best[1]+FW-1}] y[{best[2]},{best[2]+FH-1}]')

# also let width vary a bit
best2 = None
for w in (272, 274, 276, 277, 278, 280, 283):
    h = int(round(w * 2239 / 1520))
    prw = np.asarray(Image.fromarray((pdark * 255).astype(np.uint8)).resize((w, h))) > 127
    for x0 in range(580, 600):
        for y0 in range(108, 122):
            x1, y1 = x0 + w - 1, y0 + h - 1
            if y1 > 529 or x1 > 899:
                continue
            fd = dark[y0:y1 + 1, x0:x1 + 1]
            iou = (fd & prw).sum() / (fd | prw).sum()
            if best2 is None or iou > best2[0]:
                best2 = (iou, x0, y0, w, h)
print(f'   free-size best: IoU={best2[0]:.3f} x0={best2[1]} y0={best2[2]} w={best2[3]} h={best2[4]}')

# ---- B. block arrow full row profile -------------------------------------------
red = (r > 120) & (r - g > 60) & (r - b > 60)
sub = red[290:325, 450:535]
print('\nB. BLOCK ARROW rows (y: xmin..xmax w):')
for yy in range(sub.shape[0]):
    xr = np.where(sub[yy])[0]
    if len(xr):
        print(f'   y={yy+290}: {xr.min()+450}..{xr.max()+450} w={xr.max()-xr.min()+1} n={len(xr)}')

# ---- C. up arrows full profiles --------------------------------------------------
for tag, (x0, x1, y0, y1) in {'up1': (645, 680, 480, 520), 'up2': (733, 760, 110, 148)}.items():
    sub = red[y0:y1, x0:x1]
    print(f'\nC. {tag} rows:')
    for yy in range(sub.shape[0]):
        xr = np.where(sub[yy])[0]
        if len(xr):
            print(f'   y={yy+y0}: {xr.min()+x0}..{xr.max()+x0} w={xr.max()-xr.min()+1}')

# ---- D. tint cores: sample box interiors via frame masks ------------------------
def core_of(mask, tag):
    if mask.sum() < 30:
        print(f'   {tag}: n={mask.sum()} TOO FEW')
        return
    px = f15[mask]
    med = np.median(px, axis=0)
    # trim: use the 25-75 percentile spread
    print(f'   {tag}: n={mask.sum()} core=({med[0]:.0f},{med[1]:.0f},{med[2]:.0f})')

print('\nD. right-panel tint cores:')
# encoder MHA tan ~ (240,208,160)
m = (np.abs(r - 240) < 22) & (np.abs(g - 208) < 20) & (np.abs(b - 160) < 25)
m[:105, :] = False; m[:, :578] = False; m[:, 736:] = False
core_of(m, 'ENC MHA tan')
# encoder FF grayish-blue ~ (192,208,208)
m = (np.abs(r - 192) < 20) & (np.abs(g - 208) < 18) & (np.abs(b - 208) < 18)
m[:105, :] = False; m[:, :578] = False; m[:, 736:] = False
core_of(m, 'ENC FF grayblue')
# decoder yellow-green ~ (192,224,160)
m = (np.abs(r - 195) < 25) & (np.abs(g - 225) < 20) & (np.abs(b - 162) < 25)
m[:105, :] = False; m[:, :736] = False; m[:, 892:] = False
core_of(m, 'DEC yellowgreen')
# decoder green ~ (176,224,192)
m = (np.abs(r - 178) < 22) & (np.abs(g - 226) < 18) & (np.abs(b - 194) < 22)
m[:105, :] = False; m[:, :736] = False; m[:, 892:] = False
core_of(m, 'DEC green')
# where are these boxes? bboxes
def bbox_of(mask, tag):
    ys, xs = np.where(mask)
    if len(ys):
        print(f'   {tag} bbox x[{xs.min()},{xs.max()}] y[{ys.min()},{ys.max()}]')
m2 = (np.abs(r - 240) < 22) & (np.abs(g - 208) < 20) & (np.abs(b - 160) < 25)
m2[:105, :] = False; m2[:, :578] = False; m2[:, 736:] = False
bbox_of(m2, 'ENC MHA tan')
m2 = (np.abs(r - 192) < 20) & (np.abs(g - 208) < 18) & (np.abs(b - 208) < 18)
m2[:105, :] = False; m2[:, :578] = False; m2[:, 736:] = False
bbox_of(m2, 'ENC FF grayblue')
m2 = (np.abs(r - 195) < 25) & (np.abs(g - 225) < 20) & (np.abs(b - 162) < 25)
m2[:105, :] = False; m2[:, :736] = False; m2[:, 892:] = False
bbox_of(m2, 'DEC yellowgreen')
m2 = (np.abs(r - 178) < 22) & (np.abs(g - 226) < 18) & (np.abs(b - 194) < 22)
m2[:105, :] = False; m2[:, :736] = False; m2[:, 892:] = False
bbox_of(m2, 'DEC green')

# ---- E. headers clean ------------------------------------------------------------
redtxt = (r > 140) & (r - g > 60) & (r - b > 60)
sub = redtxt[108:148, 578:741]
ys, xs = np.where(sub)
print(f'\nE. ENCODER text ink: x[{xs.min()+578},{xs.max()+578}] y[{ys.min()+108},{ys.max()+108}] n={len(ys)}')
px = f15[108:148, 578:741][sub]
print('   core:', np.median(px, axis=0))
gtxt = (g > 100) & (g - r > 50) & (g - b > 30) & (r < 130)
sub = gtxt[108:150, 762:892]
ys, xs = np.where(sub)
print(f'   DECODER text ink: x[{xs.min()+762},{xs.max()+762}] y[{ys.min()+108},{ys.max()+108}] n={len(ys)}')
px = f15[108:150, 762:892][sub]
print('   core:', np.median(px, axis=0))

# ---- F. left panel Add&Norm / embedding / Linear / Softmax cores (frame LEFT = paper colors, for "same as left" check)
print('\nF. LEFT panel cores (paper-paste):')
for tag, (x0, x1, y0, y1) in {'sample boxes': (117, 394, 115, 522)}.items():
    zoneL = f15[y0:y1, x0:x1].reshape(-1, 3)
    q = (zoneL // 12) * 12
    uq, cnt = np.unique(q, axis=0, return_counts=True)
    order = np.argsort(-cnt)
    for i in order[:10]:
        c = uq[i]
        if c.min() > 228:
            continue
        print(f'   ~({c[0]},{c[1]},{c[2]}) n={cnt[i]}')
