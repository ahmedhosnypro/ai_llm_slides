from PIL import Image
import numpy as np
im = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_023.jpg').convert('RGB')).astype(int)
r, g, b = im[:,:,0], im[:,:,1], im[:,:,2]

def col_strokes(y0, y1, maskfn, minfrac, name):
    m = maskfn(r[y0:y1+1], g[y0:y1+1], b[y0:y1+1])
    h = y1-y0+1
    cp = m.sum(axis=0)
    cols = [x for x in range(150, 899) if cp[x] >= minfrac*h]
    groups=[]
    for c in cols:
        if groups and c-groups[-1][-1] <= 3: groups[-1].append(c)
        else: groups.append([c])
    print(f"{name} band y{y0}..{y1}: strokes:", [(g_[0],g_[-1]) for g_ in groups])
    return groups

# ROW1: weak red border, strong red text. Border = R-G>14, R>195
f1 = lambda R,G,B: (R-G>14)&(R-B>14)&(R>195)
g1 = col_strokes(126, 148, f1, 0.55, "ROW1 box borders")
# ROW2: blue borders
f2 = lambda R,G,B: (B-R>35)&(B>150)
g2 = col_strokes(188, 218, f2, 0.55, "ROW2 box borders")
# ROW3: strong red
f3 = lambda R,G,B: (R-G>35)&(R-B>35)&(R>120)
g3 = col_strokes(262, 300, f3, 0.55, "ROW3 box borders")

# box vertical extents: for ROW1 box1 (x 173..234) find rows where border color present at left edge col
def rowext(x0, x1, maskfn, y0, y1, name):
    m = maskfn(r[y0:y1+1, x0:x1+1], g[y0:y1+1, x0:x1+1], b[y0:y1+1, x0:x1+1])
    rp = m.sum(axis=1)
    rows = [y0+i for i,v in enumerate(rp) if v >= (x1-x0+1)*0.5]
    print(f"{name}: full-width border rows {rows}")

rowext(180, 228, f1, 118, 160, "ROW1 box1 top/bottom")
rowext(186, 236, f2, 182, 232, "ROW2 box1 top/bottom")
rowext(200, 240, f3, 256, 312, "ROW3 box1 top/bottom")
