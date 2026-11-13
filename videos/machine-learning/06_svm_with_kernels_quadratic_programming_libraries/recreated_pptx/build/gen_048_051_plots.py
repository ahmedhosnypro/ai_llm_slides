#!/usr/bin/env python3
"""Generate plot PNGs for slides 048, 049, 050, 051 from final-JSON specs."""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "assets", "045_055")
DPI = 200
rng = np.random.default_rng(7)


def base_axes(ax, xlim, ylim, xticks, yticks, grid=True, grid_color="#D9D9D9", spine="#000000"):
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_xticks(xticks)
    ax.set_yticks(yticks)
    ax.set_facecolor("white")
    if grid:
        ax.grid(True, color=grid_color, linewidth=0.6, linestyle="-" if grid_color != "#808080" else ":", alpha=0.9)
    for s in ax.spines.values():
        s.set_color(spine)
        s.set_linewidth(1.2)
    ax.tick_params(colors="#000000", labelsize=9)


def fig_for(w_norm, h_norm):
    w_in, h_in = w_norm * 13.33, h_norm * 7.5
    fig = plt.figure(figsize=(w_in, h_in), dpi=DPI)
    ax = fig.add_axes([0.14, 0.12, 0.82, 0.82])
    return fig, ax


def save(fig, name):
    p = os.path.join(OUT, name)
    fig.savefig(p, dpi=DPI, facecolor="white")
    plt.close(fig)
    print("wrote", p)


def slide_048():
    fig, ax = fig_for(0.538, 0.795)
    base_axes(ax, (0, 45), (0, 38), [0, 10, 20, 30, 40], [0, 5, 10, 15, 20, 25, 30, 35])
    t = np.linspace(0, 2 * np.pi, 85)
    r = 10.5 + rng.normal(0, 0.8, 85)
    ax.scatter(25 + r * np.cos(t), 20 + r * np.sin(t) * 0.9, s=14, c="#FF0000")
    ax.scatter(rng.uniform(4, 16, 30), rng.uniform(10, 22, 30), s=14, c="#0000FF")
    ax.scatter(rng.uniform(22, 31, 50), rng.uniform(11, 17, 50), s=14, c="#000000")
    save(fig, "slide_048_plot.png")


def slide_049():
    fig, ax = fig_for(0.508, 0.644)
    base_axes(ax, (0, 45), (0, 38), [0, 10, 20, 30, 40], [0, 5, 10, 15, 20, 25, 30, 35],
              grid_color="#A6A6A6")
    ax.grid(True, color="#A6A6A6", linewidth=0.6, linestyle=":")
    ax.scatter(rng.uniform(1, 44, 220), rng.uniform(1, 36, 220), s=4, c="#F2A0A0")
    t = np.linspace(0, 2 * np.pi, 60)
    r = 11 + rng.normal(0, 0.7, 60)
    ax.scatter(20 + r * np.cos(t), 18 + r * np.sin(t), s=16, c="#E60000")
    ax.scatter(rng.uniform(14, 40, 25), rng.uniform(2, 30, 25), s=16, c="#E60000")
    ax.scatter(rng.uniform(9, 18, 30), rng.uniform(10, 24, 30), s=16, c="#0000FF")
    ax.scatter(rng.uniform(20, 30, 40), rng.uniform(9, 22, 40), s=16, c="#000000")
    save(fig, "slide_049_plot.png")


def slide_050():
    fig, ax = fig_for(0.57, 0.80)
    base_axes(ax, (-12, 55), (-12, 45), [-10, 0, 10, 20, 30, 40, 50], [-10, 0, 10, 20, 30, 40],
              grid_color="#E3E3E3")
    ax.plot([0, 0], [0, 30], color="#2F2F2F", lw=1.6)
    ax.plot([0, 50], [0, 0], color="#2F2F2F", lw=1.6)
    ax.scatter(rng.uniform(0, 28, 70), rng.uniform(14, 28, 70), s=16, c="#0000E6")
    xs = np.linspace(14, 42, 150)
    ys = 10.5 - 7.5 * np.exp(-((xs - 29) / 7.0) ** 2) + rng.normal(0, 1.2, 150)
    ax.scatter(xs, np.clip(ys, 3, 18), s=14, c="#FF0000")
    save(fig, "slide_050_plot.png")


def slide_051():
    fig, ax = fig_for(0.52, 0.65)
    base_axes(ax, (-12, 55), (-12, 45), [-10, 0, 10, 20, 30, 40, 50], [-10, 0, 10, 20, 30, 40],
              grid_color="#D9D9D9")
    ax.plot([0, 0], [0, 30], color="#7F7F7F", lw=1.4)
    ax.plot([0, 43], [0, 0], color="#7F7F7F", lw=1.4)
    gx = np.arange(2, 28, 1.2)
    ax.scatter(gx, rng.uniform(2, 28, len(gx)), s=3, c="#0000FF", alpha=0.8)
    gx2 = np.arange(28, 43, 1.2)
    ax.scatter(gx2, rng.uniform(2, 28, len(gx2)), s=3, c="#FF0000", alpha=0.8)
    ax.scatter(rng.uniform(2, 27, 60), rng.uniform(14, 28, 60), s=16, c="#0000FF")
    xs = np.linspace(14, 40, 60)
    ys = 4 + 13 * ((xs - 23) / 13.5) ** 2
    ax.scatter(xs, ys + rng.normal(0, 0.8, 60), s=16, c="#FF0000")
    save(fig, "slide_051_plot.png")


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    slide_048()
    slide_049()
    slide_050()
    slide_051()
