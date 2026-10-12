#!/usr/bin/env python3
"""selfcheck_attempt_1.py — closed-loop render-vs-original ink comparison (attempt 1).
150dpi render: 1 render px = 1/150 in = 0.48 slide pt; slide_pt = render_px*72/150.
Original frame px -> slide pt via FX/FY (ax=17.943, sx=0.962307, sy=0.955556).
For each element: measured ink bbox in BOTH, diff in slide pt (tol ~6 frame px = 6.24 pt).
"""
import numpy as np
from PIL import Image

VID = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2"
REN = f"{VID}/recreated_pptx/qa/slide034/render_1.png"
ORIG = f"{VID}/unique_slides/slide_034.jpg"

AX, SX, SY = 17.943, 0.962307, 0.955556
def f2s(fx): return (fx - AX) / SX
def fy2s(fy): return fy / SY
# render(150dpi) px -> slide pt
R2S = 72.0 / 150.0

ren = np.asarray(Image.open(REN).convert("RGB")).astype(int)
ori = np.asarray(Image.open(ORIG).convert("RGB")).astype(int)
print(f"render {ren.shape[1]}x{ren.shape[0]}, original {ori.shape[1]}x{ori.shape[0]}")

def ink_bbox(img, y0, y1, x0, x1, mask_fn):
    m = mask_fn(img[y0:y1, x0:x1])
    ys, xs = np.where(m)
    if len(xs) == 0: return None
    return (x0 + xs.min(), x0 + xs.max(), y0 + ys.min(), y0 + ys.max())

def report(name, obox, rbox_slide, tol=6.24):
    # obox in frame px -> slide pt; rbox already slide pt
    if obox is None or rbox_slide is None:
        print(f"{name}: MISSING ink (orig={obox is not None}, render={rbox_slide is not None})")
        return
    o = [f2s(obox[0]), f2s(obox[1]), fy2s(obox[2]), fy2s(obox[3])]
    d = [rbox_slide[i] - o[i] for i in range(4)]
    worst = max(abs(v) for v in d)
    flag = "OK " if worst <= tol else "OVER"
    print(f"{flag} {name}: dx0={d[0]:+.1f} dx1={d[1]:+.1f} dy0={d[2]:+.1f} dy1={d[3]:+.1f} (slide pt, tol {tol})  orig_w={o[1]-o[0]:.0f} ren_w={rbox_slide[1]-rbox_slide[0]:.0f}")

def sl(box):  # render px -> slide pt
    return (box[0]*R2S, box[1]*R2S, box[2]*R2S, box[3]*R2S)

# masks
def redm(t):  return lambda im: (im[...,0]-im[...,1] > 35) & (im[...,0]-im[...,2] > 35) & (im.sum(axis=2) < 560)
def bluem(t): return lambda im: (im[...,2]-im[...,0] > 35) & (im.sum(axis=2) < 500)
def navy(t):  return lambda im: (im[...,2]-im[...,0] > 30) & (im.sum(axis=2) < 560)
def darkm(t): return lambda im: im.sum(axis=2) < 330
def dashm(t): return lambda im: (abs(im[...,0]-im[...,1])<28) & (im[...,2]-im[...,0] > 25) & (im.sum(axis=2) < 640)
def greenm(t): return lambda im: (im[...,1]-im[...,0] > 30) & (im[...,1]-im[...,2] > 30)
def yellowm(t): return lambda im: (im[...,0] > 200) & (im[...,1] > 190) & (im[...,2] < 170)

# render regions in slide pt -> render px
def rz(sx0, sx1, sy0, sy1): return int(sy0/R2S), int(sy1/R2S), int(sx0/R2S), int(sx1/R2S)

# 1. title (red part + blue part)
oy0, oy1, ox0, ox1 = 55, 100, 260, 710
ry0, ry1, rx0, rx1 = rz(f2s(200), f2s(760), fy2s(50), fy2s(105))
report("title.red", ink_bbox(ori, 55, 100, 260, 486, redm(0)),
       sl(ink_bbox(ren, ry0, int(fy2s(99)/R2S), rx0, int(f2s(486)/R2S), redm(0))))
report("title.blue", ink_bbox(ori, 55, 100, 487, 710, bluem(0)),
       sl(ink_bbox(ren, ry0, ry1, int(f2s(487)/R2S), rx1, bluem(0))))
# 2. subtitle
ry0, ry1, rx0, rx1 = rz(f2s(300), f2s(700), fy2s(101), fy2s(126))
report("subtitle", ink_bbox(ori, 98, 126, 300, 700, redm(0)),
       sl(ink_bbox(ren, ry0, ry1, rx0, rx1, redm(0))))
# 3. lane1 dash extents (top dash row)
report("lane1.topdash", ink_bbox(ori, 134, 139, 160, 890, dashm(0)),
       sl(ink_bbox(ren, *rz(f2s(160), f2s(895), fy2s(133), fy2s(141)), dashm(0))))
# 4. token box1 (borders): use dash mask in box1 region
report("tokbox1", ink_bbox(ori, 143, 167, 178, 242, dashm(0)),
       sl(ink_bbox(ren, *rz(f2s(176), f2s(245), fy2s(142), fy2s(169)), dashm(0))))
# 5. dots
report("dots", ink_bbox(ori, 150, 167, 628, 722, navy(0)),
       sl(ink_bbox(ren, *rz(f2s(628), f2s(722), fy2s(149), fy2s(169)), navy(0))))
