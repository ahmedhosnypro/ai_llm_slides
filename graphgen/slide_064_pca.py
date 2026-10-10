#!/usr/bin/env python3
"""Slide 064 — PCA 3-D scatter graph generator (pilot graphgen script).

Decision (documented in graphgen/README.md + qa/slide64/graphgen/PILOT_REPORT.md):
  lib      : scikit-learn + matplotlib (mpl_toolkits.mplot3d)
  function : sklearn.decomposition.PCA(n_components=3)
  algorithm: PCA (same AI algorithm as the lecture topic)
  data     : sklearn.datasets.load_iris() — the real 150-sample IRIS data
  plot     : mplot3d scatter, x=Z1 (PC1), y=Z2 (PC2), z=Z3 (PC3)

Measured from the original frame (videos/ml-intro/unique_slides/slide_064.jpg, 960x540;
PIL forensics v1-v6 banked in qa/slide64/graphgen/):
  panel box (red CC0000 thin border): x 231..719 px, y 92..493 px
      -> slide inches (1px = 1pt = 1/72in): x 3.208, y 1.278, w 6.778, h 5.569
  panes white (254,255,253), gridlines light gray ~ (221,221,221) = #DDDDDD
  clusters (screen centroids, normalized to panel): red .27/.42  green .44/.60
                                                     blue .57/.46  (nx, ny-from-top)
  point colors (spec, judge-validated): #FF0000 / #00AA00 / #0000FF
  axis ranges (spec): Z1 -3..4, Z2 -1..1.5, Z3 -0.6..0.8; red italic Z labels
Viewpoint (elev/azim) is tuned by PIL-comparing rendered cluster geometry to the
original's measured targets (view_search below), then baked as ELEV/AZIM.
"""
import argparse
import json
import math

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle
from PIL import Image
from sklearn.datasets import load_iris
from sklearn.decomposition import PCA

# ---- measured constants (see docstring) ----
PANEL_PX = (231, 92, 719, 493)          # x0,y0,x1,y1 in the 960x540 original frame
SLIDE_W_IN, SLIDE_H_IN = 13.333, 7.5
PANEL_IN = (PANEL_PX[0] / 72.0, PANEL_PX[1] / 72.0,
            (PANEL_PX[2] - PANEL_PX[0]) / 72.0, (PANEL_PX[3] - PANEL_PX[1]) / 72.0)
TARGETS = {  # cluster screen targets normalized to the panel box (nx, ny from top)
    "red":   {"c": (0.27, 0.42), "bb": (0.14, 0.24, 0.40, 0.61)},
    "green": {"c": (0.44, 0.60), "bb": (0.31, 0.48, 0.57, 0.73)},
    "blue":  {"c": (0.57, 0.46), "bb": (0.50, 0.27, 0.76, 0.67)},
}
COLORS = {"Setosa": "#FF0000", "Versicolor": "#00AA00", "Virginica": "#0000FF"}
GRID = "#DDDDDD"
BORDER = "#CC0000"
ZLAB = "#CC0000"     # red italic Z labels (measured dark-red ~ (204,0,22))
DPI = 300

ELEV, AZIM = 24, -70   # tuned by view_search + full-render sweeps (see PILOT_REPORT)
AXES_LIFT = 0.07       # mplot3d axes bottom lift, tuned so cluster verticals match the original


def pca_data():
    iris = load_iris()
    Xr = PCA(n_components=3).fit_transform(iris.data)
    return Xr, iris.target


def measure_png(path):
    """Cluster centroids + bboxes from a rendered PNG, normalized to full image."""
    a = np.asarray(Image.open(path).convert("RGB")).astype(int)
    H, W = a.shape[:2]
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    out = {}
    for name, m in [
        ("red",   (r > 230) & (g < 90) & (b < 90)),    # #FF0000 point cores; CC0000 labels/border AA excluded
        ("green", (g > 150) & (r < 90) & (b < 90)),
        ("blue",  (b > 200) & (r < 90) & (g < 90)),
    ]:
        ys, xs = np.nonzero(m)
        if not len(xs):
            out[name] = None
            continue
        out[name] = {"c": (xs.mean() / W, ys.mean() / H),
                     "bb": (xs.min() / W, ys.min() / H, xs.max() / W, ys.max() / H),
                     "n": int(len(xs))}
    return out


