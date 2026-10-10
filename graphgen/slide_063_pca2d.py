#!/usr/bin/env python3
"""Slide 063 — PCA 2-D scatter graph generator (advanced-graph worker, graphgen venv).

Plan (triage P-63 + measured facts, re-verified by qa/slide63/graphgen/forensics_v1..v5):
  lib      : scikit-learn + matplotlib
  function : sklearn.decomposition.PCA(n_components=2)
  algorithm: PCA — the same algorithm the lecture slide teaches
  data     : sklearn.datasets.load_iris() — the real 150-sample IRIS data.
  plot     : 2-D scatter, x = Z1 (PC1), y = Z2 (PC2), colored by class.

Verified by PIL forensics on videos/ml-intro/unique_slides/slide_063.jpg (960x540, 1px=1pt):
  The original IS real unscaled-IRIS PCA: mapping x = 488.5 + 56.0*z1, y = 296.5 - 117.0*z2
  (derived from the 8 x-tick labels -3..4 at 56.0 px/unit and the 6 y-tick labels
  1.5..-1.0 at 117.0 px/unit) reproduces every measured cluster bbox/centroid, and the
  real sklearn PCA cluster geometry maps onto the measured screen bboxes to ~1-3 px.
  Graph panel: red #8B0000 frame rect (246,95)-(746,495), white interior (no gridlines);
  boxed gray-pane plot area (spines ~(288,120)-(722,461), no arrowheads);
  gray ticks/labels; tiny dark-red Z1 label at ~(686,483) below the x-axis right end and
  tiny dark-red ROTATED Z2 label at ~(256,153) left of the y-axis.
  Points: Setosa #FF0000, Versicolor #00AA00, Virginica #0000FF (spec hexes;
  measured (209,15,23)/(36,151,32)/(26,19,216) — compression of exactly these),
  marker diameter ~8 px (isolated-blob area ~50 px^2).

Output: 300 dpi PNG at the panel's physical size 500x400 pt = 6.9444 x 5.5556 in
(one figure-pt = one original-px at the embed scale), for addImage at
x=246/72, y=95/72, w=500/72, h=400/72 in.
"""
import json
import math
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle
from PIL import Image
from sklearn.datasets import load_iris
from sklearn.decomposition import PCA

# ---- measured constants (original 960x540 frame, 1px = 1pt) ----
PANEL_PX = (246, 95, 746, 495)          # red plot-panel frame, outer bbox
PANE_PX = (290.5, 121.5, 719.5, 459.5)  # data area inside the gray spines
X0, PX_PER_X = 488.5, 56.0              # x = X0 + PX_PER_X * z1
Y0, PX_PER_Y = 296.5, 117.0             # y = Y0 - PX_PER_Y * z2
XLIM = ((PANE_PX[0] - X0) / PX_PER_X, (PANE_PX[2] - X0) / PX_PER_X)   # (-3.5357, 4.1250)
YLIM = ((Y0 - PANE_PX[3]) / PX_PER_Y, (Y0 - PANE_PX[1]) / PX_PER_Y) # (-1.3932, 1.4957)
Z1_LBL_C = (686, 483)                   # Z1 label center (below x-axis, right end)
Z2_LBL_C = (256, 153)                   # Z2 label center (left of y-axis, rotated 90)
COLORS = {"Setosa": "#FF0000", "Versicolor": "#00AA00", "Virginica": "#0000FF"}
FRAME_RED = "#8B0000"
SPINE_GRAY = "#8A8A8A"
TICK_GRAY = "#444444"
PT_SIZE = 64                            # marker area pt^2 -> 8 pt diameter = 8 original px
DPI = 300
W_IN = (PANEL_PX[2] - PANEL_PX[0]) / 72.0   # 6.9444
H_IN = (PANEL_PX[3] - PANEL_PX[1]) / 72.0   # 5.5556


def pca_data():
    iris = load_iris()
    Z = PCA(n_components=2).fit_transform(iris.data)
    return Z, iris.target


