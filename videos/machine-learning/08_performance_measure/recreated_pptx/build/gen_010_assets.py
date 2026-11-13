"""Slide 010 assets — fraction runs (mathtext glyphs, colored), green underbrace,
top-view sketch planes. All 600dpi transparent PNGs, placed at exact w_in."""
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, Ellipse, Polygon
from matplotlib.path import Path
from matplotlib.patches import PathPatch
from PIL import Image

OUT = "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure/recreated_pptx/build/assets"
os.makedirs(OUT, exist_ok=True)
DPI = 600
GRAY = "#6E6E6E"
GREEN = "#00B050"
RED = "#C00000"
BLACK = "#000000"


def render_run(latex, fontsize, color):
    """Render one mathtext run to a tight RGBA array."""
    fig = plt.figure(figsize=(4, 2), dpi=DPI)
    fig.patch.set_alpha(0.0)
    fig.text(0.5, 0.5, f"${latex}$", fontsize=fontsize, color=color, ha="center", va="baseline")
    fig.canvas.draw()
    buf = np.asarray(fig.canvas.buffer_rgba()).copy()
    ink = buf[:, :, 3] > 8
    ys, xs = np.where(ink)
    plt.close(fig)
    return buf[ys.min():ys.max() + 1, xs.min():xs.max() + 1]


def compose_runs(runs, fontsize, out, gap_px=6):
    """runs: list of (latex, color). Paste left-to-right into one transparent PNG."""
    parts = [render_run(t, fontsize, c) for t, c in runs]
    h = max(p.shape[0] for p in parts)
    # align baselines: mathtext va=baseline puts baseline at bottom-ish; align by bottom row
    w = sum(p.shape[1] for p in parts) + gap_px * (len(parts) - 1)
    canvas = np.zeros((h, w, 4), dtype=np.uint8)
    x = 0
    for p in parts:
        y0 = h - p.shape[0]
        canvas[y0:y0 + p.shape[0], x:x + p.shape[1]] = p
        x += p.shape[1] + gap_px
    Image.fromarray(canvas).save(out)
    return {"path": out, "w_px": int(w), "h_px": int(h),
            "w_in": round(w / DPI, 5), "h_in": round(h / DPI, 5),
            "dpi": DPI, "fontsize_pt": fontsize}


def compose_fraction(num, den, out):
    """Stack the colored mathtext runs around a horizontal fraction bar."""
    width = max(num.shape[1], den.shape[1])
    gap = 24
    bar_h = 12
    height = num.shape[0] + gap + bar_h + gap + den.shape[0]
    canvas = np.zeros((height, width, 4), dtype=np.uint8)
    x_num = (width - num.shape[1]) // 2
    x_den = (width - den.shape[1]) // 2
    canvas[:num.shape[0], x_num:x_num + num.shape[1]] = num
    bar_y = num.shape[0] + gap
    canvas[bar_y:bar_y + bar_h, :, :3] = 0
    canvas[bar_y:bar_y + bar_h, :, 3] = 255
    y_den = bar_y + bar_h + gap
    canvas[y_den:y_den + den.shape[0], x_den:x_den + den.shape[1]] = den
    Image.fromarray(canvas).save(out)
    return {"path": out, "w_px": int(width), "h_px": int(height),
            "w_in": round(width / DPI, 5), "h_in": round(height / DPI, 5),
            "dpi": DPI, "fontsize_pt": 22}


def brace(out, w_in=2.99, h_in=0.20):
    fig = plt.figure(figsize=(w_in, h_in), dpi=DPI)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    verts = [(0.002, 0.98), (0.002, 0.62),
             (0.5, 0.06), (0.998, 0.62), (0.998, 0.98)]
    codes = [Path.MOVETO, Path.LINETO, Path.CURVE4, Path.CURVE4, Path.LINETO]
    # cubic through center tip: control points pull the curve down to the tip
    # underbrace: top stubs at both ends, curve dipping to a center-bottom tip
    verts = [(0.002, 0.98), (0.002, 0.70),
             (0.005, 0.38), (0.20, 0.10), (0.47, 0.06),
             (0.50, 0.02),
             (0.53, 0.06), (0.80, 0.10), (0.995, 0.38),
             (0.998, 0.70), (0.998, 0.98)]
    codes = [Path.MOVETO, Path.LINETO,
             Path.CURVE4, Path.CURVE4, Path.CURVE4,
             Path.CURVE3, Path.CURVE3,
             Path.CURVE4, Path.CURVE4, Path.CURVE4,
             Path.LINETO]
    # CURVE3 pair needs 2 points each; rebuild cleanly with CURVE4 segments instead
    verts = [(0.002, 0.98), (0.002, 0.70),
             (0.005, 0.38), (0.20, 0.10), (0.50, 0.04),
             (0.50, 0.04),
             (0.80, 0.10), (0.995, 0.38), (0.998, 0.70), (0.998, 0.98)]
    codes = [Path.MOVETO, Path.LINETO,
             Path.CURVE4, Path.CURVE4, Path.CURVE4,
             Path.CURVE4, Path.CURVE4, Path.CURVE4,
             Path.LINETO, Path.LINETO]
    path = Path(verts, codes)
    ax.add_patch(PathPatch(path, fill=False, edgecolor=GREEN, linewidth=4.0,
                           capstyle="round", joinstyle="round"))
    fig.savefig(out, dpi=DPI, transparent=True)
    plt.close(fig)
    with Image.open(out) as im:
        return {"path": out, "w_px": im.size[0], "h_px": im.size[1],
                "w_in": round(im.size[0] / DPI, 5), "h_in": round(im.size[1] / DPI, 5), "dpi": DPI}


