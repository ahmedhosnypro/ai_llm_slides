#!/usr/bin/env python3
"""Slide 054 — tall-paren PNG generator (founder paren-defect fix, 2026-10-10).

ADOPTS the slide-053 certified construction VERBATIM (per coordinator directive
2026-10-10: "Reuse slide 53's construction; do not invent a third variant for
this defect class"): ONE smooth quadratic-Bézier centerline per delimiter,
pre-rendered at 600 dpi transparent PNG, embedded at exact size
(w = px/600 in, NEVER rescaled). See build/gen_parens53.py and
qa/slide053/paren_zoom/ (judge PASS attempt 7, founder zoom crop approved).

Replaces this slide's ARC-preset parens, which LibreOffice renders as
double-stroked hooked shapes (the founder screenshot defect: heavy near-
constant-width strokes with tight hooks colliding/clipping the digits), and
ADDS the Mean/S.D parens the previous build omitted entirely.

Geometry is PIL-measured from the ORIGINAL frame (960x540, 1px = 1pt);
forensics 5-7 (mid-band bulge-edge scan, loose ink extents, tip curls):
  - stroke bands (lum<235 mid-band): feat/norm/Mean/S.D ~3px any / ~2px core
    -> S=2.5pt; test ~4-5px any -> S=3.0pt.
  - tip-curl D (centerline tip - centerline bulge): 1..2.75px across all
    blocks within AA noise -> D=2.5pt (053's certified value).
  - ink bands (loose, lum<235, >=2px/row):
      feature   y215-263 (inkH 48)   all 9 pairs, class colors
      norm red  y324-359 (inkH 35)   washed-red strokes -> class color
      norm blue y324-361 (inkH 37)
      norm grn  y328-363 (inkH 35)
      test      y328-372 (inkH 44.5) black
      Mean      y217-259 (inkH 42.5) black   S.D y216-259 (inkH 43) black
  - conclusion parens (y446-503, inkH 57, S=3.5, black) are GEOMETRY-IDENTICAL
    to 053's certified callout -> the build REUSES
    assets/parens53/paren_{lp,rp}_57_000000.png (not regenerated here).

Run:  python3 videos/ml-intro/recreated_pptx/build/gen_parens54.py
"""
import json, os
import numpy as np
from PIL import Image
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = "videos/ml-intro/recreated_pptx/build/assets/parens54"
os.makedirs(OUT, exist_ok=True)
DPI = 600
D = 2.5        # bulge-to-tip horizontal pull, pt (centerline; original measured 1-2.75)
PAD = 0.5      # canvas safety pad, pt (AA room; placement compensates exactly)

# (class, S_pt, inkH_pt, hex) — inkH = target ink band height
CLASSES = [
    ("feat",  2.5, 48.0, "CC0000"),   # red feature columns
    ("feat",  2.5, 48.0, "0000CC"),   # blue feature columns
    ("feat",  2.5, 48.0, "2E8B22"),   # green feature columns
    ("nred",  2.5, 35.0, "CC0000"),   # normalized red columns
    ("nblue", 2.5, 37.0, "0000CC"),   # normalized blue columns
    ("ngreen", 2.5, 35.0, "2E8B22"),  # normalized green columns
    ("test",  3.0, 44.5, "000000"),   # normalized test vector (black)
    ("mean",  2.5, 42.5, "000000"),   # Mean column parens (were MISSING)
    ("sd",    2.5, 43.0, "000000"),   # S.D column parens (were MISSING)
    # att9 fix (founder zoom round 3): the ORIGINAL's Mean/S.D paren strokes are
    # FAINT neutral-gray paint — waist transects show darkest lum 155-181
    # (RGB ~(177,179,176)/(160,162,159), ZERO sub-170 pixels in the whole
    # paren window) while every solid >=2pt stroke in the same frame survives
    # dark (Mean digit '8' lum 57, S.D '4' lum 43, test paren lum 48, concl
    # paren lum 32). Solid black 2.5pt was therefore 3-6x the original ink —
    # the att8 C2 vision flag ("strokes noticeably heavier") was PIL-CONFIRMED.
    # Fix: SAME geometry (S=2.5, same inkH -> identical sidecars/anchors), color
    # = measured gray B3B3B3 (lum 179; the slide's own PLUS_GRAY precedent).
    ("mean",  2.5, 42.5, "B3B3B3"),   # Mean parens, measured faint gray
    ("sd",    2.5, 43.0, "B3B3B3"),   # S.D parens, measured faint gray
]

def bezier_x(t, x_tip, x_ctrl):
    return (1-t)**2 * x_tip + 2*(1-t)*t * x_ctrl + t**2 * x_tip

def render(cls, side, S, inkH, color):
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
    path = f"{OUT}/paren_{cls}_{side}_{inkH:.1f}_{color}.png"
    fig.savefig(path, dpi=DPI, transparent=True)
    plt.close(fig)
    # measure the actual ink bbox from the alpha channel
    a = np.array(Image.open(path))[:, :, 3]
    ys_i, xs_i = np.nonzero(a > 30)
    sidecar = {
        "px_w": a.shape[1], "px_h": a.shape[0],
        "ink_left_px": int(xs_i.min()), "ink_right_px": int(xs_i.max()),
        "ink_top_px": int(ys_i.min()), "ink_bot_px": int(ys_i.max()),
        "S_pt": S, "D_pt": D, "inkH_pt": inkH, "cls": cls, "color": color,
        "pt_per_px": 72.0 / DPI,
    }
    json.dump(sidecar, open(path.replace(".png", ".json"), "w"), indent=1)
    il, ir = sidecar["ink_left_px"]*0.12, sidecar["ink_right_px"]*0.12
    it, ib = sidecar["ink_top_px"]*0.12, sidecar["ink_bot_px"]*0.12
    print(f"{os.path.basename(path)}: canvas {a.shape[1]}x{a.shape[0]}px "
          f"({W:.1f}x{H:.1f}pt)  ink pt L{il:.2f} R{ir:.2f} T{it:.2f} B{ib:.2f} "
          f"(inkH {ib-it:.2f} vs target {inkH})")
    return path

for cls, S, inkH, color in CLASSES:
    for side in ("lp", "rp"):
        render(cls, side, S, inkH, color)
print("DONE ->", OUT)
