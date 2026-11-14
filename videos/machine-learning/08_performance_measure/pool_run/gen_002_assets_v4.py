import os
from PIL import Image, ImageDraw
import numpy as np

NS = os.environ.get("NS", "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure")
A = f"{NS}/recreated_pptx/build/assets"
scale = 10

def sigmoid_badge(S, fill, ring, curve, axis):
    img = Image.new("RGBA", (S * scale, S * scale), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.ellipse((1 * scale, 1 * scale, (S - 1) * scale, (S - 1) * scale),
              fill=fill + (255,), outline=ring + (255,), width=2 * scale)
    # L-shaped axes (left + bottom), as in the original insets
    ax0, ax1 = int(S * 0.18 * scale), int(S * 0.88 * scale)
    ay0, ay1 = int(S * 0.82 * scale), int(S * 0.16 * scale)
    d.line((ax0, ay0, ax0, ay1), fill=axis + (255,), width=scale)
    d.line((ax0, ay0, ax1, ay0), fill=axis + (255,), width=scale)
    pts = []
    for i in range(400):
        x = -6 + 12 * i / 399
        y = 1 / (1 + np.exp(-x))
        pts.append((ax0 + (ax1 - ax0) * i / 399, ay0 - (ay0 - ay1) * y))
    d.line(pts, fill=curve + (255,), width=2 * scale, joint="curve")
    return img.resize((S, S), Image.Resampling.LANCZOS)

# Activation-panel badge: orig x803-863 y96-156 (60x60)
sigmoid_badge(60, (249, 225, 251), (200, 175, 210), (112, 48, 160), (120, 120, 120)).save(f"{A}/sigmoid_002.png")
# Model-box badge: orig ~40x40 (train x693-733 y252-292)
sigmoid_badge(40, (255, 214, 228), (235, 130, 160), (112, 48, 160), (120, 120, 120)).save(f"{A}/sigmoid_badge_002.png")
print("v4 assets written with axis lines")
