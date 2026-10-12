#!/usr/bin/env python3
"""Self-check attempt 1 for slide 040: closed-loop geometry of the 150dpi render
(2001x1125, scale 150/72 = 2.0833 render-px per frame-px) vs the ORIGINAL frame's
PIL-measured ink. Tolerance ~4 frame-px (8.3 render-px)."""
import numpy as np
from PIL import Image

REN = np.asarray(Image.open(
    "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/qa/slide040/render_1.png"
).convert("RGB")).astype(int)
H, W = REN.shape[:2]
S = 150 / 72.0
r, g, b = REN[:, :, 0], REN[:, :, 1], REN[:, :, 2]
fails = []

def fr(v):  # render px -> frame px
    return v / S

def check(name, got, want, tol=4.0):
    d = abs(got - want)
    ok = d <= tol
    if not ok:
        fails.append(f"{name}: got {got:.1f} want {want} (delta {d:.1f} frame-px > tol {tol})")
    print(f"{'PASS' if ok else 'FAIL'}  {name}: got {got:.1f} want {want} (delta {d:.1f})")

# ---------- title ----------
red = (r > 120) & (g < 110) & (b < 110)
tmask = np.zeros_like(red)
tmask[int(60 * S):int(135 * S), int(60 * S):int(870 * S)] = red[int(60 * S):int(135 * S), int(60 * S):int(870 * S)]
ys, xs = np.where(tmask)
if not len(xs):
    fails.append("title: NO red ink found"); print("FAIL title ink missing")
else:
    print(f"title ink (frame px): x {fr(xs.min()):.1f}..{fr(xs.max()):.1f} y {fr(ys.min()):.1f}..{fr(ys.max()):.1f}")
    check("title x-left", fr(xs.min()), 204)
    check("title x-right", fr(xs.max()), 762)
    check("title ink-top", fr(ys.min()), 80, 4.5)
    # baseline: strong rows
    rowsum = tmask.sum(axis=1)
    strong = np.where(rowsum > 0.4 * rowsum.max())[0]
    check("title baseline", fr(strong.max()), 104, 4.5)

# ---------- navy text lines ----------
navy = (b > 90) & (r < 110) & (g < 110) & (b > r + 30) & (b > g + 30)
nmask = np.zeros_like(navy)
y0, y1 = int(350 * S), int(500 * S)
x0, x1 = int(60 * S), int(700 * S)
nmask[y0:y1, x0:x1] = navy[y0:y1, x0:x1]
rows = np.where(nmask.sum(axis=1) > 2)[0]
bands = []
if len(rows):
    s = p = rows[0]
    for c in rows[1:]:
        if c - p <= 6:
            p = c
        else:
            bands.append((s, p)); s = p = c
    bands.append((s, p))
print(f"navy bands (frame px): {[(round(fr(a),1), round(fr(bb),1)) for a, bb in bands]}")
want_bands = [(371, 391), (397, 417), (440, 459), (466, 486)]
if len(bands) != 4:
    fails.append(f"navy lines: {len(bands)} bands, want 4")
else:
    for i, (a, bb) in enumerate(bands):
        check(f"L{i+1} band-top", fr(a), want_bands[i][0], 4.5)
        check(f"L{i+1} band-bot", fr(bb), want_bands[i][1], 4.5)
    # widths: ink x-range per band
    want_w = [282, 549, 529, 421]
    want_x0 = [83, 84, 84, 83]
    for i, (a, bb) in enumerate(bands):
        xs_b = np.where(nmask[a:bb + 1].sum(axis=0) > 0)[0]
        w_fr = fr(xs_b.max() - xs_b.min() + 1)
        check(f"L{i+1} ink-width", w_fr, want_w[i], 5.0)
        check(f"L{i+1} ink-left", fr(xs_b.min()), want_x0[i], 4.5)

# ---------- yellow box ----------
fill = (r > 240) & (g > 240) & (b > 210) & (b < 246)
fm = np.zeros_like(fill)
fm[int(340 * S):int(510 * S), int(60 * S):int(700 * S)] = fill[int(340 * S):int(510 * S), int(60 * S):int(700 * S)]
ys, xs = np.where(fm)
if not len(xs):
    fails.append("yellow box: no fill found"); print("FAIL yellow fill missing")
