from PIL import Image
import numpy as np
child = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_015.jpg').convert('RGB')).astype(int)
par   = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_043.jpg').convert('RGB')).astype(int)
d = np.abs(child - par)
print('mean abs diff per channel:', d.mean(axis=(0,1)))
ds = d.sum(axis=2)
print('mean sum diff:', ds.mean(), 'p50:', np.percentile(ds,50), 'p90:', np.percentile(ds,90), 'p99:', np.percentile(ds,99))
# sample a few known-same regions: card area centers
for (name, x0,x1,y0,y1) in [
    ('card h1 mid', 300, 500, 300, 440),
    ('similar pills row', 200, 700, 270, 300),
    ('white canvas top', 30, 930, 10, 40),
    ('gray panel edge', 50, 900, 470, 530),
]:
    reg = ds[y0:y1, x0:x1]
    print(f'{name:22s} mean={reg.mean():7.1f} p90={np.percentile(reg,90):6.0f}')
