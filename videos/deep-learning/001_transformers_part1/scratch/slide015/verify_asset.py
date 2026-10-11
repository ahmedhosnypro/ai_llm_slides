# verify slide015_fig1_color.png against the frame (region classes, box tints, ink)
import numpy as np
from PIL import Image

BASE = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1'
OUT = f'{BASE}/recreated_pptx/build/assets'
f15 = np.asarray(Image.open(f'{BASE}/unique_slides/slide_015.jpg').convert('RGB')).astype(int)
ast = Image.open(f'{OUT}/slide015_fig1_color.png')
print('asset size', ast.size)
IX0, IY0, IX1, IY1 = 575, 107, 892, 522
IW, IH = IX1 - IX0 + 1, IY1 - IY0 + 1
ad = np.asarray(ast.resize((IW, IH), Image.LANCZOS)).astype(int)
fr = f15[IY0:IY1 + 1, IX0:IX1 + 1].astype(int)

diff = np.abs(ad - fr).sum(axis=2)
print(f'overall mean|diff|={diff.mean():.1f}  median={np.median(diff):.1f}  frac>90={np.mean(diff > 90):.3f}')

# class agreement
WHITE = np.array([255, 255, 255]); PEACH = np.array([253, 237, 221]); GREEN = np.array([206, 255, 225])
def clsmap(a):
    f = a.reshape(-1, 3).astype(float)
    dw = np.linalg.norm(f - WHITE, axis=1); dp = np.linalg.norm(f - PEACH, axis=1); dg = np.linalg.norm(f - GREEN, axis=1)
    dmin = np.minimum(np.minimum(dw, dp), dg)
    c = np.full(len(f), 3, int)
    c[(dmin < 18) & (dw == dmin)] = 0
    c[(dmin < 18) & (dp == dmin)] = 1
    c[(dmin < 18) & (dg == dmin)] = 2
    return c.reshape(a.shape[:2])
ca, cf = clsmap(ad), clsmap(fr)
known = (ca != 3) & (cf != 3)
print(f'class agreement on known-class px: {(ca[known] == cf[known]).mean():.3f} (n={known.sum()})')
print('asset classes: white', (ca == 0).sum(), 'peach', (ca == 1).sum(), 'green', (ca == 2).sum(), 'other', (ca == 3).sum())
print('frame classes: white', (cf == 0).sum(), 'peach', (cf == 1).sum(), 'green', (cf == 2).sum(), 'other', (cf == 3).sum())

# dark ink IoU
da = (ad.max(axis=2) < 120); df = (fr.max(axis=2) < 120)
print(f'dark ink: asset n={da.sum()} frame n={df.sum()} IoU={(da & df).sum() / (da | df).sum():.3f}')

# per-box comparison at mapped rects (frame coords -> asset coords: subtract origin)
Sx, Sy = 277 / 1520, 408 / 2239
FX0, FY0 = 598, 115
boxes = [
    ('dec Softmax', 854, 1203, 215, 271), ('dec Linear', 854, 1203, 356, 412),
    ('dec AddNorm1', 854, 1203, 511, 568), ('dec FF', 854, 1204, 602, 737),
    ('dec AddNorm2', 854, 1203, 825, 881), ('enc AddNorm1', 314, 663, 883, 939),
    ('dec MHA', 854, 1204, 914, 1048), ('enc FF', 314, 663, 970, 1105),
    ('dec AddNorm3', 854, 1203, 1191, 1247), ('enc AddNorm2', 314, 663, 1251, 1307),
    ('dec maskedMHA', 854, 1204, 1280, 1473), ('enc MHA', 314, 664, 1338, 1473),
    ('enc embedding', 315, 664, 1822, 1956), ('dec embedding', 854, 1203, 1822, 1956),
]
print('\nper-box fill comparison (frame vs asset), central band:')
for tag, x0, x1, y0, y1 in boxes:
    fx0 = int(FX0 + x0 * Sx) + 4; fx1 = int(FX0 + x1 * Sx) - 4
    fy0 = int(FY0 + y0 * Sy) + 2; fy1 = int(FY0 + y1 * Sy) - 2
    ax0, ay0 = fx0 - IX0, fy0 - IY0; ax1, ay1 = fx1 - IX0, fy1 - IY0
    fv = fr[fy0 - IY0:fy1 - IY0 + 1, fx0 - IX0:fx1 - IX0 + 1].reshape(-1, 3)
    av = ad[ay0:ay1 + 1, ax0:ax1 + 1].reshape(-1, 3)
    def mode(v):
        q = (v // 4) * 4
        u, c = np.unique(q, axis=0, return_counts=True)
        return tuple(int(x) + 2 for x in u[np.argmax(c)])
    print(f'  {tag:15s} frame={mode(fv)} asset={mode(av)}')
