from PIL import Image
import numpy as np
for name in ["slide_043","slide_044"]:
    L = np.asarray(Image.open(f"unique_slides/{name}.jpg").convert("L"))
    d = L < 120
    for label,(x0,x1,y0,y1) in [("line1",(380,920,50,78)),("line2",(380,920,78,102)),("badge",(870,920,45,95)),("vecbox",(395,560,45,80))]:
        m = d[y0:y1, x0:x1]
        ys,xs = np.where(m)
        if len(xs)==0: print(name,label,"empty"); continue
        print(f"{name} {label}: ink x {x0+xs.min()}..{x0+xs.max()}  y {y0+ys.min()}..{y0+ys.max()}  n={len(xs)}")
