#!/usr/bin/env python3
"""Pre-judge self-check for slide 014, attempt 1 (closed-loop PIL, all numbers banked).

Frame 960x540 (1px=1pt) ; render 150dpi 2001x1125 (1 frame-px = 2000/960 render-px).
"""
import subprocess
import sys
import numpy as np
from PIL import Image

VID = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1"
REN = f"{VID}/recreated_pptx/qa/slide014/render_1.png"
SC = 2000.0 / 960.0

im = Image.open(REN).convert("RGB")
a = np.asarray(im).astype(int)
H, W = a.shape[:2]
print(f"render {W}x{H}")
frame = np.asarray(Image.open(f"{VID}/unique_slides/slide_014.jpg").convert("RGB")).astype(int)

fails = []
def check(name, ok, detail=""):
    print(f"[{'PASS' if ok else 'FAIL'}] {name} {detail}")
    if not ok:
        fails.append(name)

def redmask(arr):
    R, G, B = arr[..., 0], arr[..., 1], arr[..., 2]
    return (R > 120) & (R - G > 60) & (R - B > 60)

def bluemask(arr):
    R, G, B = arr[..., 0], arr[..., 1], arr[..., 2]
    return (B > 110) & (B - R > 60) & (B - G > 60)

def darkmask(arr):
    R, G, B = arr[..., 0], arr[..., 1], arr[..., 2]
    return (R < 120) & (G < 120) & (B < 120)

def inkbox(mask, x0, y0, x1, y1):
    sub = mask[y0:y1, x0:x1]
    ys, xs = np.where(sub)
    if len(xs) == 0:
        return None
    return (x0 + xs.min(), y0 + ys.min(), x0 + xs.max(), y0 + ys.max())

def close(got, want_frame, tol_rpx=7):
    want = [v * SC for v in want_frame]
    return all(abs(g - w) <= tol_rpx for g, w in zip(got, want)), \
           [f"{g:.1f}vs{w:.1f}" for g, w in zip(got, want)]

# ---- 0. house chrome checker (shared, closed-loop) ----
r = subprocess.run([sys.executable,
                    "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/shared_patterns/house_chrome_check.py",
                    REN], capture_output=True, text=True)
print(r.stdout.strip())
if r.returncode != 0:
    print(r.stderr)
check("house_chrome_check.py", r.returncode == 0, "(shared checker verdict above)")

# ---- 1. FRAME CONTAINMENT: every drawn element inside house frame interior ----
# house frame interior at 150dpi: x in [0.15,13.18]in -> [22.5,1977.5]; y in [22.5,1102.5]
rm, dm = redmask(a), darkmask(a)
elements = {
    # name: (mask, search window in render px)
    "left_panel_border": (dm, (int(93*SC)-12, int(106*SC)-12, int(413*SC)+12, int(524*SC)+12)),
    "right_panel_border": (dm, (int(476*SC)-12, int(151*SC)-12, int(894*SC)+12, int(472*SC)+12)),
    # NOTE: window starts below the chrome panel's top border row (render y ~94) —
    # the crisp render's C00000 border passes the red threshold (the JPEG frame's
    # softened border did not), so the frame-side title window (y>=45) is NOT
    # apples-to-apples here. Title band starts at y=100 (frame 48+).
    "title_ink": (rm, (150, 100, 1850, 200)),
    "red_caption_ink": (rm, (900, 210, 1600, 300)),
}
for name, (m, (x0, y0, x1, y1)) in elements.items():
    bb = inkbox(m, x0, y0, x1, y1)
    ok = bb is not None and bb[0] >= 24 and bb[1] >= 24 and bb[2] <= 1976 and bb[3] <= 1101
    check(f"containment:{name}", ok, f"bbox={bb}")

bm = bluemask(a)
bb = inkbox(bm, 900, 950, 1900, 1101)
ok = bb is not None and bb[2] <= 1976 and bb[3] <= 1101
check("containment:blue_takeaway", ok, f"bbox={bb}")

# arc (gutter, between panels) — must not touch either panel border
arc_win = (int(404*SC), int(262*SC), int(498*SC), int(356*SC))
abb = inkbox(rm, *arc_win)
lp_right = 411.5 * SC
rp_left = 476.5 * SC
ok = abb is not None and abb[0] > lp_right + 2 and abb[2] < rp_left - 2
check("containment:arc_in_gutter", ok, f"arc bbox={abb} must be inside ({lp_right:.0f},{rp_left:.0f})")

# ---- 2. TEXT ink bands vs frame targets (same thresholds both sides) ----
# Title target = frame ink incl. antialiased skirt (loose threshold R>135,R-G>35):
# frame loose ink (210,57,750,84) — the JPEG skirt is what a crisp strict threshold
# captures; strict-vs-strict deflates the frame side by ~1px/border.
t = inkbox(rm, 150, 100, 1850, 200)
ok, d = close(t, [210, 57, 750, 84])
check("title_ink_bbox", ok, f"render={t} frame*(SC)={d}")
t = inkbox(rm, 900, 210, 1600, 300)
ok, d = close(t, [464, 117, 719, 131])
check("red_caption_ink_bbox", ok, f"render={t} frame*(SC)={d}")
t = inkbox(bm, 900, 950, 1900, 1101)
ok, d = close(t, [456, 487, 879, 509])
check("blue_takeaway_ink_bbox", ok, f"render={t} frame*(SC)={d}")

