import os
from PIL import Image, ImageDraw
import numpy as np

NS = os.environ.get("NS", "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure")
A = f"{NS}/recreated_pptx/build/assets"

# Activation-panel badge: orig pink circle bbox x803-863 y96-156 (60x60),
# fill ~(249,225,251), darker ring, purple S-curve.
scale = 10
S = 60
badge = Image.new("RGBA", (S * scale, S * scale), (0, 0, 0, 0))
draw = ImageDraw.Draw(badge)
draw.ellipse((2 * scale, 2 * scale, (S - 2) * scale, (S - 2) * scale),
             fill=(249, 225, 251, 255), outline=(200, 175, 210, 255), width=2 * scale)
pts = []
for i in range(400):
    x = -6 + 12 * i / 399
    y = 1 / (1 + np.exp(-x))
    pts.append(((10 + 40 * i / 399) * scale, (48 - 38 * y) * scale))
draw.line(pts, fill=(112, 48, 160, 255), width=3 * scale, joint="curve")
badge.resize((S, S), Image.Resampling.LANCZOS).save(f"{A}/sigmoid_002.png")

# Model-box badge: orig ~40x40 circle (train x693-733 y252-292), pink ring
# ~(255,165,196), purple curve ~(105,44,114).
S = 40
badge = Image.new("RGBA", (S * scale, S * scale), (0, 0, 0, 0))
draw = ImageDraw.Draw(badge)
draw.ellipse((1 * scale, 1 * scale, (S - 1) * scale, (S - 1) * scale),
             fill=(255, 214, 228, 255), outline=(235, 130, 160, 255), width=2 * scale)
pts = []
for i in range(400):
    x = -6 + 12 * i / 399
    y = 1 / (1 + np.exp(-x))
    pts.append(((5 + 30 * i / 399) * scale, (32 - 25 * y) * scale))
draw.line(pts, fill=(112, 48, 160, 255), width=2 * scale, joint="curve")
badge.resize((S, S), Image.Resampling.LANCZOS).save(f"{A}/sigmoid_badge_002.png")
print("v3 assets written: sigmoid_002.png 60x60 circle badge, sigmoid_badge_002.png 40x40 circle badge")
