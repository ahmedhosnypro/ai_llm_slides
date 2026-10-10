#!/usr/bin/env python3
"""Slides 043/044 — scene-A NN scatter generator (shared canonical scene, graphgen).

Decision (per ratified triage plan P-43/P-44, qa/graph_triage/triage_report.md; agy CLI
was down (HTTP 401, token stale, fresh-mint attempt also 401) so lib choice follows the
triage plan + slide-64 pilot precedent — same matplotlib/sklearn stack the pilot PASSed):
  lib      : matplotlib (points/lines/axes are geometric) + scikit-learn
  function : sklearn.neighbors.NearestNeighbors(n_neighbors=1).fit(pts).kneighbors(query)
  algorithm: nearest-neighbor search — the SAME algorithm the lecture slide teaches;
             it selects the highlighted neighbor on slide 044's right panel (computed,
             not hand-picked: argmin over the 26 measured points).
  data     : the MEASURED original point positions (canonical scene A, extracted from
             unique_slides/slide_043.jpg / slide_044.jpg by PIL forensics this session;
             re-verified vs qa/graph_triage/measured_graph_facts.json, drift <= 2 px).

Measured facts (px in the 960x540 frame, 1px = 1pt; forensics v1-v3 banked in
qa/slide43/graphgen/ and qa/slide44/graphgen/):
  - scene A left panel: 11 green, 9 cyan, 6 tan dots, red query (301.6, 356.1);
    slide 043 adds a big red dot (116.1, 344.4) near the y-axis + red '?' glyph
    (bbox 330..338 x 347..358) right of the query.
  - axes: dark-red #8B0000 L-shape, no ticks; v-line x=103.5 (arrowhead tip y~181,
    base y~188, 8 px wide), h-line y~476 ending x~440 (043/044-left) with a small
    arrowhead; 044 right panel v-line x=500, h-line y~475 ending x~837 (arrowhead).
  - 044 right panel = left scene with per-cluster x-offsets (green +391.8, cyan
    +394.9, tan +396.5, query +394.9) — measured, NOT a rigid +392 shift.
  - dot diameters (2026-10-10 re-measure, radial profiles): green 18, cyan 17.5,
    tan 18, query 16, 043 big red 26 px ink, each with a bright core (see INK);
    044-R NN highlight (yellow #FFF200) ~16 px + dashed #8B0000 circle r~11.5.
  - 044-R connector web: thin pale-pink lines from query to all 26 dots, each
    ending in a small dark-red arrowhead at the target dot's edge (044 deep-verify
    2026-10-10 pixel grids re-confirmed the marks; the earlier strict-mask hunt
    that read "no arrowheads" was too tight).
  - panel bg white (254,255,253); '?' red #E02020 (043 spec) / dark red (044 spec).

Region (addImage target, slide px -> in at 1px=1pt):
  043: x 92..452, y 160..484  -> 1.2778, 2.2222, 5.0000, 4.5000 in
  044: x 92..846, y 160..484  -> 1.2778, 2.2222, 10.4722, 4.5000 in
"""
import argparse
import json
import math

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Polygon
import numpy as np
from sklearn.neighbors import NearestNeighbors

# ---- canonical scene A (left panel, px) — verified vs originals this session ----
GREEN = [(134, 327), (134, 349), (161, 318), (161, 346), (182, 261), (182, 289),
         (191, 343), (203, 267), (218, 302), (254, 254), (288, 220)]
CYAN = [(337, 172), (345, 258), (358, 192), (358, 229), (381, 261), (385, 213),
        (400, 192), (418, 223), (433, 201)]
TAN = [(247, 445), (265, 416), (274, 442), (292, 401), (301, 438), (313, 417)]
QUERY = (301.6, 356.1)
BIG_RED_043 = (116.1, 344.4)

# 044 right-panel per-cluster x-offsets (measured from slide_044.jpg)
OFF_R = {"green": 391.8, "cyan": 394.9, "tan": 396.5, "query": 394.9}

