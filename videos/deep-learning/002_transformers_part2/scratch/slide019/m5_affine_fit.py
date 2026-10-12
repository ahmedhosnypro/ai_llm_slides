# m5: grid-search the frame->slide affine (a,b,c,d) minimizing SSD between MY frame
# and 001's frame warped forward, over the panel interior. Coarse then fine.
from PIL import Image
import numpy as np

myI = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_019.jpg').convert('RGB')
parI = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_019.jpg').convert('RGB')
my = np.asarray(myI).astype(np.float32)

def score(a, b, c, d):
    coeffs = (1.0/b, 0.0, -a/b, 0.0, 1.0/d, -c/d)
    w = np.asarray(parI.transform((960, 540), Image.AFFINE, coeffs, resample=Image.BILINEAR)).astype(np.float32)
    dd = np.abs(my - w).sum(axis=2)[46:514, 60:900]
    return dd.mean()

best = (1e9, None)
for b in [0.9595, 0.9605, 0.9613, 0.9621, 0.9629]:
    for a in [16.5, 17.5, 17.95, 18.5, 19.5]:
        for d in [0.9525, 0.9540, 0.9556, 0.9568, 0.9580]:
            for c in [-1.0, 0.0, 1.0, 2.0]:
                s = score(a, b, c, d)
                if s < best[0]:
                    best = (s, (a, b, c, d))
print('coarse best:', best)
a0, b0, c0, d0 = best[1]
for b in np.arange(b0-0.0012, b0+0.0013, 0.0004):
    for a in np.arange(a0-1.0, a0+1.01, 0.5):
        for d in np.arange(d0-0.0022, d0+0.0023, 0.0008):
            for c in np.arange(c0-1.0, c0+1.01, 0.5):
                s = score(a, b, c, d)
                if s < best[0]:
                    best = (s, (a, b, c, d))
print('fine best:', best)
a0, b0, c0, d0 = best[1]
for b in np.arange(b0-0.0004, b0+0.00045, 0.0002):
    for a in np.arange(a0-0.5, a0+0.51, 0.25):
        for d in np.arange(d0-0.0008, d0+0.00085, 0.0004):
            for c in np.arange(c0-0.5, c0+0.51, 0.25):
                s = score(a, b, c, d)
                if s < best[0]:
                    best = (s, (a, b, c, d))
print('finest best:', best)
a, b, c, d = best[1]
print(f'FINAL: frame_x = {a:.4f} + {b:.5f}*slide_x ; frame_y = {c:.4f} + {d:.5f}*slide_y')
print(f'landmarks->frame: L {a+b*42:.2f} R {a+b*919:.2f} T {c+d*45:.2f} B {c+d*540:.2f}')
print(f'badge (893,71) -> frame ({a+b*893:.1f},{c+d*71:.1f})  [measured ring center 875.5,71.0]')
np.save('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide019/affine.npy', np.array([a,b,c,d]))
