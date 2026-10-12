from PIL import Image
import numpy as np
im = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_022.jpg').convert('RGB')).astype(int)
H, W, _ = im.shape
R, G, B = im[:,:,0], im[:,:,1], im[:,:,2]

# 1. solid navy rule y=111: x extent
row = im[111, :, :].mean(axis=1)
xs = np.where(row < 160)[0]
print("navy rule y=111 x extent:", xs.min(), xs.max(), "count", len(xs))
print("navy rule color sample:", im[111, 400], im[111, 700])

# 2. vertical dark lines: dark fraction per column over y-bands
def vlines(y0, y1, label, thr=160):
    lum = im[y0:y1, :, :].mean(axis=2)
    frac = (lum < thr).mean(axis=0)
    cols = [x for x in range(45, 915) if frac[x] > 0.5]
    print(f"{label} y[{y0},{y1}] vertical dark cols:", cols)
vlines(120, 155, "band row1")
vlines(160, 185, "band gap12")
vlines(190, 260, "band row2")
vlines(265, 330, "band row3")

# 3. all horizontal lines y 200..520 (solid or dashed)
print("\nhorizontal line rows y 200..518 (darkfrac over x[170,880] > 0.3):")
for y in range(200, 518):
    lum = im[y, 170:880].mean(axis=1)
    frac = (lum < 160).mean()
    if frac > 0.3:
        print(f"  y={y}: darkfrac={frac:.2f} meanLum={lum.mean():.0f}")
