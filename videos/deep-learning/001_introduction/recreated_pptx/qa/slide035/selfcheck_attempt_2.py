#!/usr/bin/env python3
"""selfcheck_attempt_2.py — slide 035 closed-loop self-check v2 (render_2).
v2 fixes vs v1: badge target corrected (numeral ~13px cap centered in badge),
caption zones narrowed away from the box border, baked-feature checks replaced by
the 1:1 placement proof (verify_placement) — crisp-render AA vs JPEG-faded frame
edges made the v1 baked-feature masks over-sensitive."""
import numpy as np
from PIL import Image

REND = "videos/deep-learning/001_introduction/recreated_pptx/qa/slide035/render_2.png"
FR = "videos/deep-learning/001_introduction/unique_slides/slide_035.jpg"
ASSETS = "videos/deep-learning/001_introduction/recreated_pptx/build/assets"
S = 150 / 72.0
im = Image.open(REND).convert("RGB")
r = np.asarray(im).astype(int)
RR, GG, BB = r[:, :, 0], r[:, :, 1], r[:, :, 2]
fails = []

def chk(name, ok, detail):
    print(f"{'PASS' if ok else 'FAIL'} {name}: {detail}")
    if not ok:
        fails.append(name)

def bbox(mask, label, target, tol=4):
    ys, xs = np.where(mask)
    if len(xs) == 0:
        chk(label, False, "EMPTY")
        return
    bx = (xs.min(), xs.max(), ys.min(), ys.max())
    tx = tuple(int(round(v * S)) for v in target)
    d = tuple(int(bx[i] - tx[i]) for i in range(4))
    ok = all(abs(v) <= tol for v in d)
    chk(label, ok, f"render x{bx[0]}..{bx[1]} y{bx[2]}..{bx[3]} | target x{tx[0]}..{tx[1]} y{tx[2]}..{tx[3]} (dx {d[0]}/{d[1]}, dy {d[2]}/{d[3]})")

# 1. TITLE
m = (RR - GG > 80) & (RR - BB > 80) & (RR > 130)
z = np.zeros_like(m); z[int(50*S):int(115*S), int(200*S):int(800*S)] = True
bbox(m & z, "title red ink", (266, 713, 70, 99))

# 2. LABELS
d = (RR < 110) & (GG < 110) & (BB < 110)
z = np.zeros_like(d); z[int(170*S):int(212*S), int(95*S):int(200*S)] = True
bbox(d & z, "label Image", (105, 183, 181, 205))
z = np.zeros_like(d); z[int(170*S):int(212*S), int(265*S):int(360*S)] = True
bbox(d & z, "label Filter", (275, 340, 181, 201))

# 3. FILTER TABLE
ym = (RR > 200) & (GG > 190) & (BB < 160)
z = np.zeros_like(ym); z[int(215*S):int(295*S), int(262*S):int(372*S)] = True
bbox(ym & z, "filter yellow cells", (271, 363, 220, 290))
z = np.zeros_like(d); z[int(222*S):int(240*S), int(273*S):int(298*S)] = True
bbox(d & z, "filter r1c1 digit '1'", (281, 287, 226, 236), tol=5)
pxv = r[int(255*S), int(301*S)]
print(f"  filter separator color: #{pxv[0]:02X}{pxv[1]:02X}{pxv[2]:02X}")

# 4. LEFT GRID border
z = np.zeros_like(m); z[int(205*S):int(340*S), int(74*S):int(247*S)] = True
lg = (RR - GG > 50) & (RR - BB > 50) & z
bbox(lg, "left grid red border", (78, 241, 208, 336))

# 5. PANEL border
gm = (abs(RR - 191) < 35) & (abs(GG - 191) < 35) & (abs(BB - 191) < 35)
z = np.zeros_like(gm); z[int(160*S):int(440*S), int(370*S):int(895*S)] = True
bbox(gm & z, "panel gray border", (379, 886, 168, 432), tol=6)

# 6. BAKED PLACEMENT PROOF (1:1 downscale diff)
fs = im.resize((960, 540), Image.LANCZOS)
fa = np.asarray(fs).astype(int)
for name, (x0, y0, w, h) in [("leftgrid035.png", (77, 207, 167, 131)),
                              ("panelcontent035.png", (398, 185, 478, 236))]:
    asset = np.asarray(Image.open(f"{ASSETS}/{name}").convert("RGB")).astype(int)
    win = fa[y0:y0+h, x0:x0+w]
    mad = np.abs(win - asset).mean()
    chk(f"baked placement {name}", mad < 12, f"MAD={mad:.2f} at ({x0},{y0}) exact size")

