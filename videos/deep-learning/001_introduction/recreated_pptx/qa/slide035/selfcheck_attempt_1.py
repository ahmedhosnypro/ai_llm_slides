#!/usr/bin/env python3
"""selfcheck_attempt_1.py — slide 035 closed-loop render self-check (150dpi render vs frame).
Render 2001x1125 (13.333x7.5in @150dpi); frame 960x540 (1px=1pt). scale = 150/72 = 2.08333.
Tolerance: ~4 px in 150dpi space for ink-band edges (equation-law closed loop)."""
import numpy as np
from PIL import Image

REND = "videos/deep-learning/001_introduction/recreated_pptx/qa/slide035/render_1.png"
FR = "videos/deep-learning/001_introduction/unique_slides/slide_035.jpg"
S = 150 / 72.0
im = Image.open(REND).convert("RGB")
print(f"render size: {im.size} (expect ~{960*S:.0f}x{540*S:.0f})")
r = np.asarray(im).astype(int)
f = Image.open(FR).convert("RGB")
fa = np.asarray(f).astype(int)
RR, GG, BB = r[:, :, 0], r[:, :, 1], r[:, :, 2]
fails = []

def bbox(mask, label, target, tol=4):
    ys, xs = np.where(mask)
    if len(xs) == 0:
        print(f"FAIL {label}: EMPTY (target {target})")
        fails.append(label)
        return
    bx = (xs.min(), xs.max(), ys.min(), ys.max())
    tx = tuple(int(round(v * S)) for v in target)
    d = (bx[0]-tx[0], bx[1]-tx[1], bx[2]-tx[2], bx[3]-tx[3])
    ok = all(abs(v) <= tol for v in d)
    print(f"{'PASS' if ok else 'FAIL'} {label}: render x{bx[0]}..{bx[1]} y{bx[2]}..{bx[3]} | "
          f"target x{tx[0]}..{tx[1]} y{tx[2]}..{tx[3]} (dx {d[0]}/{d[1]}, dy {d[2]}/{d[3]})")
    if not ok:
        fails.append((label, d))

# 1. TITLE red ink (frame x266..713 y70..99)
m = (RR - GG > 80) & (RR - BB > 80) & (RR > 130)
z = np.zeros_like(m); z[int(50*S):int(115*S), int(200*S):int(800*S)] = True
bbox(m & z, "title red ink", (266, 713, 70, 99))

# 2. LABELS black ink
d = (RR < 110) & (GG < 110) & (BB < 110)
z = np.zeros_like(d); z[int(170*S):int(212*S), int(95*S):int(200*S)] = True
bbox(d & z, "label Image", (105, 183, 181, 205))
z = np.zeros_like(d); z[int(170*S):int(212*S), int(265*S):int(360*S)] = True
bbox(d & z, "label Filter", (275, 340, 181, 201))

# 3. FILTER TABLE: yellow fills + border
ym = (RR > 200) & (GG > 190) & (BB < 160)
z = np.zeros_like(ym); z[int(215*S):int(295*S), int(262*S):int(372*S)] = True
bbox(ym & z, "filter yellow cells", (271, 363, 220, 290))
# separator green core: sample color at frame (301, 255) scaled
px_ = r[int(255*S), int(301*S)]
print(f"filter separator color @ (301,255): #{px_[0]:02X}{px_[1]:02X}{px_[2]:02X} (target core ~#8BD33F..#ABE411)")
# filter digit ink (black in cell 1)
z = np.zeros_like(d); z[int(222*S):int(240*S), int(273*S):int(298*S)] = True
bbox(d & z, "filter r1c1 digit '1'", (281, 287, 226, 236))

# 4. LEFT GRID image placement: red border of the baked crop should land at frame x78..241 y208..336
z = np.zeros_like(m); z[int(205*S):int(340*S), int(74*S):int(247*S)] = True
lg_red = (RR - GG > 50) & (RR - BB > 50) & z
bbox(lg_red, "left grid red border", (78, 241, 208, 336))

# 5. PANEL rect border (gray #BFBFBF): verticals at x379.5/885.5, horizontals y168.5/431.5
gm = (abs(RR - 191) < 35) & (abs(GG - 191) < 35) & (abs(BB - 191) < 35)
z = np.zeros_like(gm); z[int(160*S):int(440*S), int(370*S):int(895*S)] = True
bbox(gm & z, "panel gray border", (379, 886, 168, 432), tol=6)

