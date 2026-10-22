#!/usr/bin/env python3
"""graphgen for slide 007 middle panel: 3D fitted-plane scatter with residual stems
(matplotlib mplot3d, ortho, calibrated to the measured axis endpoints).

v2 (crop-compare feedback): drop-line stems from each point to the plane, warm cream
panel + beige plane, steel-blue dots with opacity variance, red italic axis labels
(Weight rotated / Length right / Radius lower-left), z-axis arrowhead.
The red ?-badge, 2 red dots and the projection line are NATIVE pptx overlays.

Usage: graphgen/.venv/bin/python graphgen/slide_007_plane.py <out.png>
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import proj3d

W_F, H_F = 241 / 72, 203 / 72
DPI = 300
S = DPI / 72.0

O = np.array([78, 108]); XE = np.array([8, 190]); YE = np.array([234, 128]); ZE = np.array([78, 6])
def disp(p):
    return np.array([p[0] * S, (203 - p[1]) * S])
T_O, T_X, T_Y, T_Z = disp(O), disp(XE), disp(YE), disp(ZE)

ELEV, AZIM = 22.8, 18.3
ASPECT = (1.355, 1.0, 0.6986)
PANEL = "#FBF8EE"      # warm cream panel (measured warm tint)

PTS_ABS = [(471,174),(460,180),(502,186),(471,187),(492,188),(447,188),(437,199),
           (486,199),(499,199),(441,207),(419,214),(477,213),(431,220),(450,224),
           (463,221),(416,235),(399,236),(416,245),(399,247)]

def build_axes(rect):
    fig = plt.figure(figsize=(W_F, H_F), dpi=DPI, facecolor=PANEL)
    ax = fig.add_axes(rect, projection="3d")
    ax.set_facecolor(PANEL)
    ax.set_proj_type("ortho")
    ax.view_init(elev=ELEV, azim=AZIM)
    ax.set_box_aspect(ASPECT)
    ax.set_xlim(0, 10); ax.set_ylim(0, 10); ax.set_zlim(0, 10)
    for pane in (ax.xaxis.pane, ax.yaxis.pane, ax.zaxis.pane):
        pane.set_visible(False)
    ax.grid(False)
    ax.set_xticks([]); ax.set_yticks([]); ax.set_zticks([])
    return fig, ax

def endpoint_pix(ax):
    M = ax.get_proj()
    pts = np.array([[0, 0, 0], [10, 0, 0], [0, 10, 0], [0, 0, 10]], float)
    x2, y2, _ = proj3d.proj_transform(pts[:, 0], pts[:, 1], pts[:, 2], M)
    return ax.transData.transform(np.column_stack([x2, y2]))

def calibrate():
    global AZIM
    fig, ax = build_axes([0, 0, 1, 1])
    p0 = endpoint_pix(ax)
    plt.close(fig)
    if not (p0[1, 0] < p0[0, 0] < p0[2, 0]):
        AZIM = -AZIM
    W, H = W_F * DPI, H_F * DPI
    ozx, oyx = p0[0, 0], p0[2, 0]
    w = (T_Y[0] - T_O[0]) / (oyx - ozx)
    l = (T_O[0] - w * ozx) / W
    ozy, oxy = p0[0, 1], p0[1, 1]
    h = (T_X[1] - T_O[1]) / (oxy - ozy)
    b = (T_O[1] - h * ozy) / H
    return [l, b, w, h]

def invert_points(ax):
    M = ax.get_proj()
    def to_disp(R, L, Wt):
        x2, y2, _ = proj3d.proj_transform(np.array([R]), np.array([L]), np.array([Wt]), M)
        return ax.transData.transform(np.column_stack([x2, y2]))[0]
    out = []
    for (ax_, ay_) in PTS_ABS:
        u_t, v_t = (ax_ - 314) * S, (203 - (ay_ - 128)) * S
        best, bl = None, 1e18
        for R in np.linspace(0.2, 9.8, 40):
            for L in np.linspace(0.2, 9.8, 40):
                Wt = 0.35 * R + 0.45 * L + 2.0
                p = to_disp(R, L, Wt)
                d = (p[0] - u_t) ** 2 + (p[1] - v_t) ** 2
                if d < bl:
                    bl, best = d, (R, L, Wt, p)
        R, L, Wt, p = best
        p_up = to_disp(R, L, Wt + 1.0)
        dz = (p_up[1] - p[1])
        z_new = Wt + (v_t - p[1]) / dz if abs(dz) > 1e-9 else Wt
        out.append((R, L, float(np.clip(z_new, -0.5, 9.8))))
    return out

def render(rect, out, pts=None):
    fig, ax = build_axes(rect)
    LO, HI = -1.5, 11.5
    L, R = np.meshgrid(np.linspace(LO, HI, 2), np.linspace(LO, HI, 2))
    Wp = 0.45 * L + 0.35 * R + 2.0
    ax.plot_surface(R, L, Wp, color="#D9DCC5", alpha=0.32, linewidth=0, shade=False)
    for (r0, l0) in [((LO, LO), (HI, LO)), ((LO, LO), (LO, HI)),
                     ((HI, HI), (HI, LO)), ((HI, HI), (LO, HI))]:
        rr = np.linspace(r0[0], r0[1], 2)
        ll = np.linspace(l0[0], l0[1], 2)
        ax.plot(rr, ll, 0.45 * ll + 0.35 * rr + 2.0, color="#B7AB8F", lw=0.9, alpha=0.5)
    if pts is None:
        pts = invert_points(ax)
    pr = np.array([p[0] for p in pts]); pl = np.array([p[1] for p in pts]); pw = np.array([p[2] for p in pts])
    # residual drop-line stems: each dot down to the plane
    for i in range(len(pr)):
        pz = 0.35 * pr[i] + 0.45 * pl[i] + 2.0
        ax.plot([pr[i], pr[i]], [pl[i], pl[i]], [pw[i], pz],
                color="#8FA6BC", lw=0.7, alpha=0.55, zorder=2)
    rng = np.random.default_rng(3)
    alphas = 0.55 + 0.4 * rng.random(len(pr))
    for i in range(len(pr)):
        ax.scatter([pr[i]], [pl[i]], [pw[i]], s=16, c="#7D95AB", depthshade=False,
                   alpha=float(alphas[i]), zorder=3)
    axis_col = "#C9848E"
    for axis in (ax.xaxis, ax.yaxis, ax.zaxis):
        axis.line.set_color(axis_col)
        axis.line.set_linewidth(1.2)
    lk = dict(color=axis_col, linewidth=1.5)
    ax.plot([0, 10], [0, 0], [0, 0], **lk)
    ax.plot([0, 0], [0, 10], [0, 0], **lk)
    ax.plot([0, 0], [0, 0], [0, 10], **lk)
    ax.scatter([0], [0], [10], marker="^", s=28, c=axis_col, depthshade=False, zorder=5)
    # red italic axis labels (measured blob positions)
    fig.text(71 / 241, 1 - 22 / 203, "Weight", rotation=90, color="#B0576B",
             fontsize=5.5, style="italic", ha="center", va="center", family="serif")
    fig.text(223 / 241, 1 - 133 / 203, "Length", color="#B0576B",
             fontsize=5.5, style="italic", ha="center", va="center", family="serif")
    fig.text(10 / 241, 1 - 190 / 203, "Radius", color="#B0576B",
             fontsize=5.5, style="italic", ha="center", va="center", family="serif")
    fig.savefig(out, dpi=DPI, facecolor=PANEL)
    plt.close(fig)
    return pts

if __name__ == "__main__":
    import sys
    out = sys.argv[1] if len(sys.argv) > 1 else "scratch/ml02/slide007/graph/mplot_v3.png"
    rect = calibrate()
    print("azim used:", AZIM, "rect:", [round(v, 4) for v in rect])
    pts = render(rect, out)
    print("wrote", out, f"({len(pts)} points with stems)")
