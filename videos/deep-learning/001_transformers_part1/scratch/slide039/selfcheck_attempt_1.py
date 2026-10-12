#!/usr/bin/env python3
"""selfcheck_attempt_1.py — pre-judge self-checks for slide 039 attempt 1.
Checks (150dpi render 2001x1125 vs original 960x540, scale s=2001/960):
  1. FRAME CONTAINMENT (playlist-adapted): content ink within gray panel
     x[42,918] y[45,539] frame px (render x[87,1913] y[94,1123]).
  2. STRUCTURE: expected fill colors at measured element centers (panels, dot box,
     scaling/softmax/sigma, pills, Y boxes, sticker, bottom arrows).
  3. REGION INK: text/label regions contain ink (title lines, K labels, pill rows).
Prints PASS/FAIL per check with numbers."""
from PIL import Image
import numpy as np

REND = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/qa/slide039/render_1.png"
ORIG = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_039.jpg"
r = Image.open(REND).convert("RGB"); a = np.asarray(r).astype(int)
o = Image.open(ORIG).convert("RGB"); ob = np.asarray(o).astype(int)
S = a.shape[1] / 960.0
print(f"render {a.shape[1]}x{a.shape[0]}  scale {S:.4f}")

fails = []

# ---- 1. containment: non-(white/gray-panel) ink outside the panel bounds
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]
white = (R > 243) & (G > 243) & (B > 243)
grayp = (np.abs(R - 233) < 8) & (np.abs(G - 233) < 8) & (np.abs(B - 231) < 9)
# chrome red border zone: the panel outline (2px band around x87/x1913/y94) is chrome
ink = ~(white | grayp)
# bottom chrome stroke rows (1121-1125) are chrome
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
# below panel bottom: rows y>=1121 are the chrome bottom stroke (half-visible by
# design, present in the original) — exclude them from the content check
below = ink[1120:1122, :]
cnt = int(below.sum())
print(f"containment below panel bottom rows (y>1123): ink_px={cnt} {'PASS' if cnt < 60 else 'FAIL'}")
if cnt >= 60: fails.append("below panel")

# ---- 2. structure: sample expected fills (render px = frame px * S)
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
    ("leftX cell fill", (160, 311), (231, 250, 231)),
]
for name, (fx, fy), want in checks:
    got = center_fill(fx, fy)
    ok = close(got, want)
    if not ok: fails.append(f"fill {name}")
    print(f"fill {name} at ({fx},{fy}): got {got} want {want} {'PASS' if ok else 'FAIL'}")

# ---- 3. region ink presence (dark/red/blue ink where text must be)
def ink_count(fx0, fy0, fx1, fy1, mask_fn):
    x0, y0, x1, y1 = [int(v * S) for v in (fx0, fy0, fx1, fy1)]
    sub = mask_fn(a[y0:y1, x0:x1])
    return int(sub.sum())

dark_m = lambda p: (p[:, :, 0] < 120) & (p[:, :, 1] < 120) & (p[:, :, 2] < 120)
red_m = lambda p: (p[:, :, 0] > 140) & (p[:, :, 0] - p[:, :, 1] > 60) & (p[:, :, 0] - p[:, :, 2] > 60)
blue_m = lambda p: (p[:, :, 2] - p[:, :, 0] > 50) & (p[:, :, 2] > 130)
green_m = lambda p: (p[:, :, 1] - p[:, :, 0] > 30) & (p[:, :, 1] - p[:, :, 2] > 30)

regions = [
    ("title L1 ink", 210, 40, 430, 70, dark_m, 200),
    ("title L3 red X", 440, 88, 580, 122, red_m, 60),
    ("pill1 blue text", 280, 242, 320, 256, blue_m, 15),
    ("K label red", 252, 288, 266, 302, red_m, 10),
    ("Dot header ink", 270, 264, 324, 288, dark_m, 40),
    ("bottom label X1 red", 296, 514, 315, 532, red_m, 30),
    ("Y1 box green border", 450, 190, 532, 212, green_m, 40),
    ("Y1 arrow red", 483, 172, 500, 194, red_m, 40),
    ("sticker red text", 710, 440, 875, 512, red_m, 100),
    ("Wq box red border", 278, 420, 312, 447, red_m, 25),
    ("sigma glyph blue", 480, 264, 500, 282, blue_m, 10),
    ("otimes1 red", 448, 292, 464, 306, red_m, 30),
]
for name, x0, y0, x1, y1, mfn, minpx in regions:
    n = ink_count(x0, y0, x1, y1, mfn)
    ok = n >= minpx
    if not ok: fails.append(f"ink {name}")
    print(f"ink {name}: {n}px (min {minpx}) {'PASS' if ok else 'FAIL'}")

# ---- 4. geometry: key element bboxes in render vs original (scaled, tol 8 render px)
def bbox_in_render(fx0, fy0, fx1, fy1, mask_fn):
    x0, y0, x1, y1 = [int(v * S) for v in (fx0, fy0, fx1, fy1)]
    sub = mask_fn(a[y0:y1, x0:x1])
    ys, xs = np.where(sub)
    if not len(xs): return None
    return ((x0 + xs.min()) / S, (y0 + ys.min()) / S, (x0 + xs.max()) / S, (y0 + ys.max()) / S)

geo = [
    ("bottom arrow1 (red)", 290, 488, 320, 514, red_m, (299, 490, 311, 514)),
    ("Y4 box (green)", 660, 112, 755, 136, green_m, (673, 117, 742, 133)),
    ("left X box (green)", 125, 280, 195, 405, green_m, (132, 285, 187, 401)),
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
