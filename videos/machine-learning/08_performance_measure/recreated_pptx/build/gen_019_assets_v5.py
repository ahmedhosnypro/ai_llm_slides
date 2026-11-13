"""Slide 019 assets v5 — bipolar-step glyph PNGs, redrawn to match the original:
thick muted-purple (#732575, measured ~115,37,117) step line over a thin gray
axis cross, no box frame. Two sizes: full (activation circle) and small (model
circles). Judge attempt 3 MAJOR: v2 plot was maroon + thin -> washed out at
0.32 scale."""
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure/recreated_pptx/build/assets"
os.makedirs(OUT, exist_ok=True)

PURPLE = "#732575"
GRAY = "#8A8A8A"


def save_step(path, w, h, lw):
    fig = plt.figure(figsize=(w, h), dpi=600)
    ax = fig.add_axes([0.06, 0.08, 0.88, 0.86])
    ax.axhline(0, color=GRAY, linewidth=0.8)
    ax.axvline(0.5, color=GRAY, linewidth=0.8)
    ax.plot([0.0, 0.5], [-1, -1], color=PURPLE, linewidth=lw, solid_capstyle="butt")
    ax.plot([0.5, 0.5], [-1, 1], color=PURPLE, linewidth=lw, solid_capstyle="butt")
    ax.plot([0.5, 1.0], [1, 1], color=PURPLE, linewidth=lw, solid_capstyle="butt")
    for s in ("top", "right", "bottom", "left"):
        ax.spines[s].set_visible(False)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlim(-0.02, 1.02)
    ax.set_ylim(-1.25, 1.25)
    ax.set_aspect("auto")
    fig.savefig(path, dpi=600, transparent=True, bbox_inches="tight", pad_inches=0.01)
    plt.close(fig)


from PIL import Image

assets = []
for name, w, h, lw in (
    ("eq_019_step_plot", 1.5, 1.0, 4.0),
    ("eq_019_step_plot_small", 1.1, 0.85, 6.5),
):
    p = os.path.join(OUT, name + ".png")
    save_step(p, w, h, lw)
    with Image.open(p) as im:
        assets.append({"image": name + ".png", "w_px": im.size[0], "h_px": im.size[1],
                       "w_in": round(im.size[0] / 600, 4), "h_in": round(im.size[1] / 600, 4)})

with open(os.path.join(OUT, "eq_019_assets_v5.json"), "w") as f:
    json.dump(assets, f, indent=2)
for a in assets:
    print(a)