AXES = "#8B0000"
ARROW = "#C00000"       # measured arrowhead cores are brighter than the lines
PINK = "#EEE1E1"        # 044 deep-verify 2026-10-10: orig web ink core ~(235,222,222)
                       # after deblur (F4C2C2 read too saturated next to the JPEG
                       # original; qa/slide44/graphgen verify_crop_rightpanel_1.txt).
                       # PINK is used ONLY in the 044 branch (043 has no web).
WEB_TIP = "#8B0000"     # 044: small dark-red arrowheads at every connector/dot
                       # junction — deep-verify pixel grids found compact 2-3px
                       # dark-red clusters at ALL 26 junctions, color independent
                       # of the target dot's own color (real marks; the earlier
                       # "no arrowheads" hunt used too strict a mask).
YELLOW = "#FFF200"

REGIONS = {
    "043": (92, 160, 452, 484),
    "044": (92, 160, 846, 484),
}
SLIDE_SPEC = {
    "043": {"green": "#7ED957", "cyan": "#2FE0E0", "tan": "#E8C9A0",
            "query": "#E02020", "big_red": True,
            # 043 deep-verify round 2 (probe_qmark_v1, 2026-10-10): the 043
            # original's '?' is a DARK BRICK/MAROON glyph (blur-corrected paint
            # ~= #8B1A1A, the deck's accent maroon — the c5 closeup judge read
            # the old spec #E02020 as "brighter than the original's darker/
            # brick-red"), and it is ~16pt (crisp ink ~8x11 sits inside the
            # original's blurred 10x12 extent; 20pt rendered 10.1x14.4 —
            # visibly taller than the original).
            "qmark": "#8B1A1A", "qmark_pt": 16, "glossy_query": True,
            "qmark_anchor": (333.7, 355.4)},
    "044": {"green": "#7CFC00", "cyan": "#00E5E5", "tan": "#F5C98A",
            "query": "#FF0000", "qmark": "#C00000", "big_red": False,
            # 044 keeps the banked flat query dot + 20pt '?' (its PNG is
            # frozen; 044 was not flagged — this dispatch is 043 only).
            "qmark_pt": 20, "glossy_query": False,
            "qmark_anchor": (332.5, 356.7)},  # = banked QMARK anchor
}

# ---- Dot rendering — 2026-10-10 founder deep-verify fix (slide 043 dispatch) ----
# Radial profiles of the ORIGINAL frames (qa/slide43/graphgen/forensics_v4* +
# per-angle probes) show every dot is a shaded 3D ball: bright core out to
# r ~4.5-5.5 (big red r ~10.5), then a darker rim band to the ink edge
# (r ~8-9; big red r ~13). Cross-checked on slide_044.jpg — identical profile.
# The earlier flat single-color markers read dull and too small/large per
# class; these two-tone constants reproduce the measured balls.
#   d = full ink diameter (pt), d_core = bright-core diameter (pt).
INK = {
    "green": {"core": "#84FF02", "rim": "#87DF3C", "d": 18.0, "d_core": 10.5},
    "cyan":  {"core": "#14FFFB", "rim": "#44DFC8", "d": 17.5, "d_core": 10.0},
    "tan":   {"core": "#F6C89C", "rim": "#C3AF97", "d": 18.0, "d_core": 12.0},
    "query": {"core": "#E70000", "rim": "#B40310", "d": 16.0, "d_core": 9.5},
    "big":   {"core": "#EF3046", "rim": "#C83C50", "d": 26.0, "d_core": 21.0},
}
D_NN = 16.0             # 044-R yellow NN highlight (flat, as banked)
DPI = 300
AX_LW = 3.5             # measured axis core ~2 px + AA wash (mask reads 4-8; real 3.5-4)
# '?' glyph: measured ink bbox 327..337 x 347..362 (11x15) on BOTH 043 and 044;
# Arial bold 20pt lands there (17pt DejaVu rendered 7x12.5 — too small).
QMARK = {"fontsize": 20, "x": 332.5, "y": 356.7, "font": "Arial"}
#   ^ calibrated: Arial-bold va="center" centers the font bbox, not the ink;
#     (332.5, 356.7) lands the 20pt ink at 328..337 x 347..362 (graphcheck_v3).
# Per-slide anchor/size live in SLIDE_SPEC ("qmark_pt" + "qmark_anchor"); 043's
# 16pt anchor is the first guess of the same calibration loop (ink mid y sits
# ~1.8px above the va=center anchor at 16pt; ink mid x ~= anchor x).

