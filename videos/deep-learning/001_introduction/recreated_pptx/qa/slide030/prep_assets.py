#!/usr/bin/env python3
"""Asset prep for slide 030: crop left meme photo (Sobel matrix baked in) and inpaint
the screen-recording cursor artifact (spec exclusion step 17) by (a) bedding-filling
the cursor's dark outline and (b) re-drawing the bottom-right '1' glyph from the clean
top-right '1' (same glyph, same row position, alpha-blended). Crop the right Sobel
panel INCLUDING its baked red border. Banks verification numbers to out_assets.txt."""
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
    print(s)
    log.append(s)

# ---------- 1. LEFT PHOTO crop (x105..442, y284..454 inclusive) ----------
L, T, Rt, Bo = 105, 284, 443, 455   # PIL box: right/bottom exclusive
photo = a[T:Bo, L:Rt].copy()
ph, pw = photo.shape[:2]
logp(f"left photo crop box=({L},{T},{Rt},{Bo}) size {pw}x{ph}")

# ---- sample the cursor-window bedding (for threshold sanity) ----
# global cursor bbox x338..376 y388..426 -> local x233..271 y104..142
cx0, cx1, cy0, cy1 = 338 - L, 376 - L, 388 - T, 426 - T
win = photo[cy0:cy1 + 1, cx0:cx1 + 1]
wl = 0.299 * win[:, :, 0] + 0.587 * win[:, :, 1] + 0.114 * win[:, :, 2]
wred = (win[:, :, 0] > 130) & (win[:, :, 1] < 90) & (win[:, :, 2] < 90)
bed = wl[(~wred) & (wl > 190)]
logp(f"cursor window: {win.shape[0]}x{win.shape[1]}, non-red bright px n={len(bed)} "
     f"median={np.median(bed):.0f}" if len(bed) else "cursor window: no bright bedding px")

# ---- (a) inpaint dark (non-red) px in a slightly padded cursor window ----
px0, px1, py0, py1 = 334 - L, 380 - L, 386 - T, 430 - T
sub = photo[py0:py1 + 1, px0:px1 + 1]
sl = 0.299 * sub[:, :, 0] + 0.587 * sub[:, :, 1] + 0.114 * sub[:, :, 2]
sred = (sub[:, :, 0] > 130) & (sub[:, :, 1] < 90) & (sub[:, :, 2] < 90)
kill = (~sred) & (sl < 190)
logp(f"inpaint window {sub.shape[1]}x{sub.shape[0]}: killing {int(kill.sum())} dark non-red px")
# iterative neighbor fill (bedding is smooth/light)
fill = sub.copy()
known = ~kill
for it in range(60):
    if known.all():
        break
    newly = 0
    for y in range(fill.shape[0]):
        for x in range(fill.shape[1]):
            if known[y, x]:
                continue
            ys, xs = [], []
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    ny, nx = y + dy, x + dx
                    if 0 <= ny < fill.shape[0] and 0 <= nx < fill.shape[1] and known[ny, nx]:
                        ys.append(ny); xs.append(nx)
            if len(ys) >= 3:
                fill[y, x] = np.median(fill[ys, xs], axis=0)
                known[y, x] = True
                newly += 1
    if newly == 0:
        # relax: take any known neighbor
        for y in range(fill.shape[0]):
            for x in range(fill.shape[1]):
                if not known[y, x]:
                    for dy in (-2, -1, 1, 2):
                        for dx in (-2, -1, 1, 2):
                            ny, nx = y + dy, x + dx
                            if 0 <= ny < fill.shape[0] and 0 <= nx < fill.shape[1] and known[ny, nx]:
                                fill[y, x] = fill[ny, nx]; known[y, x] = True; break
                        if known[y, x]:
                            break
photo[py0:py1 + 1, px0:px1 + 1] = fill

# ---- (b) re-draw bottom-right '1' from top-right '1' (alpha blend on redness) ----
# top '1' global x357..379 y314..340 (use pad: x355..383, y310..344)
# bottom '1' global x357..379 y405..431 -> shift dy = +91
sx0, sx1, sy0, sy1 = 355 - L, 383 - L, 310 - T, 344 - T
dy = 91
src = photo[sy0:sy1 + 1, sx0:sx1 + 1]
sr, sg, sb = src[:, :, 0], src[:, :, 1], src[:, :, 2]
alpha = np.clip((sr - sg) / 150.0, 0, 1)[..., None]
dyy = dy  # local dest top = sy0 + dy
dest = photo[dyy:dyy + src.shape[0], sx0:sx1 + 1]
photo[dyy:dyy + src.shape[0], sx0:sx1 + 1] = dest * (1 - alpha) + src * alpha
logp(f"glyph '1' copied: src local x[{sx0}..{sx1}] y[{sy0}..{sy1}] -> dest y[{dyy}..{dyy + src.shape[0] - 1}] (global dy=+{dy})")

# ---- verify: no dark non-red px left in cursor window; glyph red count ----
chk = photo[py0:py1 + 1, px0:px1 + 1]
cl = 0.299 * chk[:, :, 0] + 0.587 * chk[:, :, 1] + 0.114 * chk[:, :, 2]
cred = (chk[:, :, 0] > 130) & (chk[:, :, 1] < 90) & (chk[:, :, 2] < 90)
resid = int(((~cred) & (cl < 150)).sum())
logp(f"post-inpaint residual dark non-red px (lum<150) in cursor window: {resid}")
g3 = photo[405 - T:431 - T + 1, 357 - L:379 - L + 1]
g3r = (g3[:, :, 0] > 130) & (g3[:, :, 1] < 90) & (g3[:, :, 2] < 90)
g1 = photo[314 - T:340 - T + 1, 357 - L:379 - L + 1]
g1r = (g1[:, :, 0] > 130) & (g1[:, :, 1] < 90) & (g1[:, :, 2] < 90)
logp(f"bottom '1' red px after copy: {int(g3r.sum())} (top '1' reference: {int(g1r.sum())})")
# glyph bbox check
ys, xs = np.where(g3r)
logp(f"bottom '1' bbox local x[{xs.min()}..{xs.max()}] y[{ys.min()}..{ys.max()}]"
     if len(xs) else "bottom '1': EMPTY")

Image.fromarray(photo.round().astype(np.uint8)).save(f"{ASSETS}/meme030_photo.png")

# ---------- 2. RIGHT PANEL crop incl. baked border (x534..884, y270..444) ----------
RL, RT, RRt, RBo = 534, 270, 885, 445
panel = a[RT:RBo, RL:RRt]
Image.fromarray(panel.round().astype(np.uint8)).save(f"{ASSETS}/sobel030_panel.png")
pl = 0.299 * panel[:, :, 0] + 0.587 * panel[:, :, 1] + 0.114 * panel[:, :, 2]
logp(f"right panel crop box=({RL},{RT},{RRt},{RBo}) size {panel.shape[1]}x{panel.shape[0]}")
logp(f"right panel: dark(lum<80) px={int((pl < 80).sum())}, red px={int(((panel[:,:,0]>130)&(panel[:,:,1]<90)&(panel[:,:,2]<90)).sum())}")

with open(f"{QA}/out_assets.txt", "w") as f:
    f.write("\n".join(log) + "\n")
print("assets written")
