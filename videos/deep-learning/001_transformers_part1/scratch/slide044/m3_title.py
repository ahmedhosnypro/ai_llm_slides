from PIL import Image
import numpy as np
for name in ["slide_043","slide_044"]:
    im = np.asarray(Image.open(f"unique_slides/{name}.jpg").convert("L"))
    # dark ink in the top-right zone
    z = im[40:115, 380:960]
    dark = z < 120
    # row profile
    rows = dark.sum(axis=1)
    print(f"== {name} row profile (y40..115, x380..960) ==")
    y = 40
    for r in rows:
        if r > 0: print(y, int(r))
        y += 1
