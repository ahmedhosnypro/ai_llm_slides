#!/usr/bin/env python3
"""slide011 pre-judge self-check (attempt 1): chrome, containment, equations, geometry.
Scale: render 2001x1125 vs frame 960x540 -> k = 2.084375 render px per frame px.
"""
import subprocess, sys
import numpy as np
from PIL import Image

ROOT = "/home/ahmed/Projects/ai_llm_slides"
VID = ROOT + "/videos/deep-learning/001_transformers_part1"
RENDER = VID + "/recreated_pptx/qa/slide011/render_1.png"
ORIG = VID + "/unique_slides/slide_011.jpg"

im = Image.open(RENDER).convert("RGB")
a = np.asarray(im).astype(int)
H, W = a.shape[:2]
o = np.asarray(Image.open(ORIG).convert("RGB")).astype(int)
k = W / 960.0
print(f"render {W}x{H}, k={k:.5f}")
fails, notes = [], []

# ---------- 1. house_chrome_check (shared, unmodified) ----------
for tag, path in (("RENDER", RENDER), ("ORIGINAL", ORIG)):
    r = subprocess.run([sys.executable, ROOT + "/videos/deep-learning/shared_patterns/house_chrome_check.py", path],
                       capture_output=True, text=True)
    print(f"--- house_chrome_check on {tag}: rc={r.returncode}")
    print(r.stdout.strip() or r.stderr.strip())

# ---------- 2. adapted chrome check (white-box-aware) ----------
r_, g_, b_ = a[:, :, 0], a[:, :, 1], a[:, :, 2]
gray = (np.abs(r_ - 232) < 12) & (np.abs(g_ - 232) < 12) & (np.abs(b_ - 230) < 14)
def band(x0, y0, x1, y1):
    sub = gray[int(y0*k):int(y1*k), int(x0*k):int(x1*k)]
    return sub.mean()
checks = [
    ("panel visible above white box (y 55..108)", band(60, 55, 900, 108) > 0.85),
    ("panel visible below white box (y 505..530)", band(60, 505, 900, 530) > 0.85),
    ("left border stroke at y 60..110", ((r_[int(60*k):int(110*k), int(38*k):int(46*k)] > 120) & (g_[int(60*k):int(110*k), int(38*k):int(46*k)] < 110) & (b_[int(60*k):int(110*k), int(38*k):int(46*k)] < 110)).sum() > 8),
    ("right border stroke at y 60..110", ((r_[int(60*k):int(110*k), int(914*k):int(922*k)] > 120) & (g_[int(60*k):int(110*k), int(914*k):int(922*k)] < 110) & (b_[int(60*k):int(110*k), int(914*k):int(922*k)] < 110)).sum() > 8),
    ("bottom border stroke across (row ~538-540)", ((r_[int(536*k):, :] > 120) & (g_[int(536*k):, :] < 110) & (b_[int(536*k):, :] < 110)).sum() > int(600*k)),
    ("top border stroke across (row ~43-45)", ((r_[int(42*k):int(46*k), int(100*k):int(860*k)] > 120) & (g_[int(42*k):int(46*k), int(100*k):int(860*k)] < 110) & (b_[int(42*k):int(46*k), int(100*k):int(860*k)] < 110)).sum() > int(500*k)),
]
# badge: yellow disc + purple ring near (893,71)
cx, cy, d = 893*k, 71*k, 36*k
win = np.s_[int(cy-d):int(cy+d), int(cx-d):int(cx+d)]
wr, wg, wb = r_[win], g_[win], b_[win]
yel = (wr > 200) & (wg > 200) & (wb < 190)
pys, pxs = np.where(yel)
if len(pys):
    bcx = win[1].start + (pxs.min() + pxs.max())/2
    bcy = win[0].start + (pys.min() + pys.max())/2
    checks.append((f"badge center ({bcx:.0f},{bcy:.0f}) vs ({cx:.0f},{cy:.0f})",
                   abs(bcx-cx) <= 8 and abs(bcy-cy) <= 8))
    checks.append((f"badge diameter {pxs.max()-pxs.min()+1} vs {d:.0f}",
                   abs((pxs.max()-pxs.min()+1) - d) <= 12))
