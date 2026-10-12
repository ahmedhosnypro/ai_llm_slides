#!/usr/bin/env python3
"""Asset prep v3 for slide 030 (fixes v2: kill window covered only x346.. but the
cursor outline extends to x338; and the single-pass radius-2 fill left thick-K
interiors unfilled). v3:
  - kill lum<135 non-red inside x336..382, y385..432 (full cursor incl. shadow+halo);
  - ITERATIVE inward fill (radius-2 median of already-filled non-red neighbors,
    repeated until every killed px is filled) — red is never a fill source;
  - re-draw the bottom-right '1' via alpha blend of the clean top-right '1' (dy=+91);
  - crop right Sobel panel incl. baked border.
Banks numbers to out_assets3.txt."""
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

# sanity: cursor-copy source region must be cursor-free
srczone = (slice(308, 346), slice(350, 385))
sz_k = int(((~red[srczone]) & (lum[srczone] < 100)).sum())
logp(f"sanity: lum<100 non-red px in glyph-src zone x350..385 y308..346: {sz_k} (expect ~0)")

# ---------- 1. LEFT PHOTO crop (x105..442, y284..454 inclusive) ----------
L, T, Rt, Bo = 105, 284, 443, 455
photo = a[T:Bo, L:Rt].copy()
ph_h, ph_w = photo.shape[:2]
logp(f"left photo crop box=({L},{T},{Rt},{Bo}) size {ph_w}x{ph_h}")

pl = 0.299 * photo[:, :, 0] + 0.587 * photo[:, :, 1] + 0.114 * photo[:, :, 2]
pred = (photo[:, :, 0] > 130) & (photo[:, :, 1] < 90) & (photo[:, :, 2] < 90)

GX0, GX1, GY0, GY1 = 336, 382, 385, 432
lx0, lx1, ly0, ly1 = GX0 - L, GX1 - L, GY0 - T, GY1 - T
kill = np.zeros((ph_h, ph_w), bool)
kill[ly0:ly1 + 1, lx0:lx1 + 1] = (~pred[ly0:ly1 + 1, lx0:lx1 + 1]) & (pl[ly0:ly1 + 1, lx0:lx1 + 1] < 135)
logp(f"kill mask px: {int(kill.sum())} (lum<135 non-red in x{GX0}..{GX1} y{GY0}..{GY1})")

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
                if 0 <= ny < ph_h and 0 <= nx < ph_w and filled[ny, nx] and not pred[ny, nx]:
                    ys.append(ny); xs.append(nx)
        if ys:
            fill[y, x] = np.median(fill[ys, xs], axis=0)
            filled[y, x] = True
            newly += 1
    if newly == 0:
        logp(f"fill stalled at iter {it} with {int((~filled).sum())} px left")
        break
photo = fill
logp(f"iterative fill done after {it + 1} passes; unfilled left: {int((~filled).sum())}")

# ---- glyph '1' copy: top-right '1' -> bottom-right '1' (dy=+91) ----
SX0, SX1, SY0, SY1 = 356 - L, 380 - L, 312 - T, 343 - T
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
logp(f"residual lum<100 non-red px in cursor window: {resid} (expect 0)")
resid2 = int(((~crd[win]) & (cl[win] < 120)).sum())
logp(f"residual lum<120 non-red px in cursor window: {resid2}")
g3 = photo[405 - T:431 - T + 1, 357 - L:379 - L + 1]
g3r = (g3[:, :, 0] > 130) & (g3[:, :, 1] < 90) & (g3[:, :, 2] < 90)
g1 = photo[314 - T:340 - T + 1, 357 - L:379 - L + 1]
g1r = (g1[:, :, 0] > 130) & (g1[:, :, 1] < 90) & (g1[:, :, 2] < 90)
logp(f"bottom '1' red px after copy: {int(g3r.sum())} (top '1' in photo: {int(g1r.sum())})")
ys, xs = np.where(g3r)
logp(f"bottom '1' bbox local x[{xs.min()}..{xs.max()}] y[{ys.min()}..{ys.max()}]" if len(xs) else "bottom '1': EMPTY")
gz = photo[403 - T:435 - T, 381 - L:390 - L]
gzr = int(((gz[:, :, 0] > 130) & (gz[:, :, 1] < 90) & (gz[:, :, 2] < 90)).sum())
oz = a[403:435, 381:390]
ozr = int(((oz[:, :, 0] > 130) & (oz[:, :, 1] < 90) & (oz[:, :, 2] < 90)).sum())
logp(f"ghost zone x381..390 y403..435 red px: asset={gzr} original={ozr}")
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

with open(f"{QA}/out_assets3.txt", "w") as f:
    f.write("\n".join(log) + "\n")
print("assets v3 written")
