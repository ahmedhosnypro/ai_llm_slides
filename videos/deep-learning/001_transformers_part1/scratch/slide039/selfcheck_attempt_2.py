#!/usr/bin/env python3
"""selfcheck_attempt_2.py — pre-judge self-checks for slide 039 attempt 2.
Checks (150dpi render 2001x1125 vs original 960x540, scale S=2001/960):
  1. FRAME CONTAINMENT (playlist-adapted): content ink within gray panel
     x[42,918] y[45,539] frame px (render x[87,1913] y[94,1123]).
  2. STRUCTURE: expected fill colors at measured element centers (attempt-2 palette:
     W^k 96D6A2, W^V A9CFDC, container E7FEE8, bottom cells EAF6E1, left cells E3F4E1).
  3. REGION INK: new attempt-2 elements (Y labels blue, sticker navy, bottom red X's,
     V labels red, container red X, circled-asterisk nodes, fraction ink).
  4. EQUATION CLOSED-LOOP (17 §math law): fraction PNG ink band in the render vs the
     original's measured region x[383,398] y[264,286] (m16), tol 4 render px.
  5. GEOMETRY: key element bboxes render vs original (tol 8 render px)."""
from PIL import Image
import numpy as np

REND = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/qa/slide039/render_2.png"
ORIG = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_039.jpg"
r = Image.open(REND).convert("RGB"); a = np.asarray(r).astype(int)
o = Image.open(ORIG).convert("RGB"); ob = np.asarray(o).astype(int)
S = a.shape[1] / 960.0
print(f"render {a.shape[1]}x{a.shape[0]}  scale {S:.4f}")

fails = []

# ---- 1. containment
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]
white = (R > 243) & (G > 243) & (B > 243)
grayp = (np.abs(R - 233) < 8) & (np.abs(G - 233) < 8) & (np.abs(B - 231) < 9)
ink = ~(white | grayp)
zones = {
    "left of panel (x<86)":    ink[:, :86],
    "right of panel (x>1915)": ink[:, 1916:],
    "above panel (y<92)":      ink[:92, :],
}
for name, z in zones.items():
    cnt = int(z.sum())
    status = "PASS" if cnt < 60 else "FAIL"
    if status == "FAIL": fails.append(name)
    print(f"containment {name}: ink_px={cnt} {status}")
below = ink[1120:1122, :]
cnt = int(below.sum())
print(f"containment below panel bottom rows (y>1123): ink_px={cnt} {'PASS' if cnt < 60 else 'FAIL'}")
if cnt >= 60: fails.append("below panel")

# ---- 2. structure fills
def center_fill(fx, fy, half=3):
    x, y = int(fx * S), int(fy * S)
    patch = a[y - half:y + half + 1, x - half:x + half + 1].reshape(-1, 3).mean(axis=0)
    return tuple(patch.astype(int))

def close(c1, c2, tol=22):
    return all(abs(int(c1[i]) - c2[i]) <= tol for i in range(3))

checks = [
    ("panel1 fill", (200, 430), (240, 224, 200)),
    ("panel4 fill", (870, 380), (240, 224, 200)),
    ("dot box fill", (296, 340), (216, 200, 184)),
    ("scaling box fill", (353, 385), (255, 196, 203)),
    ("softmax box fill", (406, 385), (248, 222, 250)),
    ("sigma box fill", (470, 272), (232, 248, 248)),
    ("pill1 fill", (281, 245), (248, 248, 226)),
    ("sticker fill", (715, 505), (255, 255, 0)),
    ("canvas white", (20, 300), (255, 255, 255)),
    ("gray panel", (200, 60), (233, 233, 231)),
    ("leftX cell base", (160, 311), (227, 244, 225)),
    ("leftX band yellow", (141, 299), (231, 239, 200)),
    ("Wk box fill", (210, 305), (150, 214, 162)),
    ("WV box fill", (587, 305), (169, 207, 220)),
    ("right container fill", (640, 313), (231, 254, 232)),
    ("right container yellow", (620, 296), (232, 241, 198)),
    ("bottom cell fill", (461, 470), (234, 246, 225)),
]
for name, (fx, fy), want in checks:
    got = center_fill(fx, fy)
    ok = close(got, want)
    if not ok: fails.append(f"fill {name}")
    print(f"fill {name} at ({fx},{fy}): got {got} want {want} {'PASS' if ok else 'FAIL'}")

# ---- 3. region ink presence
def ink_count(fx0, fy0, fx1, fy1, mask_fn):
    x0, y0, x1, y1 = [int(v * S) for v in (fx0, fy0, fx1, fy1)]
    sub = mask_fn(a[y0:y1, x0:x1])
    return int(sub.sum())

dark_m = lambda p: (p[:, :, 0] < 120) & (p[:, :, 1] < 120) & (p[:, :, 2] < 120)
red_m = lambda p: (p[:, :, 0] > 140) & (p[:, :, 0] - p[:, :, 1] > 60) & (p[:, :, 0] - p[:, :, 2] > 60)
blue_m = lambda p: (p[:, :, 2] - p[:, :, 0] > 50) & (p[:, :, 2] > 130)
navy_m = lambda p: (p[:, :, 2] - p[:, :, 0] > 40) & (p[:, :, 0] < 110) & (p[:, :, 2] < 160)
green_m = lambda p: (p[:, :, 1] - p[:, :, 0] > 30) & (p[:, :, 1] - p[:, :, 2] > 30)

