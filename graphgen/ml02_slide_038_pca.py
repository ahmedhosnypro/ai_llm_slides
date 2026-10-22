#!/usr/bin/env python3
"""ml02 slide 038 — 2-component PCA scatter of iris data (graphgen generator).

Decision (deck: machine-learning/02_linear-regression-classification-MSSE):
  lib      : scikit-learn + matplotlib
  function : sklearn.decomposition.PCA(n_components=2)
  algorithm: PCA (same AI algorithm as the lecture topic)
  data     : sklearn.datasets.load_iris() — the real 150-sample IRIS data
  plot     : 2-D scatter, x=Z1 (PC1), y=Z2 (PC2), 3 species clusters + 2
             semi-transparent covariance-style ellipses (measured geometry)

Measured from the original frame (unique_slides/slide_038.jpg, 960x540, 1px=1pt;
PIL forensics banked in scratch/ml02/slide038/):
  inner red border (baked): x 246..746, y 94..494  (#8B0000, 1pt)
  axes box: x 289..721, y 120..459 (black 1pt spines, all 4 sides)
  data mapping: x_px = 489 + 56*x  (ticks -3..4, pitch 56 px/unit)
                y_px = 296 - 117*y (ticks -1.0..1.5, pitch 117 px/unit)
  clusters (px): orange centroid (341.5,273.9) green (519.6,323.8) blue (607.8,286.9)
  ellipses (px, mask-PCA on fill): BLUE  center (586.1,289.4) a=218.4 b=103.4
                                   screen-angle 137.8deg  (alpha .7 over spine/border)
                                   YELL  center (341.8,271.9) a=163.6 b=41.2
                                   screen-angle 103.1deg  (alpha .7, pokes above box top)
  ellipse fills measured: yellow over white (255,255,126) -> base #FFFF47 @ alpha .70
                          blue   over white (185,207,228) -> base #9BBAD8 @ alpha .70
                          blue over gray (172,196,220) consistent with alpha .70
  Z labels: dark red #8B0000 italic mathtext; Z2 ink (252..267, 146..160),
            Z1 ink (682..695, 476..488); tick labels ~10px digit height (fs ~13)
  image bounds: frame x 245..766 (521px), y 93..495 (402px) — covers the blue
  ellipse overflow past the border (to x 763) + border AA on every side.
"""
import json
import math

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
matplotlib.rcParams["mathtext.fontset"] = "cm"
import numpy as np
from matplotlib.patches import Ellipse, Rectangle
from PIL import Image
from sklearn.datasets import load_iris
from sklearn.decomposition import PCA

# ---- measured constants (frame px, 960x540, 1px = 1pt) ----
IMG_X0, IMG_Y0, IMG_W, IMG_H = 245, 93, 521, 402     # image bounds in frame px
BORDER = (246, 94, 746, 494)                          # inner red border core
AXBOX = (289, 120, 721, 459)                          # axes box (l, t, r, b)
X0_PX, XSCALE = 489.0, 56.0                           # x_px = 489 + 56*x
Y0_PX, YSCALE = 296.0, 117.0                          # y_px = 296 - 117*y
XLIM = ((AXBOX[0] - X0_PX) / XSCALE, (AXBOX[2] - X0_PX) / XSCALE)
YLIM = ((Y0_PX - AXBOX[3]) / YSCALE, (Y0_PX - AXBOX[1]) / YSCALE)
XTICKS = list(range(-3, 5))
YTICKS = [-1.0, -0.5, 0.0, 0.5, 1.0, 1.5]

