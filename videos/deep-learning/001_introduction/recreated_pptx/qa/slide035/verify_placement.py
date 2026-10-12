#!/usr/bin/env python3
"""verify_placement.py — prove the two baked crops land at exact frame positions:
downscale the render by 150/72 to frame scale and diff against the assets 1:1."""
import numpy as np
from PIL import Image

REND = "videos/deep-learning/001_introduction/recreated_pptx/qa/slide035/render_1.png"
ASSETS = "videos/deep-learning/001_introduction/recreated_pptx/build/assets"
im = Image.open(REND).convert("RGB")
S = 150 / 72.0
# render is 2001x1125 for 13.333in; frame-scale image = render / S
rw, rh = im.size
fw, fh = int(round(rw / S)), int(round(rh / S))
fs = im.resize((fw, fh), Image.LANCZOS)
fa = np.asarray(fs).astype(int)
print(f"render {rw}x{rh} -> frame-scale {fw}x{fh}")

for name, (x0, y0, w, h) in [("leftgrid035.png", (77, 207, 167, 131)),
                              ("panelcontent035.png", (398, 185, 478, 236))]:
    asset = np.asarray(Image.open(f"{ASSETS}/{name}").convert("RGB")).astype(int)
    win = fa[y0:y0+h, x0:x0+w]
    d = np.abs(win - asset)
    mad = d.mean()
    p99 = np.percentile(d, 99)
    big = (d.sum(axis=2) > 90).sum()
    print(f"{name}: placed at ({x0},{y0}) size {w}x{h} -> MAD={mad:.2f} p99={p99:.0f} px>90diff={big} ({100*big/(w*h):.2f}%)")

# search for best offset of panelcontent if MAD high (placement error detector)
asset = np.asarray(Image.open(f"{ASSETS}/panelcontent035.png").convert("RGB")).astype(int)
best = None
for dy in range(-4, 5):
    for dx in range(-4, 5):
        win = fa[185+dy:185+dy+236, 398+dx:398+dx+478]
        m = np.abs(win - asset).mean()
        if best is None or m < best[0]:
            best = (m, dx, dy)
print(f"panelcontent best offset: dx={best[1]} dy={best[2]} MAD={best[0]:.2f}")

# caption L1/L2 clean re-measure (zones away from the box border)
r = np.asarray(im).astype(int)
RR, GG, BB = r[:, :, 0], r[:, :, 1], r[:, :, 2]
navy = (BB - RR > 40) & (BB > 100)  # strict navy (excludes border #9797B2: BB-RR=26)
z = np.zeros((r.shape[0], r.shape[1]), bool)
z[int(452*S):int(478*S), int(74*S):int(886*S)] = True
ys, xs = np.where(navy & z)
if len(xs):
    print(f"L1 navy text: x{xs.min()}..{xs.max()} y{ys.min()}..{ys.max()} (target frame x78..881 y454..476 -> render {78*S:.0f}..{881*S:.0f} y{454*S:.0f}..{476*S:.0f})")
z = np.zeros((r.shape[0], r.shape[1]), bool)
z[int(478*S):int(505*S), int(80*S):int(520*S)] = True
red2 = (RR - GG > 50) & (RR - BB > 50) & (RR > 110)
ys, xs = np.where(red2 & z)
if len(xs):
    print(f"L2 red text: x{xs.min()}..{xs.max()} y{ys.min()}..{ys.max()} (target frame x92..479 y480..502 -> render {92*S:.0f}..{479*S:.0f} y{480*S:.0f}..{502*S:.0f})")
# L2 navy parens
z = np.zeros((r.shape[0], r.shape[1]), bool)
z[int(478*S):int(505*S), int(80*S):int(100*S)] = True
ys, xs = np.where(navy & z)
if len(xs):
    print(f"L2 '(' navy: x{xs.min()}..{xs.max()} y{ys.min()}..{ys.max()} (target frame x84..92 y481..500)")
# title clean
red3 = (RR - GG > 80) & (RR - BB > 80) & (RR > 130)
z = np.zeros((r.shape[0], r.shape[1]), bool)
z[int(55*S):int(115*S), int(200*S):int(800*S)] = True
ys, xs = np.where(red3 & z)
print(f"title: x{xs.min()}..{xs.max()} y{ys.min()}..{ys.max()} (target frame x266..713 y70..99 -> render {266*S:.0f}..{713*S:.0f} y{70*S:.0f}..{99*S:.0f})")
# badge numeral center check
d = (RR < 110) & (GG < 110) & (BB < 110)
z = np.zeros((r.shape[0], r.shape[1]), bool)
z[int(53*S):int(90*S), int(875*S):int(912*S)] = True
ys, xs = np.where(d & z)
if len(xs):
    cy = (ys.min() + ys.max()) / 2 / S
    cx = (xs.min() + xs.max()) / 2 / S
    print(f"badge numeral center (frame): ({cx:.1f},{cy:.1f}) — badge center target (893,71)")
