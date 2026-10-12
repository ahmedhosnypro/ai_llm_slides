from PIL import Image
import numpy as np
im = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_022.jpg').convert('RGB')).astype(int)

# single-row dark fraction across x[170,880]
print("single-row dark fraction x[170,880], y 104..210:")
for y in range(104, 211):
    lum = im[y, 170:880].mean(axis=1)
    frac = (lum < 160).mean()
    if frac > 0.30:
        print(f"  y={y}: darkfrac={frac:.2f}  meanLum={lum.mean():.0f}")
print()
# dash check on candidate lines: runs of dark columns in the single row
def runs_row(y, x0=170, x1=880, thr=160):
    lum = im[y, x0:x1].mean(axis=1)
    on = lum < thr
    rr, s = [], None
    for i, v in enumerate(on):
        if v and s is None: s = i
        if not v and s is not None: rr.append((s+x0, i-1+x0)); s = None
    if s is not None: rr.append((s+x0, x1-1))
    return rr
for y in [111, 119, 157, 187, 188, 190, 192, 194]:
    rr = runs_row(y)
    print(f"y={y}: {len(rr)} runs", rr[:14])
