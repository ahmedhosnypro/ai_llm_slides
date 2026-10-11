#!/usr/bin/env python3
"""Closed-loop check v2: title ink in the 150dpi render vs mapped original targets.

Like-for-like metrics on BOTH images (row profiles, >=20 ink px threshold):
  ink x0/x1 (min/max ink column), cx, cap top (first row with >=20 ink px),
  baseline (last row with >=20 ink px — text has no descenders).

Targets (mapped from the original frame via slide_x=(fx-18.128)/0.961235,
slide_y=(fy+0.045)/0.956566, then x150 = pt*150/72):
  original frame rows/cols: ink x 238..710; >=20px rows: cap 271, baseline 302
  -> ink x0 228.75pt=476.56px, x1 719.76pt=1499.51px (w 1022.9px)
     cap top 282.37pt=588.27px ; baseline (302+0.045)/0.956566=315.90pt=658.13px
     cx 474.26pt=988.04px
Tolerance ~4px @150dpi.
"""
import sys
from PIL import Image

RENDER = sys.argv[1] if len(sys.argv) > 1 else "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide050/render_1.png"
im = Image.open(RENDER).convert("RGB")
px = im.load()

def is_red(c):
    r, g, b = c
    return r > 90 and r - max(g, b) > 50

X0S, X1S, Y0S, Y1S = 300, 1700, 500, 740
rows = {}
cols = {}
for y in range(Y0S, Y1S):
    n = 0
    for x in range(X0S, X1S):
        if is_red(px[x, y]):
            n += 1
            cols.setdefault(x, []).append(y)
    if n:
        rows[y] = n

xs_all = sorted(cols)
x0, x1 = xs_all[0], xs_all[-1]
cx = (x0 + x1) / 2
cap = min(y for y, n in rows.items() if n >= 20)
base = max(y for y, n in rows.items() if n >= 20)
print(f"render title ink: x {x0}..{x1} (w {x1-x0}), cx {cx:.1f}, cap {cap}, baseline {base}")

T = dict(x0=476.56, x1=1499.51, cap=588.27, base=658.13, cx=988.04)
d = {k: (x0 - T['x0'], ) for k in ()}  # placeholder
deltas = dict(x0=x0 - T['x0'], x1=x1 - T['x1'], cap=cap - T['cap'], base=base - T['base'], cx=cx - T['cx'])
print("deltas (render - target):", {k: round(v, 1) for k, v in deltas.items()})
w = x1 - x0
print(f"ink width {w} vs target {T['x1']-T['x0']:.0f} (delta {w-(T['x1']-T['x0']):+.1f}px) -> fs *= {(T['x1']-T['x0'])/w:.4f}")
ok = all(abs(v) <= 4.0 for v in deltas.values())
print("CLOSED LOOP:", "PASS (all deltas <= 4px)" if ok else "FAIL — needs correction")