def render(out, Xr, y, elev=None, azim=None, pt_s=16, fast=False, figw=None, figh=None, dpi=None):
    dpi = dpi or DPI
    elev = ELEV if elev is None else elev
    azim = AZIM if azim is None else azim
    figw = figw or PANEL_IN[2]
    figh = figh or PANEL_IN[3]
    lift = 0.0 if fast else AXES_LIFT
    fig = plt.figure(figsize=(figw, figh), dpi=dpi)
    if not fast:
        fig.patch.set_facecolor("white")
    ax = fig.add_axes([0.0, lift, 1.0, 1.0 - lift], projection="3d")
    ax.view_init(elev=elev, azim=azim)
    ax.set_xlim(-3, 4)
    ax.set_ylim(-1, 1.5)
    ax.set_zlim(-0.6, 0.8)
    for name, tgt in [(0, "Setosa"), (1, "Versicolor"), (2, "Virginica")]:
        pts = Xr[y == name]
        ax.scatter(pts[:, 0], pts[:, 1], pts[:, 2], s=pt_s, c=COLORS[tgt],
                  edgecolors=COLORS[tgt], linewidths=0.4, depthshade=False)
    # white panes, light-gray grid
    for axis in (ax.xaxis, ax.yaxis, ax.zaxis):
        axis.set_pane_color((1.0, 1.0, 1.0, 1.0))
        axis._axinfo["grid"].update(color=GRID, linewidth=0.9)
    if fast:
        ax.set_axis_off()
        ax.grid(True)
    else:
        ax.set_xticks([-3, -2, -1, 0, 1, 2, 3, 4])
        ax.set_yticks([-1.0, -0.5, 0.0, 0.5, 1.0, 1.5])
        ax.set_zticks([-0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8])
        for t in (ax.get_xticklabels() + ax.get_yticklabels() + ax.get_zticklabels()):
            t.set_color("#444444"); t.set_fontsize(8.5)
        ax.set_xlabel(r"$Z_1$", color=ZLAB, fontsize=13, style="italic", labelpad=12)
        ax.set_ylabel(r"$Z_2$", color=ZLAB, fontsize=13, style="italic", labelpad=12)
        ax.set_zlabel(r"$Z_3$", color=ZLAB, fontsize=13, style="italic", labelpad=8)
        # red panel border baked into the image (measured CC00000 thin rectangle)
        fig.add_artist(Rectangle((0.004, 0.004), 0.992, 0.992, fill=False,
                                  edgecolor=BORDER, linewidth=1.6,
                                  transform=fig.transFigure, zorder=10))
    fig.savefig(out, dpi=dpi, facecolor="white")
    plt.close(fig)


def score(meas):
    """Lower = better match of measured clusters vs original targets."""
    s = 0.0
    for name, tgt in TARGETS.items():
        m = meas.get(name)
        if m is None:
            return 1e9
        cx, cy = m["c"]; txc, tyc = tgt["c"]
        s += 2.2 * math.hypot(cx - txc, cy - tyc)
        bb = m["bb"]; tbb = tgt["bb"]
        s += 0.8 * (abs(bb[0] - tbb[0]) + abs(bb[1] - tbb[1]) +
                    abs(bb[2] - tbb[2]) + abs(bb[3] - tbb[3]))
    return s


def view_search(Xr, y, outdir):
    import os, tempfile
    best = None
    results = []
    for elev in range(5, 51, 5):
        for azim in range(-180, 181, 10):
            p = os.path.join(outdir, f"vs_{elev}_{azim}.png")
            render(p, Xr, y, elev, azim, fast=True, figw=3.4, figh=2.8, dpi=50)
            # fast render uses default dpi -> set DPI low for speed
            s = score(measure_png(p))
            results.append((s, elev, azim))
            if best is None or s < best[0]:
                best = (s, elev, azim)
    results.sort()
    print(json.dumps(results[:12], indent=0))
    return best


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument("--elev", type=float, default=ELEV)
    ap.add_argument("--azim", type=float, default=AZIM)
    ap.add_argument("--s", type=float, default=16)
    ap.add_argument("--search", action="store_true")
    ap.add_argument("--outdir", default=".")
    args = ap.parse_args()
    Xr, y = pca_data()
    if args.search:
        s, e, a = view_search(Xr, y, args.outdir)
        print("BEST", s, e, a)
    render(args.out, Xr, y, args.elev, args.azim, pt_s=args.s)
    m = measure_png(args.out)
    print(json.dumps({"file": args.out, "measured": m, "score": round(score(m), 4)}, indent=1))
