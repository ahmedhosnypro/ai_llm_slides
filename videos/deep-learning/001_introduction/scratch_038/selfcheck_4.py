from PIL import Image
import numpy as np
R = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/qa/slide038/render_2.png').convert('RGB')).astype(int)
S = R.shape[1]/960.0
r, g, b = R[...,0], R[...,1], R[...,2]
ink = (r<175)&(g<175)&(b<175)
def fb(y0,y1,x0,x1, m=None):
    m = (ink if m is None else m)[int(y0*S):int(y1*S), int(x0*S):int(x1*S)]
    ys, xs = np.nonzero(m)
    if len(xs)==0: return None
    return (round(x0+xs.min()/S,1), round(x0+xs.max()/S,1), round(y0+ys.min()/S,1), round(y0+ys.max()/S,1), int(m.sum()))
checks = [  # name, y0,y1,x0,x1, expected (x0,x1,y0,y1)
 ("RGB",      256, 296, 280, 370, (294,358,267,283)),
 ("3dims",    284, 312, 310, 360, (316,350,291,302)),
 ("arrow3d",  306, 340, 280, 322, (287,320,308,332)),
 ("7top",     322, 354, 394, 428, (404,416,331,346)),
 ("7mid",     348, 400, 434, 478, (444,466,355,395)),
 ("7right",   328, 396, 516, 562, (528,552,338,388)),
 ("3glyph",   394, 432, 388, 422, (394,418,402,424)),
 ("pencil",   394, 452, 422, 452, (424,446,398,448)),
 ("735text",  460, 504, 366, 560, (378,546,470,496)),
 ("X",        328, 364, 346, 380, (351,374,336,357)),
]
for nm, y0,y1,x0,x1, exp in checks:
    got = fb(y0,y1,x0,x1)
    print(f"{nm}: {got}  exp x{exp[0]}..{exp[1]} y{exp[2]}..{exp[3]}")
print()
# ASCII of the diagram top band from the RENDER to see annotations
def show(y0,y1,x0,x1,cell=4):
    print(f"--- render y{y0}..{y1} x{x0}..{x1} cell={cell} ---")
    print("     " + "".join(str((x//10)%10) for x in range(x0, x1, cell)))
    for y in range(y0, y1, cell):
        row=""
        for x in range(x0, x1, cell):
            row += "#" if ink[int(y*S):int((y+cell)*S), int(x*S):int((x+cell)*S)].sum()>0 else "."
        print(f"{y:4d} {row}")
show(255, 355, 240, 470)
show(350, 460, 430, 565, 5)
