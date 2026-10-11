from PIL import Image
import numpy as np
im = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_023.jpg').convert('RGB')).astype(int)
r, g, b = im[:,:,0], im[:,:,1], im[:,:,2]
X0, X1 = 62, 899
redm  = (r>120)&(r-g>45)&(r-b>45)
bluem = (b-r>45)&(b-g>35)&(b>120)
black = (r<120)&(g<120)&(b<120)

def strokes(mask, y0, y1, minlen, name):
    m = mask[y0:y1+1, :].copy()
    m[:, :X0]=False; m[:, X1:]=False
    h = y1-y0+1
    cp = m.sum(axis=0)
    cols = [i for i in range(X0, X1) if cp[i] >= minlen]
    groups=[]
    for c in cols:
        if groups and c-groups[-1][-1] <= 2: groups[-1].append(c)
        else: groups.append([c])
    print(f"{name}: {[(g_[0], g_[-1]) for g_ in groups]}")

# box borders: strokes spanning most of box height (~20px)
strokes(redm, 114, 158, 12, "ROW1 red strokes")
strokes(bluem, 186, 227, 12, "ROW2 blue strokes")
strokes(redm, 261, 305, 12, "ROW3 red strokes")
strokes(black, 114, 158, 8, "ROW1 black strokes (container dashes)")
