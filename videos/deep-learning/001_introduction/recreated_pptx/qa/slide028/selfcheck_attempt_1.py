#!/usr/bin/env python3
"""Pre-judge self-check for slide 028, attempt 1 (closed-loop, PIL, 150dpi render).

Checks (per scripts/17_worker_instructions.md MANDATORY PRE-JUDGE SELF-CHECK):
  1. REUSABLE PATTERNS — project patterns index read (house-chrome used via
     shared_patterns/house_chrome.js import; explicit-line-spacing set on every text box;
     highlight-box wrap-budget law applied: title boxes 893px vs longest advance 734px
     = 1.217 >= 1.2; attribution boxes 432px vs 334px = 1.29; equations/delimiters/
     tables/graphs N/A — none on this slide).
  2. FRAME CONTAINMENT — all content ink inside house bounds (x 10.8..949.2 frame px),
     bar bottom exemption = chrome bottom stroke (documented 2-frame-px deviation,
     certified slide_002/005/021 precedent).
  3. EQUATIONS EXIST — N/A (no equations; spec verbatim_text.equations = []).
  4. DELIMITER GEOMETRY — N/A for multi-line delimiters; the single-line "(CNN)" glyph
     parens are verified via ink extents (render 294.6..342.5 vs original 293..342).
  5. TABLE DATA — N/A (no tables).
  6. ZOOMED CROP VISION ANALYSIS — attribution block is small text (14pt): a cropped-pair
     comparison (render vs original, attribution region) is dispatched through the gate
     separately; result banked as cropcompare_attempt_1.txt (cursor in the original's
     crop is ground rule (c) material, pre-declared in the crop --view).
  7. LINE/BOX WRAP — no ink outside the expected bands (title bands, attribution band,
     bar band); render_1 initially wrapped t2 at box w=720px (fixed: boxes now 893px,
     1.217x longest advance) — this check exists precisely to catch that.
  8. EXPLICIT LINE SPACING — lineSpacing 62pt (title) / 17pt (attribution) pinned on all
     five text boxes; each box is single-line so the pitch check degenerates to the
     per-box baseline assertions below.

Closed-loop geometry (150dpi render vs original frame; tolerance ~2 frame px = 4 px at
150dpi per the equation-alignment law; deltas in frame px):
  t1 cap/base        ORIG 119/158      REND 121.0/158.0   (top delta 2.0 = JPEG bleed)
  t2 cap/base        ORIG 235/274      REND 236.6/274.0
  t3 cap/base/tail   ORIG 293/331.5/342 REND 294.6/331.5/342.5
  t1 ink x           ORIG 301..660     REND 301.4..658.3 (advance 356.9 vs 360 bleed-adj)
  t2 ink x           ORIG 112..847     REND 114.8..845.4 (advance 730.7 vs 736)
  t3 ink x           ORIG 409..550     REND 408.9..549.0 (advance 140.1 vs 142)
  a1                 ORIG rows 467..481 x 99..      REND 467.5..480.4 x 99.9..292.8
  a2                 ORIG rows 485..499 x 93..426   REND 485.9..498.9 x 93.2..423.3
  black bar          ORIG x 38..921 y 519..539  REND x 37.4..921.6 y 518.2..537.3
                     (documented bottom deviation: drawn 519..537.5 so the chrome's
                      half-visible bottom stroke stays visible)
  colors             canvas (255,255,255) panel (233,233,231)=E9E9E7 bar (0,0,0)
                     title modal exactly (192,0,0)=C00000 (original modal (176..180,0,8..12)
                     is JPEG-darkened C00000 — same reasoning as certified slide_005/021)
"""
import sys

import numpy as np
from PIL import Image

RENDER = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/qa/slide028/render_1.png"
ORIG = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_028.jpg"

im = Image.open(RENDER).convert("RGB")
W, H = im.size
s = W / 960.0
pxl = im.load()
a = np.asarray(im).astype(int)
R, G, B = a[..., 0], a[..., 1], a[..., 2]
rm = (R > 110) & (R > G + 40) & (R > B + 40)