DOT_COLORS = {0: "#E8720C", 1: "#3D9970", 2: "#2E2EB8"}
ZLAB = "#8B0000"
BORDER_C = "#8B0000"
PANEL_GRAY = (233 / 255.0, 233 / 255.0, 231 / 255.0)  # E9E9E7
TICK_FS = 13
Z_FS = 18
DOT_S = 62.0                    # scatter area pt^2 (closed-loop tuned to JPEG-measured dots)
ELL_ALPHA = 0.70
ELL = {  # measured in px space; converted to data space below
    "yellow": {"c_px": (342.5, 270.0), "a_px": 166.3, "b_px": 41.0, "ang_screen": 103.1,
               "fc": "#FFFF47"},
    "blue":   {"c_px": (586.1, 289.4), "a_px": 218.4, "b_px": 103.4, "ang_screen": 137.8,
               "fc": "#9BBAD8"},
}
# original measured targets for the closed-loop check (frame px)
TARGETS = {
    "centroids": {0: (341.5, 273.9), 1: (519.6, 323.8), 2: (607.8, 286.9)},
    "bboxes": {0: (305, 136, 369, 409), 1: (435, 213, 575, 446), 2: (515, 132, 705, 438)},
    "ell_bboxes": {"yellow": (288, 108, 397, 432), "blue": (410, 124, 763, 454)},
    "z2_ink": (252, 146, 267, 160),
    "z1_ink": (682, 476, 695, 488),
    "dot_run_median": 7.0,
}
DPI = 300


def px_to_data(px, py):
    return (px - X0_PX) / XSCALE, (Y0_PX - py) / YSCALE


def ell_px_to_data(c_px, a_px, b_px, ang_screen_deg):
    """Ellipse param set in screen-px space -> data space (matplotlib Ellipse args)."""
    th = math.radians(ang_screen_deg)
    R = np.array([[math.cos(th), -math.sin(th)], [math.sin(th), math.cos(th)]])
    M_px = R @ np.diag([a_px, b_px])                 # px space, y DOWN
    T = np.array([[1.0 / XSCALE, 0.0], [0.0, -1.0 / YSCALE]])
    M_d = T @ M_px                                   # data space, y UP
    U, S, Vt = np.linalg.svd(M_d)
    ang = math.degrees(math.atan2(U[1, 0], U[0, 0]))
    c_d = px_to_data(*c_px)
    return c_d, S[0], S[1], ang


def pca_scores():
    iris = load_iris()
    Z = PCA(n_components=2).fit_transform(iris.data)
    y = iris.target
    # sign search: PCA sign is arbitrary; choose the flip matching the original
    best, bconf = None, None
    for s1 in (1, -1):
        for s2 in (1, -1):
            Zs = Z * np.array([s1, s2])
            err = 0.0
            for c in (0, 1, 2):
                t = TARGETS["centroids"][c]
                cd = px_to_data(*t)
                m = Zs[y == c].mean(axis=0)
                err += ((m[0] - cd[0]) / 0.5) ** 2 + ((m[1] - cd[1]) / 0.25) ** 2
            if best is None or err < best:
                best, bconf = err, (s1, s2)
    return Z * np.array(bconf), y, bconf


