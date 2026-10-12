# m11 (slide005): 2px ASCII tint maps of the two orange band zones (frame space).
from PIL import Image
import numpy as np

myI = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_005.jpg').convert('RGB')
wI = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide005/warped_001_018.png')
my = np.asarray(myI).astype(np.float32)
w = np.asarray(wI).astype(np.float32)
ORANGE = np.array([237, 125, 49], np.float32)
d = ORANGE - w
den = (d * d).sum(axis=2) + 1e-6
a = np.clip(((my - w) * d).sum(axis=2) / den, 0, 1)
res = np.abs(w + a[..., None] * d - my).max(axis=2)
tint = (res < 30) & (a > 0.40) & (a < 0.90)

def to_build_x(fx): return (fx - 18.0787) / 0.961084
def to_build_y(fy): return (fy - 0.4700) / 0.957187

def zone(name, x0, x1, y0, y1):
    print(f'== {name} (frame x{x0}..{x1} y{y0}..{y1}, 2px cells; #=tint, .=none) ==')
    xr = list(range(x0, x1, 2))
    print('     ' + ''.join('|' if (x % 50) < 2 else ('5' if (x % 50) < 5 else ' ') for x in xr))
    for y in range(y0, y1, 2):
        row = ''.join('#' if tint[y:y+2, x:x+2].mean() > 0.5 else ('+' if tint[y:y+2, x:x+2].mean() > 0.2 else '.') for x in xr)
        by = to_build_y(y)
        print(f'{by:5.0f} {row}')
    print('     ' + ''.join('|' if (x % 50) < 2 else ('5' if (x % 50) < 5 else ' ') for x in xr))
    print('     ' + ''.join(str(int(to_build_x(x)) % 10) if (x % 10) < 2 else ' ' for x in xr))

zone('BAND B zone', 555, 770, 325, 425)
zone('BAND C zone', 700, 900, 245, 430)
