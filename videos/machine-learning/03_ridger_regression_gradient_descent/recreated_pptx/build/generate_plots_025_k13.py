#!/usr/bin/env python3
"""Generate the four loss-function-shape plots for slide 025 (k13).
# k13: att13 adjudication fixes —
#   BR rebuilt: mountainous landscape (MATLAB-peaks-style surface, the canonical
#   non-convex loss terrain) with a real gradient-descent path + arrowhead down
#   to a minima, AXES-FREE (att13: original has no axes/ticks; recreation must
#   not add them), jet cmap, light wireframe, surface filling the measured frame.
#   Orientation/coverage tuned by PIL correlation against the original frame's
#   jet height map (see qa/slide_025/graphgen/br_view_search.py).
#   BL: x/y tick labels no longer clipped at the redrect border (att13 MAJOR):
#   axes rect lifted [0.05,0.09,0.90,0.88] + zoom 1.00 (was [0.05,0.04,0.90,0.92]
#   zoom 1.06 — tick ink crossed the frame line at y523.5).
#   TL/TR: unchanged from k12.
# k12: crop_12 leg fixes — TR tick size 5.4 + zoom 1.08 + floor-contour alpha .85/lw .6,
# BL X/Y axis labels + tick pad 0.5, BR descent path lw 1.5 + tick pad 0.5.
# k11: crop_11_TR leg fixes — invert x-axis (tick order), sharper/taller spike,
# dotted gridlines, floor contour projection, thinner redrect. (k8: zoom<=1.10 so every 3-D tick label stays inside the figure (k7 clipped them),
# TL super-gaussian dome (flat crown, steep flanks) with jet norm stretched so the
# crown reads olive/green (no red cap), heavier floor contours, coarser mesh.

Regions measured from unique_slides/slide_025.jpg (960x540, 1px = 1/72in):
  TL x85..265 y115..288 | TR x616..879 y115..317
  BL x83..376  y290..527 | BR x615..880 y344..531
Each PNG is 300dpi at figsize = box_px/72 and is placed at box_px/72 inches.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import os
from matplotlib.lines import Line2D
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import proj3d

OUT = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/build/assets"
os.makedirs(OUT, exist_ok=True)

DPI = 300
JET = plt.get_cmap("jet")
RED = (0.75, 0.0, 0.0)
BLK = "black"
TICKC = "#333333"

PLOTS = {
    "tl": dict(x0=85,  y0=115, w=180, h=173, elev=32, azim=60),
    "tr": dict(x0=616, y0=115, w=263, h=202, elev=30, azim=60),
    "bl": dict(x0=83,  y0=290, w=293, h=237, elev=28, azim=-62),
    "br": dict(x0=615, y0=344, w=265, h=187, elev=26, azim=-62),
}


def figure(spec, rect=(0.05, 0.04, 0.90, 0.92)):
    fig = plt.figure(figsize=(spec["w"] / 72.0, spec["h"] / 72.0), dpi=DPI)
    ax = fig.add_axes(list(rect), projection="3d")
    ax.view_init(elev=spec["elev"], azim=spec["azim"])
    return fig, ax


def axis_style(ax, tsize=6.0, pad=-1):
    for axis in (ax.xaxis, ax.yaxis, ax.zaxis):
        axis.set_pane_color((1, 1, 1, 0.0))
        axis._axinfo["grid"].update(color="#E4E4E4", linewidth=0.3, linestyle=":")
        axis.line.set_linewidth(0.4)
        axis.set_tick_params(pad=pad, labelsize=tsize, length=1.5, width=0.4)
    for t in ax.get_xticklabels() + ax.get_yticklabels() + ax.get_zticklabels():
        t.set_fontsize(tsize)
        t.set_color(TICKC)


def mesh(ax, X, Y, Z, **kw):
    ax.plot_surface(X, Y, Z, cmap=JET, shade=False, antialiased=True,
                    rstride=4, cstride=4, linewidth=0.28,
                    edgecolor=(0.05, 0.05, 0.05, 0.55), **kw)


def proj_xy(ax, x, y, z):
    """3-D data point -> figure-fraction (fx, fy)."""
    x2, y2, _ = proj3d.proj_transform(x, y, z, ax.get_proj())
    disp = ax.transData.transform([(x2, y2)])[0]
    return (disp[0] / fig_w(ax), 1.0 - disp[1] / fig_h(ax))


def fig_w(ax):
    return ax.figure.get_size_inches()[0] * DPI


def fig_h(ax):
    return ax.figure.get_size_inches()[1] * DPI


def redrect(fig, spec, inset=3):
    x0 = inset / spec["w"]
    x1 = 1.0 - inset / spec["w"]
    y0 = 1.0 - inset / spec["h"]
    y1 = inset / spec["h"]
    for (a0, b0, a1, b1) in ((x0, y0, x0, y1), (x1, y0, x1, y1),
                             (x0, y0, x1, y0), (x0, y1, x1, y1)):
        fig.add_artist(Line2D([a0, a1], [b0, b1], transform=fig.transFigure,
                              color=RED, lw=0.7, zorder=40, solid_capstyle="butt"))


def save(fig, name):
    fig.savefig(os.path.join(OUT, "plot_025_%s.png" % name), dpi=DPI,
                facecolor="white")
    plt.close(fig)
    print("wrote plot_025_%s.png" % name)


# ── TL: concave dome (one maximum), ticks 2/0/-2 both base axes, 0/-5 z-axis,
#      contour rings projected on the floor ────────────────────────────────────
def plot_tl():
    spec = PLOTS["tl"]
    fig, ax = figure(spec)
    x = np.linspace(-2, 2, 80)
    X, Y = np.meshgrid(x, x)
    R = np.sqrt(X ** 2 + Y ** 2)
    Z = 7.0 * np.exp(-((X ** 2 + Y ** 2) / 1.15) ** 2) - 4.6 \
        - 0.9 * np.exp(-((R - 1.5) / 0.30) ** 2)
    Z = np.clip(Z, -5.0, None)
    Zn = (Z - Z.min()) / max(Z.max() - Z.min(), 1e-9)
    ax.plot_surface(X, Y, Z, facecolors=JET(0.60 * Zn), shade=False,
                    antialiased=True, rstride=3, cstride=3, linewidth=0.40,
                    edgecolor=(0.05, 0.05, 0.05, 0.75))
    ax.contour(X, Y, Z, levels=12, zdir="z", offset=-5.0,
               colors=[JET(0.60 * t) for t in np.linspace(0, 1, 12)],
               linewidths=0.8)
    ax.set_xlim(-2, 2); ax.set_ylim(-2, 2); ax.set_zlim(-5, 2)
    ax.set_xticks([2, 0, -2]); ax.set_yticks([2, 0, -2])
    ax.set_zticks([0, -5])
    axis_style(ax)
    ax.set_box_aspect((1, 1, 0.85), zoom=1.08)
    redrect(fig, spec)
    save(fig, "tl")


# ── TR: convex bowl (one minimum), x/y ticks 100..-100 step 50, z 0..2 x10^4,
#      multiplier text outside the box top-left ────────────────────────────────
def plot_tr():
    spec = PLOTS["tr"]
    fig, ax = figure(spec)
    x = np.linspace(-100, 100, 90)
    X, Y = np.meshgrid(x, x)
    R2 = X ** 2 + Y ** 2
    Z = 0.8 * R2 / 10000.0 + 1.98 * np.exp(-(R2) / (20.0 ** 2))
    mesh(ax, X, Y, Z)
    ax.set_xlim(-100, 100); ax.set_ylim(-100, 100); ax.set_zlim(0, 2)
    ax.invert_xaxis()   # orig left-edge tick order 100..-100 top->bottom
    ax.contour(X, Y, Z, levels=10, zdir="z", offset=0.0,
               colors="#8A8A8A", linewidths=0.6, alpha=0.85)
    ax.set_xticks([100, 50, 0, -50, -100])
    ax.set_yticks([100, 50, 0, -50, -100])
    ax.set_zticks([2, 1.5, 1, 0.5, 0])
    ax.set_zticklabels(["2", "1.5", "1", "0.5", "0"])
    axis_style(ax, tsize=5.4)
    ax.set_box_aspect((1, 1, 0.62), zoom=1.08)
    ax.text2D(0.02, 0.97, r"$\times 10^{4}$", transform=ax.transAxes,
              fontsize=6.0, color=TICKC, va="top", zorder=50)
    redrect(fig, spec)
    save(fig, "tr")


# ── BL: non-convex two-peak/two-valley surface, x/y ticks -3..3 step 1,
#      z -6..8 step 2, red X markers at the extrema, labels at the measured
#      slide-px positions (Global Maxima top-center, Local Maxima mid-right,
#      Local Minima lower-right, Global Minima lower-left) ─────────────────────
def plot_bl():
    spec = PLOTS["bl"]
    fig, ax = figure(spec, rect=(0.05, 0.09, 0.90, 0.88))
    x = np.linspace(-3, 3, 100)
    X, Y = np.meshgrid(x, x)
    Z = (4.6 * np.exp(-((X - 0.2) ** 2 + (Y - 0.4) ** 2) * 0.9)
         + 3.4 * np.exp(-((X + 1.9) ** 2 + (Y - 1.7) ** 2) * 1.5)
         - 4.8 * np.exp(-((X + 0.7) ** 2 + (Y + 1.6) ** 2) * 1.1)
         - 3.6 * np.exp(-((X - 1.8) ** 2 + (Y + 1.3) ** 2) * 1.4))
    mesh(ax, X, Y, Z)
    ax.set_xlim(-3, 3); ax.set_ylim(-3, 3); ax.set_zlim(-6, 8)
    ax.set_xticks([-3, -2, -1, 0, 1, 2, 3])
    ax.set_yticks([-3, -2, -1, 0, 1, 2, 3])
    ax.set_zticks([-6, -4, -2, 0, 2, 4, 6, 8])
    axis_style(ax, tsize=5.5, pad=0.5)
    ax.set_xlabel("X", fontsize=5.5, color=TICKC, labelpad=0)
    ax.set_ylabel("Y", fontsize=5.5, color=TICKC, labelpad=0)
    ax.set_box_aspect((1, 1, 0.95), zoom=1.00)

    def extremum(cx, cy, want_max):
        d = (X - cx) ** 2 + (Y - cy) ** 2
        m = d < 0.9 ** 2
        masked = np.where(m, Z, -1e9 if want_max else 1e9)
        i = np.argmax(masked) if want_max else np.argmin(masked)
        return X.flat[i], Y.flat[i], Z.flat[i]

    PEAKS = {
        "GM":  extremum(0.2, 0.4, True),
        "LMx": extremum(-1.9, 1.7, True),
        "LMn": extremum(1.8, -1.3, False),
        "GMn": extremum(-0.7, -1.6, False),
    }
    # label slide-px (measured) -> figure fraction; BL figure origin (83,290)
    BW, BH = spec["w"], spec["h"]
    LABELS = {   # key: (text, slide_x, slide_y, ha)
        "GM":  ("Global Maxima", 254, 307, "center"),
        "LMx": ("Local Maxima",  312, 396, "center"),
        "LMn": ("Local Minima",  313, 458, "center"),
        "GMn": ("Global Minima", 156, 455, "center"),
    }
    for key, (txt, sx, sy, ha) in LABELS.items():
        fxp = (sx - spec["x0"]) / BW
        fyp = 1.0 - (sy - spec["y0"]) / BH
        fig.text(fxp, fyp, txt, fontsize=6.2, color=BLK, ha=ha, va="center",
                 zorder=45)
        px_, py_, pz_ = PEAKS[key]
        ex, ey = proj_xy(ax, px_, py_, pz_)
        # leader from label toward the marker
        lx, ly = fxp, fyp
        fig.add_artist(Line2D([lx, ex], [ly, ey], transform=fig.transFigure,
                              color=BLK, lw=0.6, zorder=42))
        fig.add_artist(Line2D([ex], [ey], transform=fig.transFigure,
                              marker="x", color=RED, markersize=5,
                              markeredgewidth=1.6, zorder=46, linestyle="none"))

    redrect(fig, spec)
    save(fig, "bl")


# ── BR: mountainous non-convex landscape (MATLAB-peaks-style terrain — the
#      canonical gradient-descent playground) with a real GD path + arrowhead
#      down to a minima; AXES-FREE per the original (no box, ticks, gridlines);
#      orientation/coverage PIL-matched to the original frame ──────────────────
def peaks_surface(X, Y):
    return (3.0 * (1.0 - X) ** 2 * np.exp(-X ** 2 - (Y + 1.0) ** 2)
            - 10.0 * (X / 5.0 - X ** 3 - Y ** 5) * np.exp(-X ** 2 - Y ** 2)
            - 1.0 / 3.0 * np.exp(-(X + 1.0) ** 2 - Y ** 2))


def plot_br():
    spec = PLOTS["br"]
    fig, ax = figure(spec, rect=(0.03, 0.03, 0.94, 0.94))
    x = np.linspace(-3, 3, 110)
    X, Y = np.meshgrid(x, x)
    Z = peaks_surface(X, Y)
    ax.plot_surface(X, Y, Z, cmap=JET, shade=False, antialiased=True,
                    rstride=6, cstride=6, linewidth=0.22,
                    edgecolor=(0.05, 0.05, 0.05, 0.35))
    ax.set_xlim(-3, 3); ax.set_ylim(-3, 3)
    zlo, zhi = -6.5, 8.5
    ax.set_zlim(zlo, zhi)
    ax.set_box_aspect((1, 1, 0.78), zoom=1.24)
    ax.view_init(elev=26, azim=-62)   # PIL-matched: peaks upper-middle band,
    ax.set_axis_off()                 # valleys front-bottom; axes-free

    # real gradient descent from the global-max peak down to a minima
    def Zf(px, py):
        return peaks_surface(px, py)

    def grad(px, py):
        e = 1e-4
        return ((Zf(px + e, py) - Zf(px - e, py)) / (2 * e),
                (Zf(px, py + e) - Zf(px, py - e)) / (2 * e))

    # start on the tallest summit, near the frame's top-center in this view
    ix, iy = np.unravel_index(np.argmax(Z), Z.shape)
    px_, py_ = X[ix, iy] * 0.92, Y[ix, iy] * 0.92
    lr = 0.30
    path = []
    for _ in range(140):
        path.append((px_, py_))
        gx, gy = grad(px_, py_)
        px_ -= lr * gx
        py_ -= lr * gy
    path = np.array(path)
    pz = np.array([Zf(a, b) for a, b in path])

    zoff = 0.45
    ax.plot(path[:, 0], path[:, 1], pz + zoff, color="black", lw=2.0,
            zorder=100, solid_capstyle="round")

    # arrowhead at the path end (drawn in figure space from projected points)
    (ex, ey), (ex2, ey2) = proj_xy(ax, path[-1, 0], path[-1, 1], pz[-1] + zoff), \
        proj_xy(ax, path[-6, 0], path[-6, 1], pz[-6] + zoff)
    ar = FancyArrowPatch(posA=(ex2, ey2), posB=(ex, ey),
                         transform=fig.transFigure, arrowstyle="-|>",
                         mutation_scale=9, color="black", lw=0.8, zorder=101)
    fig.add_artist(ar)

    redrect(fig, spec)
    save(fig, "br")


plot_tl()
plot_tr()
plot_bl()
plot_br()
print("all four plots written (k13)")