else:
    checks.append(("badge yellow disc present", False))
pur = (wb > 150) & (wr > 70) & (wr < 180) & (wg < 130)
checks.append(("badge purple ring present", pur.sum() >= 10))
for name, ok in checks:
    (notes if ok else fails).append(("CHROME " + name))
    print(("  OK  " if ok else "  FAIL") + " chrome: " + name)

# ---------- 3. containment: content ink inside the border strokes ----------
ink = (np.abs(r_ - 254) + np.abs(g_ - 255) + np.abs(b_ - 253)) > 90  # non-white/non-panel-ish
# canvas margins must be empty; the 2px ring just inside each stroke must be empty
# (the side-exit arrow's faithful tip reaches x=913 < 914, so the right ring starts at 914)
out_left  = int(ink[:, : int(40*k)].sum())
out_right = int(ink[:, int(922*k):].sum())
out_top   = int(ink[: int(43*k), :].sum())
ring_bottom = int(ink[int(533.5*k):int(536.5*k), int(100*k):int(860*k)].sum())
ring_right  = int(ink[int(60*k):int(500*k), int(914*k):int(916.5*k)].sum())
ring_left   = int(ink[int(60*k):int(500*k), int(43.5*k):int(46*k)].sum())
ring_top    = int(ink[int(46.5*k):int(49*k), int(100*k):int(860*k)].sum())
print(f"containment: canvas-margin ink L{out_left} R{out_right} T{out_top}; "
      f"inner-ring ink bottom={ring_bottom} right={ring_right} left={ring_left} top={ring_top}")
if max(out_left, out_right, out_top, ring_bottom, ring_right, ring_left, ring_top) > 30:
    fails.append(f"CONTAINMENT margin L{out_left} R{out_right} T{out_top} "
                 f"ring b{ring_bottom} r{ring_right} l{ring_left} t{ring_top}")
else:
    notes.append("CONTAINMENT all content inside border strokes")

# ---------- 4. geometry: block bboxes vs measured (frame px) ----------
def bbox_of(mask):
    ys, xs = np.where(mask)
    return (xs.min(), ys.min(), xs.max(), ys.max()) if len(xs) else None
def cbox(x0, y0, x1, y1):
    return (int(x0*k), int(y0*k), int(x1*k), int(y1*k))
def close(b, ref, tol=7):
    return b is not None and all(abs(b[i]-ref[i]) <= tol for i in range(4))

yellow = (r_ > 210) & (g_ > 210) & (b_ < 120)
oy = 162*k
yb = bbox_of(yellow[int(oy):int(oy+130*k), :])
yb = (yb[0], yb[1]+int(oy), yb[2], yb[3]+int(oy)) if yb else None
ref_y = cbox(479, 162, 904, 283)
print("yellow bbox render:", yb, "ref:", ref_y)
if not close(yb, ref_y): fails.append(f"GEOM yellow block {yb} vs {ref_y}")
else: notes.append("GEOM yellow block ok")

orange = (r_ > 230) & (g_ > 130) & (g_ < 205) & (b_ > 50) & (b_ < 155)
ob = bbox_of(orange[int(295*k):int(460*k), :int(495*k)])
ob = (ob[0], ob[1]+int(295*k), ob[2], ob[3]+int(295*k)) if ob else None
ref_o = cbox(46, 306, 487, 451)
print("orange bbox render:", ob, "ref:", ref_o)
if not close(ob, ref_o): fails.append(f"GEOM orange block {ob} vs {ref_o}")
else: notes.append("GEOM orange block ok")

# note box fill bbox
beige = (np.abs(r_-234) < 8) & (np.abs(g_-230) < 8) & (np.abs(b_-221) < 10)
nb = bbox_of(beige[int(400*k):int(535*k), int(450*k):int(900*k)])
nb = (nb[0]+int(450*k), nb[1]+int(400*k), nb[2]+int(450*k), nb[3]+int(400*k)) if nb else None
ref_n = cbox(459, 410, 889, 523)
print("notebox bbox render:", nb, "ref:", ref_n)
if not close(nb, ref_n, 8): fails.append(f"GEOM note box {nb} vs {ref_n}")
else: notes.append("GEOM note box ok")

