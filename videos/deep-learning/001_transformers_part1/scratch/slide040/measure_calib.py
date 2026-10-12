#!/usr/bin/env python3
"""Calibrate JPEG bias using KNOWN chrome colors in the frame, then infer text colors."""
import numpy as np
from PIL import Image

FR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_040.jpg"
im = np.asarray(Image.open(FR).convert("RGB")).astype(int)

print("=== KNOWN references ===")
# Panel gray (large area, true E9E9E7 = 233,233,231)
patch = im[280:320, 600:700].reshape(-1, 3)
print("panel (true E9E9E7):", np.median(patch, axis=0))

# White margin (true FFFFFF)
print("margin (true FFFFFF):", np.median(im[5:40, 400:500].reshape(-1, 3), axis=0))

# Bottom border stroke rows 537-539 (true C00000 = 192,0,0), clean cols 300..700
band = im[535:540, 300:700]
print("bottom border col 450:", [tuple(im[y, 450]) for y in range(534, 540)])
r = band[:, :, 0]; g = band[:, :, 1]; b = band[:, :, 2]
mask = (r.astype(int) - g > 30)
pix = band[mask]
print("border red-ish n=", len(pix), "min RGB:", pix.min(axis=0), "p10:", np.percentile(pix, 10, axis=0))

# Badge numeral ink (true 333333 = 51,51,51) on FDFD96
zone = im[60:84, 880:908]
dark = (zone.sum(axis=2) < 350)
pix = zone[dark]
if len(pix):
    print("badge numeral n=", len(pix), "min:", pix.min(axis=0), "p10:", np.percentile(pix, 10, axis=0))

# Badge yellow (true FDFD96 = 253,253,150) — large-ish disc
r2, g2, b2 = im[:, :, 0], im[:, :, 1], im[:, :, 2]
yel = (r2 > 200) & (g2 > 200) & (b2 < 190)
ys, xs = np.where(yel)
pix = im[ys, xs]
print("badge yellow median:", np.median(pix, axis=0), "n=", len(pix))

print("=== TEXT (unknown true colors) ===")
# Title red ink: min/p10 per channel + luma of core
zone = im[195:245, 220:710]
red = (zone[:, :, 0] > 120) & (zone[:, :, 1] < 100) & (zone[:, :, 2] < 100)
pix = zone[red]
print("title red n=", len(pix), "p90 (brightest):", np.percentile(pix, 90, axis=0))
luma = pix @ np.array([0.299, 0.587, 0.114])
print("title red luma p75/p90:", np.percentile(luma, [75, 90]).round(1))

# Blue ink
zone = im[336:374, 160:470]
blue = (zone[:, :, 2] > 100) & (zone[:, :, 0] < 120) & (zone[:, :, 1] < 120)
pix = zone[blue]
print("blue1 n=", len(pix), "p90:", np.percentile(pix, 90, axis=0))
luma = pix @ np.array([0.299, 0.587, 0.114])
print("blue1 luma p75/p90:", np.percentile(luma, [75, 90]).round(1))
# theoretical lumas
for name, rgb in [("000099", (0, 0, 153)), ("0000B0", (0, 0, 176)), ("0000CC", (0, 0, 204)), ("2222CC", (34, 34, 204))]:
    print(f"  luma {name} = {0.114 * rgb[2] + 0.587 * rgb[1] + 0.299 * rgb[0]:.1f}")
for name, rgb in [("990000", (153, 0, 0)), ("C00000", (192, 0, 0)), ("CC0000", (204, 0, 0)), ("E00000", (224, 0, 0))]:
    print(f"  luma {name} = {0.299 * rgb[0]:.1f}")
