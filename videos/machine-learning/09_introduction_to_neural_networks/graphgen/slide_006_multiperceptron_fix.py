#!/usr/bin/env python3
import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle
from matplotlib.lines import Line2D

V = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks"
OUT = V + "/recreated_pptx/build/slide_006_perceptron_multiclass.png"
META = V + "/recreated_pptx/build/slide_006_perceptron_multiclass.json"
DPI = 300
CROP = (390, 140, 896, 500)
W_IN = (CROP[2] - CROP[0]) * (13.03 / 839)
H_IN = (CROP[3] - CROP[1]) * (7.2 / 456)

fig = plt.figure(figsize=(W_IN, H_IN), dpi=DPI)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(CROP[0], CROP[2])
ax.set_ylim(CROP[3], CROP[1])
ax.axis("off")
fig.patch.set_alpha(0.0)
ax.set_facecolor("none")

ax.add_patch(Rectangle((424, 154), 895 - 424, 499 - 154, facecolor="#FFFFFF",
                       edgecolor="#9AA8E0", linewidth=0.8, zorder=0))

input_rows = [("$x_1$", 167, "#000000"), ("$x_2$", 215, "#000000"),
              ("$x_3$", 286, "#000000"), (r"$\ldots$", 309, "#000000"),
              (r"$\ldots$", 331, "#000000"), ("$x_n$", 399, "#000000"),
              ("$1$", 420, "#CC0000")]
sigma_rows = [186, 320, 455]
colors = ["#CC0000", "#1A34C8", "#00A600"]

for _, y, _ in input_rows:
    for sy, color in zip(sigma_rows, colors):
        ax.add_line(Line2D([440, 657], [y, sy], color=color, alpha=0.24,
                           linewidth=0.45, zorder=1))

for label, y, color in input_rows:
    ax.text(410, y, label, ha="center", va="center", fontsize=12,
            color=color, zorder=4)

weight_labels = [
    [("$w_{11}$", 440, 167), ("$w_{12}$", 493, 258), ("$w_{13}$", 493, 276),
     ("$w_{1n}$", 493, 298), ("$b_1$", 493, 389)],
    [("$w_{21}$", 575, 297), ("$w_{22}$", 554, 309), ("$w_{23}$", 560, 330),
     ("$w_{2n}$", 560, 351), ("$b_2$", 582, 364)],
    [("$w_{m1}$", 584, 385), ("$w_{m2}$", 572, 400), ("$w_{m3}$", 572, 414),
     ("$w_{mn}$", 566, 429), ("$b_m$", 577, 449)],
]
for group, color in zip(weight_labels, colors):
    for label, x, y in group:
        ax.text(x, y, label, ha="center", va="center", fontsize=10,
                color=color, zorder=4)

for i, (sy, color) in enumerate(zip(sigma_rows, colors)):
    ax.add_patch(Circle((681, sy), 20, facecolor="#E1FBF9",
                        edgecolor="#40A0A0", linewidth=0.8, zorder=3))
    ax.text(681, sy, r"$\Sigma$", ha="center", va="center",
            fontsize=20, color="#000000", zorder=4)
    ax.annotate("", xy=(720, sy), xytext=(701, sy),
                arrowprops=dict(arrowstyle="-|>", color="#C00000", lw=1.0,
                                mutation_scale=8), zorder=5)
    ax.add_patch(Rectangle((720, sy - 15.5), 48, 31, facecolor="#F8E1F9",
                           edgecolor="#B048B0", linewidth=0.8, zorder=3))
    ax.add_line(Line2D([744, 744], [sy - 10, sy + 10], color="#241478", linewidth=1.2, zorder=4))
    ax.add_line(Line2D([744, 759], [sy - 8, sy - 8], color="#241478", linewidth=1.2, zorder=4))
    ax.add_line(Line2D([731, 744], [sy + 9, sy + 9], color="#241478", linewidth=1.2, zorder=4))
    ax.annotate("", xy=(795, sy), xytext=(768, sy),
                arrowprops=dict(arrowstyle="-|>", color="#C00000", lw=1.0,
                                mutation_scale=8), zorder=5)
    roman = ["I", "II", "m"][i]
    ax.text(803, sy - 5, f">0 Class {roman}", ha="left", va="center",
            fontsize=10, color="#000000", zorder=4)
    ax.text(803, sy + 8, f"<0 Not Class {roman}", ha="left", va="center",
            fontsize=10, color="#000000", zorder=4)

for y in [355, 382, 411]:
    ax.add_patch(Circle((681, y), 6.5, facecolor="#E1FBF9",
                        edgecolor="#40A0A0", linewidth=0.7, zorder=3))

fig.savefig(OUT, dpi=DPI, transparent=True)
plt.close(fig)
with open(META, "w") as f:
    json.dump({"image": "slide_006_perceptron_multiclass.png", "dpi": DPI,
               "position": {"x": 0.15 + (CROP[0] - 60) * (13.03 / 839),
                            "y": 0.15 + (CROP[1] - 60) * (7.2 / 456),
                            "w": W_IN, "h": H_IN}}, f, indent=2)
print(OUT)
