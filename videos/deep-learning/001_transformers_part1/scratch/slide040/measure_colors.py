#!/usr/bin/env python3
"""Core ink colors via mask erosion + per-channel median (JPEG-stable)."""
import numpy as np
from PIL import Image

FR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_040.jpg"
im = np.asarray(Image.open(FR).convert("RGB")).astype(int)
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]

def erode(m):
    e = m.copy()
    e[1:, :] &= m[:-1, :]
    e[:-1, :] &= m[1:, :]
    e[:, 1:] &= m[:, :-1]
    e[:, :-1] &= m[:, 1:]
    return e

def core_color(mask, y0, y1, x0, x1, label, rounds=2):
    sub = mask[y0:y1, x0:x1].copy()
    for _ in range(rounds):
        if sub.sum() < 20:
            break
        # erode within the sub-region
        e = sub.copy()
        e[1:, :] &= sub[:-1, :]
        e[:-1, :] &= sub[1:, :]
        e[:, 1:] &= sub[:, :-1]
        e[:, :-1] &= sub[:, 1:]
        sub = e
    ys, xs = np.where(sub)
    if not len(ys):
        print(label, "no core pixels")
        return
    pix = im[y0:y1, x0:x1][ys, xs]
    med = np.median(pix, axis=0).astype(int)
    print(f"{label}: n={len(ys)} median RGB={tuple(med)} hex=#{med[0]:02X}{med[1]:02X}{med[2]:02X}")

red = (r > 120) & (g < 100) & (b < 100)
core_color(red, 195, 245, 220, 710, "title red core")
blue = (b > 100) & (r < 120) & (g < 120)
core_color(blue, 336, 374, 160, 470, "blue1 core")
core_color(blue, 416, 454, 160, 510, "blue2 core")

# percentile spread for title red (diagnostic)
sub = im[195:245, 220:710]
m = red[195:245, 220:710]
ys, xs = np.where(m)
pix = sub[ys, xs]
print("title red p25/p50/p75 per channel:")
for c, name in enumerate("RGB"):
    print(f"  {name}: {np.percentile(pix[:, c], [25, 50, 75]).round(0)}")
sub = im[336:374, 160:470]
m = blue[336:374, 160:470]
ys, xs = np.where(m)
pix = sub[ys, xs]
print("blue1 p25/p50/p75 per channel:")
for c, name in enumerate("RGB"):
    print(f"  {name}: {np.percentile(pix[:, c], [25, 50, 75]).round(0)}")
