"""Closed-loop check: render_1.png (2001x1125) vs original frame measurements (960x540).
scale = 2001/960 = 2.0844."""
from PIL import Image
import numpy as np
R = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/qa/slide038/render_1.png').convert('RGB')).astype(int)
H, W = R.shape[:2]
S = W / 960.0
print(f"render {W}x{H} scale {S:.4f}")
r, g, b = R[...,0], R[...,1], R[...,2]
ink  = (r<175)&(g<175)&(b<175)
red  = ((r-g)>40)&((r-b)>40)&(r>110)
blue = ((b-r)>40)&((b-g)>20)&(b>110)

def fb(v): return v*S  # frame px -> render px
def fbox(mask, y0,y1,x0,x1):
    m = mask[int(fb(y0)):int(fb(y1)), int(fb(x0)):int(fb(x1))]
    ys, xs = np.nonzero(m)
    if len(xs)==0: return None
    return (x0+xs.min()/1, x0+xs.max(), y0+ys.min(), y0+ys.max()) if False else (
        int(x0+xs.min()), int(x0+xs.max()), int(y0+ys.min()), int(y0+ys.max()))

def report(name, got, exp, tol=4):
    if got is None: print(f"{name}: EMPTY  (expected {exp})"); return
    d = [got[i]-exp[i] for i in range(4)]
    ok = all(abs(d[i])<=tol for i in range(4))
    print(f"{name}: got x{got[0]}..{got[1]} y{got[2]}..{got[3]}  exp x{exp[0]}..{exp[1]} y{exp[2]}..{exp[3]}  d={d} {'OK' if ok else '<<< FIX'}")

# these helpers report in FRAME px (divide render px by S)
def fboxF(mask, y0,y1,x0,x1):
    m = mask[int(fb(y0)):int(fb(y1)), int(fb(x0)):int(fb(x1))]
    ys, xs = np.nonzero(m)
    if len(xs)==0: return None
    return (round(x0+xs.min()/S,1), round(x0+xs.max()/S,1), round(y0+ys.min()/S,1), round(y0+ys.max()/S,1))

report("title", fboxF(red, 55, 110, 200, 800), (333, 633, 67, 101), 4)
report("fbox border top", fboxF(blue, 110, 128, 300, 700), (300, 700, 117, 120), 3)
report("line1", fboxF(ink, 128, 165, 95, 880), (102, 774, 139, 158), 5)
report("line3", fboxF(ink, 196, 232, 95, 880), (102, 277, 209, 223), 5)
report("dbox top border", fboxF(red, 243, 260, 300, 700), (300, 700, 250, 253), 3)
# dashed lines zone
report("dashes zone", fboxF(ink, 348, 396, 348, 388), (350, 386, 353, 389), 4)
# circles zone (any of the 5 circle colors)
circ = ((g>120)&(b>120)&(r<110)) | (((r>180)&(g<100)&(b<100))) | ((r>170)&(g>170)&(b<110)) | ((r>80)&(r<180)&(b>80)&(b<190)&(g<90)) | ((g>110)&(r<110)&(b<110)&((g-b)>40))
report("circles zone", fboxF(circ, 350, 390, 600, 810), (610, 792, 355, 382), 5)
# brown slab
brown = ((r-g)>40)&((g-b)>25)&(r>120)&(b<130)
report("brown slab", fboxF(brown, 285, 445, 240, 370), (260, 352, 293, 437), 6)
# stack colored
report("stack colors", fboxF(circ, 330, 405, 385, 560), (393, 550, 337, 399), 5)
# '=' bars
report("eq bars", fboxF(blue, 355, 380, 560, 605), (572, 592, 362, 374), 4)
# annotations present? ink in zones
for nm, (y0,y1,x0,x1) in {"RGB":(260,290,285,365), "3dims":(285,310,310,355),
  "7top":(325,350,398,420), "7mid":(350,398,438,472), "7right":(332,392,520,558),
  "3+pencil":(396,450,390,450), "735weights":(465,500,372,552)}.items():
    m = ink[int(fb(y0)):int(fb(y1)), int(fb(x0)):int(fb(x1))]
    print(f"ink {nm}: {m.sum()} px {'OK' if m.sum()>30 else '<<< MISSING'}")
# containment: no ink outside formula box / diagram box
inside_checks = [
  ("above title band", 55, 66, 100, 860),
]
m = ink[int(fb(46)):int(fb(66)), int(fb(60)):int(fb(860))]
print("ink between rule and title (should be ~0):", m.sum())
m = ink[int(fb(236)):int(fb(249)), int(fb(95)):int(fb(876))]
print("ink between boxes (should be ~0):", m.sum())
m = ink[int(fb(513)):int(fb(517)), int(fb(186)):int(fb(806))]
print("ink below dbox (should be ~0):", m.sum())