# 043 query dot — glossy 3D ball, deep-verify round 2 (probe_qmark_v1,
# 2026-10-10). The c5 x3-closeup judge read the concentric two-tone disc as
# "larger and flatter" than the original: the original's solid red runs only to
# r~7.5 (strong-red edge 6.75; 8..8.5 is a faded JPEG halo), and its shading is
# a top-lit gradient, not concentric: center (232,0,0), top rims bright
# (UL r6.5 (190,0,12)), bottom rims dark (LL (163,0,11), LR (167,18,38)).
# Three stacked discs (z base < mid < core) reproduce all measured tones:
#   center -> #E80000 (measured core EXACT), top rim r6.5 -> mid disc, bottom
#   rim r6.5 -> base disc (163,0,11 = measured LL EXACT), strong-red edge ~6.7.
# Offsets are in data px; y grows downward, so negative dy = visually UP.
QUERY_GLOSSY = {
    "base": {"c": "#A3000B", "d": 15.0},
    "mid":  {"c": "#C40004", "d": 12.6, "off": (-0.2, -0.55)},
    "core": {"c": "#E80000", "d": 10.0, "off": (-0.1, -0.3)},
}


def shift(points, dx):
    return [(x + dx, y) for (x, y) in points]


def draw_axes(ax, vx, vy_base, hy, hx_end, h_arrow, z=4, lw=None):
    """Dark-red L axes with small filled arrowheads (all sizes in px = pt).

    z=4 puts the axes ABOVE the big-red dot: the original's v-axis crosses
    OVER the big red's left rim (seam probe: maroon (152,80,91)/(192,40,55) on
    top of red at x102..104, red visible only from x105; white left of x101 —
    qa/slide43/graphgen forensics, 2026-10-10). No other dot touches the axes.

    lw=None -> the 043-calibrated AX_LW; slide 044's own frame measures a
    thinner core (2 px + 1 px wash; v4b transects + arrow grids, 2026-10-10)
    and passes lw=2.5 explicitly.
    """
    _lw = AX_LW if lw is None else lw
    ax.plot([vx, vx], [188.0, vy_base], color=AXES, lw=_lw, solid_capstyle="butt", zorder=z)
    ax.add_patch(Polygon([(vx, 181.0), (vx - 3.8, 188.5), (vx + 3.8, 188.5)],
                         closed=True, facecolor=ARROW, edgecolor=ARROW, zorder=z))
    ax.plot([vx, hx_end], [hy, hy], color=AXES, lw=_lw, solid_capstyle="butt", zorder=z)
    tx, bx, hh = h_arrow
    ax.add_patch(Polygon([(tx, hy), (bx, hy - hh), (bx, hy + hh)],
                         closed=True, facecolor=ARROW, edgecolor=ARROW, zorder=z))


def dots(ax, pts, d, color, z=3, d_core=None, core=None, rim=None):
    """Dots as shaded 3D balls: darker rim circle with a bright core circle on
    top (two flat "o" markers). Pass d_core/core/rim to shade; omit for flat."""
    if not pts:
        return
    xs, ys = zip(*pts)
    if d_core:
        ax.plot(xs, ys, "o", markersize=d, markerfacecolor=rim or color,
                markeredgecolor=rim or color, linestyle="none", zorder=z)
        ax.plot(xs, ys, "o", markersize=d_core, markerfacecolor=core or color,
                markeredgecolor=core or color, linestyle="none", zorder=z + 0.05)
    else:
        ax.plot(xs, ys, "o", markersize=d, markerfacecolor=color,
                markeredgecolor=color, linestyle="none", zorder=z)


