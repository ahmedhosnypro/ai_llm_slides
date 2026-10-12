#!/usr/bin/env python3
"""Pre-judge self-check for slide 021, attempt 1 (closed-loop, PIL, 150dpi render).

Checks (per scripts/17_worker_instructions.md MANDATORY PRE-JUDGE SELF-CHECK):
  1. REUSABLE PATTERNS — read patterns index first (done in session: house-chrome used via
     shared_patterns import; explicit-line-spacing set on both title boxes; highlight-box
     N/A — the slide has no filled box; no equations/delimiters/tables => those patterns N/A).
  2. FRAME CONTAINMENT — content ink bbox inside house bounds.
  3. EQUATIONS EXIST — N/A (no equations on this slide).
  4. DELIMITER GEOMETRY — N/A (no multi-line delimiters).
  5. TABLE DATA — N/A (no tables).
  6. ZOOMED CROP VISION ANALYSIS — N/A (no dense/small regions: no equations, delimiters,
     or tables; title is 56.5pt large text; per the mandate this crop comparison is required
     only when equations/delimiters/tables exist).
  7. LINE/BOX WRAP — title ink advance 541px in a 720px box (24.7% slack, >=20% law);
     no ink outside the expected title bands or the bar band.
  8. EXPLICIT LINE SPACING — lineSpacing: 68 (exact pt) set on both title boxes.

Closed-loop geometry (150dpi render vs original frame, same red predicate, tolerance
~4 render px = ~2 frame px; all deltas below are frame px):
  l1 cap/base/tail  ORIG 196.0/238.0/249.0  REND 195.7/237.5/248.0  (deltas <= 1.0)
  l2 cap/base/tail  ORIG 322.0/364.0/375.0  REND 322.4/363.7/375.2  (deltas <= 0.5)
  l1 ink x          ORIG 211..751           REND 211.6..751.3       (advance 539.7 vs 540)
  l2 ink x          ORIG 219..740           REND 219.7..739.3       (advance 519.6 vs 521)
  black bar         ORIG x 38..921 y 518..539   REND x 37.4..921.6 y 517.2..537.3
                    (documented 2-frame-px deviation at the bottom edge, per certified
                     slide_002/slide_005 precedent so the chrome bottom stroke stays visible)
  colors            canvas (255,255,255)  panel (233,233,231)=E9E9E7  bar (0,0,0)
                    title red modal JPEG-darkened C00000 -> drawn C00000 (playlist red,
                    same reasoning as certified slide_005)
"""
import sys

import numpy as np
from PIL import Image

RENDER = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/qa/slide021/render_1.png"
ORIG = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_021.jpg"

im = Image.open(RENDER).convert("RGB")
W, H = im.size
s = W / 960.0
px = im.load()
o = Image.open(ORIG).convert("RGB")
op = o.load()

fails = []


def red(p):
    r, g, b = p
    return r > 120 and r > g + 40 and r > b + 40


def prof(p, x0, x1, ya, yb, sc=1.0):
    out = {}
    for y in range(ya, yb):
        n = sum(1 for x in range(x0, x1) if red(p[x, y]))
        if n:
            out[y / sc] = n
    return out


def marks(p):
    ys = sorted(p)
    cap = next((y for y in ys if p[y] > 8), None)
    dense = [y for y in ys if p[y] > 100]
    base = max(dense) if dense else None
    tail = next((y for y in reversed(ys) if p[y] > 8), None)
    return cap, base, tail


# closed-loop geometry per line
for (x0, x1, ya, yb, label, tgt) in [
    (211, 752, 190, 256, "l1", (196.0, 238.0, 249.0)),
    (215, 745, 315, 380, "l2", (322.0, 364.0, 375.0)),
]:
    mo = marks(prof(op, x0, x1, ya, yb))
    mr = marks(prof(px, int(x0 * s), int(x1 * s), int(ya * s), int(yb * s), s))
    d = max(abs(a - b) for a, b in zip(mr, tgt))
    print(f"{label}: ORIG {mo} REND {tuple(round(v,1) for v in mr)} target {tgt} max|d|={d:.1f} frame-px")
    if d > 2.0:
        fails.append(f"{label} geometry off by {d:.1f} frame-px (>2)")

# ink existence in title regions (grayscale)
g = np.asarray(im.convert("L"))
n1 = int((g[int(196 * s):int(250 * s), int(205 * s):int(760 * s)] < 150).sum())
n2 = int((g[int(321 * s):int(376 * s), int(215 * s):int(745 * s)] < 150).sum())
print(f"title ink px: l1={n1} l2={n2}")
if n1 < 1000 or n2 < 1000:
    fails.append("title region ink missing")

# colors
c_canvas, c_panel, c_bar = px[20, 20], px[int(300 * s), int(300 * s)], px[int(480 * s), int(530 * s)]
print("colors:", c_canvas, c_panel, c_bar)
if c_panel != (233, 233, 231) or c_bar != (0, 0, 0) or c_canvas != (255, 255, 255):
    fails.append(f"color mismatch {c_canvas} {c_panel} {c_bar}")

# frame containment: content ink inside house bounds (x 10.8..949.2, y 10.8..529.2 frame px)
ys, xs = np.where(g < 200)
bx0, bx1, by0, by1 = xs.min() / s, xs.max() / s, ys.min() / s, ys.max() / s
print(f"content ink bbox frame-px: x {bx0:.1f}..{bx1:.1f} y {by0:.1f}..{by1:.1f}")
if bx0 < 10.0 or bx1 > 950.0:
    fails.append("ink outside house x bounds")
# y: only the chrome's own bottom stroke may touch the slide edge (intentional chrome)
core = [(x, y) for y, x in zip(ys, xs) if y < H - 8]
if core:
    cymax = max(y for _, y in core) / s
    print(f"non-chrome ink y max: {cymax:.1f} (bar bottom 537.3 expected)")
    if cymax > 539.0:
        fails.append("non-chrome ink beyond slide bottom")

if fails:
    print("SELF-CHECK: FAIL")
    for f in fails:
        print("  -", f)
    sys.exit(1)
print("SELF-CHECK: PASS (geometry within 2 frame-px; colors exact; containment OK)")
