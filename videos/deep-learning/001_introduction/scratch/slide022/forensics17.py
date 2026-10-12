from PIL import Image
import numpy as np
from collections import Counter
im = Image.open('videos/deep-learning/001_introduction/unique_slides/slide_022.jpg').convert('RGB')
a = np.asarray(im).astype(int)

def sat_modal(x0,y0,x1,y1,pred,label):
    sub = a[y0:y1, x0:x1].reshape(-1,3)
    sel = np.array([c for c in sub if pred(c)])
    if len(sel)==0: print(label, "none"); return
    sel2 = sel[np.argsort(sel.sum(axis=1))]
    k = max(1, len(sel)//5)
    print(f"{label}: n={len(sel)} darkest20 modal={Counter(map(tuple,sel2[:k])).most_common(3)}")

# block border (pink) pixels: strong chroma, not red, not blue-text
blk_border = lambda c: (c[0]>140 and c[2]>120 and abs(c[0]-c[2])<90 and c[0]-c[1]>40) or (c[2]>150 and c[2]-c[0]>25 and c[0]-c[1]>25)
sat_modal(474,409,507,433, blk_border, "step block border")
# circle outline fragments (right arc 'B' zone)
sat_modal(434,407,446,432, lambda c: c[2]>110 and c[2]-c[0]>25, "circle right-arc")
# O/P text
sat_modal(582,415,610,429, lambda c: sum(c)<330, "O/P text")
# input '1' red + weight 'b' blue in diagram
sat_modal(252,489,258,501, lambda c: c[0]>110 and c[0]-c[1]>40, "diagram red 1")
sat_modal(288,487,298,500, lambda c: c[2]>90 and c[2]-c[0]>30, "diagram blue b")
sat_modal(289,357,306,370, lambda c: c[2]>90 and c[2]-c[0]>30, "diagram blue w1")
# callout text ink
sat_modal(640,405,800,440, lambda c: sum(c)<340, "callout text ink")
# box borders: top border of diagram box
sat_modal(300,349,500,354, lambda c: c[0]>140 and c[0]-c[1]>25 and c[0]-c[2]>20, "diagram box top border")
sat_modal(100,87,400,93, lambda c: c[0]>140 and c[0]-c[1]>25 and c[0]-c[2]>20, "left box top border")
sat_modal(100,252,700,258, lambda c: c[0]>140 and c[0]-c[1]>25 and c[0]-c[2]>20, "decision box top border")
sat_modal(630,394,810,400, lambda c: c[0]>140 and c[0]-c[1]>25, "callout top border")
# equation glyph color: w/x entries in eq boxes (should be black)
sat_modal(597,132,616,146, lambda c: sum(c)<340, "eq2 w1 glyphs")
sat_modal(121,121,137,136, lambda c: sum(c)<340, "eq1 x1 glyphs")
# underline of labels? rows just below labels
sat_modal(297,173,410,180, lambda c: c[2]>90 and c[2]-c[0]>20, "eq1 label underline zone")
