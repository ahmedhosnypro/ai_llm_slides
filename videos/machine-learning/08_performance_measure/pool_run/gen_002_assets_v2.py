import os
from PIL import Image, ImageDraw
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

NS = os.environ.get("NS", "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure")
A = f"{NS}/recreated_pptx/build/assets"

# Activation plot: original plot region x807-857 y104-144 (50x40 px) -> aspect 1.25
fig, ax = plt.subplots(figsize=(50 / 100, 40 / 100), dpi=400)
ax.plot(np.linspace(-6, 6, 400), 1 / (1 + np.exp(-np.linspace(-6, 6, 400))),
        color="#7030A0", lw=2.2)
ax.set_xlim(-6, 6); ax.set_ylim(-0.05, 1.05)
ax.set_xticks([]); ax.set_yticks([])
for sp in ("top", "right"):
    ax.spines[sp].set_visible(False)
for sp in ("left", "bottom"):
    ax.spines[sp].set_color("#888888"); ax.spines[sp].set_linewidth(0.8)
fig.subplots_adjust(left=0.06, right=0.97, top=0.95, bottom=0.10)
fig.savefig(f"{A}/sigmoid_002.png", facecolor="white")
plt.close(fig)

# Model-box sigmoid badge: original purple icon bbox ~40x40 (circular pink badge)
scale = 10
badge = Image.new("RGBA", (40 * scale, 40 * scale), (0, 0, 0, 0))
draw = ImageDraw.Draw(badge)
draw.ellipse((0, 0, 40 * scale - 1, 40 * scale - 1), fill=(255, 225, 255, 255))
points = []
for i in range(400):
    x = -6 + 12 * i / 399
    y = 1 / (1 + np.exp(-x))
    points.append(((4 + 32 * i / 399) * scale, (33 - 26 * y) * scale))
draw.line(points, fill=(112, 48, 160, 255), width=2 * scale, joint="curve")
badge.resize((40, 40), Image.Resampling.LANCZOS).save(f"{A}/sigmoid_badge_002.png")
print("v2 assets written: sigmoid_002.png (50x40 aspect), sigmoid_badge_002.png (40x40 circle)")
