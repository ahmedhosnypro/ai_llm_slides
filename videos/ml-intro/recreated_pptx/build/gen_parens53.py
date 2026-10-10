#!/usr/bin/env python3
"""Slide 053 — tall-paren PNG generator (founder paren-defect fix, 2026-10-10).

Replaces the ARC-preset parens (which LibreOffice renders as a double-stroked
blob with merged top/bottom caps — the founder's "inner curve on top and
bottom"; see qa/slide053/paren_zoom/*_defect.txt and measure_parens_attempt7.out)
with 600dpi transparent PNGs of ONE smooth quadratic-Bezier centerline per
delimiter, per P3 (one glyph/shape sized to span ALL enclosed lines).

Geometry is PIL-measured from the ORIGINAL frame (960x540, 1px = 1pt):
  - grid colored columns: paren ink band y212.5-266.5 (h54), bulge-to-tip
    horizontal pull D ~ 2.5pt, stroke 2-4px (washed)  -> S=3.0pt
  - test column (black):              y212-270  (h58), stroke 4-6px -> S=4.0pt
  - callout result-box (black):       y446-503  (h57), stroke 3-4px -> S=3.5pt
Curve: quadratic Bezier  P0=(tip, ytop+S/2)  P1=(2*bulge-tip, ymid)  P2=(tip, ybot-S/2)
  => bulge at exact mid-height, single monotonic bow (NO hooks possible),
     near-vertical terminals (dx/dt at tips = 4*(bulge-tip) = -2*2*2.5pt over
     54pt height ~ 10.5deg off vertical — matches the original's measured
     terminal profile). Round caps land the ink exactly on y_top/y_bot.

Each PNG gets a sidecar .json with the PIL-measured ink bbox so the build
lands the ink at the exact target anchors (w = px/600 in, NEVER rescaled).

Run:  python3 videos/ml-intro/recreated_pptx/build/gen_parens53.py
"""
import json, os
import numpy as np
from PIL import Image
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = "videos/ml-intro/recreated_pptx/build/assets/parens53"
os.makedirs(OUT, exist_ok=True)
DPI = 600
D = 2.5        # bulge-to-tip horizontal pull, pt (original measured 2-2.5)
PAD = 0.5      # canvas safety pad, pt (AA room; placement compensates exactly)

# (name, S_pt, inkH_pt, hex)  — inkH = target ink band height
CLASSES = [
    ("grid", 3.0, 54.0, "C00000"),   # red class columns
    ("grid", 3.0, 54.0, "0000CC"),   # blue class columns
    ("grid", 3.0, 54.0, "2E8B22"),   # green class columns
    ("test", 4.0, 58.0, "000000"),   # test column (black)
    ("call", 3.5, 57.0, "000000"),   # result-box callout (black)
]

def bezier_x(t, x_tip, x_ctrl):
    return (1-t)**2 * x_tip + 2*(1-t)*t * x_ctrl + t**2 * x_tip

def render(side, S, inkH, color):
    # canvas in pt: width must hold bulge(stroke S/2 each side) + D + pads
    W = S + D + 2*PAD
    H = inkH + 2*PAD
    if side == "lp":      # "(" bulge at LEFT edge region
        x_bulge = PAD + S/2.0
        x_tip   = x_bulge + D
    else:                 # ")" bulge at RIGHT edge region
        x_bulge = W - PAD - S/2.0
        x_tip   = x_bulge - D
    x_ctrl = 2*x_bulge - x_tip
    t = np.linspace(0.0, 1.0, 400)
    xs = bezier_x(t, x_tip, x_ctrl)
    ys = np.linspace(PAD + S/2.0, H - PAD - S/2.0, 400)   # linear: ctrl on midpoint
    fig = plt.figure(figsize=(W/72.0, H/72.0))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis("off")
    ax.plot(xs, ys, lw=S, color="#" + color, solid_capstyle="round",
            solid_joinstyle="round")
    path = f"{OUT}/paren_{side}_{inkH:.0f}_{color}.png"
    fig.savefig(path, dpi=DPI, transparent=True)
    plt.close(fig)
    # measure the actual ink bbox from the alpha channel
    a = np.array(Image.open(path))[:, :, 3]
    ys_i, xs_i = np.nonzero(a > 30)
    sidecar = {
        "px_w": a.shape[1], "px_h": a.shape[0],
        "ink_left_px": int(xs_i.min()), "ink_right_px": int(xs_i.max()),
        "ink_top_px": int(ys_i.min()), "ink_bot_px": int(ys_i.max()),
        "S_pt": S, "D_pt": D, "inkH_pt": inkH, "color": color,
        "pt_per_px": 72.0 / DPI,
    }
    json.dump(sidecar, open(path.replace(".png", ".json"), "w"), indent=1)
    il, ir = sidecar["ink_left_px"]*0.12, sidecar["ink_right_px"]*0.12
    it, ib = sidecar["ink_top_px"]*0.12, sidecar["ink_bot_px"]*0.12
    print(f"{os.path.basename(path)}: canvas {a.shape[1]}x{a.shape[0]}px "
          f"({W:.1f}x{H:.1f}pt)  ink pt L{il:.2f} R{ir:.2f} T{it:.2f} B{ib:.2f} "
          f"(inkH {ib-it:.2f} vs target {inkH})")
    return path

for name, S, inkH, color in CLASSES:
    for side in ("lp", "rp"):
        render(side, S, inkH, color)
print("DONE ->", OUT)
