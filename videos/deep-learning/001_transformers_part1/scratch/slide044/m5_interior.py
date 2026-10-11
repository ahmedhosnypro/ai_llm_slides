from PIL import Image
import numpy as np
im = np.asarray(Image.open("unique_slides/slide_044.jpg").convert("RGB"), dtype=np.int16)
R,G,B = im[...,0], im[...,1], im[...,2]
L = np.asarray(Image.open("unique_slides/slide_044.jpg").convert("L"))
purple = (R > 120) & (R < 210) & (B > 170) & (B - G > 25) & (R - G > 10)
# panel interior
x0,x1,y0,y1 = 742, 904, 84, 294
sub_p = purple[y0:y1, x0:x1]
sub_d = L[y0:y1, x0:x1] < 130   # dark ink
sub_m = (np.abs(R-G)<25)&(np.abs(G-B)<25)&(L<200)  # mid-gray box borders
# print a 2px-row summary: purple count, dark count, gray-border count
for yy in range(0, y1-y0, 3):
    band_p = sub_p[yy:yy+3].sum()
    band_d = sub_d[yy:yy+3].sum()
    band_m = sub_m[yy:yy+3].sum()
    if band_p or band_d or band_m > 30:
        print(f"y {y0+yy:3d}: purple {band_p:4d} dark {band_d:4d} gray {band_m:4d}")
