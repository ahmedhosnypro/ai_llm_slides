from PIL import Image
import numpy as np
R = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/qa/slide038/render_2.png').convert('RGB')).astype(int)
S = R.shape[1]/960.0
r, g, b = R[...,0], R[...,1], R[...,2]
ink = (r<175)&(g<175)&(b<175)
def fboxF(y0,y1,x0,x1):
    m = ink[int(y0*S):int(y1*S), int(x0*S):int(x1*S)]
    ys, xs = np.nonzero(m)
    if len(xs)==0: return None
    return (round(x0+xs.min()/S,1), round(x0+xs.max()/S,1), round(y0+ys.min()/S,1), round(y0+ys.max()/S,1), int(m.sum()))
# (expected_x0,exp_x1,exp_y0,exp_y1), zone(y0,y1,x0,x1)
ann = {
 "RGB":        ((294, 358, 267, 283), (258, 292, 285, 365)),
 "3dims+arrow":((316, 350, 291, 332), (284, 356, 284, 340)),
 "7top":       ((404, 416, 331, 346), (396, 424, 324, 352)),
 "7mid":       ((444, 466, 355, 395), (436, 474, 350, 398)),
 "7right":     ((528, 552, 338, 388), (520, 560, 330, 396)),
 "3glyph":     ((394, 418, 402, 424), (388, 424, 396, 432)),
 "735weights": ((378, 546, 470, 496), (368, 556, 462, 504)),
 "X":          ((351, 374, 336, 357), (346, 378, 330, 362)),
}
for nm, (exp, zone) in ann.items():
    got = fboxF(*zone)
    if got is None: print(f"ann {nm}: EMPTY <<<"); continue
    print(f"ann {nm}: got x{got[0]}..{got[1]} y{got[2]}..{got[3]} n={got[4]}  exp x{exp[0]}..{exp[1]} y{exp[2]}..{exp[3]}")
