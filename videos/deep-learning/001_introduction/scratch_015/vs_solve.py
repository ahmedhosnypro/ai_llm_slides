#!/usr/bin/env python3
"""Native-scale shape test for the 'vs' glyph pair: candidates rendered at fitted
sizes, aligned by best 2D offset, IoU + grayscale NCC on the original crop."""
import numpy as np
from PIL import Image, ImageFont, ImageDraw

IM = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_015.jpg"
im = np.asarray(Image.open(IM).convert("RGB")).astype(int)
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]
red = (r > 120) & (g < 110) & (b < 110)
m = red[260:300, 460:520]
ys, xs = np.where(m)
crop = m[ys.min():ys.max()+1, xs.min():xs.max()+1]
gray = (255 - im[260:300, 460:520, 0].astype(float))  # darkness of red channel
gcrop = gray[ys.min():ys.max()+1, xs.min():xs.max()+1]
print("crop", crop.shape)

SERIF = "/usr/share/fonts/liberation/LiberationSerif-Bold.ttf"
SANS = "/usr/share/fonts/liberation/LiberationSans-Bold.ttf"

def render(text, path, size):
    f = ImageFont.truetype(path, size)
    img = Image.new("L", (200, 120), 0)
    ImageDraw.Draw(img).text((20, 20), text, font=f, fill=255)
    a = np.asarray(img) > 100
    ys, xs = np.where(a)
    return a[ys.min():ys.max()+1, xs.min():xs.max()+1]

def best_iou(crop, cand):
    # slide cand over crop at all offsets (both directions), take max IoU
    ch, cw = crop.shape; nh, nw = cand.shape
    best = 0; bestncc = -1
    H = max(ch, nh)+4; W = max(cw, nw)+4
    A = np.zeros((H, W), bool); A[2:2+ch, 2:2+cw] = crop
    Ag = np.zeros((H, W)); Ag[2:2+ch, 2:2+cw] = gcrop
    for dy in range(0, H-nh+1):
        for dx in range(0, W-nw+1):
            B = np.zeros((H, W), bool); B[dy:dy+nh, dx:dx+nw] = cand
            i = (A & B).sum(); u = (A | B).sum()
            v = i/u
            if v > best:
                best = v
                Bg = np.zeros((H, W)); Bg[dy:dy+nh, dx:dx+nw] = 1.0
                # ncc on darkness
                a_ = Ag - Ag.mean(); b_ = Bg - Bg.mean()
                bestncc = (a_*b_).sum()/np.sqrt((a_**2).sum()*(b_**2).sum())
    return best, bestncc

cands = [
    ("serif 'vs'@43", "vs", SERIF, 43), ("serif 'vs'@44", "vs", SERIF, 44),
    ("serif 'VS'@30", "VS", SERIF, 30), ("serif 'VS'@31", "VS", SERIF, 31),
    ("serif 'vs'@48", "vs", SERIF, 48), ("serif 'VS'@36", "VS", SERIF, 36),
    ("sans 'vs'@34", "vs", SANS, 34), ("sans 'VS'@29", "VS", SANS, 29),
]
for lab, t, p, s in cands:
    c = render(t, p, s)
    i, n = best_iou(crop, c)
    print(f"{lab}: cand {c.shape}  IoU={i:.3f}  NCC={n:.3f}")
