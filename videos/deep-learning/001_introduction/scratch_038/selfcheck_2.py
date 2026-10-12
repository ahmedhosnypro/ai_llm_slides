"""Closed-loop check 2: render_2.png vs original measurements, incl annotation bboxes."""
from PIL import Image
import numpy as np
R = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/qa/slide038/render_2.png').convert('RGB')).astype(int)
H, W = R.shape[:2]
S = W / 960.0
r, g, b = R[...,0], R[...,1], R[...,2]
ink  = (r<175)&(g<175)&(b<175)
red  = ((r-g)>40)&((r-b)>40)&(r>110)
blue = ((b-r)>40)&((b-g)>20)&(b>110)

def fboxF(mask, y0,y1,x0,x1):
    m = mask[int(y0*S):int(y1*S), int(x0*S):int(x1*S)]
    ys, xs = np.nonzero(m)
    if len(xs)==0: return None
    return (round(x0+xs.min()/S,1), round(x0+xs.max()/S,1), round(y0+ys.min()/S,1), round(y0+ys.max()/S,1))

def report(name, got, exp, tol=4):
    if got is None: print(f"{name}: EMPTY (exp {exp})"); return
    d = [round(got[i]-exp[i],1) for i in range(4)]
    ok = all(abs(x)<=tol for x in d)
    print(f"{name}: got x{got[0]}..{got[1]} y{got[2]}..{got[3]} d={d} {'OK' if ok else '<<< FIX'}")

report("title", fboxF(red, 50, 110, 250, 750), (333, 633, 67, 101), 4)
report("line1", fboxF(ink, 128, 168, 95, 880), (102, 774, 139, 158), 5)
report("line2", fboxF(ink, 168, 200, 95, 880), (102, 758, 174, 192), 5)
report("line3", fboxF(ink, 200, 232, 95, 880), (102, 277, 209, 223), 5)
report("circles", fboxF((g>120)&(b>120)&(r<110) | ((r>170)&(g>170)&(b<110)) | ((r>80)&(r<180)&(b>80)&(b<190)&(g<90)), 348, 392, 600, 800), (610, 792, 355, 382), 5)
# annotations: ink bboxes vs original measured zones
ann = {
 "RGB":        ((294, 358, 267, 283), (285, 365, 258, 292)),
 "3dims":      ((316, 350, 291, 302), (308, 356, 284, 312)),
 "7top":       ((404, 416, 331, 346), (396, 424, 324, 352)),
 "7mid":       ((444, 466, 355, 395), (436, 474, 348, 400)),
 "7right":     ((528, 552, 338, 388), (520, 560, 330, 396)),
 "3":          ((394, 418, 402, 424), (388, 424, 396, 430)),
 "735weights": ((378, 546, 470, 496), (368, 556, 462, 504)),
}
for nm, (exp, zone) in ann.items():
    got = fboxF(ink, *zone)
    if got is None: print(f"ann {nm}: EMPTY <<<"); continue
    dx0 = round(got[0]-exp[0],1); dx1 = round(got[1]-exp[1],1)
    print(f"ann {nm}: got x{got[0]}..{got[1]} y{got[2]}..{got[3]}  exp x{exp[0]}..{exp[1]} y{exp[2]}..{exp[3]}  dx0={dx0} dx1={dx1}")
# containment
for nm, (y0,y1,x0,x1) in {"between boxes":(236,249,95,876), "below dbox":(513,517,186,806), "above title":(48,64,100,860)}.items():
    m = ink[int(y0*S):int(y1*S), int(x0*S):int(x1*S)]
    print(f"ink {nm}: {m.sum()} (want ~0)")
