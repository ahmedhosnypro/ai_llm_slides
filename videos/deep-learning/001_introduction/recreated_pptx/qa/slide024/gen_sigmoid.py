#!/usr/bin/env python3
"""Render the sigmoid-activation glyph (black curve, transparent bg, 600dpi) for the
slide_024 neurons. Display target ~11pt wide x 14pt tall -> figsize (11/72, 14/72) in."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np, json

W_IN, H_IN = 11 / 72, 14 / 72
fig = plt.figure(figsize=(W_IN, H_IN), dpi=600)
ax = fig.add_axes([0, 0, 1, 1])
x = np.linspace(-5.6, 5.6, 400)
ax.plot(x, 1 / (1 + np.exp(-x)), color="black", lw=1.4, solid_capstyle="round")
ax.set_xlim(-5.6, 5.6); ax.set_ylim(0, 1)
ax.axis("off")
out = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/build/assets/sigmoid_curve.png"
fig.savefig(out, transparent=True, dpi=600)
plt.close(fig)
from PIL import Image
im = Image.open(out)
# tight-crop to ink
alpha = np.asarray(im)[:, :, 3]
ys, xs = np.nonzero(alpha > 8)
im.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1)).save(out)
im2 = Image.open(out)
print(json.dumps({"w_px": im2.width, "h_px": im2.height,
                  "w_in": im2.width / 600, "h_in": im2.height / 600}))
