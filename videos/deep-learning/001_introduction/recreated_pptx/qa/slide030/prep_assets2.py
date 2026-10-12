#!/usr/bin/env python3
"""Asset prep v2 for slide 030 (fixes v1's red-bleed: v1 killed lum<190 across the
whole cursor window and flood-filled, smearing the mid-dark photo background and
propagating red from the row-2 '2' glyph).
v2: (a) kill ONLY near-black non-red px (lum<130) inside the tight cursor bbox
        x346..380 y386..430, fill each from a LOCAL radius-2 median of non-killed,
        NON-RED neighbors (red px are never fill sources);
    (b) re-draw the bottom-right '1' (cursor-notched) by alpha-blending the clean
        top-right '1' (src x356..380 y312..343, dy=+91), alpha from redness only;
    (c) crop right Sobel panel incl. baked border (unchanged from v1).
Verifies residuals + ghost-red counts and banks to out_assets2.txt."""
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
logp(f"left photo crop box=({L},{T},{Rt},{Bo}) size {ph_w}x{ph_h}")

# ---- (a) tight cursor inpaint ----
GX0, GX1, GY0, GY1 = 346, 380, 386, 430     # tight cursor bbox (global, incl. halo)
lx0, lx1, ly0, ly1 = GX0 - L, GX1 - L, GY0 - T, GY1 - T
pl = 0.299 * photo[:, :, 0] + 0.587 * photo[:, :, 1] + 0.114 * photo[:, :, 2]
pred = (photo[:, :, 0] > 130) & (photo[:, :, 1] < 90) & (photo[:, :, 2] < 90)
kill = np.zeros((ph_h, ph_w), bool)
kill[ly0:ly1 + 1, lx0:lx1 + 1] = (~pred[ly0:ly1 + 1, lx0:lx1 + 1]) & (pl[ly0:ly1 + 1, lx0:lx1 + 1] < 130)
logp(f"kill mask px: {int(kill.sum())} (near-black non-red in x{GX0}..{GX1} y{GY0}..{GY1})")

fill = photo.copy()
known = ~kill
for y in range(ph_h):
    for x in range(ph_w):
        if kill[y, x]:
            ys, xs = [], []
            for dy in range(-2, 3):
                for dx in range(-2, 3):
                    ny, nx = y + dy, x + dx
                    if 0 <= ny < ph_h and 0 <= nx < ph_w and known[ny, nx] and not pred[ny, nx]:
                        ys.append(ny); xs.append(nx)
            if ys:
                fill[y, x] = np.median(fill[ys, xs], axis=0)
known = known | kill  # second pass: now use filled values too (smoother halo)
photo = fill
logp("inpaint pass 1 done (local radius-2 median, red excluded as source)")

# ---- (b) glyph '1' copy: top-right '1' -> bottom-right '1' (dy=+91) ----
SX0, SX1, SY0, SY1 = 356 - L, 380 - L, 312 - T, 343 - T   # local, clamped to glyph + 1px halo
DY = 91
src = photo[SY0:SY1 + 1, SX0:SX1 + 1]
alpha = np.clip((src[:, :, 0] - src[:, :, 1]) / 150.0, 0, 1)[..., None]
dyy = SY0 + DY
dest = photo[dyy:dyy + src.shape[0], SX0:SX1 + 1]
photo[dyy:dyy + src.shape[0], SX0:SX1 + 1] = dest * (1 - alpha) + src * alpha
logp(f"glyph copy: src local x[{SX0}..{SX1}] y[{SY0}..{SY1}] -> dest y[{dyy}..{dyy + src.shape[0] - 1}] (global dy=+{DY})")

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
logp(f"bottom '1' red px after copy: {int(g3r.sum())} (top '1' in photo: {int(g1r.sum())})")
ys, xs = np.where(g3r)
logp(f"bottom '1' bbox local x[{xs.min()}..{xs.max()}] y[{ys.min()}..{ys.max()}]" if len(xs) else "bottom '1': EMPTY")
# ghost check: red in x381..390, y403..435 (should match original's count there)
gzone = photo[403 - T:435 - T, 381 - L:390 - L]
gzr = (gzone[:, :, 0] > 130) & (gzone[:, :, 1] < 90) & (gzone[:, :, 2] < 90)
oz = a[403:435, 381:390]
ozr = (oz[:, :, 0] > 130) & (oz[:, :, 1] < 90) & (oz[:, :, 2] < 90)
logp(f"ghost zone x381..390 y403..435 red px: asset={int(gzr.sum())} original={int(ozr.sum())}")
# red-bleed check above the glyph: x334..380 y386..402 red counts
bleed_a = int(crd[386 - T:402 - T, 334 - L:380 - L].sum())
bleed_o = int(red[386:402, 334:380].sum())
logp(f"red-bleed zone x334..380 y386..402: asset={bleed_a} original={bleed_o}")

Image.fromarray(photo.round().astype(np.uint8)).save(f"{ASSETS}/meme030_photo.png")

# ---------- 2. RIGHT PANEL crop incl. baked border (x534..884, y270..444) ----------
RL, RT, RRt, RBo = 534, 270, 885, 445
panel = a[RT:RBo, RL:RRt]
Image.fromarray(panel.round().astype(np.uint8)).save(f"{ASSETS}/sobel030_panel.png")
pl2 = 0.299 * panel[:, :, 0] + 0.587 * panel[:, :, 1] + 0.114 * panel[:, :, 2]
logp(f"right panel crop box=({RL},{RT},{RRt},{RBo}) size {panel.shape[1]}x{panel.shape[0]}")
logp(f"right panel: dark(lum<80) px={int((pl2 < 80).sum())}, red px={int(((panel[:,:,0]>130)&(panel[:,:,1]<90)&(panel[:,:,2]<90)).sum())}")

with open(f"{QA}/out_assets2.txt", "w") as f:
    f.write("\n".join(log) + "\n")
print("assets v2 written")
