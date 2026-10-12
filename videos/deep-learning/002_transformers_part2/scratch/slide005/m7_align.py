# m7 (slide005): local alignment between my frame and warped render_5.
# Brute-force (dx,dy) correlation over several patches -> per-region shift.
# Then scan the inset bottom-circle rows in both images (colored blob centers).
from PIL import Image
import numpy as np

myI = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_005.jpg').convert('RGB')
rwI = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide005/warped_render5.png')
my = np.asarray(myI).astype(np.float32)
rw = np.asarray(rwI).astype(np.float32)

def best_shift(x0, y0, x1, y1, rng=6):
    """find (dx,dy) minimizing SSD of my vs rw shifted"""
    best = None
    for dy in range(-rng, rng + 1):
        for dx in range(-rng, rng + 1):
            a = my[y0:y1, x0:x1]
            b = rw[y0+dy:y1+dy, x0+dx:x1+dx]
            if a.shape != b.shape or a.size == 0:
                continue
            s = np.abs(a - b).mean()
            if best is None or s < best[0]:
                best = (s, dx, dy)
    return best

# patches: (name, x0,y0,x1,y1) in FRAME px
patches = [
    ('title', 220, 56, 520, 85),
    ('left_inset_frame', 75, 250, 215, 475),
    ('center_inset_frame', 310, 235, 505, 495),
    ('center_circles', 320, 465, 500, 495),
    ('arch_enc_top', 590, 100, 700, 200),
    ('arch_dec_mid', 730, 260, 830, 380),
    ('callout1_border', 85, 98, 500, 145),
]
for name, x0, y0, x1, y1 in patches:
    s, dx, dy = best_shift(x0, y0, x1, y1)
    print(f'{name:20s} best shift dx={dx:+d} dy={dy:+d}  SSD {s:.1f}')

# circle scan: bottom rows of center inset (frame y460..500, x300..510)
def blobs(img, x0, x1, y0, y1, pred, minpx=8):
    reg = img[y0:y1, x0:x1]
    m = pred(reg)
    cols = {}
    ys, xs = np.where(m)
    for yy, xx in zip(ys, xs):
        cols.setdefault(xx + x0, []).append(yy + y0)
    # cluster columns
    runs = []
    cur = []
    last = None
    for x in sorted(cols):
        if last is not None and x - last > 3:
            runs.append(cur); cur = []
        cur.append(x); last = x
    if cur: runs.append(cur)
    out = []
    for run in runs:
        if len(run) * 3 < minpx: continue
        px = [p for x in run for p in cols[x]]
        out.append((run[0], run[-1], min(px), max(px), len(px)))
    return out

nonwhite = lambda r: (np.abs(r - np.array([250, 250, 248])).sum(axis=2) > 150) & (r.sum(axis=2) < 600)
print('== center inset bottom (frame x300-510, y455-505): colored blobs ==')
print('  MY  :', blobs(my, 300, 510, 455, 505, nonwhite))
print('  REND:', blobs(rw, 300, 510, 455, 505, nonwhite))
print('== left inset bottom (frame x80-220, y420-480) ==')
print('  MY  :', blobs(my, 80, 220, 420, 480, nonwhite))
print('  REND:', blobs(rw, 80, 220, 420, 480, nonwhite))