def plane(out, w_in, h_in, marking):
    """Top-view sketch aircraft, nose pointing right. marking: 'skull' | 'windows'."""
    fig = plt.figure(figsize=(w_in, h_in), dpi=DPI)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    lw = 1.1
    ec = GRAY
    ax.add_patch(Ellipse((0.50, 0.50), 0.88, 0.15, fill=False, edgecolor=ec, linewidth=lw))
    ax.add_patch(Ellipse((0.84, 0.50), 0.11, 0.09, fill=False, edgecolor=ec, linewidth=0.8))
    ax.add_patch(Polygon([(0.46, 0.56), (0.30, 0.99), (0.43, 0.99), (0.56, 0.56)],
                         closed=True, fill=False, edgecolor=ec, linewidth=lw))
    ax.add_patch(Polygon([(0.46, 0.44), (0.30, 0.01), (0.43, 0.01), (0.56, 0.44)],
                         closed=True, fill=False, edgecolor=ec, linewidth=lw))
    ax.add_patch(Polygon([(0.10, 0.55), (0.02, 0.86), (0.10, 0.86), (0.18, 0.55)],
                         closed=True, fill=False, edgecolor=ec, linewidth=lw))
    ax.add_patch(Polygon([(0.10, 0.45), (0.02, 0.14), (0.10, 0.14), (0.18, 0.45)],
                         closed=True, fill=False, edgecolor=ec, linewidth=lw))
    if marking == "skull":
        ax.add_patch(Circle((0.58, 0.54), 0.055, fill=False, edgecolor=BLACK, linewidth=0.9))
        ax.plot([0.545, 0.615], [0.47, 0.40], color=BLACK, linewidth=0.9)
        ax.plot([0.545, 0.615], [0.40, 0.47], color=BLACK, linewidth=0.9)
    else:
        for i, x in enumerate([0.56, 0.64, 0.72, 0.80]):
            ax.add_patch(Circle((x, 0.50), 0.022, fill=False, edgecolor=BLACK, linewidth=0.7))
    fig.savefig(out, dpi=DPI, transparent=True, bbox_inches="tight", pad_inches=0.005)
    plt.close(fig)
    with Image.open(out) as im:
        return {"path": out, "w_px": im.size[0], "h_px": im.size[1],
                "w_in": round(im.size[0] / DPI, 5), "h_in": round(im.size[1] / DPI, 5), "dpi": DPI}


manifest = {}
manifest["frac_num"] = compose_runs([("\\mathbf{T}", BLACK), ("\\mathbf{P}", RED)], 22,
                                    os.path.join(OUT, "eq_010_frac_num.png"))
manifest["frac_den"] = compose_runs([("\\mathbf{T}", BLACK), ("\\mathbf{P}", RED), ("+", BLACK), ("\\mathbf{F}", RED), ("\\mathbf{N}", RED)], 22,
                                    os.path.join(OUT, "eq_010_frac_den.png"), gap_px=10)
with Image.open(os.path.join(OUT, "eq_010_frac_num.png")) as im:
    num = np.asarray(im)
with Image.open(os.path.join(OUT, "eq_010_frac_den.png")) as im:
    den = np.asarray(im)
manifest["fraction"] = compose_fraction(num, den, os.path.join(OUT, "eq_010_fraction.png"))
manifest["brace"] = brace(os.path.join(OUT, "brace_010.png"))
manifest["plane_pos"] = plane(os.path.join(OUT, "plane_010_pos.png"), 1.10, 0.55, "skull")
manifest["plane_neg"] = plane(os.path.join(OUT, "plane_010_neg.png"), 1.15, 0.55, "windows")
with open(os.path.join(OUT, "eq_010_assets.json"), "w") as f:
    json.dump(manifest, f, indent=2)
for k, v in manifest.items():
    print(k, v["w_px"], "x", v["h_px"], f"{v['w_in']}x{v['h_in']}in")
