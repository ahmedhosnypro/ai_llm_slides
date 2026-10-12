#!/usr/bin/env python3
"""Closed-loop PIL ink check v3 (attempt 2): render_2 (150dpi, 2000x1125).
v2 + NEW rotated-label strip checks (the v2 gap that let the IN(IN()) unit bug
through: rotated 'Scaling by sqrt(d)' / 'Mask' / 'Soft max' must land at their
intended frame-strip centers, not at center+w/2)."""
from PIL import Image
import numpy as np

REN = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide054/render_2.png"
A = np.asarray(Image.open(REN).convert("RGB")).astype(int)
H, W, _ = A.shape
R, G, B = A[..., 0], A[..., 1], A[..., 2]
X0, SX, SY = 18.63, 0.96123, 0.95556
K = 150 / 72.0

def tgt(fx0, fy0, fx1, fy1):
    return [(fx0 - X0) / SX * K, fy0 / SY * K, (fx1 - X0) / SX * K, fy1 / SY * K]

def bbox_in(x0, y0, x1, y1, mask_fn, pad=4):
    x0, y0, x1, y1 = int(x0 - pad), int(y0 - pad), int(x1 + pad), int(y1 + pad)
    x0 = max(0, x0); y0 = max(0, y0); x1 = min(W, x1); y1 = min(H, y1)
    sub = A[y0:y1, x0:x1]
    m = mask_fn(sub[..., 0], sub[..., 1], sub[..., 2])
    ys, xs = np.where(m)
    if len(ys) == 0: return None
    return [x0 + xs.min(), y0 + ys.min(), x0 + xs.max(), y0 + ys.max(), int(m.sum())]

is_red    = lambda r,g,b: (r-g>=60)&(r-b>=50)&(r>=140)
is_dark   = lambda r,g,b: (r<120)&(g<120)&(b<120)
is_yellow = lambda r,g,b: (r>=215)&(g>=215)&(r-b>=40)
is_blue   = lambda r,g,b: (b-r>=50)&(b>=120)
is_green  = lambda r,g,b: (g-r>=18)&(g-b>=18)&(g>=150)
is_navy   = lambda r,g,b: (b-r>=60)&(b>=110)&(r<120)
is_mag    = lambda r,g,b: (r>=185)&(b>=185)&(g<=185)&(r-g>=30)
is_wvpink = lambda r,g,b: (abs(r-242)<=16)&(abs(g-188)<=24)&(abs(b-216)<=16)
is_tan    = lambda r,g,b: (abs(r-216)<=20)&(abs(g-200)<=20)&(abs(b-185)<=20)&(r-b>=15)
is_purple = lambda r,g,b: (b-g>=50)&(r-g>=30)&(b>=120)&(r<200)&(g<130)

checks = [
    ("title(red)",          (97, 66, 577, 84),    is_red),
    ("chip1(-inf)",         (731, 64, 763, 84),   is_yellow),
    ("chip3(empty)",        (806, 59, 838, 75),   is_yellow),
    ("left_container",      (78, 219, 153, 379),  is_green),
    ("wk_boxes",            (175, 228, 202, 368), is_green),
    ("dotproduct_box",      (265, 189, 347, 385), is_tan),
    ("dots(navy)",          (281, 233, 342, 363), is_navy),
    ("fraction(red)",       (421, 187, 448, 218), is_red),
    ("mask_col",            (456, 191, 484, 385), is_green),
    ("mask_cells(yellow)",  (459, 231, 478, 364), is_yellow),
    ("ellipse(dark)",       (432, 390, 506, 434), is_dark),
    ("sigma_glyph(navy)",   (601, 193, 610, 206), is_navy),
    ("output_box(green)",   (570, 114, 628, 139), is_green),
    ("nodes(red)",          (548, 228, 660, 360), is_red),
    ("wv_boxes(blue)",      (706, 226, 736, 371), is_blue),
    ("right_container",     (752, 220, 827, 379), is_green),
    ("bottom_container",    (193, 457, 490, 495), is_green),
    ("magenta_Z2",          (277, 466, 335, 483), is_mag),
    ("wq_box(pink)",        (278, 416, 317, 448), is_wvpink),
    ("legend_box(green)",   (725, 448, 887, 512), is_green),
    ("legend_caption(navy)",(775, 499, 853, 507), is_blue),
    ("legend_Wbox(yellow)", (784, 455, 811, 482), is_yellow),
    # NEW v3: rotated label strips (ink must sit at the INTENDED frame strip)
    ("rot_scaling(red)",    (386, 250, 410, 356), is_red),      # strip frame x 386..410, y ~250..356
    ("rot_mask(green)",     (464, 194, 478, 226), is_green),     # strip frame x 464..478, y 194..226
    ("rot_softmax(purple)", (515, 240, 531, 286), is_purple),    # strip frame x 515..531, y 240..286
    ("sigma_glyph2(purple)",(514, 288, 531, 322), is_purple),    # large final-sigma glyph
]

print(f"{'check':24s} {'target px':36s} {'measured px':36s} {'dL dT dR dB':26s} verdict")
fails = 0
for name, fbox, mask in checks:
    t = tgt(*fbox)
    m = bbox_in(t[0], t[1], t[2], t[3], mask, pad=5)
    if m is None:
        print(f"{name:24s} MISSING INK  <-- FAIL"); fails += 1; continue
    d = [m[0]-t[0], m[1]-t[1], m[2]-t[2], m[3]-t[3]]
    ok = all(abs(v) <= 6 for v in d)
    if not ok: fails += 1
    print(f"{name:24s} [{t[0]:6.1f},{t[1]:6.1f},{t[2]:6.1f},{t[3]:6.1f}] "
          f"[{m[0]:6d},{m[1]:6d},{m[2]:6d},{m[3]:6d}] [{d[0]:+5.1f},{d[1]:+5.1f},{d[2]:+5.1f},{d[3]:+5.1f}] {'OK' if ok else 'CHECK'}")

# containment: no stray ink beyond the chrome panel
zones = {
    "left":  (0, 0, int((56 - X0) / SX * K), H),
    "right": (int((905 - X0) / SX * K), 0, W, H),
    "top":   (0, 0, W, int(39 / SY * K)),
}
print("\ncontainment vs house panel:")
for zn, (zx0, zy0, zx1, zy1) in zones.items():
    sub = A[max(0,zy0):min(H,zy1), max(0,zx0):min(W,zx1)]
    for nm, mk in {"red": is_red, "dark": is_dark}.items():
        n = int(mk(sub[...,0], sub[...,1], sub[...,2]).sum())
        flag = "OK" if n < 40 else "STRAY INK"
        if n >= 40: fails += 1
        print(f"  {nm}/{zn}: {n}px {flag}")
print(f"\nTOTAL FAILS: {fails}")
