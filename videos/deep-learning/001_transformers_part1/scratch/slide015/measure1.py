# slide 015 frame measurement (960x540, 1px = 1pt = 1/72 in)
# Ground truth: unique_slides/slide_015.jpg
import numpy as np
from PIL import Image
from scipy import ndimage

BASE = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1'
f15 = np.asarray(Image.open(f'{BASE}/unique_slides/slide_015.jpg').convert('RGB')).astype(int)
f14 = np.asarray(Image.open(f'{BASE}/unique_slides/slide_014.jpg').convert('RGB')).astype(int)
H, W = f15.shape[:2]
print('frame size', W, H)

# ---- 1. left-half inheritance check vs slide_014 frame -----------------------
d = np.abs(f15[:, :460] - f14[:, :460]).sum(axis=2)
print(f'left-half (x<460) diff vs slide014 frame: mean={d.mean():.2f} max={d.max()} n>60={(d>60).sum()}')
ys, xs = np.where(d > 60)
if len(ys):
    print(f'  diff>60 bbox x[{xs.min()},{xs.max()}] y[{ys.min()},{ys.max()}]')
    lab, n = ndimage.label(d > 60)
    print('  components:', n)
    for i in range(1, n + 1):
        yy, xx = np.where(lab == i)
        if len(yy) > 20:
            print(f'    comp{i}: n={len(yy)} x[{xx.min()},{xx.max()}] y[{yy.min()},{yy.max()}]')

r, g, b = f15[:, :, 0], f15[:, :, 1], f15[:, :, 2]

def components(mask, min_n=15, tag=''):
    lab, n = ndimage.label(mask)
    out = []
    for i in range(1, n + 1):
        yy, xx = np.where(lab == i)
        if len(yy) >= min_n:
            out.append((len(yy), int(xx.min()), int(xx.max()), int(yy.min()), int(yy.max())))
    out.sort(reverse=True)
    for n_, x0, x1, y0, y1 in out[:14]:
        print(f'  {tag} comp n={n_} x[{x0},{x1}] y[{y0},{y1}] w={x1-x0+1} h={y1-y0+1}')
    return out

def core(mask):
    """median color of mask pixels"""
    if mask.sum() == 0:
        return None
    px = f15[mask]
    return tuple(int(v) for v in np.median(px, axis=0))

# ---- 2. strong red elements (excl. title band and badge) ---------------------
red = (r > 140) & (g < 90) & (b < 90) & (r - g > 80)
red_ex = red.copy()
red_ex[:100, :] = False          # title band
red_ex[:100, 855:] = False
print('\n== RED elements (excl title/badge) ==')
red_comps = components(red_ex, tag='red')

# ---- 3. strong green (panel border + Decoder header) -------------------------
green = (g > 110) & (g - r > 55) & (g - b > 35) & (r < 120)
print('\n== STRONG GREEN (border/decoder header) ==')
green_comps = components(green, tag='green')
print('green core color:', core(green))

# ---- 4. peach shading region --------------------------------------------------
peach = (r > 235) & (g > 205) & (g < 248) & (b > 190) & (b < 235) & (r - b > 20)
print('\n== PEACH shading ==')
peach_comps = components(peach, min_n=200, tag='peach')
print('peach core:', core(peach))

# ---- 5. light green shading ---------------------------------------------------
lgreen = (r > 195) & (r < 235) & (g > 225) & (b > 185) & (b < 230) & (g - b > 12)
print('\n== LIGHT GREEN shading ==')
lg_comps = components(lgreen, min_n=200, tag='lgreen')
print('lgreen core:', core(lgreen))

# ---- 6. white panel cards (right) ---------------------------------------------
white = (r > 242) & (g > 242) & (b > 242)
col_counts = white[:, 440:].sum(axis=0)
row_counts = white[90:, 440:].sum(axis=1)
# find contiguous white column span in right half
cols = np.where(col_counts > 60)[0] + 440
print('\nright-half white columns span:', cols.min() if len(cols) else None, cols.max() if len(cols) else None)
rows = np.where(row_counts > 60)[0] + 90
print('right-half white rows span:', rows.min() if len(rows) else None, rows.max() if len(rows) else None)

# ---- 7. left panel verify vs parent values ------------------------------------
print('\n== LEFT PANEL verify (parent: x[93.5,411.5] y[106,522.5], fig x[117,394] y[115,522]) ==')
black = (r < 90) & (g < 90) & (b < 90)
lp = black[100:530, 85:420]
print('left panel zone black px:', lp.sum())
# left figure colored-box mask
sat = (np.max(f15[:, :, :3], axis=2) - np.min(f15[:, :3], axis=2)) > 40
lf = sat[100:530, 100:410]
ys, xs = np.where(lf)
print('left figure colored bbox x[%d,%d] y[%d,%d]' % (xs.min() + 100, xs.max() + 100, ys.min() + 100, ys.max() + 100))

# ---- 8. dominant colors in right panel zone ------------------------------------
print('\n== RIGHT HALF dominant colors (x 440..940, y 100..540) ==')
zone = f15[100:540, 440:940].reshape(-1, 3)
q = (zone // 16) * 16
uq, cnt = np.unique(q, axis=0, return_counts=True)
order = np.argsort(-cnt)
for i in order[:24]:
    c = uq[i]
    print(f'  rgb~({c[0]},{c[1]},{c[2]}) n={cnt[i]}')
