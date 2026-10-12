from PIL import Image
import numpy as np
from scipy import ndimage
im = Image.open('videos/deep-learning/001_introduction/unique_slides/slide_022.jpg').convert('RGB')
a = np.asarray(im).astype(int)
r, g, b = a[:,:,0], a[:,:,1], a[:,:,2]

# 1) brace probe: x 522..556, y 260..332 — print any pixel darker than bg
print("== brace probe (raw min per column) ==")
for x in range(522, 558):
    col = a[258:334, x]
    mn = col.sum(axis=1).min()
    ys = np.nonzero(col.sum(axis=1) < 560)[0]
    if len(ys):
        print(f"x={x}: ink rows {258+ys.min()}..{258+ys.max()} n={len(ys)} sample={tuple(a[258+ys[len(ys)//2], x])}")

# 2) saturation-modal colors of key glyphs
def satmodal(x0,y0,x1,y1,pred,label):
    sub = a[y0:y1, x0:x1].reshape(-1,3)
    sel = np.array([c for c in sub if pred(c)])
    if len(sel)==0: print(label, "none"); return
    sel2 = sel[np.argsort(sel.sum(axis=1))]  # darkest first
    k = max(1, len(sel)//5)
    core = sel2[:k]
    from collections import Counter
    print(f"{label}: n={len(sel)} darkest-20% modal={Counter(map(tuple,core)).most_common(3)}")

isred = lambda c: c[0]>110 and c[0]-c[1]>40 and c[0]-c[2]>40
isblu = lambda c: c[2]>90 and c[2]-c[0]>30
isdrk = lambda c: c.sum()<330
satmodal(86,159,100,173, isdrk, "eq1 X glyph")
satmodal(559,159,576,174, lambda c: isdrk(c) or isred(c), "eq2 W glyph")
satmodal(108,286,123,304, lambda c: isdrk(c) or isred(c), "eq3 d(X) X glyph")
satmodal(156,287,174,302, isdrk, "eq3 W glyph")
satmodal(178,160,195,172, isred, "eq1 red arrow")
satmodal(502,287,523,300, isred, "eq3 red arrow")
satmodal(602,106,613,121, isred, "eq2 red b")
satmodal(426,287,457,302, isred, "eq3 red b*1")
satmodal(297,159,408,177, isblu, "eq1 blue label")
satmodal(668,159,763,177, isblu, "eq2 blue label")
satmodal(614,311,742,327, isblu, "case3 blue text")
satmodal(240,62,720,84, isred, "title red")
# 3) brace red?
satmodal(524,260,556,334, lambda c: isred(c) or c.sum()<430, "brace region any ink")