# 6. purple bar
def purpm(t): return lambda im: (im[...,0] > 95) & (im[...,0] < 200) & (im[...,1] < 70) & (im[...,2] > 95) & (im[...,2] < 200)
report("bar", ink_bbox(ori, 208, 258, 160, 895, purpm(0)),
       sl(ink_bbox(ren, *rz(f2s(160), f2s(895), fy2s(208), fy2s(258)), purpm(0))))
# 7. bar yellow text
report("bar.yellow", ink_bbox(ori, 220, 252, 175, 885, yellowm(0)),
       sl(ink_bbox(ren, *rz(f2s(175), f2s(885), fy2s(220), fy2s(252)), yellowm(0))))
# 8. lane3 dash + fill
def vecfill(t): return lambda im: (im[...,0] > 235) & (im[...,2] > 235) & (im[...,1] > 200) & (im[...,1] < 245) & (im[...,0]-im[...,1] > 5)
report("lane3.fill", ink_bbox(ori, 291, 327, 160, 895, vecfill(0)),
       sl(ink_bbox(ren, *rz(f2s(160), f2s(895), fy2s(289), fy2s(330)), vecfill(0))))
# 9. vector box1 (pink fill)
def pinkm(t): return lambda im: (im[...,0] > 238) & (im[...,1] > 190) & (im[...,1] < 232) & (im[...,2] > 200) & (im[...,2] < 245)
report("vecbox1.fill", ink_bbox(ori, 300, 321, 172, 245, pinkm(0)),
       sl(ink_bbox(ren, *rz(f2s(172), f2s(245), fy2s(298), fy2s(323)), pinkm(0))))
# 10. vector text box1
report("vectext1", ink_bbox(ori, 302, 320, 180, 240, navy(0)),
       sl(ink_bbox(ren, *rz(f2s(180), f2s(240), fy2s(300), fy2s(322)), navy(0))))
# 11. brace (dark red)
report("brace", ink_bbox(ori, 334, 353, 170, 880, redm(0)),
       sl(ink_bbox(ren, *rz(f2s(170), f2s(880), fy2s(332), fy2s(356)), redm(0))))
# 12. summary box border (green)
report("sumbox", ink_bbox(ori, 358, 508, 215, 835, greenm(0)),
       sl(ink_bbox(ren, *rz(f2s(215), f2s(835), fy2s(356), fy2s(510)), greenm(0))))
# 13. summary lines L1..L5 (dark or red or yellow)
def anwm(t):
    red2 = (im_r := None)
    return None
def linemask(im):
    s = im.sum(axis=2)
    r, g, b = im[...,0], im[...,1], im[...,2]
    return (s < 330) | ((r-g > 35) & (r-b > 35) & (s < 560)) | ((r > 200) & (g > 190) & (b < 170))
LINES = [("L1", 372, 390, 240, 810), ("L2", 391, 412, 240, 810), ("L3", 413, 433, 240, 810),
         ("L4", 434, 456, 240, 810), ("L5", 470, 500, 240, 810)]
for nm, y0, y1, x0, x1 in LINES:
    report(f"sum.{nm}", ink_bbox(ori, y0, y1, x0, x1, linemask),
           sl(ink_bbox(ren, *rz(f2s(x0), f2s(x1), fy2s(y0-2), fy2s(y1+2)), linemask)))
# 14. lab1 lines (navy, x<164)
for nm, y0, y1 in [("lab1.Position", 138, 154), ("lab1.Information", 155, 174), ("lab1.paren", 179, 197)]:
    report(nm, ink_bbox(ori, y0, y1, 58, 164, navy(0)),
           sl(ink_bbox(ren, *rz(f2s(56), f2s(165), fy2s(y0-2), fy2s(y1+2)), navy(0))))
# 15. lab3 lines (red x<164 + navy paren)
for nm, y0, y1, m in [("lab3.Positional", 216, 233, redm(0)), ("lab3.Embedding", 234, 252, redm(0)),
                      ("lab3.paren", 255, 272, navy(0))]:
    report(nm, ink_bbox(ori, y0, y1, 58, 166, m),
           sl(ink_bbox(ren, *rz(f2s(56), f2s(167), fy2s(y0-2), fy2s(y1+2)), m)))
# 16. arrows
report("arrow1", ink_bbox(ori, 174, 218, 505, 545, redm(0)),
       sl(ink_bbox(ren, *rz(f2s(505), f2s(545), fy2s(172), fy2s(220)), redm(0))))
report("arrow2", ink_bbox(ori, 250, 292, 505, 545, redm(0)),
       sl(ink_bbox(ren, *rz(f2s(505), f2s(545), fy2s(248), fy2s(294)), redm(0))))
# 17. highlight N-1 (strict mask: JPEG halo inflates looser masks on the original —
#      the drawn rect 431..492 was cross-checked against the strict core 435..489: dx -4.0/+2.1)
def ylwmid(t): return lambda im: (im[...,0] > 210) & (im[...,1] > 200) & (im[...,2] < 170) & (im[...,0]-im[...,2] > 60)
report("highlight", ink_bbox(ori, 405, 440, 400, 530, ylwmid(0)),
       sl(ink_bbox(ren, *rz(f2s(400), f2s(530), fy2s(403), fy2s(442)), ylwmid(0))))