def render(out, Z, y, pt_s=PT_SIZE, z1_fs=10, tick_fs=9, labelpad=(4.0, 4.0)):
    fig = plt.figure(figsize=(W_IN, H_IN), dpi=DPI)
    fig.patch.set_facecolor("white")
    # axes placed exactly at the pane (data area), in figure fractions
    ax = fig.add_axes([
        (PANE_PX[0] - PANEL_PX[0]) / (PANEL_PX[2] - PANEL_PX[0]),
        (PANEL_PX[3] - PANE_PX[3]) / (PANEL_PX[3] - PANEL_PX[1]),
        (PANE_PX[2] - PANE_PX[0]) / (PANEL_PX[2] - PANEL_PX[0]),
        (PANE_PX[3] - PANE_PX[1]) / (PANEL_PX[3] - PANEL_PX[1]),
    ])
    ax.set_xlim(*XLIM)
    ax.set_ylim(*YLIM)
    ax.set_facecolor("white")
    for cls, name in [(0, "Setosa"), (1, "Versicolor"), (2, "Virginica")]:
        pts = Z[y == cls]
        ax.scatter(pts[:, 0], pts[:, 1], s=pt_s, c=COLORS[name],
                   edgecolors=COLORS[name], linewidths=0.3)
    # boxed gray spines (all four; no arrowheads, no grid)
    for sp in ax.spines.values():
        sp.set_color(SPINE_GRAY)
        sp.set_linewidth(1.8)
    ax.set_xticks(list(range(-3, 5)))
    ax.set_yticks([-1.0, -0.5, 0.0, 0.5, 1.0, 1.5])
    ax.tick_params(colors=TICK_GRAY, labelsize=tick_fs, length=3.5, width=1.0,
                   direction="out", pad=labelpad[0])
    for t in ax.get_xticklabels() + ax.get_yticklabels():
        t.set_color(TICK_GRAY)
    # tiny dark-red Z labels at the measured positions (figure coords, center anchor).
    # Z2 orientation: graph-leg vision comparison (graph_check_1.txt, attempt 1 PASS)
    # read the original's Z2 as HORIZONTAL; PIL components were ambiguous (9x13 px
    # smudge) — vision evidence wins -> render Z2 unrotated. Font 9pt ~= measured ink.
    fx = lambda px: (px - PANEL_PX[0]) / (PANEL_PX[2] - PANEL_PX[0])
    fy = lambda py: (PANEL_PX[3] - py) / (PANEL_PX[3] - PANEL_PX[1])
    fig.text(fx(Z1_LBL_C[0]), fy(Z1_LBL_C[1]), r"$Z_1$", color=FRAME_RED,
             fontsize=z1_fs, ha="center", va="center", style="italic")
    fig.text(fx(Z2_LBL_C[0]), fy(Z2_LBL_C[1]), r"$Z_2$", color=FRAME_RED,
             fontsize=z1_fs, ha="center", va="center", style="italic")
    # red panel frame baked into the image (measured #8B0000 rect at the panel bbox)
    fig.add_artist(Rectangle((0.004, 0.004), 0.992, 0.992, fill=False,
                             edgecolor=FRAME_RED, linewidth=2.0,
                             transform=fig.transFigure, zorder=10))
    fig.savefig(out, dpi=DPI, facecolor="white")
    plt.close(fig)


def measure_png(path):
    """Measure the rendered PNG, reporting coordinates in ORIGINAL-frame px
    (downscale to 500x400 = the 960-frame region, then offset by the panel origin)."""
    im = Image.open(path).convert("RGB")
    im = im.resize((PANEL_PX[2] - PANEL_PX[0], PANEL_PX[3] - PANEL_PX[1]), Image.LANCZOS)
    a = np.asarray(im).astype(int)
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    out = {}
    # frame lines (red)
    redish = (r > 90) & (g < 90) & (b < 90)
    cols = np.nonzero(redish.sum(axis=0) > 100)[0]
    rows = np.nonzero(redish.sum(axis=1) > 100)[0]
    out["frame_vcols"] = [int(c) + PANEL_PX[0] for c in cols]
    out["frame_hrows"] = [int(rr) + PANEL_PX[1] for rr in rows]
    # spines (gray)
    grayish = (abs(r - g) < 12) & (abs(g - b) < 12) & (r > 90) & (r < 210)
    scols = np.nonzero(grayish.sum(axis=0) > 150)[0]
    srows = np.nonzero(grayish.sum(axis=1) > 150)[0]
    out["spine_vcols"] = [int(c) + PANEL_PX[0] for c in scols]
    out["spine_hrows"] = [int(rr) + PANEL_PX[1] for rr in srows]
    # clusters
    for name, m in [
        ("red", (r > 200) & (g < 90) & (b < 90)),
        ("green", (g > 110) & (r < 110) & (b < 110)),
        ("blue", (b > 150) & (r < 110) & (g < 110)),
    ]:
        ys, xs = np.nonzero(m)
        if len(xs):
            out[name] = {"n": int(len(xs)),
                        "bbox": [int(xs.min()) + PANEL_PX[0], int(ys.min()) + PANEL_PX[1],
                                 int(xs.max()) + PANEL_PX[0], int(ys.max()) + PANEL_PX[1]],
                        "centroid": [round(float(xs.mean()) + PANEL_PX[0], 1),
                                      round(float(ys.mean()) + PANEL_PX[1], 1)]}
        else:
            out[name] = None
    # tick-label ink rows below the pane (x ticks) and columns left of it (y ticks)
    sub = a  # 500x400, coords offset below
    darkish = (r < 170) & (g < 170) & (b < 170)
    band = darkish[370:400, :]   # below-pane band in image coords (orig y 465..495)
    cols2 = np.nonzero(band.sum(axis=0) > 0)[0]
    out["xtick_ink_cols"] = [int(c) + PANEL_PX[0] for c in cols2]
    band2 = darkish[:, 25:45]   # left-of-pane band in image coords (orig x 271..291)
    rows2 = np.nonzero(band2.sum(axis=1) > 0)[0]
    out["ytick_ink_rows"] = [int(rr) + PANEL_PX[1] for rr in rows2]
    return out