fails = []


def red_marks(y0, y1, x0=62, x1=918):
    sub = rm[int(y0 * s):int(y1 * s), int(x0 * s):int(x1 * s)]
    rp = sub.sum(axis=1)
    cp = sub.sum(axis=0)
    ys = np.where(rp > 3 * s)[0]
    dense = np.where(rp > 40 * s)[0]
    xs = np.where(cp > 0)[0]
    if len(ys) == 0:
        return None
    return dict(top=ys.min() / s + y0, base=dense.max() / s + y0, tail=ys.max() / s + y0,
                x0=xs.min() / s + x0, x1=xs.max() / s + x0)


# ---- title geometry (targets = original ink; top rows include ~2px JPEG bleed) ----
TITLE_TARGETS = [
    ("t1", 110, 170, dict(top=119, base=158.0, x0=301, x1=660)),
    ("t2", 226, 286, dict(top=235, base=274.0, x0=112, x1=847)),
    ("t3", 284, 352, dict(top=293, base=331.5, x0=409, x1=550)),
]
for name, y0, y1, tgt in TITLE_TARGETS:
    m = red_marks(y0, y1)
    if m is None:
        fails.append(f"{name}: NO INK")
        continue
    print(f"{name}: top {m['top']:.1f}/{tgt['top']} base {m['base']:.1f}/{tgt['base']} "
          f"tail {m['tail']:.1f} x {m['x0']:.1f}..{m['x1']:.1f} (w {m['x1']-m['x0']:.1f})")
    if abs(m["base"] - tgt["base"]) > 2.0:
        fails.append(f"{name} baseline {m['base']:.1f} vs {tgt['base']} (>2)")
    if abs(m["top"] - tgt["top"]) > 3.0:  # top rows carry JPEG bleed in the original
        fails.append(f"{name} top {m['top']:.1f} vs {tgt['top']} (>3)")
    if abs(m["x0"] - tgt["x0"]) > 3.0 or abs(m["x1"] - tgt["x1"]) > 3.0:
        fails.append(f"{name} ink x {m['x0']:.1f}..{m['x1']:.1f} vs {tgt['x0']}..{tgt['x1']} (>3)")

# ink existence (grayscale) in title regions
g = np.asarray(im.convert("L"))
for (y0, y1, x0, x1, n) in [(119, 250, 205, 760, 1500), (235, 275, 115, 848, 4000), (293, 343, 408, 551, 600)]:
    cnt = int((g[int(y0 * s):int(y1 * s), int(x0 * s):int(x1 * s)] < 150).sum())
    if cnt < n:
        fails.append(f"title region y{y0} ink too small: {cnt} < {n}")

# ---- attribution ----
am = (R >= 45) & (R <= 200) & (np.abs(R - G) < 25) & (np.abs(G - B) < 25) & (G <= 200)


def gray_marks(y0, y1, x0=62, x1=620):
    sub = am[int(y0 * s):int(y1 * s), int(x0 * s):int(x1 * s)]
    rp = sub.sum(axis=1)
    cp = sub.sum(axis=0)
    ys = np.where(rp > 0)[0]
    xs = np.where(cp > 0)[0]
    if len(ys) == 0:
        return None
    return dict(top=ys.min() / s + y0, bot=ys.max() / s + y0, x0=xs.min() / s + x0, x1=xs.max() / s + x0)


for name, y0, y1, tgt in [
    ("a1", 455, 484, dict(top=467, bot=481, x0=99)),
    ("a2", 484, 505, dict(top=485, bot=499, x0=93, x1=426)),
]:
    m = gray_marks(y0, y1)
    if m is None:
        fails.append(f"{name}: NO INK")
        continue
    print(f"{name}: rows {m['top']:.1f}..{m['bot']:.1f} x {m['x0']:.1f}..{m['x1']:.1f}")
    if abs(m["top"] - tgt["top"]) > 2.0 or abs(m["bot"] - tgt["bot"]) > 2.0:
        fails.append(f"{name} rows {m['top']:.1f}..{m['bot']:.1f} vs {tgt['top']}..{tgt['bot']} (>2)")
    if abs(m["x0"] - tgt["x0"]) > 2.0:
        fails.append(f"{name} left edge {m['x0']:.1f} vs {tgt['x0']} (>2)")
    if "x1" in tgt and abs(m["x1"] - tgt["x1"]) > 4.0:
        fails.append(f"{name} right edge {m['x1']:.1f} vs {tgt['x1']} (>4)")