# single-band (no wrap): ink rows contiguous within band
for name, m, (x0, y0, x1, y1) in [
    ("title", rm, (150, 100, 1850, 220)),
    ("redcap", rm, (900, 210, 1600, 300)),
    ("blue", bm, (900, 950, 1900, 1105)),
]:
    rows = np.where(m[y0:y1, x0:x1].sum(axis=1) > 0)[0]
    gaps = np.diff(rows) if len(rows) > 1 else np.array([0])
    check(f"nowrap:{name}", gaps.max() <= 3 if len(gaps) else True,
          f"ink rows {rows.min()+y0}..{rows.max()+y0}, max row gap {gaps.max() if len(gaps) else 0}")

# ---- 3. FIGURES: pastel|ink IoU vs frame, per panel ----
def figmask(arr):
    R, G, B = arr[..., 0], arr[..., 1], arr[..., 2]
    mx = np.maximum(np.maximum(R, G), B); mn = np.minimum(np.minimum(R, G), B)
    return ((mx - mn > 22) & (mx > 140)) | ((R < 110) & (G < 110) & (B < 110))

def panel_iou(name, fpix, rbox_frame):
    x0, y0, x1, y1 = [int(round(v * SC)) for v in rbox_frame]
    sub = a[y0:y1, x0:x1]
    # downscale render crop to frame resolution for apples-to-apples IoU
    crop = Image.fromarray(sub.astype(np.uint8)).resize((x1f := int(rbox_frame[2] - rbox_frame[0]),
                                                         int(rbox_frame[3] - rbox_frame[1])), Image.LANCZOS)
    ca = np.asarray(crop).astype(int)
    A, Bm = figmask(fpix), figmask(ca)
    iou = (A & Bm).sum() / max((A | Bm).sum(), 1)
    check(f"figure_iou:{name}", iou >= 0.60, f"IoU={iou:.3f} (frame rect {rbox_frame})")
    return iou

panel_iou("left", frame[115:522, 117:394], (117, 115, 394, 522))
panel_iou("right", frame[176:453, 478:885], (478, 176, 885, 453))

# ---- 4. ARC: red-mask IoU vs frame in gutter ----
gx0, gy0, gx1, gy1 = 404, 262, 498, 356
sub = a[int(gy0*SC):int(gy1*SC), int(gx0*SC):int(gx1*SC)]
crop = Image.fromarray(sub.astype(np.uint8)).resize((gx1-gx0, gy1-gy0), Image.LANCZOS)
ca = np.asarray(crop).astype(int)
A, Bm = redmask(frame[gy0:gy1, gx0:gx1]), redmask(ca)
iou = (A & Bm).sum() / max((A | Bm).sum(), 1)
check("arc_iou", iou >= 0.70, f"IoU={iou:.3f}")

# ---- 5. PANEL BORDERS present (dark line at 4 edges each) ----
def line_dark(arr, pts, tol=3):
    hits = 0
    for (x, y) in pts:
        x2, y2 = int(x*SC), int(y*SC)
        win = arr[max(0,y2-tol):y2+tol+1, max(0,x2-tol):x2+tol+1]
        if darkmask(win).any() or (win[...,0]<170).any():
            hits += 1
    return hits, len(pts)

for name, pts in {
    "left_panel":  [(x, 106) for x in (150, 250, 350)] + [(x, 522.5) for x in (150, 250, 350)] +
                   [(93.5, y) for y in (150, 300, 450)] + [(411.5, y) for y in (150, 300, 450)],
    "right_panel": [(x, 152) for x in (550, 650, 750)] + [(x, 470.5) for x in (550, 650, 750)] +
                   [(476.5, y) for y in (200, 300, 420)] + [(892.5, y) for y in (200, 300, 420)],
}.items():
    hits, n = line_dark(a, pts)
    check(f"panel_border:{name}", hits == n, f"{hits}/{n} probe points show dark border ink")

# ---- 6. PANEL INTERIOR white ----
for name, box in {"left": (130, 130, 380, 500), "right": (500, 200, 860, 440)}.items():
    x0, y0, x1, y1 = [int(v*SC) for v in box]
    interior = a[y0+6:y1-6:4, x0+6:x1-6:4]
    frac_white = ((interior > 235).all(axis=2)).mean()
    check(f"panel_white:{name}", frac_white > 0.55, f"white frac={frac_white:.2f} (figure ink occupies the rest)")

print("\nRESULT:", "ALL PASS" if not fails else f"FAILURES: {fails}")
sys.exit(0 if not fails else 1)
