# m6: precise badge scanline + iterative masked affine fit (exclude delta px).
from PIL import Image
import numpy as np

myI = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_019.jpg').convert('RGB')
parI = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_019.jpg').convert('RGB')
my = np.asarray(myI).astype(np.float32)

# --- precise badge ring: purple stroke profile along row/col through center
a_ = my.astype(int)
r, g, b = a_[...,0], a_[...,1], a_[...,2]
purple = (b > r + 30) & (b > g + 40) & (b > 120) & (r > 60) & (r < 190)
seg = purple[50:95, 860:895]
ys, xs = np.where(seg)
print('purple rows hist:', {int(y+50): int((ys==y).sum()) for y in sorted(set(ys))})
print('purple cols hist:', {int(x+860): int((xs==x).sum()) for x in sorted(set(xs))})
cy_ring = ys.mean() + 50; cx_ring = xs.mean() + 860
print(f'ring centroid ({cx_ring:.1f},{cy_ring:.1f}); extremes x {xs.min()+860}..{xs.max()+860} y {ys.min()+50}..{ys.max()+50}')

def warp(a, b, c, d):
    coeffs = (1.0/b, 0.0, -a/b, 0.0, 1.0/d, -c/d)
    return np.asarray(parI.transform((960, 540), Image.AFFINE, coeffs, resample=Image.BILINEAR)).astype(np.float32)

# fit on non-delta pixels only; keep landmarks as soft anchors
def fit(a, b, c, d, iters=3):
    for it in range(iters):
        w = warp(a, b, c, d)
        dd = np.abs(my - w).sum(axis=2)
        mask = np.zeros(dd.shape, bool)
        mask[46:514, 60:900] = True
        mask &= dd < 120          # exclude delta + halo pixels
        ys, xs = np.where(mask)
        # subsample for speed
        sel = np.random.RandomState(0).choice(len(xs), 40000, replace=False)
        xs, ys = xs[sel], ys[sel]
        # model: fx = a + b*sx ; fy = c + d*sy ; sx,sy = inverse-mapped frame px
        sx = (xs - a) / b; sy = (ys - c) / d
        # solve for (a,b) and (c,d) by least squares on residual alignment:
        # minimize over small adjustments using scipy-free normal equations on
        # gradient-weighted SSD is complex; use local shift field instead:
        from scipy import ndimage  # may not exist; fallback below
        return a, b, c, d
    return a, b, c, d

# scipy may be missing -> do a direct parameter search on masked SSD
def masked_score(a, b, c, d, mask):
    w = warp(a, b, c, d)
    dd = np.abs(my - w).sum(axis=2)
    return dd[mask].mean()

mask = np.zeros((540, 960), bool)
mask[46:514, 60:900] = True

best = (1e9, (17.9473, 0.96129, 0.2031, 0.95676))
# iterate: fit, exclude outliers, refit
a, b, c, d = best[1]
for it in range(4):
    w = warp(a, b, c, d)
    dd = np.abs(my - w).sum(axis=2)
    m2 = mask & (dd < (150 if it == 0 else 90))
    loc = (1e9, None)
    for bb in np.arange(b-0.002, b+0.0021, 0.0005):
        for aa in np.arange(a-1.5, a+1.51, 0.5):
            for ddd in np.arange(d-0.002, d+0.0021, 0.0005):
                for cc in np.arange(c-1.5, c+1.51, 0.5):
                    s = masked_score(aa, bb, cc, ddd, m2)
                    if s < loc[0]: loc = (s, (aa, bb, cc, ddd))
    # refine around loc
    a0, b0, c0, d0 = loc[1]
    for bb in np.arange(b0-0.0005, b0+0.00055, 0.00025):
        for aa in np.arange(a0-0.5, a0+0.51, 0.25):
            for ddd in np.arange(d0-0.0005, d0+0.00055, 0.00025):
                for cc in np.arange(c0-0.5, c0+0.51, 0.25):
                    s = masked_score(aa, bb, cc, ddd, m2)
                    if s < loc[0]: loc = (s, (aa, bb, cc, ddd))
    a, b, c, d = loc[1]
    print(f'iter{it}: masked-SSD {loc[0]:.3f} a={a:.3f} b={b:.5f} c={c:.3f} d={d:.5f} '
          f'| landmarks->frame L {a+b*42:.2f} R {a+b*919:.2f} T {c+d*45:.2f} B {c+d*540:.2f}')
print('FINAL:', a, b, c, d)
print(f'badge (893,71) -> frame ({a+b*893:.1f},{c+d*71:.1f}); measured ring ({cx_ring:.1f},{cy_ring:.1f})')
np.save('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide019/affine.npy', np.array([a,b,c,d]))