# measured original targets for the closed-loop check (forensics v2..v5)
TARGETS = {
    "frame": (246, 95, 746, 495),
    "spines": (288, 120, 722, 461),
    "xtick_cols": [321.5, 377.5, 433, 488.5, 545.5, 600.5, 657.5, 713.5],
    "ytick_rows": [121, 180, 238, 296.5, 354.5, 413.5],
    "clusters": {
        "red": {"c": (340.5, 271.5), "bb": (306, 136, 370, 410)},
        "green": {"c": (521.8, 321.4), "bb": (438, 216, 575, 444)},
        "blue": {"c": (614.3, 287.1), "bb": (518, 136, 701, 435)},
    },
}


def score(meas):
    """Closed-loop score vs measured original (original-frame px; lower = better)."""
    s = 0.0
    notes = []
    for edge, val, tgt in [("frame_left", meas["frame_vcols"], 246), ("frame_right", meas["frame_vcols"], 746)]:
        if not val:
            return 1e9, ["frame line missing"]
    fl = min(meas["frame_vcols"]); fr = max(meas["frame_vcols"])
    ft = min(meas["frame_hrows"]); fb = max(meas["frame_hrows"])
    for nm, v, t in [("frame_left", fl, 246), ("frame_right", fr, 746),
                     ("frame_top", ft, 95), ("frame_bottom", fb, 495)]:
        d = abs(v - t)
        s += d
        notes.append(f"{nm}: {v} vs {t} (d={d})")
    sl = min(meas["spine_vcols"]); sr = max(meas["spine_vcols"])
    st = min(meas["spine_hrows"]); sb = max(meas["spine_hrows"])
    for nm, v, t in [("spine_left", sl, 289), ("spine_right", sr, 721),
                     ("spine_top", st, 121), ("spine_bottom", sb, 461)]:
        d = abs(v - t)
        s += 0.5 * d
        notes.append(f"{nm}: {v} vs {t} (d={d})")
    for name, tgt in TARGETS["clusters"].items():
        m = meas.get(name)
        if not m:
            return 1e9, [f"cluster {name} missing"]
        cx, cy = m["centroid"]; tcx, tcy = tgt["c"]
        d = math.hypot(cx - tcx, cy - tcy)
        s += d
        notes.append(f"{name} centroid: ({cx},{cy}) vs ({tcx},{tcy}) (d={d:.1f})")
        bb = m["bbox"]; tbb = tgt["bb"]
        db = sum(abs(bb[i] - tbb[i]) for i in range(4)) / 4.0
        s += 0.5 * db
        notes.append(f"{name} bbox: {bb} vs {tbb} (avg d={db:.1f})")
    # tick label bands
    if meas["xtick_ink_cols"]:
        xs = meas["xtick_ink_cols"]
        notes.append(f"xtick ink cols span {min(xs)}..{max(xs)} (target ink 315..716)")
        s += abs(min(xs) - 315) + abs(max(xs) - 716)
    if meas["ytick_ink_rows"]:
        ys = meas["ytick_ink_rows"]
        notes.append(f"ytick ink rows span {min(ys)}..{max(ys)} (target ink 117..418)")
        s += abs(min(ys) - 117) + abs(max(ys) - 418)
    return round(s, 2), notes


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "graph_v1.png"
    pt_s = float(sys.argv[2]) if len(sys.argv) > 2 else PT_SIZE
    Z, y = pca_data()
    render(out, Z, y, pt_s=pt_s)
    m = measure_png(out)
    sc, notes = score(m)
    print(json.dumps({"file": out, "score": sc, "measured": m}, indent=1))
    print("\n".join(notes))
