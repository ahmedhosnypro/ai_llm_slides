from PIL import Image, ImageFont
import numpy as np
from collections import Counter
FR="/usr/share/fonts/liberation/LiberationSans-Regular.ttf"
FB="/usr/share/fonts/liberation/LiberationSans-Bold.ttf"
import os; print("exist:", os.path.exists(FR), os.path.exists(FB))
def adv(t, pt, bold=False): return ImageFont.truetype(FB if bold else FR, pt*100).getlength(t)/100.0
for t, meas in [("Feature Invariants",208),("Features Invariants are",227),("is",12),("Problem dependent",183),
                ("Rotation Invariant",176),("Scaling Invariant",166),("Translation invariant",203),("Mirroring Invariant",183)]:
    row=f" '{t}' meas {meas}: "
    for pt in (20,21,22,24,25):
        row += f"[{pt} r{adv(t,pt):.0f}/b{adv(t,pt,True):.0f}] "
    print(row)

im = Image.open('videos/deep-learning/001_introduction/unique_slides/slide_012.jpg').convert('RGB')
a = np.asarray(im).astype(int)
# bullet3/4 row profiles
for lbl,(y0,y1) in [("bullet3",(320,346)),("bullet4",(364,388))]:
    print(f"\n{lbl} rows {y0}..{y1} ink counts (x 127..340):")
    for y in range(y0,y1):
        ink=sum(1 for x in range(127,341) if a[y,x].sum()<430)
        print(f"  {y}:{ink}", end="")
    print()
# bullet3 heavy-row ink EXCLUDING x 185..215 (cursor zone)
print("\nbullet3 excluding cursor zone x185..215:")
for y in range(320,346):
    ink=sum(1 for x in range(127,341) if a[y,x].sum()<430 and not (185<=x<=215))
    print(f"  {y}:{ink}", end="")
print()
# dot cores (sum<250)
print("\ndot cores sum<300:")
for (y0,y1) in [(232,252),(276,296),(320,340),(364,384)]:
    pts=[(y,x) for y in range(y0,y1) for x in range(100,130) if a[y,x].sum()<300]
    if pts:
        ys=[p[0] for p in pts]; xs=[p[1] for p in pts]
        print(f"  y {min(ys)}..{max(ys)} x {min(xs)}..{max(xs)} c({(min(xs)+max(xs))/2},{(min(ys)+max(ys))/2}) n={len(pts)}")
# black text modal color (bullets)
print("\nbullet text modal:", Counter(tuple(a[y,x]) for y in range(240,246) for x in range(130,300) if a[y,x].sum()<200).most_common(2))
# header black modal
print("header black modal:", Counter(tuple(a[y,x]) for y in range(170,180) for x in range(386,560) if a[y,x].sum()<200).most_common(2))
