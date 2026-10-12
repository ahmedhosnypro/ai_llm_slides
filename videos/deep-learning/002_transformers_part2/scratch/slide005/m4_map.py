# m4 (slide005): per-pixel tint classification vs warp with alpha least-squares,
# rendered as an ASCII map (3px cells) so band/callout/arrow shapes are readable.
# Classes: Y yellow-overlay, O orange-overlay, R strict red ink (C00000-like),
# . matches warp, ? other diff.
from PIL import Image
import numpy as np

A, Bx, C, D = 20.9473, 0.95679, 2.2031, 0.95651
myI = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_005.jpg').convert('RGB')
wI = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide005/warped_001_f21.png')
my = np.asarray(myI).astype(np.float32)
w = np.asarray(wI).astype(np.float32)
H, W = my.shape[:2]

YELLOW = np.array([255, 255, 0], np.float32)
ORANGE = np.array([237, 125, 49], np.float32)

def diffmag():
    return np.abs(my - w).max(axis=2)

Dd = diffmag()

def alpha_fit(tint):
    num = ((my - w) * (tint - w)).sum(axis=2)
    den = ((tint - w) ** 2).sum(axis=2) + 1e-6
    a = np.clip(num / den, 0, 1)
    res = np.abs(w + a[..., None] * (tint - w) - my).max(axis=2)
    return a, res

ay, ry = alpha_fit(YELLOW)
ao, ro = alpha_fit(ORANGE)

ymask = (ry < 22) & (ay > 0.30) & (ay < 0.68) & (Dd > 28)
omask = (ro < 22) & (ao > 0.30) & (ao < 0.68) & (Dd > 28)
redm = (my[..., 0] > 120) & (my[..., 1] < 90) & (my[..., 2] < 90)
match = Dd <= 28

cls = np.full((H, W), '?', '<U1')
cls[match] = '.'
cls[omask] = 'O'
cls[ymask] = 'Y'
cls[redm] = 'R'   # red ink wins over tint classes

# ASCII map, 3px cells, frame space, y 44..516, x 60..900
out = []
for y in range(44, 516, 3):
    row = []
    for x in range(60, 900, 3):
        cell = cls[y:y+3, x:x+3]
        vals, cnts = np.unique(cell, return_counts=True)
        order = np.argsort(-cnts)
        # prefer showing R/Y/O if present at >=25% of cell
        pick = '.'
        for v in vals[order]:
            if v in 'RYO' and cnts[order][list(vals).index(v)] >= 2:
                pick = v; break
            if v == '.':
                pick = '.'; break
        row.append(pick)
    out.append(''.join(row))
open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide005/m4_map.txt', 'w').write('\n'.join(out))
print('map written; frame y44->516 rows, x60->900 cols (3px cells)')
print('legend: Y yellow overlay, O orange overlay, R red ink, . = warp-match, ? other')
# print with a coarse x ruler
print('     ' + ''.join(str(((60 + 3*i) // 100) % 10) if (60 + 3*i) % 100 < 3 else ' ' for i in range(len(out[0]))))
for i, r in enumerate(out):
    if i % 10 == 0:
        print(f'{44 + 3*i:4d} {r}')
    else:
        print('     ' + r)