# ---------- 5. equations: ink present + closed-loop band compare (render vs original) ----------
def ink_mask(img, x0, y0, x1, y1, thr=560):
    sub = img[int(y0*k if img is a else y0): int(y1*k if img is a else y1),
              int(x0*k if img is a else x0): int(x1*k if img is a else x1)]
    return sub.sum(axis=2) < thr
EQS = {
    "x1": (138, 470, 170, 498), "x2": (272, 470, 305, 498), "x3": (406, 470, 440, 498),
    "o1": (536, 114, 572, 140), "o2": (670, 114, 706, 140), "o3": (806, 114, 842, 140),
}
for name, (x0, y0, x1, y1) in EQS.items():
    mr = ink_mask(a, x0, y0, x1, y1)
    n_ink = int(mr.sum())
    if n_ink < 12:
        fails.append(f"EQ {name}: no ink in render region (n={n_ink})")
        continue
    ys, xs = np.where(mr)
    rb = (xs.min()/k + x0, ys.min()/k + y0, xs.max()/k + x0, ys.max()/k + y0)
    mo = ink_mask(o, x0, y0, x1, y1) if False else (o[int(y0):int(y1), int(x0):int(x1)].sum(axis=2) < 560)
    yso, xso = np.where(mo)
    ob2 = (xso.min() + x0, yso.min() + y0, xso.max() + x0, yso.max() + y0)
    dmax = max(abs(rb[i]-ob2[i]) for i in range(4))
    print(f"EQ {name}: render(frame-px) {tuple(round(v,1) for v in rb)} vs orig {ob2}  maxdev={dmax:.1f}px")
    if dmax > 8:
        fails.append(f"EQ {name} band dev {dmax:.1f}px > 8: {tuple(round(v,1) for v in rb)} vs {ob2}")
    else:
        notes.append(f"EQ {name} band dev {dmax:.1f}px ok")

# ---------- 6. text bands: title/subtitle/labels/bullets present at measured bands ----------
def band_ink(x0, y0, x1, y1, thr=520):
    sub = a[int(y0*k):int(y1*k), int(x0*k):int(x1*k)]
    return int((sub.sum(axis=2) < thr).sum())
BANDS = {
    "title": (350, 54, 580, 90), "subtitle": (325, 92, 600, 115),
    "Decoder": (683, 86, 772, 109), "enc-label": (170, 196, 396, 216),
    "dec-label": (625, 348, 852, 368), "Encoder": (220, 505, 306, 527),
    "yellow-text": (515, 212, 866, 234), "orange-text": (90, 366, 440, 391),
    "heading": (462, 417, 742, 442), "b1": (462, 443, 710, 464),
    "b2": (462, 469, 890, 492), "b3": (462, 495, 718, 517),
    "attention": (248, 254, 328, 272),
}
for name, bb in BANDS.items():
    n = band_ink(*bb)
    print(f"BAND {name}: ink px={n}")
    if n < 15:
        fails.append(f"BAND {name}: too little ink (n={n})")
    else:
        notes.append(f"BAND {name} present")

# ---------- 7. note text line pitch (render) ----------
sub = a[int(440*k):int(520*k), int(460*k):int(740*k)].sum(axis=2) < 480
rows = np.where(sub.sum(axis=1) > 2)[0]
if len(rows):
    groups = np.split(rows, np.where(np.diff(rows) > 4)[0]+1)
    tops = [int(g[0]/k + 440) for g in groups if len(g) > 3]
    print("note text line tops (frame px):", tops)
    if len(tops) >= 3:
        pitches = [tops[i+1]-tops[i] for i in range(len(tops)-1)]
        print("pitches:", pitches, "(orig: 25.5, 26, 26)")
        if max(abs(p-26) for p in pitches) > 4:
            fails.append(f"NOTE pitch off: {pitches}")

print("\n==== SUMMARY ====")
print("FAILS:", len(fails))
for f in fails: print("  -", f)
print("OK:", len(notes))