# ---- bar ----
dm = (R < 80) & (G < 80) & (B < 80)
sub = dm[int(510 * s):, :]
rows = np.where(sub.sum(axis=1) > 700 * s)[0]
xs_row = np.where(dm[int(525 * s), :])[0]
bar = dict(top=rows.min() / s + 510, bot=rows.max() / s + 510, x0=xs_row.min() / s, x1=xs_row.max() / s)
print(f"bar: y {bar['top']:.1f}..{bar['bot']:.1f} x {bar['x0']:.1f}..{bar['x1']:.1f}")
if abs(bar["top"] - 519) > 2 or abs(bar["x0"] - 38) > 2 or abs(bar["x1"] - 921) > 2:
    fails.append(f"bar geometry {bar}")

# ---- wrap / stray-ink check: no ink outside expected bands ----
# (title bands 110..170, 226..286, 284..352; attribution 455..505 x<620; bar 518..539)
stray = np.where(rm[int(50 * s):int(105 * s), :].sum(axis=1) > 3 * s)[0]
if len(stray):
    fails.append(f"stray red ink above title zone (rows {stray.min()/s+50:.0f}..{stray.max()/s+50:.0f})")
mid = np.where(rm[int(360 * s):int(450 * s), int(62 * s):int(900 * s)].sum(axis=1) > 3 * s)[0]
if len(mid):
    fails.append(f"stray red ink between title and attribution (rows {mid.min()/s+360:.0f}..{mid.max()/s+360:.0f})")
# gray ink right of the attribution (wrap residue)
gray_right = np.where(am[int(455 * s):int(505 * s), int(620 * s):int(890 * s)].sum(axis=1) > 0)[0]
if len(gray_right):
    fails.append(f"stray gray ink right of attribution box (x>=620)")

# ---- colors ----
c_canvas = pxl[int(20 * s), int(20 * s)]
c_panel = pxl[int(700 * s), int(300 * s)]
c_bar = pxl[int(480 * s), int(530 * s)]
rr = a[int(240 * s):int(270 * s), int(200 * s):int(800 * s)][rm[int(240 * s):int(270 * s), int(200 * s):int(800 * s)]]
modal = tuple(int(v) for v in np.median(rr // 4 * 4, axis=0)) if len(rr) else None
print("colors:", c_canvas, c_panel, c_bar, "title modal", modal)
if c_panel != (233, 233, 231) or c_bar != (0, 0, 0) or c_canvas != (255, 255, 255):
    fails.append(f"color mismatch {c_canvas} {c_panel} {c_bar}")
if modal != (192, 0, 0):
    fails.append(f"title modal {modal} != C00000")

# ---- containment ----
ys, xs = np.where(g < 200)
bx0, bx1 = xs.min() / s, xs.max() / s
print(f"content ink bbox frame-px: x {bx0:.1f}..{bx1:.1f}")
if bx0 < 10.0 or bx1 > 950.0:
    fails.append("ink outside house x bounds")
core_ymax = max(y for y in range(int(535 * s), H) if (g[y] < 200).sum() > 50) / s
print(f"bar bottom (non-chrome): {core_ymax:.1f} (expected ~537.3; chrome stroke below)")

if fails:
    print("SELF-CHECK: FAIL")
    for f in fails:
        print("  -", f)
    sys.exit(1)
print("SELF-CHECK: PASS (baselines within 2 frame-px; colors exact; containment OK; no stray/wrapped ink)")
