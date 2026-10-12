#!/usr/bin/env python3
"""calibrate_eq_tokens — slide_042 equation token decomposition (resume worker, 2026-10-12).

The previous worker's 4 whole-equation \dfrac renders are 1.6-1.8x too tall vs the
original ink (calibrated to width only; the original's subscripts are wider than STIX's
0.7em, so width-matching inflates the stack) and would collide across lines. Per the
slide-031 certified precedent (per-entry mathtext renders at measured anchors), this
script decomposes each of the 4 equations into measured INK-BOX-anchored tokens:

  - letter/run tokens rendered with Liberation Serif (Italic for variables — the
    original is Times-like italic serif; Regular for upright '=', '+', '1') at 600 dpi
    transparent PNG, each solved to its own measured ink box (LS over w/h, with
    per-token width/height priority);
  - pure-geometry strokes (fraction bars, minus signs) as native pptx rects (exact).

Every token is placed at its measured ink top-left in the build (ink anchoring — the
ALIGNMENT LAW's horizontal/vertical rule), and the closed-loop 150dpi check verifies
each equation's ink edges vs the original within ~4px@150dpi.

Outputs: build/assets/eq42tok/NN_*.png + .json sidecars + eq42tok_manifest.json
"""
import json
import os
from PIL import Image, ImageDraw, ImageFont

ROOT = "/home/ahmed/Projects/ai_llm_slides"
VID = f"{ROOT}/videos/deep-learning/001_introduction"
OUT = f"{VID}/recreated_pptx/build/assets/eq42tok"
os.makedirs(OUT, exist_ok=True)

DPI = 600.0
S = DPI / 72.0  # px per pt

ITAL = "/usr/share/fonts/liberation/LiberationSerif-Italic.ttf"
REG = "/usr/share/fonts/liberation/LiberationSerif-Regular.ttf"

# name, text, font, ink_left, ink_top, target_w, target_h, priority
# priority: 'ls' least-squares | 'w' width | 'h' height | 'c' height + centered-x
TOKENS = [
    # ---- EQ1  h_out = (h_in - h_f)/s + 1   (bar y357..358 x401..467) ----
    ("e1_h1",  "h",   ITAL, 343, 351, 8, 10, "ls"),
    ("e1_out", "out", ITAL, 353, 359, 21, 5.5, "track"),
    ("e1_eq",  "=",  REG,  383, 355, 12, 5, "ls"),
    ("e1_h2",  "h",   ITAL, 402, 341, 8, 11.5, "ls"),
    ("e1_in",  "in",  REG, 413, 344, 11, 9, "track"),
    ("e1_h3",  "h",   ITAL, 449, 341, 8, 11.5, "ls"),
    ("e1_f1",  "f",   ITAL, 461, 346, 6, 7, "c"),
    ("e1_s1",  "s",   ITAL, 430, 363.8, 8, 6.8, "ls"),
    ("e1_pl",  "+",  REG,  473, 353, 11, 9, "ls"),
    ("e1_1",   "1",  REG,  492, 352, 5, 10, "ls"),
    # ---- EQ2  w_out = (w_in - w_f)/s + 1   (bar y392..393 x402..472) ----
    ("e2_w1",  "w",   ITAL, 340, 389, 13, 7, "ls"),
    ("e2_out", "out", ITAL, 353, 393, 21, 6, "track"),
    ("e2_eq",  "=",  REG,  384, 390, 11, 5, "ls"),
    ("e2_w2",  "w",   ITAL, 402, 378, 12, 7, "ls"),
    ("e2_in",  "in",  REG, 416, 382, 11, 7, "track"),
    ("e2_w3",  "w",   ITAL, 452, 378, 12, 7, "ls"),
    ("e2_f1",  "f",   ITAL, 464, 381, 6, 8, "c"),
    ("e2_s1",  "s",   ITAL, 433, 399, 6, 6, "ls"),
    ("e2_pl",  "+",  REG,  479, 387, 10, 10, "ls"),
    ("e2_1",   "1",  REG,  497, 388, 5, 9, "ls"),
    # ---- EQ3  d_out = n_f ----
    ("e3_d1",  "d",   ITAL, 343, 414, 9, 10, "ls"),
    ("e3_out", "out", ITAL, 354, 421, 21, 6, "track"),
    ("e3_eq",  "=",  REG,  384, 418, 11, 4, "ls"),
    ("e3_n",   "n",   ITAL, 403, 417, 8, 7, "ls"),
    ("e3_f",   "f",   ITAL, 412, 420, 6, 9, "c"),
    # ---- EQ4  d_f = d_in ----
    ("e4_d1",  "d",   ITAL, 359, 440, 9, 10, "ls"),
    ("e4_f1",  "f",   ITAL, 369, 443, 6, 11, "c"),
    ("e4_eq",  "=",  REG,  384, 444, 12, 5, "ls"),
    ("e4_d2",  "d",   ITAL, 402, 440, 10, 10, "ls"),
    ("e4_in",  "in",  REG, 413, 447, 12, 7, "track"),
]

