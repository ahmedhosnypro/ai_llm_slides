from PIL import Image
import numpy as np
from collections import Counter

im = Image.open("videos/deep-learning/001_introduction/unique_slides/slide_031.jpg").convert("RGB")
a = np.asarray(im).astype(int)

def modal_dark(x0,x1,y0,y1,maxsum,label):
    band = a[y0:y1, x0:x1].reshape(-1,3)
    sel = band[band.sum(axis=1) < maxsum]
    c = Counter(map(tuple, sel))
    print(f"{label}: n={len(sel)} top modal:", c.most_common(5))

# blue body text strokes (interior of glyphs)
modal_dark(109, 760, 142, 161, 240, "L1 blue text")
modal_dark(109, 240, 195, 212, 240, "L2 blue text")
modal_dark(108, 760, 220, 243, 240, "L3a blue text")
modal_dark(388, 597, 445, 465, 240, "label blue text")
# reds
modal_dark(152, 470, 302, 324, 330, "bullet1 red text")
modal_dark(136, 151, 302, 319, 330, "bullet dot")
modal_dark(180, 779, 87, 121, 330, "title red")
# borders (rows fully across)
modal_dark(100, 880, 133, 135, 700, "content box top border")
modal_dark(98, 101, 140, 360, 700, "content box left border")
modal_dark(378, 380, 437, 474, 700, "label box left border")
modal_dark(625, 627, 390, 500, 700, "matrix left border")
# matrix glyphs
modal_dark(648, 820, 400, 492, 300, "matrix glyph black")
