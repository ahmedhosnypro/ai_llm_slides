from PIL import Image
import numpy as np
im = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_022.jpg').convert('RGB')).astype(int)
R, G, B = im[:,:,0], im[:,:,1], im[:,:,2]
lum = im.mean(axis=2)
dark = lum < 175

def runs_at(y, x0=160, x1=892, thr=175, minw=3):
    row = im[y, x0:x1].mean(axis=1)
    on = row < thr
    rr, s = [], None
    for i, v in enumerate(on):
        if v and s is None: s = i
        if not v and s is not None:
            if i-s >= minw: rr.append((s+x0, i-1+x0))
            s = None
    if s is not None: rr.append((s+x0, x1-1))
    return rr

# ROW 3: box top border rows ~272-273, bottom ~293-294
print("ROW3 y=272 dark runs:", runs_at(272))
print("ROW3 y=273 dark runs:", runs_at(273))
print("ROW3 y=293 dark runs:", runs_at(293))
print("ROW3 y=294 dark runs:", runs_at(294))
# ROW 1: box borders — find top/bottom border rows first
for y in range(122, 158):
    rr = runs_at(y, 170, 560, 175, 8)
    wide = [r for r in rr if r[1]-r[0] > 40]
    if wide: print(f"ROW1 y={y} wide dark runs:", wide)
