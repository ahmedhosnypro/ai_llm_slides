# f3: iterative masked affine fit: frame(002:37) <- frame(001:19), delta regions masked.
# Adapted from certified 002:19 methodology (scratch/slide019/m6_iterfit.py).
from PIL import Image
import numpy as np

myI = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_037.jpg').convert('RGB')
parI = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_019.jpg').convert('RGB')
my = np.asarray(myI).astype(np.float32)

def warp(a, b, c, d):
    coeffs = (1.0/b, 0.0, -a/b, 0.0, 1.0/d, -c/d)
    return np.asarray(parI.transform((960, 540), Image.AFFINE, coeffs, resample=Image.BILINEAR)).astype(np.float32)

base = np.zeros((540, 960), bool)
base[46:514, 60:900] = True
# delta masks (my-frame px): title band, badge numeral, pin/disc/dashed-stack box
delta = np.zeros((540, 960), bool)
delta[40:100, 55:835] = True     # title band (different text) incl. badge numeral zone x850+ separately
delta[40:100, 845:915] = True    # badge numeral 37 vs 19
delta[115:410, 555:785] = True   # pin + red disc + red dashed stack box + funnel convergence zone
mask = base & ~delta

def masked_score(a, b, c, d):
    w = warp(a, b, c, d)
    dd = np.abs(my - w).sum(axis=2)
    return dd[mask].mean()

best = (1e9, (20.4, 0.9576, 2.5, 0.9562))
a, b, c, d = best[1]
for it in range(4):
    w = warp(a, b, c, d)
    dd = np.abs(my - w).sum(axis=2)
    m2 = mask & (dd < (170 if it == 0 else 100))
    loc = (1e9, None)
    for bb in np.arange(b-0.002, b+0.0021, 0.0005):
        for aa in np.arange(a-1.5, a+1.51, 0.5):
            for ddd in np.arange(d-0.002, d+0.0021, 0.0005):
                for cc in np.arange(c-1.5, c+1.51, 0.5):
                    s = masked_score(aa, bb, cc, ddd) if False else None
            # vectorized inner replaced below
    # do the 4D search with a smaller grid first
    for bb in np.arange(b-0.0015, b+0.0016, 0.0005):
        for aa in np.arange(a-1.0, a+1.01, 0.5):
            for ddd in np.arange(d-0.0015, d+0.0016, 0.0005):
                for cc in np.arange(c-1.0, c+1.01, 0.5):
                    s = masked_score(aa, bb, cc, ddd)
                    if s < loc[0]: loc = (s, (aa, bb, cc, ddd))
    a0, b0, c0, d0 = loc[1]
    for bb in np.arange(b0-0.0005, b0+0.00055, 0.00025):
        for aa in np.arange(a0-0.5, a0+0.51, 0.25):
            for ddd in np.arange(d0-0.0005, d0+0.00055, 0.00025):
                for cc in np.arange(c0-0.5, c0+0.51, 0.25):
                    s = masked_score(aa, bb, cc, ddd)
                    if s < loc[0]: loc = (s, (aa, bb, cc, ddd))
    a, b, c, d = loc[1]
    print(f'iter{it}: masked-SSD {loc[0]:.3f} a={a:.4f} b={b:.5f} c={c:.4f} d={d:.5f} '
          f'| L {a+b*38.95:.2f} R {a+b*920.09:.2f} T {c+d*43.10:.2f} B {c+d*538.09:.2f}')

print('FINAL f37:', a, b, c, d)
print(f'landmarks->frame: L {a+b*38.95:.2f} (meas 57.7) R {a+b*920.09:.2f} (meas 901.5) '
      f'T {c+d*43.10:.2f} (meas 43.7) B {c+d*538.09:.2f} (meas ~517.0)')
print(f'badge (893,71) build -> frame ({a+b*893+ (20.9473-893*0.95679)*0:.1f}...)')  # placeholder
# composite to BUILD pt using 001's certified frame->build mapping (002:19 m9 constants):
B1, A1, D1, C1 = 1.004491, -2.998, 1.000708, -1.812
def to_build(fx, fy):
    f1x = (fx - a)/b; f1y = (fy - c)/d
    return (f1x - A1)/B1, (f1y - C1)/D1
for lbl, (fx, fy) in {'arch_frame_TL': (568, 102), 'arch_frame_BR': (877, 503),
                      'insetA_TL': (78, 260), 'insetA_BR': (202, 471),
                      'insetB_TL': (308, 238), 'insetB_BR': (507, 493)}.items():
    bx, by = to_build(fx, fy)
    print(f'{lbl}: frame({fx},{fy}) -> build ({bx:.1f},{by:.1f})')
np.save('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide037/f37_affine.npy', np.array([a, b, c, d]))