def shaded(ax, kind, pts, z=3):
    """Draw a whole cluster from the measured INK palette."""
    s = INK[kind]
    dots(ax, pts, s["d"], s["core"], z=z, d_core=s["d_core"], core=s["core"], rim=s["rim"])


def glossy_query(ax, pt, z=5):
    """043 query dot as a top-lit glossy ball (QUERY_GLOSSY discs, base->core).

    Replaces the concentric two-tone disc after the c5 x3-closeup judge read
    the original as a smaller, dimensionally-shaded marker ("brighter red
    highlight toward the upper-left/center, darker maroon rim / lower-right
    shadow") — see probe_qmark_v1 + QUERY_GLOSSY above for every measured tone.
    """
    x, y = pt
    for i, key in enumerate(("base", "mid", "core")):
        g = QUERY_GLOSSY[key]
        ox, oy = g.get("off", (0.0, 0.0))
        # markeredgewidth=0: the default marker edge stroke (lw 1.5, half
        # outside the path) inflates each disc's solid radius by ~0.4-0.6 px —
        # the round-2 transects measured base solid to 7.9 (nominal 7.5) and
        # that same inflation is what made the v3 d16 dot read "visibly
        # larger" (effective ~8.7 vs the original's solid 7.5). Banked cluster
        # dots keep the default edge (their INK d values were calibrated
        # through the same pipeline); the glossy discs are sized from absolute
        # original radii and must render exact.
        ax.plot([x + ox], [y + oy], "o", markersize=g["d"],
                markerfacecolor=g["c"], markeredgecolor=g["c"],
                markeredgewidth=0, linestyle="none", zorder=z + i * 0.05)


