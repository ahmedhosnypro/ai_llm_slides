#!/usr/bin/env python3
"""Read-only adjudication of the concurrent worker's render_1.png vs the frame.
Checks the disputed elements: orange heads, K.q position, title y, X2 highlight
color, W-box fills, circle tint, q2 position, node fills."""
import numpy as np
from PIL import Image

R = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide008/render_1.png"
F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_008.jpg"
ren = np.asarray(Image.open(R).convert("RGB")).astype(int)
frm = np.asarray(Image.open(F).convert("RGB")).astype(int)
print("render size:", ren.shape, "frame size:", frm.shape)
RH, RW = ren.shape[:2]  # ~2001x1125 at 150dpi; frame 960x540
sc = RH / 540.0  # render px per frame px (~2.08)

def rpx(fx, fy):
    return ren[int(fy * sc), int(fx * sc)]

# 1) orange heads in the render? (frame has none)
r_, g_, b_ = ren[:, :, 0], ren[:, :, 1], ren[:, :, 2]
orange = (r_ > 140) & (g_ > 70) & (g_ < 160) & (b_ < 90) & (r_ - g_ > 40)
ys, xs = np.where(orange)
print("render orange px:", len(xs), ("bbox x %d..%d y %d..%d" % (xs.min(), xs.max(), ys.min(), ys.max())) if len(xs) else "")
# frame-side expected head zones in render px: left heads frame x 152..162, rows y ~236.5 etc.
for (fx0, fx1, fy) in [(150, 165, 236.5), (725, 742, 236.5)]:
    win = orange[int(fy * sc) - 20:int(fy * sc) + 20, int(fx0 * sc):int(fx1 * sc)]
    print(f"  orange in render near frame ({fx0}..{fx1}, y~{fy}): {int(win.sum())} px")

# 2) K.q ink position in render vs frame: red text right of DP box (frame x 345..375, y 190..215)
def ink_bbox(im, x0, x1, y0, y1, thresh=110):
    sub = im[y0:y1, x0:x1]
    m = (sub[:, :, 0] > 120) & (sub[:, :, 0] - sub[:, :, 1] > 50) & (sub[:, :, 0] - sub[:, :, 2] > 40)
    ys, xs = np.where(m)
    if not len(xs): return None
    return (x0 + xs.min(), x0 + xs.max(), y0 + ys.min(), y0 + ys.max(), len(xs))
fb = ink_bbox(frm, 340, 385, 185, 215)
rb = ink_bbox(ren, int(340 * sc), int(385 * sc), int(185 * sc), int(215 * sc))
print("K.q ink frame:", fb, " render:", rb, "(render px; /2.083 -> frame px)")

# 3) title L1 ink top in render vs frame: frame rows ~53..73 (L1), render ~y 110..152
def row_ink(im, y0, y1, x0, x1):
    sub = im[y0:y1, x0:x1]
    dk = (sub.sum(axis=2) < 330)
    rows = np.where(dk.sum(axis=1) > 8)[0]
    return (y0 + rows.min(), y0 + rows.max()) if len(rows) else None
ft = row_ink(frm, 45, 100, 200, 760)
rt = row_ink(ren, int(45 * sc), int(100 * sc), int(200 * sc), int(760 * sc))
print("title band ink rows frame:", ft, " render (frame-px):", (rt[0] / sc, rt[1] / sc) if rt else None)

# 4) X2 highlight color: render at the highlight ring (frame x ~334, y ~471) vs frame
print("highlight px render @frame(334,471):", tuple(rpx(334, 471)), " frame:", tuple(frm[471, 334]))
print("highlight px render @frame(289,477):", tuple(rpx(289, 477)), " frame:", tuple(frm[477, 289]))

# 5) W-box fills: render @ frame(180, 240) etc.
for (fx, fy, nm) in [(180, 240, "W_k r1"), (710, 240, "W_v r1"), (180, 285, "W_k r2")]:
    print(f"{nm}: render {tuple(rpx(fx, fy))} vs frame {tuple(frm[fy, fx])}")

# 6) circle tint over peach: frame (262, 415) inside circle left arc
print("circle tint: render @frame(262,415):", tuple(rpx(262, 415)), " frame:", tuple(frm[415, 262]))
print("circle tint: render @frame(350,400):", tuple(rpx(350, 400)), " frame:", tuple(frm[400, 350]))

# 7) q2 label ink: frame window x 278..312, y 380..400 (their claim: ink 383..395)
fb2 = ink_bbox(frm, 276, 315, 378, 402, thresh=110)
rb2 = ink_bbox(ren, int(276 * sc), int(315 * sc), int(378 * sc), int(402 * sc))
print("q2-region darkred ink frame:", fb2, " render:", rb2)

# 8) node interior fill: render @ frame node centers
for (cx, cy) in [(532, 246), (563, 288)]:
    fx = (cx - 17.628) / 0.961232
    fy = cy * 0.955556
    print(f"node @slide({cx},{cy}) frame({fx:.0f},{fy:.0f}): render {tuple(rpx(fx, fy))} frame {tuple(frm[int(fy), int(fx)])}")

# 9) whole-render vs whole-frame coarse diff heatmap (downsampled 4x) to find biggest zones
small_r = np.asarray(Image.open(R).convert("RGB").resize((240, 135))).astype(int)
small_f = np.asarray(Image.open(F).convert("RGB").resize((240, 135))).astype(int)
d = np.abs(small_r - small_f).sum(axis=2)
print("coarse diff: mean", d.mean().round(1), "max", d.max())
ys, xs = np.where(d > 120)
if len(ys):
    print("high-diff cells (frame-px approx):", [(int(x * 4), int(y * 4)) for y, x in zip(ys[:20], xs[:20])])
