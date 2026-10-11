from PIL import Image
import numpy as np
a = np.asarray(Image.open("unique_slides/slide_043.jpg").convert("RGB"), dtype=np.int16)
b = np.asarray(Image.open("unique_slides/slide_044.jpg").convert("RGB"), dtype=np.int16)
d = np.abs(a-b).max(axis=2)
mask = d > 30

def region(name, x0,x1,y0,y1):
    m = mask[y0:y1, x0:x1]
    if m.sum()==0:
        print(f"{name}: no delta"); return
    ys,xs = np.where(m)
    print(f"{name}: {m.sum()} px, x {x0+xs.min()}..{x0+xs.max()}, y {y0+ys.min()}..{y0+ys.max()}")

# vecbox area (43: vecbox 400,50 70x22; Y2 label; 1xd label at 473..499)
region("vecbox+label", 380, 560, 40, 110)
# title line1 (43 ink x527..867 y54..76)
region("title-line1", 500, 875, 45, 80)
# badge (43 center 893,71 d36)
region("badge", 870, 920, 45, 95)
# title line2 (43 ink x606..797 y78..99)
region("title-line2", 560, 830, 76, 105)
# below-title strip
region("y100-150", 560, 920, 100, 150)
# inset region
region("inset-zone", 700, 925, 40, 400)
# what about lower zones
region("y150-300 full", 0, 960, 150, 300)
region("y300-380", 0, 960, 300, 380)
