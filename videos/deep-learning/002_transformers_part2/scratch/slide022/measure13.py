from PIL import Image
import numpy as np
im = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_022.jpg').convert('RGB')).astype(int)

def runs_at(y, x0=160, x1=892, thr=200, minw=8):
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

print("ROW1 wide dark runs (thr200) y122..152:")
for y in range(122, 153):
    rr = [r for r in runs_at(y, 170, 892, 200, 8) if len(runs_at(y,170,892,200,8))>=0]
    rr = runs_at(y, 170, 892, 200, 8)
    wide = [r for r in rr if r[1]-r[0] > 35]
    if len(wide) >= 4: print(f"  y={y}:", wide)
print("ROW2 wide dark runs (thr200) y188..228:")
for y in range(188, 229):
    rr = runs_at(y, 170, 892, 200, 8)
    wide = [r for r in rr if r[1]-r[0] > 35]
    if len(wide) >= 4: print(f"  y={y}:", wide)
