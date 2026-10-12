from PIL import Image
import numpy as np
im = np.asarray(Image.open('slide-1.png').convert('RGB')).astype(int)
H, W, _ = im.shape
print("render size:", W, H)
r, g, b = im[:,:,0], im[:,:,1], im[:,:,2]
luma = (0.299*r+0.587*g+0.114*b)
S = 150/72.0   # slide pt -> render px
def px(pt): return pt * S

# ink mask: not gray panel, not white canvas... content ink = differs from both bg types
ink = (luma < 215)  # dark-ish ink (text/borders)
def bbox(y0,y1,x0,x1,label):
    m = ink[int(y0):int(y1), int(x0):int(x1)]
    rows = np.where(m.any(axis=1))[0]; cols = np.where(m.any(axis=0))[0]
    if len(rows)==0: print(f"{label}: EMPTY"); return None
    print(f"{label}: y {int(y0)+rows.min()}..{int(y0)+rows.max()}  x {int(x0)+cols.min()}..{int(x0)+cols.max()}")
    return (int(y0)+rows.min(), int(y0)+rows.max(), int(x0)+cols.min(), int(x0)+cols.max())

# targets in render px
t_title = (px(61.7), px(80.5), px(334.3), px(698.5))
print("title target y", f"{t_title[0]:.0f}..{t_title[1]:.0f}", "x", f"{t_title[2]:.0f}..{t_title[3]:.0f}")
bbox(px(40), px(105), px(300), px(720), "title ink")
print("subtitle target y", f"{px(88.9):.0f}..{px(107.7):.0f}", "x", f"{px(362.4):.0f}..{px(682.8):.0f}")
bbox(px(108), px(120), px(330), px(710), "subtitle ink (y108-120 window upper part)")
# full subtitle band
bbox(px(105), px(125), px(330), px(710), "subtitle ink")

print()
print("containers target (y0,y1,x0,x1) render px:")
for nm,(cx0,cy0,cx1,cy1) in {
 "R1": (147.6,123.4,896.7,164.2), "R2": (145.5,195.5,893.1,235.8), "R3": (144.0,273.4,894.4,316.3)}.items():
    print(f"  {nm}: y {px(cy0):.0f}..{px(cy1):.0f} x {px(cx0):.0f}..{px(cx1):.0f}")
bbox(px(115), px(170), px(140), px(910), "R1 container+boxes ink")
bbox(px(188), px(242), px(140), px(905), "R2 container+boxes ink")
bbox(px(266), px(322), px(140), px(906), "R3 container+boxes ink")

print()
print("highlight box target y", f"{px(363.9):.0f}..{px(525.9):.0f}", "x", f"{px(54.5):.0f}..{px(907.6):.0f}")
# fill color sample
fy, fx = int(px(445)), int(px(500))
print("hl fill sample:", tuple(im[fy,fx]), "vs target ~(232,252,250)")
fy2, fx2 = int(px(520)), int(px(700))
print("hl fill sample2:", tuple(im[fy2,fx2]))

print()
print("text lines target cap..base (render px):")
for nm, cap, base, x0, x1 in [
  ("lead", 384.8, 398.3, 64.9, 890.9), ("problems", 408.8, 421.3, 63.8, 142.9),
  ("b1", 431.8, 444.3, 99.2, 773.4), ("b2L1", 453.8, 466.3, 99.2, 896.2),
  ("b2L2", 476.8, 489.3, 84.7, 338.5), ("b3", 499.8, 512.3, 99.2, 754.6)]:
    print(f"  {nm}: y {px(cap):.0f}..{px(base):.0f} x {px(x0):.0f}..{px(x1):.0f}")
