from PIL import Image
import numpy as np
R = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/qa/slide038/render_4.png').convert('RGB')).astype(int)
S = R.shape[1]/960.0
r, g, b = R[...,0], R[...,1], R[...,2]
ink = (r<175)&(g<175)&(b<175)
def fb(y0,y1,x0,x1):
    m = ink[int(y0*S):int(y1*S), int(x0*S):int(x1*S)]
    ys, xs = np.nonzero(m)
    if len(xs)==0: return None
    return (round(x0+xs.min()/S,1), round(x0+xs.max()/S,1), round(y0+ys.min()/S,1), round(y0+ys.max()/S,1))
print("dash-7 zone:", fb(350, 402, 372, 400), "exp cluster (378,398,354,399)")
print("dashes ext:", fb(352, 392, 346, 392), "exp (350,392,353,389)")
print("arrow3d:", fb(292, 340, 278, 336), "exp ~(284,334,295,338)")
print("pencil strokes:", fb(394, 452, 422, 452), "exp (424,446,398,448)")
print("7top:", fb(324, 352, 396, 424), "exp (404,416,331,346)")
print("title:", end=" ")
red = ((r-g)>40)&((r-b)>40)&(r>110)
m = red[int(55*S):int(110*S), int(250*S):int(750*S)]
ys, xs = np.nonzero(m)
print((round(250+xs.min()/S,1), round(250+xs.max()/S,1), round(55+ys.min()/S,1), round(55+ys.max()/S,1)), "exp (333,633,67,101)")
# containment re-checks
for nm,(y0,y1,x0,x1) in {"between boxes":(236,249,95,876),"below dbox":(513,517,186,806)}.items():
    m2 = ink[int(y0*S):int(y1*S), int(x0*S):int(x1*S)]
    print(f"ink {nm}: {m2.sum()} (want 0)")
