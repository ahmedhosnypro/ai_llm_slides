from PIL import Image
import numpy as np
im = np.asarray(Image.open("unique_slides/slide_044.jpg").convert("RGB"), dtype=np.int16)
R,G,B = im[...,0], im[...,1], im[...,2]
# saturated green border pixels: green dominant, dark-ish
green = (G > 110) & (G - R > 50) & (G - B > 50)
ys, xs = np.where(green)
print("green px:", len(xs), "bbox x", xs.min(), xs.max(), "y", ys.min(), ys.max())
# cluster: the inset border should be a rectangle. Print histogram of green by column (x>600)
for x0,x1,y0,y1,label in [(600,960,40,420,"right zone")]:
    sub = green[y0:y1, x0:x1]
    cols = sub.sum(axis=0); rows = sub.sum(axis=1)
    cnz = np.where(cols > 20)[0]; rnz = np.where(rows > 20)[0]
    print(label, "border cols:", (x0+cnz.min(), x0+cnz.max()) if len(cnz) else None)
    print(label, "border rows:", (y0+rnz.min(), y0+rnz.max()) if len(rnz) else None)
    # print column profile edges
    print("  col profile sample:", [(x0+int(i), int(cols[i])) for i in cnz[:8]], "...", [(x0+int(i), int(cols[i])) for i in cnz[-8:]])
    print("  row profile sample:", [(y0+int(i), int(rows[i])) for i in rnz[:8]], "...", [(y0+int(i), int(rows[i])) for i in rnz[-8:]])
