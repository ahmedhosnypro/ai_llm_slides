from PIL import Image
import numpy as np
from scipy import ndimage
from collections import Counter
im = Image.open('videos/deep-learning/001_introduction/unique_slides/slide_022.jpg').convert('RGB')
a = np.asarray(im).astype(int)
r, g, b = a[:,:,0], a[:,:,1], a[:,:,2]

# (a) underline check under X (eq1), W (eq2), X (eq3), and d(..) parens
for label,(x0,y0,x1,y1) in {
 "under eq1 X (84..101,171..178)": (84,171,101,178),
 "under eq2 W (557..577,172..179)": (557,172,577,179),
 "under eq3 X (106..124,302..309)": (106,302,124,309),
 "under eq3 W (154..175,300..307)": (154,300,175,307),
}.items():
    sub = a[y0:y1, x0:x1]
    dark = (sub.sum(axis=2) < 430).sum()
    print(label, "dark px:", dark)

# (b) callout text lines: components
ink = (r<170)&(g<170)&(b<180) | ((r>120)&(r>g+50)&(r>b+50))
inkd = ndimage.binary_dilation(ink, iterations=1)
lab, n = ndimage.label(inkd[395:445, 630:820])
comps = []
for i in range(1, n+1):
    ys, xs = np.nonzero(lab==i)
    if len(xs) < 5: continue
    comps.append((630+int(xs.min()), 395+int(ys.min()), 630+int(xs.max()), 395+int(ys.max()), len(xs)))
comps.sort(key=lambda c:(c[1]//6, c[0]))
print("\ncallout text comps:")
for c in comps: print(c)
if comps:
    l1 = [c for c in comps if c[1] < 425]; l2 = [c for c in comps if c[1] >= 425]
    for nm, L in [("line1", l1), ("line2", l2)]:
        if L:
            x0 = min(c[0] for c in L); x1 = max(c[2] for c in L)
            y0 = min(c[1] for c in L); y1 = max(c[3] for c in L)
            print(f"{nm}: bbox=({x0},{y0})-({x1},{y1}) center_x={(x0+x1)/2}")

# (c) case arrow color (586,271)-(601,301) zone
def sat_modal(x0,y0,x1,y1,pred,label):
    sub = a[y0:y1, x0:x1].reshape(-1,3)
    sel = np.array([c for c in sub if pred(c)])
    if len(sel)==0: print(label, "none"); return
    sel2 = sel[np.argsort(sel.sum(axis=1))]
    k = max(1, len(sel)//5)
    print(f"{label}: n={len(sel)} darkest20={Counter(map(tuple,sel2[:k])).most_common(3)}")
sat_modal(585,269,602,282, lambda c: sum(c)<430, "case1 arrow")
sat_modal(585,291,602,304, lambda c: sum(c)<430, "case2 arrow")
sat_modal(586,313,602,326, lambda c: sum(c)<430, "case3 arrow")
sat_modal(553,265,576,285, lambda c: sum(c)<430, "case1 '>0'")
