import os
from PIL import Image
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

NS = os.environ.get("NS", "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure")
A = f"{NS}/recreated_pptx/build/assets"
orig = Image.open(f"{NS}/unique_slides/slide_002.jpg").convert("RGB")

# Plane panes: crop interiors of the two bordered panes (excludes the border strokes).
# Measured borders: pos pane x82..237 y137..509; neg pane x333..481 y137..509.
pos = orig.crop((84, 140, 84 + 151, 140 + 362))    # 151x362, matches PANE_POS placement
neg = orig.crop((336, 140, 336 + 144, 140 + 362))   # 144x362, matches PANE_NEG placement
pos.save(f"{A}/pane_pos_002.png")
neg.save(f"{A}/pane_neg_002.png")

# Sigmoid schematic: white field, thin gray axes, purple S-curve, no ticks/labels
# (original plot at x807-857 y104-144 is schematic; build places asset at 170x64 and 44x18 pt).
fig, ax = plt.subplots(figsize=(170 / 100, 64 / 100), dpi=400)
ax.plot(np.linspace(-6, 6, 400), 1 / (1 + np.exp(-np.linspace(-6, 6, 400))),
        color="#7030A0", lw=2.2)
ax.set_xlim(-6, 6); ax.set_ylim(-0.05, 1.05)
ax.set_xticks([]); ax.set_yticks([])
for sp in ("top", "right"):
    ax.spines[sp].set_visible(False)
for sp in ("left", "bottom"):
    ax.spines[sp].set_color("#888888"); ax.spines[sp].set_linewidth(0.8)
fig.subplots_adjust(left=0.04, right=0.98, top=0.96, bottom=0.08)
fig.savefig(f"{A}/sigmoid_002.png", facecolor="white")
plt.close(fig)
print("assets written:", os.listdir(A))