else:
    print(f"yellow fill (frame px): x {fr(xs.min()):.1f}..{fr(xs.max()):.1f} y {fr(ys.min()):.1f}..{fr(ys.max()):.1f}")
    check("box fill-left", fr(xs.min()), 76, 4.5)
    check("box fill-right", fr(xs.max()), 684, 4.5)
    check("box fill-top", fr(ys.min()), 365, 4.5)
    check("box fill-bottom", fr(ys.max()), 489, 4.5)
# border color sample (top stroke)
bx, by = int(300 * S), int(362.5 * S)
patch = REN[by - 4:by + 5, bx - 40:bx + 40].reshape(-1, 3)
dark = patch[patch.sum(axis=1).argsort()[:20]].mean(axis=0)
print(f"box top stroke darkest ~ #{int(dark[0]):02X}{int(dark[1]):02X}{int(dark[2]):02X} (want ~A59FC3)")

# ---------- photos (pixel-exact embeds) ----------
nonbg = (np.abs(r - 233) > 22) | (np.abs(g - 233) > 22) | (np.abs(b - 231) > 22)
for label, (X0, X1, Y0, Y1) in {
    "cat": (90, 410, 148, 326),
    "dog": (425, 738, 150, 326),
    "grid": (718, 895, 344, 504),
}.items():
    sub = nonbg[int(Y0 * S):int(Y1 * S), int(X0 * S):int(X1 * S)]
    ys, xs = np.where(sub)
    if not len(xs):
        fails.append(f"{label}: image missing"); print(f"FAIL {label} missing")
        continue
    gx0, gx1 = fr(xs.min() + X0 * S), fr(xs.max() + X0 * S)
    gy0, gy1 = fr(ys.min() + Y0 * S), fr(ys.max() + Y0 * S)
    print(f"{label} content: x {gx0:.1f}..{gx1:.1f} y {gy0:.1f}..{gy1:.1f}")
    check(f"{label} left", gx0, {"cat": 97, "dog": 432, "grid": 725}[label], 3.0)
    check(f"{label} top", gy0, {"cat": 155, "dog": 158, "grid": 351}[label], 3.0)
    check(f"{label} right", gx1, {"cat": 403, "dog": 731, "grid": 888}[label], 3.0)
    check(f"{label} bottom", gy1, {"cat": 319, "dog": 319, "grid": 497}[label], 3.0)

# ---------- arrow ----------
redm = np.zeros_like(red)
redm[int(410 * S):int(455 * S), int(660 * S):int(724 * S)] = red[int(410 * S):int(455 * S), int(660 * S):int(724 * S)]
ys, xs = np.where(redm)
if not len(xs):
    fails.append("arrow: no red outline"); print("FAIL arrow missing")
else:
    print(f"arrow red (frame px): x {fr(xs.min()):.1f}..{fr(xs.max()):.1f} y {fr(ys.min()):.1f}..{fr(ys.max()):.1f}")
    check("arrow left", fr(xs.min()), 674, 4.5)
    check("arrow right", fr(xs.max()), 716, 5.0)
    check("arrow top", fr(ys.min()), 423, 4.5)
    check("arrow bottom", fr(ys.max()), 440, 4.5)
white = (r > 248) & (g > 248) & (b > 248)
wm = np.zeros_like(white)
wm[int(410 * S):int(455 * S), int(660 * S):int(724 * S)] = white[int(410 * S):int(455 * S), int(660 * S):int(724 * S)]
ys, xs = np.where(wm)
print(f"arrow white fill px: {len(xs)} (want > 50)")

# ---------- wrap/containment: no ink below L4 band or left of box ----------
band = nmask[int(495 * S):int(510 * S), :]
if band.sum() > 5:
    fails.append("ink found below L4 band (possible wrap/overflow)")
print(f"ink below L4 (y 495..510 frame): {int(band.sum())} px")

print()
if fails:
    print("SELF-CHECK: FAIL")
    for f in fails:
        print("  -", f)
    raise SystemExit(1)
print("SELF-CHECK: ALL PASS")
