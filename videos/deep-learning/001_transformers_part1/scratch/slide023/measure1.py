import numpy as np
from PIL import Image

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_023.jpg').convert('RGB')
a = np.asarray(im).astype(int)
H, W = a.shape[:2]

def mask_near(rgb, tol):
    d = np.abs(a - np.array(rgb)).sum(axis=2)
    return d <= tol

def comps(m, min_px=30):
    # simple connected components via scipy-free BFS on downsampled grid
    from collections import deque
    seen = np.zeros_like(m, dtype=bool)
    out = []
    ys, xs = np.nonzero(m)
    coords = set(zip(ys.tolist(), xs.tolist()))
    for y0, x0 in zip(ys.tolist(), xs.tolist()):
        if seen[y0, x0]:
            continue
        q = deque([(y0, x0)])
        seen[y0, x0] = True
        pts = []
        while q:
            y, x = q.popleft()
            pts.append((y, x))
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    ny, nx = y+dy, x+dx
                    if 0 <= ny < H and 0 <= nx < W and not seen[ny, nx] and m[ny, nx]:
                        seen[ny, nx] = True
                        q.append((ny, nx))
        if len(pts) >= min_px:
            py = [p[0] for p in pts]; px = [p[1] for p in pts]
            out.append((min(px), min(py), max(px), max(py), len(pts)))
    return sorted(out, key=lambda b: -b[4])

regions = {
 'yellow FFFFCC': ((255,255,204), 60),
 'cyan CCFFFF': ((204,255,255), 60),
 'pink FFCCCC': ((255,204,204), 60),
 'red CC0000': ((204,0,0), 90),
 'blue 0000CC': ((0,0,204), 90),
 'green 009900': ((0,153,0), 90),
}
for name,(rgb,tol) in regions.items():
    m = mask_near(rgb, tol)
    cc = comps(m, min_px=80)
    print(f'== {name}: total px={m.sum()}')
    for b in cc[:14]:
        print(f'   bbox x{b[0]}..{b[2]} y{b[1]}..{b[3]}  w={b[2]-b[0]+1} h={b[3]-b[1]+1} px={b[4]}')
