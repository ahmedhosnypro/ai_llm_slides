from PIL import Image
import numpy as np
im = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_023.jpg').convert('RGB')).astype(int)
r, g, b = im[:,:,0], im[:,:,1], im[:,:,2]

def region_report(y0, y1, name):
    sub = slice(y0, y1+1)
    ink = (abs(r[sub]-233) + abs(g[sub]-233) + abs(b[sub]-231)) > 60
    rows = np.where(ink.any(axis=1))[0]
    cols = np.where(ink.any(axis=0))[0]
    print(f"== {name}: y {y0+rows.min()}..{y0+rows.max()}  x {cols.min()}..{cols.max()}")
    # column profile: find box borders (vertical strokes)
    cp = ink.sum(axis=0)
    strokes = [i for i in range(len(cp)) if cp[i] >= (rows.max()-rows.min())*0.5]
    # group consecutive
    groups = []
    for s in strokes:
        if groups and s - groups[-1][-1] <= 1: groups[-1].append(s)
        else: groups.append([s])
    print("   vertical strokes (col groups):", [(g_[0], g_[-1]) for g_ in groups])

region_report(108, 165, "ROW1 words strip")
region_report(180, 235, "ROW2 pos strip")
region_report(255, 312, "ROW3 index strip")
