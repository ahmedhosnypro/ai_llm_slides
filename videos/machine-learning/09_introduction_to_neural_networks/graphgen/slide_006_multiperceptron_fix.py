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
W_IN, H_IN = 6.53, 4.82

fig = plt.figure(figsize=(W_IN, H_IN), dpi=DPI)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, 12)
ax.set_ylim(0, 8)
ax.axis("off")
fig.patch.set_facecolor("white")
ax.add_patch(Rectangle((0.06, 0.06), 11.88, 7.88, fill=False,
                       edgecolor="#C00000", linewidth=1.2))

input_x = 0.85
input_rows = [("$x_1$", 5.55), ("$x_2$", 5.05), ("$x_3$", 4.55),
              (r"$\ldots$", 4.05), (r"$\ldots$", 3.55),
              ("$x_n$", 3.05), ("$1$", 2.55)]
sigma_x = 5.55
sigma_rows = [6.55, 4.05, 1.05]
activation_x = 7.15
output_x = 8.55
colors = ["#C00000", "#1A34C8", "#00A600"]

for _, y in input_rows:
    for sy in sigma_rows:
        ax.add_line(Line2D([1.15, sigma_x - 0.25], [y, sy],
                           color="#DDD5D5", linewidth=0.55, zorder=1))

for label, y in input_rows:
    ax.text(input_x, y, label, ha="center", va="center", fontsize=12,
            color="#C00000" if label == "$1$" else "#000000", zorder=4)

weight_labels = [
    [("$w_{11}$", 1.75, 5.95), ("$w_{12}$", 1.75, 5.55),
     ("$w_{13}$", 1.75, 5.15), ("$w_{1n}$", 2.05, 3.55), ("$b_1$", 2.05, 2.45)],
    [("$w_{21}$", 3.25, 5.25), ("$w_{22}$", 3.25, 4.85),
     ("$w_{23}$", 3.25, 4.45), ("$w_{2n}$", 3.45, 3.15), ("$b_2$", 3.45, 2.25)],
    [("$w_{m1}$", 4.55, 3.75), ("$w_{m2}$", 4.55, 3.35),
     ("$w_{m3}$", 4.55, 2.95), ("$w_{mn}$", 4.55, 2.55), ("$b_m$", 4.55, 1.95)],
]
for group, color in zip(weight_labels, colors):
    for label, x, y in group:
        ax.text(x, y, label, ha="center", va="center", fontsize=10,
                color=color, zorder=4)

for i, (sy, color) in enumerate(zip(sigma_rows, colors)):
    ax.add_patch(Circle((sigma_x, sy), 0.30, facecolor="#E0F2F1",
                        edgecolor="#000000", linewidth=1.0, zorder=3))
    ax.text(sigma_x, sy, r"$\Sigma$", ha="center", va="center",
            fontsize=18, color="#000000", zorder=4)
    ax.annotate("", xy=(activation_x - 0.42, sy), xytext=(sigma_x + 0.32, sy),
                arrowprops=dict(arrowstyle="-|>", color="#C00000", lw=1.2,
                                mutation_scale=12), zorder=5)
    ax.add_patch(Rectangle((activation_x - 0.42, sy - 0.34), 0.84, 0.68,
                           facecolor="#FBE5FA", edgecolor="#B048B0",
                           linewidth=1.0, zorder=3))
    ax.add_line(Line2D([activation_x - 0.20, activation_x],
                       [sy - 0.15, sy - 0.15], color="#241478", linewidth=1.2, zorder=4))
    ax.add_line(Line2D([activation_x, activation_x],
                       [sy - 0.15, sy + 0.15], color="#241478", linewidth=1.2, zorder=4))
    ax.add_line(Line2D([activation_x, activation_x + 0.22],
                       [sy + 0.15, sy + 0.15], color="#241478", linewidth=1.2, zorder=4))
    ax.add_line(Line2D([activation_x + 0.04, activation_x + 0.04],
                       [sy - 0.25, sy + 0.25], color="#C089C0", linewidth=0.7, zorder=4))
    ax.annotate("", xy=(output_x - 0.12, sy), xytext=(activation_x + 0.44, sy),
                arrowprops=dict(arrowstyle="-|>", color="#C00000", lw=1.2,
                                mutation_scale=12), zorder=5)
    roman = ["I", "II", "m"][i]
    ax.text(output_x, sy + 0.13, f">0 Class {roman}", ha="left", va="center",
            fontsize=10, color="#000000")
    ax.text(output_x, sy - 0.13, f"<0 Not Class {roman}", ha="left", va="center",
            fontsize=10, color="#000000")

for y in [3.05, 2.55, 2.05]:
    ax.add_patch(Circle((sigma_x, y), 0.09, facecolor="#E0F2F1",
                        edgecolor="#9FCFC9", linewidth=0.8))

fig.savefig(OUT, dpi=DPI, facecolor="white")
plt.close(fig)
with open(META, "w") as f:
    json.dump({"image": "slide_006_perceptron_multiclass.png", "dpi": DPI,
               "position": {"x": 5.89, "y": 2.12, "w": W_IN, "h": H_IN}}, f, indent=2)
print(OUT)