# 6. PANEL CONTENT crop: yellow 3x3 fills should land at frame x405..576 y201..328
z = np.zeros_like(ym); z[int(195*S):int(335*S), int(398*S):int(600*S)] = True
bbox(ym & z, "panel yellow 3x3 (baked)", (405, 576, 201, 328))
# green cells c5/r5 baked
gm2 = (GG - RR > 60) & (GG - BB > 40)
z = np.zeros_like(gm2); z[int(370*S):int(420*S), int(634*S):int(695*S)] = True
bbox(gm2 & z, "panel green c5 r5 (baked)", (637, 691, 375, 416))
# output '4' dark glyph (baked) — should land ~x708..728 y204..214 (frame)
dd = (RR < 120) & (GG < 120) & (BB < 120)
z = np.zeros_like(dd); z[int(200*S):int(220*S), int(705*S):int(735*S)] = True
bbox(dd & z, "output '4' glyph (baked)", (708, 728, 204, 214), tol=6)

# 7. CAPTION BOX: fill + border
lm = (RR > 240) & (GG > 240) & (BB > 220) & (RR - BB > 8)
z = np.zeros_like(lm); z[int(440*S):int(512*S), int(60*S):int(900*S)] = True
bbox(lm & z, "caption light fill", (68, 890, 447, 507), tol=6)
bm = (BB - RR > 15) & (BB > 120)
z = np.zeros_like(bm); z[int(440*S):int(515*S), int(60*S):int(900*S)] = True
bbox(bm & z, "caption blue border+text", (67, 891, 445, 508), tol=6)

# 8. CAPTION TEXT LINES
z = np.zeros_like(bm); z[int(450*S):int(478*S), int(70*S):int(895*S)] = True
bbox(bm & z, "caption L1 navy ink", (78, 881, 450, 477), tol=6)
red2 = (RR - GG > 50) & (RR - BB > 50) & (RR > 110)
z = np.zeros_like(red2); z[int(477*S):int(505*S), int(80*S):int(520*S)] = True
bbox(red2 & z, "caption L2 red ink", (92, 479, 480, 502), tol=6)

# 9. CONTAINMENT: caption box border vs text; panel content vs panel border; house frame
# caption text inside box (L1/L2 within x67..891 y445..508)
z = np.zeros_like(bm); z[int(445*S):int(508*S), int(67*S):int(892*S)] = True
ys, xs = np.where((bm | red2) & z)
inside = (xs.min() >= 67*S-2) and (xs.max() <= 892*S+2) and (ys.min() >= 445*S-2) and (ys.max() <= 508*S+2)
print(f"{'PASS' if inside else 'FAIL'} caption text inside box: x{xs.min()}..{xs.max()} y{ys.min()}..{ys.max()}")
if not inside: fails.append("caption containment")
# panel content image inside panel border
z = np.zeros_like(dd); z[int(180*S):int(425*S), int(395*S):int(880*S)] = True
pcontent = (np.abs(RR - 254) + np.abs(GG - 255) + np.abs(BB - 255) < 30) & z
ys, xs = np.where(~pcontent & z & (dd | (RR - GG > 60)))
# simpler: any dark/colored ink in x395..880 y185..420 should be within x398..875 y185..420
ink = (dd | (RR - GG > 60) | (GG - RR > 60)) & z
ys, xs = np.where(ink)
inside2 = xs.min() >= int(398*S)-2 and xs.max() <= int(876*S)+2 and ys.min() >= int(185*S)-2 and ys.max() <= int(421*S)+2
print(f"{'PASS' if inside2 else 'FAIL'} panel-content ink within crop bounds: x{xs.min()}..{xs.max()} y{ys.min()}..{ys.max()} (bounds {int(398*S)}..{int(876*S)} / {int(185*S)}..{int(421*S)})")
if not inside2: fails.append("panel content containment")

# 10. cursor zone in render should be clean white (inpaint worked, no ghost)
z = r[int(362*S):int(392*S), int(720*S):int(752*S)]
nonwhite = ((z[:, :, 0] < 240) | (z[:, :, 1] < 240) | (z[:, :, 2] < 235)).sum()
print(f"{'PASS' if nonwhite == 0 else 'FAIL'} cursor zone clean (nonwhite={nonwhite})")
if nonwhite: fails.append("cursor ghost")

# 11. badge numeral ink
z = np.zeros_like(d); z[int(53*S):int(90*S), int(875*S):int(912*S)] = True
bbox(d & z, "badge numeral 35", (884, 902, 62, 82), tol=6)

print()
print("FAILS:", fails if fails else "none")