regions = [
    ("title L1 ink", 210, 40, 430, 70, dark_m, 200),
    ("title L3 red X", 440, 88, 580, 122, red_m, 60),
    ("Y1 label blue", 470, 138, 498, 162, navy_m, 25),
    ("Y4 label blue", 697, 75, 726, 102, navy_m, 25),
    ("pill1 blue text", 280, 242, 320, 256, blue_m, 15),
    ("K label red", 252, 288, 266, 302, red_m, 10),
    ("Dot header ink", 270, 264, 324, 288, dark_m, 40),
    ("bottom label X1 red", 296, 514, 315, 532, red_m, 30),
    ("bottom row cell X2 red", 333, 458, 362, 480, red_m, 15),
    ("left box X glyph red", 150, 291, 165, 307, red_m, 8),
    ("container X glyph red", 631, 291, 644, 307, red_m, 8),
    ("V1 label red", 532, 284, 551, 302, red_m, 8),
    ("Y1 box green border", 450, 190, 532, 212, green_m, 40),
    ("Y1 arrow red", 483, 172, 500, 194, red_m, 40),
    ("sticker navy text", 700, 440, 885, 512, navy_m, 120),
    ("Wq box red border", 278, 420, 312, 447, red_m, 25),
    ("sigma glyph blue", 480, 264, 500, 282, blue_m, 10),
    ("astnode1 red", 448, 292, 464, 306, red_m, 30),
    ("fraction ink red", 380, 260, 404, 290, red_m, 60),
    ("denominator box red", 378, 272, 404, 291, red_m, 40),
    ("mesh dark blue", 285, 300, 320, 380, blue_m, 30),
]
for name, x0, y0, x1, y1, mfn, minpx in regions:
    n = ink_count(x0, y0, x1, y1, mfn)
    ok = n >= minpx
    if not ok: fails.append(f"ink {name}")
    print(f"ink {name}: {n}px (min {minpx}) {'PASS' if ok else 'FAIL'}")

# ---- 4. equation closed-loop: fraction ink band vs original measured region
def band_bbox(img, fx0, fy0, fx1, fy1, mask_fn, scale):
    x0, y0, x1, y1 = [int(v * scale) for v in (fx0, fy0, fx1, fy1)]
    sub = mask_fn(img[y0:y1, x0:x1])
    ys, xs = np.where(sub)
    if not len(xs): return None
    return ((x0 + xs.min()) / scale, (y0 + ys.min()) / scale,
            (x0 + xs.max()) / scale, (y0 + ys.max()) / scale)

ren_bb = band_bbox(a, 375, 255, 410, 295, red_m, S)
org_bb = band_bbox(ob, 375, 255, 410, 295, red_m, 1.0)
if ren_bb is None or org_bb is None:
    print(f"equation band: render={ren_bb} original={org_bb} FAIL")
    fails.append("equation band")
else:
    dmax = max(abs(ren_bb[i] - org_bb[i]) for i in range(4))
    # tolerance ~4 px @150dpi = 4/S frame px
    tol = 4.0 / S
    ok = dmax <= tol
    if not ok: fails.append("equation band")
    print(f"equation band: render={[round(v,1) for v in ren_bb]} original={[round(v,1) for v in org_bb]} "
          f"maxd={dmax:.2f} frame-px (tol {tol:.2f}) {'PASS' if ok else 'FAIL'}")

# ---- 5. geometry bboxes
def bbox_in_render(fx0, fy0, fx1, fy1, mask_fn):
    x0, y0, x1, y1 = [int(v * S) for v in (fx0, fy0, fx1, fy1)]
    sub = mask_fn(a[y0:y1, x0:x1])
    ys, xs = np.where(sub)
    if not len(xs): return None
    return ((x0 + xs.min()) / S, (y0 + ys.min()) / S, (x0 + xs.max()) / S, (y0 + ys.max()) / S)

geo = [
    ("bottom arrow1 (red)", 290, 488, 320, 514, red_m, (299, 490, 311, 514)),
    ("bottom arrow2 bar (red)", 385, 488, 404, 514, red_m, (390, 490, 398, 513)),
    ("Y4 box (green)", 660, 112, 755, 136, green_m, (673, 117, 742, 133)),
    ("left X box (green)", 125, 280, 195, 405, green_m, (132, 285, 187, 401)),
    ("right container (green)", 605, 278, 678, 418, green_m, (612, 283, 670, 413)),
]
for name, x0, y0, x1, y1, mfn, orig_bb in geo:
    bb = bbox_in_render(x0, y0, x1, y1, mfn)
    if bb is None:
        print(f"geom {name}: NO INK FAIL"); fails.append(f"geom {name}"); continue
    dmax = max(abs(bb[i] - orig_bb[i]) for i in range(4))
    ok = dmax <= 8
    if not ok: fails.append(f"geom {name}")
    print(f"geom {name}: render{[round(v,1) for v in bb]} vs orig{list(orig_bb)} maxd={dmax:.1f} {'PASS' if ok else 'FAIL'}")

print()
if fails:
    print("SELFCHECK RESULT: FAIL —", len(fails), "issue(s):", fails)
else:
    print("SELFCHECK RESULT: PASS (all checks)")