# pure-geometry strokes -> native rects in the build (frame px)
RECTS = {
    "bars":  [
        {"name": "e1_bar", "x": 401, "y": 357.1, "w": 67, "h": 1.5},
        {"name": "e2_bar", "x": 402, "y": 392.1, "w": 71, "h": 1.5},
    ],
    "minus": [
        {"name": "e1_mi", "x": 432, "y": 345.6, "w": 13, "h": 1.4},
        {"name": "e2_mi", "x": 435, "y": 380.6, "w": 10, "h": 1.3},
    ],
}


def ink_at(fontpath, size_px, text):
    """Render text on transparent canvas, return (ink_w, ink_h, cropped RGBA)."""
    f = ImageFont.truetype(fontpath, int(round(size_px)))
    # generous canvas
    W = int(size_px * (len(text) + 2) * 1.2) + 80
    H = int(size_px * 3) + 80
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.text((40, 40), text, font=f, fill=(0, 0, 0, 255))
    bbox = im.getbbox()
    if bbox is None:
        raise RuntimeError(f"no ink for {text!r}")
    return bbox[2] - bbox[0], bbox[3] - bbox[1], im.crop(bbox)


def render_token(fontpath, text, fs_pt):
    return ink_at(fontpath, fs_pt * S, text)



def render_tracked(fontpath, text, fs_pt, target_w_frame):
    """Draw letters individually (italic) with inter-letter gaps solved so the run's
    ink width == target_w_frame; ink height == natural at fs (height-solved)."""
    Sloc = DPI / 72.0
    f = ImageFont.truetype(fontpath, int(round(fs_pt * Sloc)))
    letters = list(text)
    widths = []
    for ch in letters:
        im = Image.new("RGBA", (int(fs_pt * Sloc * 3) + 80, int(fs_pt * Sloc * 3) + 80), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        d.text((40, 40), ch, font=f, fill=(0, 0, 0, 255))
        bb = im.getbbox()
        widths.append(bb[2] - bb[0])
    natural = sum(widths)
    target_px = target_w_frame * Sloc
    gap = (target_px - natural) / max(1, len(letters) - 1) if len(letters) > 1 else 0
    W = int(target_px + fs_pt * Sloc) + 80
    H = int(fs_pt * Sloc * 3) + 80
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    x = 40.0
    for ch, w in zip(letters, widths):
        d.text((x, 40), ch, font=f, fill=(0, 0, 0, 255))
        x += w + gap
    bb = im.getbbox()
    return bb[2] - bb[0], bb[3] - bb[1], im.crop(bb)


manifest = {"tokens": [], "rects": RECTS, "dpi": DPI,
            "note": "ink-anchored token decomposition; see calibrate_eq_tokens.py header"}
for (name, text, fontp, xl, yt, tw, th, prio) in TOKENS:
    # em-unit ink dims at probe (probe ink is in 600dpi px -> convert to pt, per 100pt)
    w100, h100, _ = render_token(fontp, text, 100.0)
    w_em, h_em = (w100 / S) / 100.0, (h100 / S) / 100.0
    fs_w, fs_h = tw / w_em, th / h_em
    if prio == "w":
        fs = fs_w
    elif prio == "h":
        fs = fs_h
    elif prio == "c":
        fs = fs_h
    elif prio == "h15":
        fs = fs_h * 1.15
    else:
        fs = (tw * w_em + th * h_em) / (w_em * w_em + h_em * h_em)
    fs = round(fs, 2)
    if prio == "track":
        fs_h2 = th / h_em
        fs = round(fs_h2, 2)
        w, h, im = render_tracked(fontp, text, fs, tw)
    else:
        w, h, im = render_token(fontp, text, fs)
    png = f"{OUT}/{name}.png"
    im.save(png)
    x_left = xl + (tw - w / S) / 2.0 if prio == "c" else xl
    entry = {"name": name, "text": text, "png": png, "fs_pt": fs,
             "ink_left": round(x_left, 2), "ink_top": yt,
             "w_px": w, "h_px": h, "w_in": round(w / DPI, 5), "h_in": round(h / DPI, 5),
             "target_w": tw, "target_h": th, "w_err": round(w - tw, 2), "h_err": round(h - th, 2)}
    manifest["tokens"].append(entry)
    print(f"[{name}] {text!r} fs {fs} -> {w}x{h}px  target {tw}x{th}  err (w{entry['w_err']:+.1f}, h{entry['h_err']:+.1f})")

json.dump(manifest, open(f"{OUT}/eq42tok_manifest.json", "w"), indent=1)
print("manifest ->", f"{OUT}/eq42tok_manifest.json")
print("DONE")
