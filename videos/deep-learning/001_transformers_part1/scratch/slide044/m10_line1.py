from PIL import Image
import numpy as np
for name in ["slide_043","slide_044"]:
    L = np.asarray(Image.open(f"unique_slides/{name}.jpg").convert("L"))
    m = (L<120)[50:78, 480:920]
    ys,xs = np.where(m)
    print(name, "line1 ink (x480+):", (480+xs.min(), 480+xs.max()), "y", (50+ys.min(), 50+ys.max()), "n=",len(xs))
    # column profile coarse: where are the gaps (word boundaries)?
    colc = (L<120)[50:78, 480:920].sum(axis=0)
    prof = "".join("#" if c>2 else ("." if c>0 else " ") for c in colc)
    print("  ", prof)
