from PIL import Image
import numpy as np

child = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_015.jpg').convert('RGB')).astype(int)
par   = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_043.jpg').convert('RGB')).astype(int)

# parent-measured card colors and spec colors for child — probe both
targets = {
 'h1 salmon': [(0xEF,0x8C,0x96),(0xF0,0x80,0x80),(0xEE,0x8A,0x8A)],
 'h2 lavender': [(0xC5,0xC1,0xF4),(0xC9,0xA8,0xD8)],
 'h3 yellow': [(0xF8,0xFF,0x9A),(0xED,0xE8,0x7F)],
 'h4 green': [(0xD4,0xFF,0xE5),(0xC8,0xE6,0xB8)],
 'h5 peach': [(0xF7,0xE2,0xCD),(0xF5,0xCE,0x9A)],
}
def bbox(img, colors, tol):
    m = np.zeros(img.shape[:2], bool)
    for c in colors:
        m |= (np.abs(img - np.array(c)).sum(axis=2) < tol)
    if not m.any(): return None, 0
    ys, xs = np.where(m)
    return (xs.min(), xs.max(), ys.min(), ys.max()), m.sum()

for name, cols in targets.items():
    for tol in (30, 60):
        bb_c, n_c = bbox(child, cols, tol)
        bb_p, n_p = bbox(par, cols, tol)
        print(f'{name:11s} tol={tol:3d} CHILD bbox={bb_c} n={n_c:6d}   PARENT bbox={bb_p} n={n_p:6d}')
    print()