def render(nnn, out, region=None):
    spec = SLIDE_SPEC[nnn]
    x0, y0, x1, y1 = region if region else REGIONS[nnn]
    w_in, h_in = (x1 - x0) / 72.0, (y1 - y0) / 72.0
    fig = plt.figure(figsize=(w_in, h_in), dpi=DPI)
    fig.patch.set_facecolor("white")
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(x0, x1)
    ax.set_ylim(y1, y0)          # inverted: y grows downward (screen px)
    ax.axis("off")

    # left panel (both slides). Z-order measured on the originals: clusters at
    # the bottom; the 043 big red ON TOP of the greens (seam (126,344) is red
    # over green rim) but UNDER the axes (z 3.5 < 4); query/'?' on top.
    if nnn == "044":
        # 044 frame: axis core 2 px + 1 px wash (arrow grids + v4b transects,
        # qa/slide44/graphgen 2026-10-10) -> lw 2.5, not the 043-calibrated
        # AX_LW 3.5; left h-arrow measured tip 444 / base 432 / hh 4.0.
        draw_axes(ax, 103.5, 476.5, 476.5, 434.0, (444.0, 432.0, 4.0), lw=2.5)
    else:
        draw_axes(ax, 103.5, 476.5, 476.5, 434.0, (441.0, 431.5, 3.9))
    shaded(ax, "green", GREEN, z=3)
    shaded(ax, "cyan", CYAN, z=3)
    shaded(ax, "tan", TAN, z=3)
    if spec["big_red"]:
        shaded(ax, "big", [BIG_RED_043], z=3.5)
    if spec.get("glossy_query"):
        glossy_query(ax, QUERY, z=5)
    else:
        shaded(ax, "query", [QUERY], z=5)
    # '?' right of the query — per-slide size/anchor (043 round-2 re-measure:
    # ~16pt dark-maroon glyph, ink inside the original's blurred 329..338 x
    # 347..360 extent; 044 keeps the banked 20pt calibration).
    qx, qy = spec.get("qmark_anchor", (QMARK["x"], QMARK["y"]))
    ax.text(qx, qy, "?", fontsize=spec.get("qmark_pt", QMARK["fontsize"]),
            fontweight="bold", fontfamily=QMARK["font"], color=spec["qmark"],
            ha="center", va="center", zorder=6)

    if nnn == "044":
        # right panel axes (044 frame: thinner core, see left-panel note)
        draw_axes(ax, 500.0, 475.5, 475.5, 827.0, (837.0, 826.5, 3.7), lw=2.5)
        # right panel points (measured per-cluster offsets)
        rg, rc, rt = (shift(GREEN, OFF_R["green"]), shift(CYAN, OFF_R["cyan"]),
                      shift(TAN, OFF_R["tan"]))
        rq = (QUERY[0] + OFF_R["query"], QUERY[1])
        all_pts = rg + rc + rt
        # connector web: thin pale-pink lines from query to all 26 dots (under the dots)
        for (px_, py_) in all_pts:
            ax.plot([rq[0], px_], [rq[1], py_], color=PINK, lw=1.2,
                    solid_capstyle="butt", zorder=1)
        # small dark-red arrowheads at every connector/dot junction (044 original
        # only; measured: compact 2-3px dark-red clusters, tip at the dot's ink
        # edge, base ~3 px out along the line, half-width 1.5 — forensics 2026-10-10)
        radii = ([INK["green"]["d"] / 2] * len(rg) + [INK["cyan"]["d"] / 2] * len(rc)
                 + [INK["tan"]["d"] / 2] * len(rt))
        for (tp, rad) in zip(all_pts, radii):
            ux, uy = tp[0] - rq[0], tp[1] - rq[1]
            L = math.hypot(ux, uy)
            ux, uy = ux / L, uy / L
            tipx, tipy = tp[0] - ux * rad, tp[1] - uy * rad
            basex, basey = tipx - ux * 3.0, tipy - uy * 3.0
            ax.add_patch(Polygon([(tipx, tipy),
                                  (basex - uy * 1.5, basey + ux * 1.5),
                                  (basex + uy * 1.5, basey - ux * 1.5)],
                                 closed=True, facecolor=WEB_TIP, edgecolor=WEB_TIP,
                                 zorder=2))
        # NN computation (same algorithm as the lecture topic, on the measured data)
        nn = NearestNeighbors(n_neighbors=1).fit(np.array(all_pts))
        dist, idx = nn.kneighbors(np.array([rq]))
        nn_pt = all_pts[int(idx[0][0])]
        assert nn_pt in rt, f"computed NN {nn_pt} is not the expected tan point"
        # draw tan cluster with the NN replaced by the yellow highlight
        shaded(ax, "tan", [p for p in rt if p != nn_pt], z=3)
        dots(ax, [nn_pt], D_NN, YELLOW, z=4)
        # dashed NN ring — 044 re-measure (720-sample circle walk, 2026-10-10):
        # ink band r 11.6..13.4 around the NN dot -> radius 12.5, lw 1.8;
        # ~14 dashes of ~1.5-2 px with ~3.5-4 px gaps. NB: matplotlib SCALES a
        # patch's (0,(on,off)) dash spec by the line width, so the spec below is
        # the target divided by lw 1.8 (effective on/off = 2.0/3.5 pt).
        ax.add_patch(Circle(nn_pt, 12.5, fill=False, edgecolor=AXES, lw=1.8,
                            linestyle=(0, (2 / 1.8, 3.5 / 1.8)), zorder=4))
        shaded(ax, "green", rg, z=3)
        shaded(ax, "cyan", rc, z=3)
        shaded(ax, "query", [rq], z=5)
        print(f"[{nnn}] computed NN of query {rq}: {nn_pt} dist={float(dist[0][0]):.1f}px")

    fig.savefig(out, dpi=DPI, facecolor="white")
    plt.close(fig)
    print(f"[{nnn}] wrote {out} region=({x0},{y0})-({x1},{y1}) "
          f"addImage x={x0/72:.4f} y={y0/72:.4f} w={w_in:.4f} h={h_in:.4f} in")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("slide", choices=["043", "044"])
    ap.add_argument("out")
    ap.add_argument("--region", default=None,
                    help="canvas override x0,y0,x1,y1 in slide px (ink coords unchanged)")
    a = ap.parse_args()
    region = None
    if a.region:
        region = tuple(int(v) for v in a.region.split(","))
        assert len(region) == 4
    render(a.slide, a.out, region=region)
