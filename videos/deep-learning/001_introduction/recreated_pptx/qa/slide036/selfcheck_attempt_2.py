#!/usr/bin/env python3
# selfcheck_attempt_2.py — mandatory pre-judge closed-loop check on render_2.png (150dpi).
# Compares measured render bands against the original frame's PIL measurements
# (measure5_out.txt / fit_fonts_out.txt). Scale: render_px = frame_px * (W/960).
from PIL import Image
import numpy as np
from collections import Counter

RENDER = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/qa/slide036/render_2.png"
im = np.array(Image.open(RENDER).convert("RGB")).astype(int)
H, W = im.shape[:2]
sx, sy = W / 960.0, H / 540.0
print(f"render {W}x{H}, scale {sx:.4f}x{sy:.4f}")

def band_rows(mask, y0, y1, x0, x1, minpx=2):
    out = []
    for y in range(y0, y1):
        n = mask[y, x0:x1].sum()
        out.append((y, n))
    return out

def ink_bbox(mask, y0, y1, x0, x1):
    sub = mask[y0:y1, x0:x1]
    ys, xs = np.where(sub)
    if not len(ys):
        return None
    return (xs.min() + x0, ys.min() + y0, xs.max() + x0, ys.max() + y0)

ok = lambda cond, msg: print(("  PASS " if cond else "  FAIL ") + msg)

# ---- 1. title (red) ----
red = (im[:, :, 0] > 130) & (im[:, :, 1] < 80) & (im[:, :, 2] < 80)
t = ink_bbox(red, int(40*sx and 0) + int(50*sy), int(145*sy), int(100*sx), int(860*sx))
print("== TITLE ==")
# split lines by empty rows
rows = red[int(50*sy):int(145*sy), int(100*sx):int(860*sx)].sum(axis=1)
lines, inl = [], False
for i, n in enumerate(rows):
    if n > 2 and not inl: s = i; inl = True
    elif n <= 2 and inl: lines.append((50*sy + s, 50*sy + i - 1)); inl = False
if inl: lines.append((50*sy + s, 50*sy + len(rows) - 1))
exp = [(62, 92), (101, 131)]
for i, (a, b) in enumerate(lines[:2]):
    band = red[int(a):int(b)+1, int(100*sx):int(860*sx)]
    xs = np.where(band.any(axis=0))[0]
    e = exp[i]
    print(f"  L{i+1}: y {a/sy:.1f}..{b/sy:.1f} (exp {e[0]}..{e[1]}), x {xs.min()/sx:.0f}..{xs.max()/sx:.0f}")
    ok(abs(a/sy - e[0]) <= 4 and abs(b/sy - e[1]) <= 4, f"L{i+1} vertical within 4px")
# L1 advance target 643
if len(lines) >= 1:
    a, b = lines[0]
    band = red[int(a):int(b)+1, int(100*sx):int(860*sx)]
    xs = np.where(band.any(axis=0))[0]
    adv = (xs.max() - xs.min()) / sx
    ok(abs(adv - 643) <= 13, f"L1 advance {adv:.0f} vs 643 (+-13)")

# ---- 2. content box border ----
print("== CONTENT BOX (exp rows 156/501, cols 110/839) ==")
for label, axis in [("top", 156), ("bottom", 501)]:
    y0, y1 = int((axis-6)*sy), int((axis+6)*sy)
    found = [y for y in range(y0, y1) if red[y, int(300*sx):int(700*sx)].sum() > 400]
    ok(found and abs(found[0]/sy - axis) <= 3, f"{label} border row {found[:1]} vs {axis}")
for label, axis in [("left", 110), ("right", 839)]:
    x0, x1 = int((axis-6)*sx), int((axis+6)*sx)
    found = [x for x in range(x0, x1) if red[int(200*sy):int(480*sy), x].sum() > 150]
    ok(found and abs(found[0]/sx - axis) <= 3, f"{label} border col {found[:1]} vs {axis}")

