#!/usr/bin/env python3
"""measure10.py — per-word title font discrimination (col-profile IoU per word)."""
from PIL import Image, ImageFont, ImageDraw
import numpy as np

BASE = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction"
a = np.asarray(Image.open(f"{BASE}/unique_slides/slide_044.jpg").convert("RGB")).astype(int)

band = a[60:108, 205:760]
ink = (band[..., 0] > 140) & (band[..., 1] < 110) & (band[..., 2] < 110)

# measured word boxes (from measure7): (text, x0, x1) in frame px
WORDS = [("Solution?", 211, 358), ("Zero-padding!", 371, 586), ("Others", 620, 721), ("!!", 736, 750)]

cands = [("Arial-Bold", "/usr/share/fonts/TTF/Arialbd.TTF", 32.4),
         ("Calibri-Bold", "/usr/share/fonts/TTF/calibrib.ttf", 37.7)]

def colprof(mask, Ht=33):
    im2 = Image.fromarray((mask * 255).astype(np.uint8))
    s = Ht / im2.height
    im2 = im2.resize((max(1, int(im2.width * s)), Ht))
    mm = np.asarray(im2) > 100
    return mm.sum(axis=0).astype(float)

tot = {}
for name, path, size in cands:
    f = ImageFont.truetype(path, int(round(size * 4)))
    print(f"--- {name} ---")
    s = 0.0
    for text, wx0, wx1 in WORDS:
        om = ink[:, wx0 - 205:wx1 - 205 + 1]
        oy = np.where(om.any(axis=1))[0]
        om = om[oy.min():oy.max() + 1]
        bb = f.getbbox(text)
        W, H = (bb[2] - bb[0]) + 20, (bb[3] - bb[1]) + 20
        img = Image.new("L", (W, H), 255)
        ImageDraw.Draw(img).text((10 - bb[0] / 4, 10 - bb[1] / 4), text, font=f, fill=0)
        m = np.asarray(img) < 128
        ys2, xs2 = np.where(m)
        m = m[ys2.min():ys2.max() + 1, xs2.min():xs2.max() + 1]
        po, pm = colprof(om), colprof(m)
        best = 0
        for sh in range(-8, 9):
            if sh >= 0:
                a1, b1 = po[sh:], pm[:len(po) - sh]
            else:
                a1, b1 = po[:len(po) + sh], pm[-sh:]
            L = min(len(a1), len(b1))
            if L < 10: continue
            a1b, b1b = a1[:L], b1[:L]
            iou = np.minimum(a1b, b1b).sum() / max(1e-9, np.maximum(a1b, b1b).sum())
            best = max(best, iou)
        print(f"  '{text}': orig w {om.shape[1]} render w {m.shape[1]} -> col-IoU {best:.3f}")
        s += best
    tot[name] = s / len(WORDS)
print("MEAN per-word col-IoU:", {k: round(v, 3) for k, v in tot.items()})
