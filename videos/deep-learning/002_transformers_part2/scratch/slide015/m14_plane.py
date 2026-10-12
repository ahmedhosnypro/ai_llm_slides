from PIL import Image
import numpy as np
im = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_015.jpg').convert('RGB')).astype(int)
r,g,b = im[:,:,0], im[:,:,1], im[:,:,2]
# grayish + mid-light: the plane over panel/white
grayish = (np.abs(r-g)<14) & (np.abs(g-b)<14) & (r>175) & (r<222)
# restrict to x 70..520, y 50..260 (zone), exclude chrome border
m = np.zeros_like(grayish); m[52:255, 72:520] = grayish[52:255, 72:520]
ys, xs = np.where(m)
print('plane-over-empty px:', len(xs))
# per-row extents (every 10 rows)
for y in range(55, 256, 10):
    row = np.where(m[y])[0]
    if len(row) > 5:
        # longest run
        d = np.split(row, np.where(np.diff(row) > 6)[0]+1)
        seg = max(d, key=len)
        print(f'  y={y:3d}: x {seg.min():3d}..{seg.max():3d}  (n={len(row)})')
    else:
        print(f'  y={y:3d}: -')
