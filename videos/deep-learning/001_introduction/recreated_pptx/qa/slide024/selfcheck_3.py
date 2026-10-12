#!/usr/bin/env python3
"""Closed-loop check: render_3.png (150dpi) vs measured frame constants (960x540, 1px=1pt).
Scale: 150/72 render px per frame px. Tolerance ~4 render px (~2 frame px)."""
import numpy as np
from PIL import Image

R = np.asarray(Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/qa/slide024/render_3.png").convert("RGB")).astype(int)
S = 150 / 72.0
COL_CX = [160, 261.5, 426.5, 590, 676.5]
ROW_CY = [211.5, 285.5, 366.5]
H, W = R.shape[:2]
ok = lambda name, got, exp, tol=4: print(f"{'OK ' if all(abs(g-e)<=tol for g,e in zip(got,exp)) else 'FAIL'} {name}: got {got} exp {exp}")

BEIGE = np.array([218, 208, 196])
def f2r(v): return int(round(v * S))

def bbox(mask, x0, y0):
    yy, xx = np.nonzero(mask)
    if not len(yy): return None
    return [x0 + xx.min(), y0 + yy.min(), x0 + xx.max(), y0 + yy.max()]

print(f"render {W}x{H}, scale {S:.4f}")
# 1. title ink (red in top strip)
redm = (R[:, :, 0] > 130) & (R[:, :, 1] < 90) & (R[:, :, 2] < 90)
b = bbox(redm[f2r(50):f2r(110), f2r(250):f2r(720)], f2r(250), f2r(50))
ok("title ink [x0,y0,x1,y1]r", b, [f2r(v) for v in (328, 60, 643, 95)], 12)
print(f"  title width {b[2]-b[0]}r = {(b[2]-b[0])/S:.1f}f (exp 315f); center {(b[0]+b[2])/2/S:.1f}f (exp 485.5)")
# 2. beige panel
bm = (np.abs(R - BEIGE).sum(axis=2) < 45)
b = bbox(bm[f2r(150):f2r(430), f2r(50):f2r(800)], f2r(50), f2r(150))
ok("beige panel", b, [f2r(v) for v in (64, 165, 785, 417)], 10)
# 3. white output boxes (white runs inside panel right zone)
whm = (R[:, :, 0] > 245) & (R[:, :, 1] > 245) & (R[:, :, 2] > 240)
for tag, (x0, y0) in {"out1": (700, 195), "out2": (700, 267), "out3": (700, 349)}.items():
    b = bbox(whm[f2r(y0):f2r(y0 + 35), f2r(x0):f2r(800)], f2r(x0), f2r(y0))
    exp = {"out1": (723, 206, 781, 219), "out2": (723, 278, 781, 291), "out3": (723, 360, 781, 373)}[tag]
    ok(f"outbox {tag}", b, [f2r(v) for v in exp], 8)
# 4. error bar
erm = (R[:, :, 0] > 110) & (R[:, :, 1] < 70) & (R[:, :, 2] < 70)
b = bbox(erm[f2r(170):f2r(400), f2r(780):f2r(825)], f2r(780), f2r(170))
ok("error bar", b, [f2r(v) for v in (797, 180, 818, 393)], 8)
# 5. class boxes (light green fills)
cg = (R[:, :, 1] > 235) & (R[:, :, 0] > 195) & (R[:, :, 0] < 245) & (R[:, :, 2] < 225)
for tag, (x0, y0) in {"class1": (815, 190), "class2": (815, 263), "class3": (815, 345)}.items():
    b = bbox(cg[f2r(y0):f2r(y0 + 45), f2r(x0):f2r(905)], f2r(x0), f2r(y0))
    exp = {"class1": (825, 202, 891, 221), "class2": (825, 275, 891, 293), "class3": (825, 357, 891, 374)}[tag]
    ok(f"class {tag}", b, [f2r(v) for v in exp], 8)
# 6. callouts
prevm = (np.abs(R - np.array([222, 235, 243])).sum(axis=2) < 30)
curm = (np.abs(R - np.array([221, 255, 184])).sum(axis=2) < 30)
nxtm = (np.abs(R - np.array([242, 204, 157])).sum(axis=2) < 30)
for (tag, (x0, y0, x1, y1), m) in [("prev", (210, 432, 317, 470), prevm), ("cur", (374, 418, 481, 470), curm), ("nxt", (548, 433, 637, 468), nxtm)]:
    b = bbox(m[f2r(y0):f2r(y1), f2r(x0):f2r(x1)], f2r(x0), f2r(y0))
    exp = {"prev": (220, 428, 307, 461), "cur": (384, 428, 471, 461), "nxt": (558, 430, 627, 459)}[tag]
    ok(f"callout {tag}", b if b else [0, 0, 0, 0], [f2r(v) for v in exp], 9)
# 7. magenta boxes + dash
mm = (R[:, :, 0] > 200) & (R[:, :, 2] > 200) & (R[:, :, 1] < 190)
b = bbox(mm[f2r(115):f2r(165), f2r(50):f2r(160)], f2r(50), f2r(115))
ok("magenta IS", b, [f2r(v) for v in (64, 127, 140, 155)], 8)
b = bbox(mm[f2r(115):f2r(136), f2r(800):f2r(905)], f2r(800), f2r(115))
ok("magenta SL", b, [f2r(v) for v in (820, 125, 888, 154)], 8)
dashrow = mm[f2r(138):f2r(145), f2r(200):f2r(800)]
print(f"{'OK ' if dashrow.sum() > 40 else 'FAIL'} dash band ink px: {int(dashrow.sum())}")
# 8. neuron centers via fill masks (cols 2/3/4 saturated enough)
def centers(fill_test, c):
    out = []
    for r, cy in enumerate(ROW_CY):
        x0, y0 = int((COL_CX[c] - 22) * S), int((cy - 22) * S)
        sub = fill_test[y0:y0 + int(44 * S), x0:x0 + int(44 * S)]
        yy, xx = np.nonzero(sub)
        if len(yy): out.append((round((x0 + xx.mean()) / S, 1), round((y0 + yy.mean()) / S, 1)))
        else: out.append(None)
    return out
bluem = (R[:, :, 2] - R[:, :, 0] > 8) & (R[:, :, 2] > 200) & (R[:, :, 1] > 190)
greenm = (R[:, :, 1] - R[:, :, 0] > 25) & (R[:, :, 1] > 230)
orangem = (R[:, :, 0] - R[:, :, 2] > 30) & (R[:, :, 0] > 220)
print("col2 centers:", centers(bluem, 1), "exp", [(261.5, cy) for cy in ROW_CY])
print("col3 centers:", centers(greenm, 2), "exp", [(426.5, cy) for cy in ROW_CY])
print("col4 centers:", centers(orangem, 3), "exp", [(590.0, cy) for cy in ROW_CY])
# 9. red mesh ink present in gap midpoints
for (tag, y, x0, x1) in [("A-gap r1r1", 212, 300, 390), ("B-gap r1r1", 212, 460, 560), ("A-gap r1r3", 300, 340, 365)]:
    sub = erm[f2r(y - 3):f2r(y + 3), f2r(x0):f2r(x1)]
    print(f"{'OK ' if sub.sum() > 3 else 'FAIL'} mesh {tag}: {int(sub.sum())} red px")
# 10. containment: no content ink beyond house panel (x42..918, y45..540) except nothing
edge = ((R[:, :, 0] < 200) | (R[:, :, 1] < 200) | (R[:, :, 2] < 200))
print("containment: ink px in margin x<42:", int(edge[:, :f2r(41)].sum()), " x>918:", int(edge[:, f2r(919):].sum()),
      " y<45:", int(edge[:f2r(44), :].sum()))
print("done")
