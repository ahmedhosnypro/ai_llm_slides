#!/usr/bin/env python3
"""Generate slide 017's three W-box interiors as 600-dpi transparent PNGs.

Region per band = the W box's interior in frame px (960x540, 1px = 1pt):
  origin (507, 128/266/404), size 115 x 123 px  (parent 013's certified W-box
  origin/size, re-measured on 017's frame: border centreline x507..622,
  y127..251 / 265..389 / 403..527).

Contents (all measured from unique_slides/slide_017.jpg, see
qa/slide017/measure_017.txt):
  * red italic serif "W" with a red underline bar
  * black "=" (two bars)
  * thin black parentheses spanning the three stacked values
  * the three vector values, black serif (0.1/1.95/0.03 | 1.2/0.72/0.77 |
    1.77/0.32/0.99) at the frame's measured baselines
  * the blue ||W||^2 = <value> line (3.8 | 2.45 | 4.2) with a blue underline
    under the W, at the frame's measured position
  Unlike slide 013 there is NO pale-yellow ellipse on 017 — measured 0 pale-yellow
  px inside the three boxes.

matplotlib mathtext (STIX = Times-like) is the deck's certified mechanism for
math; images are placed at exact px/600 inches, never rescaled.
"""
import json
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import PathPatch
from matplotlib.path import Path
from matplotlib import rcParams

rcParams["mathtext.fontset"] = "stix"
rcParams["font.family"] = "Liberation Serif"

HERE = os.path.dirname(os.path.abspath(__file__))
W_PX, H_PX = 115, 123
RED = "#C00000"
BLACK = "#000000"
BLUE = "#0000A7"

# per band: y0 = interior origin y; every item in ABSOLUTE frame px
BANDS = [
    dict(y0=128,
         w=dict(cx=530.0, base=172.4, under=(521.0, 538.5, 178.0)),
         eq=dict(x0=543.0, x1=555.5, y1=168.6, y2=173.6),
         parens=dict(ltip=557.5, lbody=560.2, rtip=606.5, rbody=603.8, yt=137.0, yb=211.5),
         digits=[("0.1", 582.5, 156.0), ("1.95", 582.5, 180.5), ("0.03", 582.5, 206.0)],
         norm=dict(x_abs=524.0, x_eq=567.0, x_val=582.0, base=240.0,
                   under=(530.0, 545.0), text="3.8")),
    dict(y0=266,
         w=dict(cx=535.5, base=310.5, under=(528.5, 543.5, 315.5)),
         eq=dict(x0=549.0, x1=560.5, y1=306.5, y2=311.7),
         parens=dict(ltip=561.0, lbody=563.7, rtip=611.0, rbody=608.3, yt=274.0, yb=350.0),
         digits=[("1.2", 588.5, 293.0), ("0.72", 588.5, 318.5), ("0.77", 588.5, 344.0)],
         norm=dict(x_abs=521.0, x_eq=573.0, x_val=588.0, base=378.5,
                   under=(527.0, 542.0), text="2.45")),
    dict(y0=404,
         w=dict(cx=530.5, base=449.0, under=(522.0, 539.0, 455.0)),
         eq=dict(x0=544.0, x1=555.5, y1=444.5, y2=449.5),
         parens=dict(ltip=557.5, lbody=560.2, rtip=606.5, rbody=603.8, yt=412.0, yb=487.0),
         digits=[("1.77", 583.0, 431.0), ("0.32", 583.0, 456.0), ("0.99", 583.0, 482.0)],
         norm=dict(x_abs=521.0, x_eq=570.0, x_val=585.0, base=514.0,
                   under=(527.0, 542.0), text="4.2")),
]

DIGIT_FS = 21.5      # measured value ink height 14px ~ STIX cap 0.662em
W_FS = 21.5
NORM_FS = 20.5

sidecar = []
for i, b in enumerate(BANDS, start=1):
    y0 = b["y0"]
    fig = plt.figure(figsize=(W_PX / 72.0, H_PX / 72.0), dpi=600)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(507, 507 + W_PX)
    ax.set_ylim(y0 + H_PX, y0)          # inverted y: frame coordinates
    ax.axis("off")
    fig.patch.set_alpha(0)

    # ── "W" red italic + red underline ──────────────────────────────────────
    W = b["w"]
    ax.text(W["cx"], W["base"], r"$W$", fontsize=W_FS, color=RED,
            ha="center", va="baseline", zorder=3)
    ax.plot([W["under"][0], W["under"][1]], [W["under"][2], W["under"][2]],
            color=RED, lw=1.6, zorder=3)

    # ── "=" two black bars ──────────────────────────────────────────────────
    E = b["eq"]
    for yy in (E["y1"], E["y2"]):
        ax.plot([E["x0"], E["x1"]], [yy, yy], color=BLACK, lw=1.5, zorder=3)

    # ── parentheses as cubic Beziers ────────────────────────────────────────
    P = b["parens"]
    for tip, body in ((P["ltip"], P["lbody"]), (P["rtip"], P["rbody"])):
        verts = [(tip, P["yt"]), (body, P["yt"] + 18), (body, P["yb"] - 18), (tip, P["yb"])]
        codes = [Path.MOVETO, Path.CURVE4, Path.CURVE4, Path.CURVE4]
        ax.add_patch(PathPatch(Path(verts, codes), facecolor="none",
                               edgecolor=BLACK, lw=0.9, zorder=3))

    # ── stacked vector values ───────────────────────────────────────────────
    for txt, cx, base in b["digits"]:
        ax.text(cx, base, txt, fontsize=DIGIT_FS, color=BLACK,
                ha="center", va="baseline", zorder=3)

    # ── ||W||^2 = value (blue) with underline under the W ───────────────────
    N = b["norm"]
    ax.text(N["x_abs"], N["base"], r"$\|W\|^2$", fontsize=NORM_FS, color=BLUE,
            ha="left", va="baseline", zorder=3)
    ax.text(N["x_eq"], N["base"], r"$=$", fontsize=NORM_FS, color=BLUE,
            ha="left", va="baseline", zorder=3)
    ax.text(N["x_val"], N["base"], "$%s$" % N["text"], fontsize=NORM_FS, color=BLUE,
            ha="left", va="baseline", zorder=3)
    ax.plot([N["under"][0], N["under"][1]], [N["base"] + 2.2, N["base"] + 2.2],
            color=BLUE, lw=1.3, zorder=3)

    name = "wbox17_band%d.png" % i
    fig.savefig(os.path.join(HERE, name), dpi=600, transparent=True)
    plt.close(fig)
    sidecar.append(dict(image=name, origin=(507, y0), size_px=(W_PX, H_PX)))

with open(os.path.join(HERE, "wbox17_sidecar.json"), "w") as f:
    json.dump(sidecar, f, indent=2)
print(json.dumps(sidecar, indent=2))