def build_figure(out, Z, y):
    fig = plt.figure(figsize=(IMG_W / 72.0, IMG_H / 72.0), dpi=DPI)
    fig.patch.set_facecolor("white")
    # gray strip right of the border (the slide's panel showing through)
    bx0, by0, bx1, by1 = BORDER[0] - IMG_X0, BORDER[1] - IMG_Y0, BORDER[2] - IMG_X0, BORDER[3] - IMG_Y0
    fig.add_artist(Rectangle((bx1 / IMG_W, 0), 1 - bx1 / IMG_W, 1,
                             transform=fig.transFigure, facecolor=PANEL_GRAY,
                             edgecolor="none", zorder=0))
    # inner red border (under the axes content; ellipse alpha tints it, as measured)
    fig.add_artist(Rectangle((bx0 / IMG_W, 1 - by1 / IMG_H),
                             (bx1 - bx0) / IMG_W, (by1 - by0) / IMG_H,
                             transform=fig.transFigure, fill=False,
                             edgecolor=BORDER_C, linewidth=1.0, zorder=0.4))
    # axes
    l, t, r, b = AXBOX
    ax = fig.add_axes([(l - IMG_X0) / IMG_W, (IMG_H - (b - IMG_Y0)) / IMG_H,
                       (r - l) / IMG_W, (b - t) / IMG_H])
    ax.set_xlim(*XLIM)
    ax.set_ylim(*YLIM)
    ax.set_facecolor("white")
    for c in (0, 1, 2):
        pts = Z[y == c]
        ax.scatter(pts[:, 0], pts[:, 1], s=DOT_S, c=DOT_COLORS[c],
                   linewidths=0, zorder=2)
    for name in ("yellow", "blue"):
        e = ELL[name]
        (cx, cy), a, b, ang = ell_px_to_data(e["c_px"], e["a_px"], e["b_px"], e["ang_screen"])
        p = Ellipse((cx, cy), 2 * a, 2 * b, angle=ang,
                    facecolor=e["fc"], alpha=ELL_ALPHA, edgecolor="none",
                    clip_on=False, zorder=1)
        ax.add_patch(p)
        p.set_clip_on(False)   # add_patch re-attaches the axes clip path — kill it again
    ax.set_xticks(XTICKS)
    ax.set_yticks(YTICKS)
    ax.tick_params(length=3.5, width=1.0, labelsize=TICK_FS, colors="black")
    for spine in ax.spines.values():
        spine.set_linewidth(1.0)
        spine.set_color("black")
    # Z labels (dark red italic mathtext, measured ink centers)
    z2c = px_to_data((TARGETS["z2_ink"][0] + TARGETS["z2_ink"][2]) / 2,
                     (TARGETS["z2_ink"][1] + TARGETS["z2_ink"][3]) / 2)
    z1c = px_to_data((TARGETS["z1_ink"][0] + TARGETS["z1_ink"][2]) / 2,
                     (TARGETS["z1_ink"][1] + TARGETS["z1_ink"][3]) / 2)
    ax.text(z2c[0], z2c[1], r"$Z_2$", color=ZLAB, fontsize=Z_FS,
            ha="center", va="center", clip_on=False, zorder=4)
    ax.text(z1c[0], z1c[1], r"$Z_1$", color=ZLAB, fontsize=Z_FS,
            ha="center", va="center", clip_on=False, zorder=4)
    fig.savefig(out, dpi=DPI, facecolor="white")
    plt.close(fig)


def measure_render(path):
    """Measure the rendered PNG (300dpi) and convert to frame px (1px=1pt)."""
    im = Image.open(path).convert("RGB")
    sc = 72.0 / DPI  # render px -> frame px
    a = np.asarray(im).astype(int)
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    out = {}
    om = (r > 200) & (g > 80) & (g < 175) & (b < 90)
    gm = (g > 110) & (r < 110) & (b < 130)
    bm = (b > 140) & (r < 110) & (g < 110)
    for nm, m in (("orange", om), ("green", gm), ("blue", bm)):
        ys, xs = np.nonzero(m)
        out[nm] = {"centroid": (xs.mean() * sc + IMG_X0, ys.mean() * sc + IMG_Y0),
                   "bbox": (xs.min() * sc + IMG_X0, ys.min() * sc + IMG_Y0,
                            xs.max() * sc + IMG_X0, ys.max() * sc + IMG_Y0)}
    blue_ex = b - (r + g) / 2.0
    lb = blue_ex > 14
    ys, xs = np.nonzero(lb)
    out["ell_blue_bbox"] = (xs.min() * sc + IMG_X0, ys.min() * sc + IMG_Y0,
                            xs.max() * sc + IMG_X0, ys.max() * sc + IMG_Y0)
    yl = (r + g - 2 * b > 120) & (r > 200)
    ys, xs = np.nonzero(yl)
    out["ell_yellow_bbox"] = (xs.min() * sc + IMG_X0, ys.min() * sc + IMG_Y0,
                              xs.max() * sc + IMG_X0, ys.max() * sc + IMG_Y0)
    # Z label ink (dark red text left of box / below box); windows in frame px,
    # slices converted to render px relative to the image origin (IMG_X0, IMG_Y0)
    red = (r > 110) & (g < 95) & (b < 95)
    wins = {"z2_ink": (248, 130, 280, 200), "z1_ink": (640, 462, 740, 492)}
    for nm, (wx0, wy0, wx1, wy1) in wins.items():
        sl = np.s_[int((wy0 - IMG_Y0) / sc):int((wy1 - IMG_Y0) / sc),
                  int((wx0 - IMG_X0) / sc):int((wx1 - IMG_X0) / sc)]
        rr = red[sl]
        ys, xs = np.nonzero(rr)
        if len(xs):
            out[nm] = (xs.min() * sc + wx0, ys.min() * sc + wy0,
                       xs.max() * sc + wx0, ys.max() * sc + wy0)
        else:
            out[nm] = None
    # dot run widths (orange)
    runs = []
    for yy in range(om.shape[0]):
        xs = np.where(om[yy])[0]
        if len(xs):
            d = np.diff(xs)
            for seg in np.split(xs, np.where(d > 1)[0] + 1):
                runs.append(len(seg))
    out["dot_run_median"] = float(np.median(runs)) * sc if runs else None
    return out


