from PIL import Image
import numpy as np
F = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_017.jpg").convert("RGB")
a = np.asarray(F).astype(int)
# find distinct-color runs per scanline in the chip zone
def rle(y, x0, x1, tol=26):
    out=[]; start=x0; ref=a[y,x0].copy()
    for x in range(x0,x1):
        if np.abs(a[y,x]-ref).sum() > tol:
            out.append((start, x-1, tuple(ref)))
            start=x; ref=a[y,x].copy()
        else:
            ref = 0.9*ref + 0.1*a[y,x]  # slow drift
    out.append((start, x1-1, tuple(ref)))
    return [(s,e,tuple(int(v) for v in t)) for s,e,t in out if e-s>=4]
for y in [186, 205, 222, 240, 258, 276, 294]:
    print("y=%d:" % y)
    for s,e,c in rle(y, 380, 700):
        print("   x %3d..%3d rgb(%3d,%3d,%3d)" % (s,e,*c))
