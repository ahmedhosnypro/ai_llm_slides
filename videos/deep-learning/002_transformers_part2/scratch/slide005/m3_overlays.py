# m3 (slide005): classify translucent overlay pixels (yellow ~45% / orange ~50% over
# the warped 001:19 reference), find their connected components -> band rectangles
# in build pt. Also isolate my dashed red arrows (C00000 dashes not present in warp).
from PIL import Image
import numpy as np
from collections import deque

A, Bx, C, D = 20.9473, 0.95679, 2.2031, 0.95651

def to_build(fx, fy):
    return (fx - 18.0787) / 0.961084, (fy - 0.4700) / 0.957187

myI = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_005.jpg').convert('RGB')
wI = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide005/warped_001_f21.png')
my = np.asarray(myI).astype(np.float32)
w = np.asarray(wI).astype(np.float32)

YELLOW = np.array([255, 255, 0], np.float32)
ORANGE = np.array([237, 125, 49], np.float32)

def blend_mask(tint, alpha, tol):
    exp = alpha * tint + (1 - alpha) * w
    d = np.abs(my - exp).max(axis=2)
    return d < tol

ymask = blend_mask(YELLOW, 0.45, 42)
omask = blend_mask(ORANGE, 0.50, 42)
ymask |= blend_mask(YELLOW, 0.55, 42)
omask |= blend_mask(ORANGE, 0.60, 42)

# restrict to panel interior
inner = np.zeros(ymask.shape, bool); inner[50:512, 64:896] = True
ymask &= inner; omask &= inner

def components(mask, minpx):
    lab = np.zeros(mask.shape, np.int32); nid = 0; comps = []
    H, W = mask.shape
    for y in range(H):
        xs = np.where(mask[y] & (lab[y] == 0))[0]
        for x in xs:
            if lab[y, x]: continue
            nid += 1; q = deque([(y, x)]); lab[y, x] = nid; pts = []
            while q:
                cy, cx = q.popleft(); pts.append((cy, cx))
                for dy in (-2, -1, 0, 1, 2):
                    for dx in (-2, -1, 0, 1, 2):
                        ny, nx = cy+dy, cx+dx
                        if 0 <= ny < H and 0 <= nx < W and mask[ny, nx] and lab[ny, nx] == 0:
                            lab[ny, nx] = nid; q.append((ny, nx))
            comps.append(pts)
    return [p for p in comps if len(p) >= minpx]

print('== YELLOW overlay components (>=300px) ==')
for pts in sorted(components(ymask, 300), key=len, reverse=True):
    ys = [p[0] for p in pts]; xs = [p[1] for p in pts]
    y0, y1, x0, x1 = min(ys), max(ys), min(xs), max(xs)
    bx0, by0 = to_build(x0, y0); bx1, by1 = to_build(x1, y1)
    print(f'  {len(pts):6d}px frame x{x0}..{x1} y{y0}..{y1}  build x{bx0:.1f}..{bx1:.1f} y{by0:.1f}..{by1:.1f}')

print('== ORANGE overlay components (>=300px) ==')
for pts in sorted(components(omask, 300), key=len, reverse=True):
    ys = [p[0] for p in pts]; xs = [p[1] for p in pts]
    y0, y1, x0, x1 = min(ys), max(ys), min(xs), max(xs)
    bx0, by0 = to_build(x0, y0); bx1, by1 = to_build(x1, y1)
    print(f'  {len(pts):6d}px frame x{x0}..{x1} y{y0}..{y1}  build x{bx0:.1f}..{bx1:.1f} y{by0:.1f}..{by1:.1f}')

# --- dashed red arrows: C00000-ish red in my frame NOT matched by warp red ---
redm = (my[..., 0] > 120) & (my[..., 0] - my[..., 1] > 55) & (my[..., 0] - my[..., 2] > 45)
wred = (w[..., 0] > 120) & (w[..., 0] - w[..., 1] > 55) & (w[..., 0] - w[..., 2] > 45)
# dilate wred by 2 so near-matching dashes don't count
wd = wred.copy()
for s in (1, 2):
    wd[s:, :] |= wred[:-s, :]; wd[:-s, :] |= wred[s:, :]
    wd[:, s:] |= wred[:, :-s]; wd[:, :-s] |= wred[:, s:]
arrow = redm & ~wd & inner
print('== RED dash pixels not in warp (>=40px comps) ==')
for pts in sorted(components(arrow, 40), key=len, reverse=True)[:20]:
    ys = [p[0] for p in pts]; xs = [p[1] for p in pts]
    y0, y1, x0, x1 = min(ys), max(ys), min(xs), max(xs)
    bx0, by0 = to_build(x0, y0); bx1, by1 = to_build(x1, y1)
    cols = np.array([my[p] for p in pts]).mean(axis=0)
    print(f'  {len(pts):5d}px frame x{x0}..{x1} y{y0}..{y1}  build x{bx0:.1f}..{bx1:.1f} y{by0:.1f}..{by1:.1f}  mean {tuple(int(v) for v in cols)}')

np.save('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide005/ymask.npy', ymask)
np.save('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide005/omask.npy', omask)