def compare(meas):
    rep = {"pass": True, "deltas": []}

    def add(name, got, want, tol):
        d = max(abs(g - w) for g, w in zip(got, want)) if got else 999
        ok = d <= tol
        rep["pass"] &= ok
        rep["deltas"].append(f"{name}: got {tuple(round(v,1) for v in got) if got else None} "
                             f"want {tuple(round(v,1) for v in want)} maxdelta {d:.1f}px tol {tol} {'OK' if ok else 'FAIL'}")

    for i, nm in ((0, "orange"), (1, "green"), (2, "blue")):
        add(f"centroid {nm}", meas[nm]["centroid"], TARGETS["centroids"][i], 6.0)
        add(f"bbox {nm}", meas[nm]["bbox"], TARGETS["bboxes"][i], 12.0)
    add("ellipse yellow bbox", meas["ell_yellow_bbox"], TARGETS["ell_bboxes"]["yellow"], 10.0)
    add("ellipse blue bbox", meas["ell_blue_bbox"], TARGETS["ell_bboxes"]["blue"], 10.0)
    if meas.get("z2_ink"):
        add("Z2 ink", meas["z2_ink"], TARGETS["z2_ink"], 4.0)
    else:
        rep["pass"] = False
        rep["deltas"].append("Z2 ink: MISSING")
    if meas.get("z1_ink"):
        add("Z1 ink", meas["z1_ink"], TARGETS["z1_ink"], 4.0)
    else:
        rep["pass"] = False
        rep["deltas"].append("Z1 ink: MISSING")
    dr = meas.get("dot_run_median")
    if dr is not None:
        ok = abs(dr - TARGETS["dot_run_median"]) <= 1.0
        rep["pass"] &= ok
        rep["deltas"].append(f"dot run median: got {dr:.2f} want {TARGETS['dot_run_median']} "
                             f"{'OK' if ok else 'FAIL'}")
    else:
        rep["pass"] = False
        rep["deltas"].append("dot runs: MISSING")
    rep["pass"] = bool(rep["pass"])
    return rep


if __name__ == "__main__":
    import argparse
    import os
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--dot-s", type=float, default=DOT_S)
    ap.add_argument("--tick-fs", type=float, default=TICK_FS)
    ap.add_argument("--z-fs", type=float, default=Z_FS)
    args = ap.parse_args()
    DOT_S, TICK_FS, Z_FS = args.dot_s, args.tick_fs, args.z_fs
    Z, y, signs = pca_scores()
    print(f"PCA sign flip chosen: {signs}")
    for c, nm in ((0, "setosa"), (1, "versicolor"), (2, "virginica")):
        m = Z[y == c].mean(axis=0)
        cd = px_to_data(*TARGETS["centroids"][c])
        print(f"  {nm}: model centroid ({m[0]:.2f},{m[1]:.2f}) target ({cd[0]:.2f},{cd[1]:.2f})")
    build_figure(args.out, Z, y)
    print("wrote", args.out)
    if args.check:
        meas = measure_render(args.out)
        rep = compare(meas)
        print(json.dumps(rep, indent=1))