# ---- 3. crops present: probe pixels (tile interiors must equal original pixels) ----
print("== CROP TILE PROBES (render vs original, same frame px) ==")
orig = np.array(Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_036.jpg").convert("RGB")).astype(int)
probes = {"slab_top": (260, 190), "slab_body": (300, 300), "filter_unit": (440, 300)}
allok = True
for name, (fx, fy) in probes.items():
    rx, ry = int(fx * sx), int(fy * sy)
    d = np.abs(im[ry, rx] - orig[fy, fx]).max()
    allok &= d <= 30
    print(f"  {name} @({fx},{fy}): render {tuple(im[ry,rx])} vs orig {tuple(orig[fy,fx])} maxd={d}")
ok(allok, "tile probe pixels match (JPEG noise <=30)")

# ---- 4. '=' bars (cyan) ----
print("== '=' BARS (exp x506..535, y290..293 / 298..301) ==")
cy = (im[:, :, 2] > im[:, :, 0] + 40) & (im[:, :, 2] > 150) & (im[:, :, 1] > 120)
eqb = ink_bbox(cy, int(280*sy), int(310*sy), int(495*sx), int(545*sx))
if eqb:
    print(f"  bbox x {eqb[0]/sx:.1f}..{eqb[2]/sx:.1f} y {eqb[1]/sy:.1f}..{eqb[3]/sy:.1f}")
    ok(abs(eqb[0]/sx - 506) <= 4 and abs(eqb[2]/sx - 535) <= 4, "= x extent")
    ok(abs(eqb[1]/sy - 290) <= 4 and abs(eqb[3]/sy - 301) <= 4, "= y extent")
else:
    ok(False, "= sign found")

# ---- 5. '+' (gray) ----
print("== '+' (exp x554..563, y312..319) ==")
g = (np.abs(im[:, :, 0] - im[:, :, 1]) < 14) & (np.abs(im[:, :, 1] - im[:, :, 2]) < 14) & \
    (im.mean(axis=2) > 150) & (im.mean(axis=2) < 215)
pb = ink_bbox(g, int(305*sy), int(325*sy), int(548*sx), int(570*sx))
if pb:
    print(f"  bbox x {pb[0]/sx:.1f}..{pb[2]/sx:.1f} y {pb[1]/sy:.1f}..{pb[3]/sy:.1f}")
    ok(abs(pb[0]/sx - 554) <= 4 and abs(pb[2]/sx - 563) <= 4 and abs(pb[1]/sy - 312) <= 4 and abs(pb[3]/sy - 319) <= 4, "+ extent")
else:
    ok(False, "+ found")

# ---- 6. neuron ----
print("== NEURON (ring exp 573..611 x 282..310) ==")
o = (im[:, :, 0] > 170) & (im[:, :, 1] > 90) & (im[:, :, 1] < 180) & (im[:, :, 2] < 90)
nb = ink_bbox(o, int(275*sy), int(318*sy), int(565*sx), int(620*sx))
if nb:
    print(f"  ring bbox x {nb[0]/sx:.1f}..{nb[2]/sx:.1f} y {nb[1]/sy:.1f}..{nb[3]/sy:.1f}")
    ok(abs(nb[0]/sx - 573) <= 4 and abs(nb[2]/sx - 611) <= 4 and abs(nb[1]/sy - 282) <= 4 and abs(nb[3]/sy - 310) <= 4, "neuron ring extent")
else:
    ok(False, "neuron ring found")
cyn = (im[:, :, 2] > 180) & (im[:, :, 0] < 120) & (im[:, :, 1] > 140)
cb = ink_bbox(cyn, int(283*sy), int(308*sy), int(575*sx), int(610*sx))
if cb:
    print(f"  core bbox x {cb[0]/sx:.1f}..{cb[2]/sx:.1f} y {cb[1]/sy:.1f}..{cb[3]/sy:.1f}")
    ok(abs(cb[0]/sx - 580) <= 4 and abs(cb[1]/sy - 287) <= 4, "neuron core extent")

# ---- 7. arrow-to-neuron (dark diagonal) ----
print("== ARROW-TO-NEURON (exp tip (611,325) tail (660,408)) ==")
d = im.mean(axis=2) < 120
ab = ink_bbox(d, int(318*sy), int(412*sy), int(600*sx), int(670*sx))
if ab:
    print(f"  bbox x {ab[0]/sx:.1f}..{ab[2]/sx:.1f} y {ab[1]/sy:.1f}..{ab[3]/sy:.1f}")
    ok(abs(ab[0]/sx - 609) <= 5 and abs(ab[1]/sy - 324) <= 5 and abs(ab[2]/sx - 661) <= 6 and abs(ab[3]/sy - 409) <= 6, "arrow extent")
else:
    ok(False, "arrow found")

# ---- 8. question (black, exp x157..794 y410..455) ----
print("== QUESTION ==")
qb = ink_bbox(d, int(400*sy), int(462*sy), int(140*sx), int(810*sx))
if qb:
    print(f"  bbox x {qb[0]/sx:.1f}..{qb[2]/sx:.1f} y {qb[1]/sy:.1f}..{qb[3]/sy:.1f}")
    ok(abs(qb[0]/sx - 157) <= 8 and abs(qb[2]/sx - 794) <= 13, "question x extent (adv 638)")
    ok(abs(qb[1]/sy - 410) <= 6 and abs(qb[3]/sy - 455) <= 8, "question y band")
else:
    ok(False, "question found")

# ---- 9. equation (red, exp x339..592 y458..479) — EXISTENCE + POSITION ----
print("== EQUATION (red ink, exp x339..592 y458..479) ==")
eqr = (im[:, :, 0] > 140) & (im[:, :, 1] < 95) & (im[:, :, 2] < 95)
eb = ink_bbox(eqr, int(448*sy), int(495*sy), int(300*sx), int(620*sx))
if eb:
    print(f"  bbox x {eb[0]/sx:.1f}..{eb[2]/sx:.1f} y {eb[1]/sy:.1f}..{eb[3]/sy:.1f}")
    ok(abs(eb[0]/sx - 339) <= 4 and abs(eb[2]/sx - 592) <= 5, "equation x extent (adv 254)")
    ok(abs(eb[1]/sy - 458) <= 4 and abs(eb[3]/sy - 479) <= 4, "equation y band")
else:
    ok(False, "EQUATION HAS INK (BLOCKER if empty)")

# ---- 10. frame containment ----
print("== CONTAINMENT (box 110..839 x 156..501; panel 42..918 x 45..540) ==")
ink_any = (np.abs(im - im.mean(axis=2, keepdims=True)).max(axis=2) > 40) | (im.mean(axis=2) < 190)
# interior of the box must not touch the box border rows/cols with content ink
inside_v = ink_any[int(158*sy):int(500*sy), :]
x_ink = np.where(inside_v.any(axis=0))[0]
ok(x_ink.min()/sx >= 111 and x_ink.max()/sx <= 838, f"box interior ink x {x_ink.min()/sx:.0f}..{x_ink.max()/sx:.0f} within 111..838")
# title must not cross panel top (45) or the box top
tro = np.where(red[:int(150*sy)].any(axis=1))[0]
ok(tro.min()/sy >= 46, f"title ink top {tro.min()/sy:.1f} below panel top 45")
