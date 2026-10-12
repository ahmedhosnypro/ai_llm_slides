#!/usr/bin/env python3
"""Asset prep v5 for slide 030 (v4 + sources exclude lum<100 (dark cursor remnant at x383..384 must not propagate) + kill window x388)
7x7 NON-RED median over every kill-mask px to vote out the dark anti-aliasing
halo of the row-2 '2' glyph that bled into the filled region)."""
import numpy as np
from PIL import Image

SRC = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_030.jpg"
ASSETS = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/build/assets"
QA = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/qa/slide030"

im = Image.open(SRC).convert("RGB")
a = np.asarray(im).astype(float)
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]
lum = 0.299 * R + 0.587 * G + 0.114 * B
red = (R > 130) & (G < 90) & (B < 90)

log = []
def logp(s):
    print(s); log.append(s)

# ---------- 1. LEFT PHOTO crop (x105..442, y284..454 inclusive) ----------
L, T, Rt, Bo = 105, 284, 443, 455
photo = a[T:Bo, L:Rt].copy()
ph_h, ph_w = photo.shape[:2]

pl = 0.299 * photo[:, :, 0] + 0.587 * photo[:, :, 1] + 0.114 * photo[:, :, 2]
pred = (photo[:, :, 0] > 130) & (photo[:, :, 1] < 90) & (photo[:, :, 2] < 90)

GX0, GX1, GY0, GY1 = 336, 388, 385, 432
lx0, lx1, ly0, ly1 = GX0 - L, GX1 - L, GY0 - T, GY1 - T
kill = np.zeros((ph_h, ph_w), bool)
kill[ly0:ly1 + 1, lx0:lx1 + 1] = (~pred[ly0:ly1 + 1, lx0:lx1 + 1]) & (pl[ly0:ly1 + 1, lx0:lx1 + 1] < 135)
logp(f"kill mask px: {int(kill.sum())}")

filled = ~kill.copy()
fill = photo.copy()
for it in range(80):
    todo = np.where(~filled)
    if len(todo[0]) == 0:
        break
    newly = 0
    for y, x in zip(todo[0].tolist(), todo[1].tolist()):
        ys, xs = [], []
        for dy in range(-2, 3):
            for dx in range(-2, 3):
                ny, nx = y + dy, x + dx
                if 0 <= ny < ph_h and 0 <= nx < ph_w and filled[ny, nx] and not pred[ny, nx] and fill[ny, nx].mean() >= 100:
                    ys.append(ny); xs.append(nx)
        if ys:
            fill[y, x] = np.median(fill[ys, xs], axis=0)
            filled[y, x] = True
            newly += 1
    if newly == 0:
        break
logp(f"iterative fill done after {it + 1} passes; unfilled left: {int((~filled).sum())}")

# post-fill smoothing: 7x7 NON-RED median over every killed px (votes out the
# dark '2'-glyph anti-aliasing halo that the inward fill propagated)
sm = photo.copy()
kys, kxs = np.where(kill)
for y, x in zip(kys.tolist(), kxs.tolist()):
    vals = []
    for dy in range(-3, 4):
        for dx in range(-3, 4):
            ny, nx = y + dy, x + dx
            if 0 <= ny < ph_h and 0 <= nx < ph_w and not pred[ny, nx] and fill[ny, nx].mean() >= 100:
                vals.append(fill[ny, nx])
    if vals:
        sm[y, x] = np.median(np.array(vals), axis=0)
photo = sm
logp("post-fill 7x7 non-red median applied over kill mask")

# ---- glyph '1' copy: top-right '1' -> bottom-right '1' (dy=+91) ----
SX0, SX1, SY0, SY1 = 356 - L, 380 - L, 312 - T, 343 - T
DY = 91
src = photo[SY0:SY1 + 1, SX0:SX1 + 1]
alpha = np.clip((src[:, :, 0] - src[:, :, 1]) / 150.0, 0, 1)[..., None]
dyy = SY0 + DY
dest = photo[dyy:dyy + src.shape[0], SX0:SX1 + 1]
photo[dyy:dyy + src.shape[0], SX0:SX1 + 1] = dest * (1 - alpha) + src * alpha
logp(f"glyph copy dy=+{DY} done")

# ---- verify ----
cl = 0.299 * photo[:, :, 0] + 0.587 * photo[:, :, 1] + 0.114 * photo[:, :, 2]
crd = (photo[:, :, 0] > 130) & (photo[:, :, 1] < 90) & (photo[:, :, 2] < 90)
win = (slice(ly0, ly1 + 1), slice(lx0, lx1 + 1))
resid = int(((~crd[win]) & (cl[win] < 100)).sum())
logp(f"residual lum<100 non-red px in cursor window: {resid}")
g3 = photo[405 - T:431 - T + 1, 357 - L:379 - L + 1]
g3r = (g3[:, :, 0] > 130) & (g3[:, :, 1] < 90) & (g3[:, :, 2] < 90)
g1 = photo[314 - T:340 - T + 1, 357 - L:379 - L + 1]
g1r = (g1[:, :, 0] > 130) & (g1[:, :, 1] < 90) & (g1[:, :, 2] < 90)
logp(f"bottom '1' red px after copy: {int(g3r.sum())} (top '1': {int(g1r.sum())})")
ys, xs = np.where(g3r)
logp(f"bottom '1' bbox local x[{xs.min()}..{xs.max()}] y[{ys.min()}..{ys.max()}]" if len(xs) else "bottom '1': EMPTY")
gz = photo[403 - T:435 - T, 381 - L:390 - L]
gzr = int(((gz[:, :, 0] > 130) & (gz[:, :, 1] < 90) & (gz[:, :, 2] < 90)).sum())
oz = a[403:435, 381:390]
ozr = int(((oz[:, :, 0] > 130) & (oz[:, :, 1] < 90) & (oz[:, :, 2] < 90)).sum())
logp(f"ghost zone red px: asset={gzr} original={ozr}")
bleed_a = int(crd[386 - T:402 - T, 334 - L:380 - L].sum())
bleed_o = int(red[386:402, 334:380].sum())
logp(f"red-bleed zone: asset={bleed_a} original={bleed_o}")
# '2' glyph integrity (row-2 col-3, y359..387 x357..379): red count must be unchanged
t2 = photo[359 - T:387 - T + 1, 357 - L:379 - L + 1]
t2r = int(((t2[:, :, 0] > 130) & (t2[:, :, 1] < 90) & (t2[:, :, 2] < 90)).sum())
o2 = a[359:387 + 1, 357:379 + 1]
o2r = int(((o2[:, :, 0] > 130) & (o2[:, :, 1] < 90) & (o2[:, :, 2] < 90)).sum())
logp(f"row-2 '2' red px: asset={t2r} original={o2r}")

Image.fromarray(photo.round().astype(np.uint8)).save(f"{ASSETS}/meme030_photo.png")

# ---------- 2. RIGHT PANEL crop incl. baked border (x534..884, y270..444) ----------
RL, RT, RRt, RBo = 534, 270, 885, 445
panel = a[RT:RBo, RL:RRt]
Image.fromarray(panel.round().astype(np.uint8)).save(f"{ASSETS}/sobel030_panel.png")
logp(f"right panel crop box=({RL},{RT},{RRt},{RBo}) size {panel.shape[1]}x{panel.shape[0]}")

with open(f"{QA}/out_assets5.txt", "w") as f:
    f.write("\n".join(log) + "\n")
print("assets v5 written")