# 7. CAPTION BOX
lm = (RR > 240) & (GG > 240) & (BB > 220) & (RR - BB > 8)
z = np.zeros_like(lm); z[int(440*S):int(512*S), int(60*S):int(900*S)] = True
bbox(lm & z, "caption light fill", (68, 890, 447, 507), tol=6)
bm = (BB - RR > 15) & (BB > 120)
z = np.zeros_like(bm); z[int(440*S):int(515*S), int(60*S):int(900*S)] = True
bbox(bm & z, "caption blue border+text", (67, 891, 445, 508), tol=6)

# 8. CAPTION TEXT (clean zones)
navy = (BB - RR > 40) & (BB > 100)
z = np.zeros((r.shape[0], r.shape[1]), bool)
z[int(450*S):int(480*S), int(74*S):int(886*S)] = True
ys, xs = np.where(navy & z)
if len(xs):
    bx = (xs.min(), xs.max(), ys.min(), ys.max())
    tx = (int(78*S), int(881*S), int(452*S), int(477*S))
    ddx = (bx[0]-tx[0], bx[1]-tx[1], bx[2]-tx[2], bx[3]-tx[3])
    ok = abs(ddx[0]) <= 5 and abs(ddx[1]) <= 8 and abs(ddx[2]) <= 5 and abs(ddx[3]) <= 6
    chk("caption L1 navy", ok, f"x{bx[0]}..{bx[1]} y{bx[2]}..{bx[3]} | target x{tx[0]}..{tx[1]} y{tx[2]}..{tx[3]} (dx {ddx[0]}/{ddx[1]}, dy {ddx[2]}/{ddx[3]})")
red2 = (RR - GG > 50) & (RR - BB > 50) & (RR > 110)
z = np.zeros((r.shape[0], r.shape[1]), bool)
z[int(477*S):int(506*S), int(80*S):int(520*S)] = True
ys, xs = np.where(red2 & z)
if len(xs):
    bx = (xs.min(), xs.max(), ys.min(), ys.max())
    tx = (int(92*S), int(479*S), int(480*S), int(502*S))
    ddx = (bx[0]-tx[0], bx[1]-tx[1], bx[2]-tx[2], bx[3]-tx[3])
    ok = abs(ddx[0]) <= 5 and abs(ddx[1]) <= 8 and abs(ddx[2]) <= 5 and abs(ddx[3]) <= 6
    chk("caption L2 red", ok, f"x{bx[0]}..{bx[1]} y{bx[2]}..{bx[3]} | target x{tx[0]}..{tx[1]} y{tx[2]}..{tx[3]} (dx {ddx[0]}/{ddx[1]}, dy {ddx[2]}/{ddx[3]})")
    wrender = (bx[1]-bx[0])/S; wtarget = 479-92
    chk("caption L2 red width", abs(wrender - wtarget) <= 8, f"{wrender:.1f} vs {wtarget} frame px")
# navy paren present
z = np.zeros((r.shape[0], r.shape[1]), bool)
z[int(478*S):int(505*S), int(80*S):int(100*S)] = True
ys, xs = np.where(navy & z)
chk("caption L2 '(' navy exists", len(xs) > 0, f"n={len(xs)}" + (f" x{xs.min()}..{xs.max()} y{ys.min()}..{ys.max()}" if len(xs) else ""))

# 9. CONTAINMENT
z = np.zeros((r.shape[0], r.shape[1]), bool)
z[int(445*S):int(508*S), int(67*S):int(892*S)] = True
ys, xs = np.where(((BB - RR > 15) & (BB > 120) | red2) & z)
inside = xs.min() >= int(67*S)-2 and xs.max() <= int(892*S)+2 and ys.min() >= int(445*S)-2 and ys.max() <= int(508*S)+2
chk("caption text inside box", inside, f"x{xs.min()}..{xs.max()} y{ys.min()}..{ys.max()}")
z = r[int(362*S):int(392*S), int(720*S):int(752*S)]
nonwhite = ((z[:, :, 0] < 240) | (z[:, :, 1] < 240) | (z[:, :, 2] < 235)).sum()
chk("cursor zone clean", nonwhite == 0, f"nonwhite={nonwhite}")

# 10. BADGE numeral centered in badge circle (frame center 893,71)
z = np.zeros((r.shape[0], r.shape[1]), bool)
z[int(53*S):int(90*S), int(875*S):int(912*S)] = True
ys, xs = np.where(d & z)
if len(xs):
    cx, cy = (xs.min()+xs.max())/2/S, (ys.min()+ys.max())/2/S
    chk("badge numeral centered", abs(cx-893) <= 3 and abs(cy-71) <= 3, f"center ({cx:.1f},{cy:.1f}) target (893,71)")

print()
print("FAILS:", fails if fails else "none")
