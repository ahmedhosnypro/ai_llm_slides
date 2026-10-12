#!/usr/bin/env python3
"""measure7.py — final pass: title word-position discrimination (Arial vs Calibri),
bullet solve with corrected 'and', gridline modals from long clean segments,
operator render-size solve, note-box text left-bearing check."""
from PIL import Image, ImageFont, ImageDraw
import numpy as np

BASE = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction"
im = Image.open(f"{BASE}/unique_slides/slide_044.jpg").convert("RGB")
a = np.asarray(im).astype(int)

def runs(mask_1d, min_len=1):
    idx = np.where(mask_1d)[0]
    if len(idx) == 0:
        return []
    out, s, p = [], idx[0], idx[0]
    for v in idx[1:]:
        if v == p + 1:
            p = v
        else:
            if p - s + 1 >= min_len:
                out.append((s, p))
            s = p = v
    if p - s + 1 >= min_len:
        out.append((s, p))
    return out

def exact_modal(x0, x1, y0, y1, n=5):
    reg = a[y0:y1, x0:x1].reshape(-1, 3)
    vals, counts = np.unique(reg, axis=0, return_counts=True)
    order = np.argsort(-counts)[:n]
    return [(tuple(int(c) for c in vals[i]), int(counts[i])) for i in order]

# --- 1) title word segments vs predicted word positions ---
band = a[60:105, 205:760]
ink = (band[..., 0] > 140) & (band[..., 1] < 110) & (band[..., 2] < 110)
colc = ink.sum(axis=0)
segs = []
s = None
for i, v in enumerate(colc):
    if v >= 1 and s is None: s = i
    elif v == 0 and s is not None: segs.append((s + 205, i - 1 + 205)); s = None
if s is not None: segs.append((s + 205, len(colc) - 1 + 205))
merged = []
for w in segs:
    if merged and w[0] - merged[-1][1] <= 4: merged[-1] = (merged[-1][0], w[1])
    else: merged.append(list(w))
print("title word segments (gap>4):", merged)
print("title word lefts:", [m[0] for m in merged], "rights:", [m[1] for m in merged])

TITLE = "Solution? Zero-padding! , Others !!"
for name, path, size in [("Arial-Bold", "/usr/share/fonts/TTF/Arialbd.TTF", 32.4),
                         ("Calibri-Bold", "/usr/share/fonts/TTF/calibrib.ttf", 37.7),
                         ("Carlito-Bold", "/usr/share/fonts/carlito/Carlito-Bold.ttf", 37.7)]:
    f = ImageFont.truetype(path, int(round(size * 4)))
    words = ["Solution?", "Zero-padding!", ",", "Others", "!!"]
    # simulate: text starts at ink-left 211; find each word's ink start via advance
    full = "Solution? Zero-padding! , Others !!"
    # walk tokens with their separators
    tokens = [("Solution?", " "), ("Zero-padding!", " "), (",", " "), ("Others", " "), ("!!", "")]
    x = 0.0
    pred = []
    fl = ImageFont.truetype(path, int(round(size * 4)))
    for t, sep in tokens:
        # ink left offset of the word itself
        bb = fl.getbbox(t)
        pred.append(211 + x + bb[0] / 4)
        x += fl.getlength(t) / 4 + (fl.getlength(sep) / 4 if sep else 0)
    print(f"{name} predicted word ink lefts: {[round(p) for p in pred]}")
    print(f"   full advance: {fl.getlength(full)/4:.0f} (target 541)")

# --- 2) bullet solve corrected ---
words = [("For", 31), ("surround", 89), ("the", 32), ("image", 58), ("with", 43), ("and", 36), ("layers", 55), ("of", 20)]
for name, path in [("Arial", "/usr/share/fonts/TTF/Arial.TTF"),
                   ("Calibri", "/usr/share/fonts/TTF/calibri.ttf"),
                   ("Carlito", "/usr/share/fonts/carlito/Carlito-Regular.ttf")]:
    offs = []
    for text, tgt in words:
        best = None
        for size10 in range(160, 300):
            size = size10 / 10
            f = ImageFont.truetype(path, int(round(size * 4)))
            w = f.getlength(text) / 4
            if best is None or abs(w - tgt) < best[1]:
                best = (size, abs(w - tgt), w)
        offs.append((best[0], best[2]))
    sizes = [o[0] for o in offs]
    print(f"BULLET {name}: sizes {[round(s,1) for s in sizes]} mean {sum(sizes)/len(sizes):.1f} spread {max(sizes)-min(sizes):.1f}")

# word-left prediction check for bullet (Calibri 23.5): place segments and compare
fl = ImageFont.truetype("/usr/share/fonts/TTF/calibri.ttf", 94)
meas_lefts = {"For": 136, "surround": 243, "the": 340, "image": 380, "with": 445, "and": 607, "layers": 766, "of": 828, "zero": 855}
print("bullet measured word lefts:", meas_lefts)

# --- 3) gridline modals from long clean segments ---
print("o55 v-line x701 boundary modal:", exact_modal(700, 703, 240, 340, 5))
print("g77 v-line x219 boundary modal:", exact_modal(218, 222, 300, 350, 5))
print("f33 v-line x469 modal (long):", exact_modal(468, 472, 250, 310, 5))
print("o55 h-line y263 modal:", exact_modal(660, 700, 262, 265, 5))
print("g77 h-line y293 modal:", exact_modal(150, 200, 292, 295, 5))

# --- 4) operator render-size solve: '*' ink 7x7 at (407..413, 278..284); '=' 14x6 ---
for name, path in [("Arial-Bold", "/usr/share/fonts/TTF/Arialbd.TTF"), ("Calibri-Bold", "/usr/share/fonts/TTF/calibrib.ttf")]:
    for ch, tw, th in [("*", 7, 7), ("=", 14, 6)]:
        best = None
        for size10 in range(120, 400):
            size = size10 / 10
            f = ImageFont.truetype(path, int(round(size * 4)))
            bb = f.getbbox(ch)
            w, h = (bb[2] - bb[0]) / 4, (bb[3] - bb[1]) / 4
            err = abs(w - tw) + abs(h - th)
            if best is None or err < best[0]:
                best = (err, size, w, h, bb[1] / 4, bb[0] / 4)
        print(f"OP {name} '{ch}': best size {best[1]} ink {best[2]:.1f}x{best[3]:.1f} (target {tw}x{th}) topOff {best[4]:.1f} leftOff {best[5]:.1f}")

# --- 5) note text: L1 bold left bearing + per-line left check at TNR 21 ---
fl = ImageFont.truetype("/usr/share/fonts/liberation/LiberationSerif-Regular.ttf", 84)
fb = ImageFont.truetype("/usr/share/fonts/liberation/LiberationSerif-Bold.ttf", 84)
for t, f, ink_left in [("Original 5x5", fb, 88), ("After padding ONE  pixel (surrounding the image) it will be 7x7", fl, 89),
                       ("After apply one filter  of size 3x3, output will be 5x5 again", fl, 90),
                       ("After apply one filter  of size 3x3 , output will be 5x5 again", fl, 90),
                       ("Do the same for next applied filter", fl, 88)]:
    bb = f.getbbox(t)
    print(f"NOTE '{t[:28]}...' adv {f.getlength(t)/4:.0f} inkoff {bb[0]/4:.1f} -> box left for ink {ink_left}: {ink_left - bb[0]/4:.1f}")
