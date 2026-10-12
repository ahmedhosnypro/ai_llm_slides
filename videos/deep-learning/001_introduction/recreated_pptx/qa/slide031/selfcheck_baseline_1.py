"""Measure rendered baselines via heavy-row (max navy/red count) method — the same
method used on the original — and compare 1:1 with the original's baselines."""
from PIL import Image
import numpy as np

RENDER = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/qa/slide031/render_1.png"
im = Image.open(RENDER).convert("RGB")
a = np.asarray(im).astype(int)
H, W, _ = a.shape
S = W / 960.0
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]
navy = (R < 90) & (G < 90) & (B > 95) & (B - R > 60)
red = (R > 100) & (R - G > 50) & (R - B > 40)

def baseline(mask, x0, x1, y0, y1, label, target):
    m = mask[int(y0*S):int(y1*S), int(x0*S):int(x1*S)]
    counts = m.sum(axis=1)
    # heavy bottom row: last row with count >= 0.5*max in the band
    mx = counts.max()
    heavy = np.where(counts >= 0.5 * mx)[0]
    bl = y0 + heavy[-1] / S
    print(f"  {label}: heavy baseline {bl:.1f} (target {target}, d {bl-target:+.1f})")

print("== rendered baselines (heavy-row) vs original ==")
baseline(navy, 109, 663, 140, 168, "L1", 159.5)
baseline(navy, 109, 236, 194, 218, "L2", 211.5)
baseline(navy, 108, 742, 220, 245, "L3a", 237.5)
baseline(navy, 109, 472, 247, 271, "L3b", 263.5)
baseline(navy, 388, 590, 443, 468, "label", 464.5)
baseline(red, 180, 778, 85, 125, "title", 113.5)
baseline(red, 152, 468, 300, 326, "bullet1", 318)
baseline(red, 152, 480, 339, 360, "bullet2", 357)
