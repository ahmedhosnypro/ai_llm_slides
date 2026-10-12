from PIL import Image
import numpy as np
im = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_022.jpg').convert('RGB')).astype(int)
H, W, _ = im.shape
# For each row 60..519: classify mean color of x in [170, 890] (right of left labels)
print("row-band scan (y: mean RGB of x[170,890], n non-gray):")
prev = None
for y in range(58, 519):
    seg = im[y, 170:890]
    r, g, b = seg[:,0], seg[:,1], seg[:,2]
    # non-neutral = saturation-ish
    sat = np.abs(r-g) + np.abs(g-b) + np.abs(r-b)
    ns = (sat > 24).mean()
    mean = seg.mean(axis=0).astype(int)
    key = (round(mean[0]/8), round(mean[1]/8), round(mean[2]/8), round(ns,2))
    if key != prev:
        print(f"  y={y:3d} mean=({mean[0]},{mean[1]},{mean[2]}) satfrac={ns:.2f}")
        prev = key
