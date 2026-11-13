#!/usr/bin/env python3
"""Wave-3 assets for slide 025: measured graphs and colored 2D equations."""
import json
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

OUT = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/build"
DPI = 600
RED = "#c00000"
BLUE = "#0000c0"


def graph(path, kind):
    fig = plt.figure(figsize=(287 / 72, 148 / 72), dpi=200)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(-3, 3)
    ax.set_ylim(-3, 3) if kind == "linear" else ax.set_ylim(-1.5, 1.5)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_facecolor("white")
    fig.patch.set_facecolor("white")
    for spine in ax.spines.values():
        spine.set_color(BLUE)
        spine.set_linewidth(1.5)
    ax.annotate("", xy=(2.75, 0), xytext=(-2.75, 0),
                arrowprops=dict(arrowstyle="-|>", color="black", lw=1.3,
                                mutation_scale=13, shrinkA=0, shrinkB=0))
    top = 2.75 if kind == "linear" else 1.35
    bottom = -2.75 if kind == "linear" else -1.35
    ax.annotate("", xy=(0, top), xytext=(0, bottom),
                arrowprops=dict(arrowstyle="-|>", color="black", lw=1.3,
                                mutation_scale=13, shrinkA=0, shrinkB=0))
    if kind == "linear":
        ax.plot([-2.15, 2.15], [-2.15, 2.15], color=RED, lw=1.8)
    else:
        low, high = (0.0, 1.0) if kind == "unipolar" else (-1.0, 1.0)
        ax.plot([-2.45, 0], [low, low], color=RED, lw=1.8)
        ax.plot([0, 2.45], [high, high], color=RED, lw=1.8)
        ax.plot([0, 0], [low, high], color=RED, lw=1.8)
    ax.text(-0.42, top - 0.08, r"$f(x)$", color=RED, fontsize=13,
            ha="right", va="top")
    ax.text(2.55, -0.18 if kind == "linear" else -0.28, r"$x$", color=RED,
            fontsize=13, ha="center", va="top")
    fig.savefig(path, dpi=200, facecolor="white", edgecolor="none")
    plt.close(fig)


def render_eq(parts, name, target_px):
    from matplotlib.font_manager import FontProperties

    def once(fs):
        fig = plt.figure(figsize=(14, 5), dpi=DPI)
        fig.patch.set_alpha(0)
        fig.canvas.draw()
        renderer = fig.canvas.get_renderer()
        prop = FontProperties(size=fs)
        widths = []
        for mathtext, _ in parts:
            w, _, _ = renderer.get_text_width_height_descent(
                f"${mathtext}$", prop, ismath=True)
            widths.append(w)
        x = 0.08
        for (mathtext, color), w in zip(parts, widths):
            fig.text(x, 0.5, f"${mathtext}$", fontsize=fs, color=color,
                     ha="left", va="center")
            x += w / (14 * DPI)
        fig.canvas.draw()
        buf = np.asarray(fig.canvas.buffer_rgba())
        ink = buf[:, :, 3] > 8
        rows = np.where(ink.any(axis=1))[0]
        cols = np.where(ink.any(axis=0))[0]
        plt.close(fig)
        return buf, rows, cols, sum(widths)

    buf, rows, cols, width = once(20)
    fs = 20 * (target_px * DPI / 72) / width
    buf, rows, cols, _ = once(fs)
    pad = 6
    y0, y1 = max(rows[0] - pad, 0), min(rows[-1] + pad, buf.shape[0])
    x0, x1 = max(cols[0] - pad, 0), min(cols[-1] + pad, buf.shape[1])
    out = f"{OUT}/{name}.png"
    Image.fromarray(buf[y0:y1, x0:x1]).save(out)
    return {"name": name, "image": f"{name}.png", "w_px": int(x1 - x0),
            "h_px": int(y1 - y0), "w_in": round((x1 - x0) / DPI, 5),
            "h_in": round((y1 - y0) / DPI, 5), "dpi": DPI,
            "font_size_pt": fs, "color": "mixed",
            "mathtext": " + ".join(mt for mt, _ in parts)}


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    graph(f"{OUT}/slide_025_linear_w3.png", "linear")
    graph(f"{OUT}/slide_025_unipolar_step_w3.png", "unipolar")
    graph(f"{OUT}/slide_025_bipolar_step_w3.png", "bipolar")
    eqs = [
        ([(r"F(x) = x \qquad", "black"),
          (r"\mathit{Linear\ (No\ Activation)}", "red")],
         "eq_s025_linear_w3", 250),
        ([(r"F(x) = ", "black"),
          (r"\mathrm{Uni-polar\ Unit\ Step}", "red"),
          (r"= \left\{ \substack{0\ \ \mathrm{for}\ x < 0 \\ 1\ \ \mathrm{for}\ x \geq 0} \right.", "green")],
         "eq_s025_unipolar_w3", 275),
        ([(r"F(x) = ", "black"),
          (r"\mathrm{Bi-polar\ Unit\ Step}", "red"),
          (r"= \left\{ \substack{-1\ \ \mathrm{for}\ x < 0 \\ 1\ \ \mathrm{for}\ x \geq 0} \right.", "green")],
         "eq_s025_bipolar_w3", 310),
    ]
    results = [render_eq(parts, name, width) for parts, name, width in eqs]
    with open(f"{OUT}/slide_025_equations_w3.json", "w") as f:
        json.dump({"slide": "025", "equations": results}, f, indent=2)
    for e in results:
        print(e["name"], e["w_in"], e["h_in"])
