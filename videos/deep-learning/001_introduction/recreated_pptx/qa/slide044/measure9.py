#!/usr/bin/env python3
"""measure9.py — title font discrimination: column-ink-profile IoU of the original
title band vs PIL renders of candidate bold fonts at metric-solved sizes."""
from PIL import Image, ImageFont, ImageDraw
import numpy as np

BASE = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction"
a = np.asarray(Image.open(f"{BASE}/unique_slides/slide_044.jpg").convert("RGB")).astype(int)

# original title ink: x 211..751, y 68..100 (red on gray)
band = a[60:108, 205:760]
ink = (band[..., 0] > 140) & (band[..., 1] < 110) & (band[..., 2] < 110)
ys, xs = np.where(ink)
y0, y1, x0, x1 = ys.min(), ys.max(), xs.min(), xs.max()
orig = ink[y0:y1 + 1, x0:x1 + 1]
print(f"orig title ink {orig.shape[1]}x{orig.shape[0]}")

TITLE = "Solution? Zero-padding! , Others !!"
cands = [("Arial-Bold", "/usr/share/fonts/TTF/Arialbd.TTF", 32.4),
         ("Calibri-Bold", "/usr/share/fonts/TTF/calibrib.ttf", 37.7),
         ("Carlito-Bold", "/usr/share/fonts/carlito/Carlito-Bold.ttf", 37.7)]
for name, path, size in cands:
    f = ImageFont.truetype(path, int(round(size * 4)))
    bb = f.getbbox(TITLE)
    W, H = (bb[2] - bb[0]) + 20, (bb[3] - bb[1]) + 20
    img = Image.new("L", (W, H), 255)
    d = ImageDraw.Draw(img)
    d.text((10 - bb[0] / 4, 10 - bb[1] / 4), TITLE, font=f, fill=0)
    m = np.asarray(img) < 128
    ys2, xs2 = np.where(m)
    m = m[ys2.min():ys2.max() + 1, xs2.min():xs2.max() + 1]
    # normalize both to height 33 (orig ink h) and compare column profiles
    def colprof(mask, Ht):
        im2 = Image.fromarray((mask * 255).astype(np.uint8))
        s = Ht / im2.height
        im2 = im2.resize((max(1, int(im2.width * s)), Ht))
        mm = np.asarray(im2) > 100
        return mm.sum(axis=0), mm
    po, orig_r = colprof(orig, 33)
    pm, rend_r = colprof(m, 33)
    # align by cross-correlation over ±12 px
    best = (-1, 0)
    for sh in range(-12, 13):
        if sh >= 0:
            a1, b1 = po[sh:], pm[:len(po) - sh]
        else:
            a1, b1 = po[:len(po) + sh], pm[-sh:]
        L = min(len(a1), len(b1))
        a1, b1 = a1[:L], b1[:L]
        if L == 0:
            continue
        inter = np.minimum(a1, b1).sum(); union = np.maximum(a1, b1).sum()
        iou = inter / union if union else 0
        if iou > best[0]: best = (iou, sh)
    # row profile IoU too (cap/x-height structure)
    ro = orig_r.sum(axis=1).astype(float); rm = rend_r.sum(axis=1).astype(float)
    row_iou = np.minimum(ro, rm).sum() / np.maximum(ro, rm).sum()
    print(f"{name}: col-IoU {best[0]:.3f} (shift {best[1]}) row-IoU {row_iou:.3f}")
