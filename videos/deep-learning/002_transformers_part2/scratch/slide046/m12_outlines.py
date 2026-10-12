from PIL import Image
import numpy as np
for fname, y0, y1 in [('045', 168, 183), ('046', 66, 80)]:
    a = np.asarray(Image.open(f'videos/deep-learning/002_transformers_part2/unique_slides/slide_{fname}.jpg').convert('RGB')).astype(int)
    seg = a[y0:y1]
    lum = seg.mean(axis=2)
    dark = (lum < 200).sum(axis=0)   # count of dark px per column across the band
    # find local runs of columns with >=8 dark px
    cols = np.where(dark >= 8)[0]
    # group consecutive
    groups = []
    for c in cols:
        if groups and c - groups[-1][-1] <= 1: groups[-1].append(c)
        else: groups.append([c])
    centers = [sum(g)/len(g) for g in groups]
    print(f'{fname} top-row dark vertical lines:', [round(c,1) for c in centers])
    print(f'  -> slide x:', [round((c-17.582)/0.962329,1) for c in centers])
