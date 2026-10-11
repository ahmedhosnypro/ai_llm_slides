#!/usr/bin/env python3
"""Fit font sizes for slide_039 elements: PIL ink-width fit per candidate font.
Targets in slide pt. Prints best size + height check per element."""
from PIL import Image, ImageFont, ImageDraw
import json

SRC = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_039.jpg"
img = Image.open(SRC).convert("RGB")
px = img.load()
SH, DH, SV = 0.96123, 18.63, 0.95556
def S(fx, fy): return (round((fx - DH) / SH, 1), round(fy / SV, 1))
def ink(p): return sum(p) < 640

out = {}

# --- bullet line text bboxes (excluding dots x<95, excluding cursor) ---
def bboxf(x0, x1, y0, y1):
    pts = [(x, y) for y in range(y0, y1 + 1) for x in range(x0, x1 + 1) if ink(px[x, y])]
    if not pts: return None
    return [min(p[0] for p in pts), min(p[1] for p in pts), max(p[0] for p in pts), max(p[1] for p in pts)]
b1 = bboxf(95, 470, 442, 461)
b2 = bboxf(95, 760, 463, 484)
out["b1_frame"] = b1
out["b2_frame"] = b2
out["b1_slide"] = S(b1[0], b1[1]) + S(b1[2], b1[3])
out["b2_slide"] = S(b2[0], b2[1]) + S(b2[2], b2[3])
# column profile of b1 tail to locate cursor vs comma
colp = {x: sum(1 for y in range(442, 461) if ink(px[x, y])) for x in range(400, 475)}
out["b1_tail_colprof"] = colp

# cursor bbox: rows 448..478, x 430..475 (find dark blob not in text rows)
cur = bboxf(430, 480, 449, 480)
out["cursor_frame"] = cur

# --- font fitting ---
FONTS = {
    "Verdana": "/usr/share/fonts/TTF/Verdana.TTF",
    "VerdanaB": "/usr/share/fonts/TTF/Verdanab.TTF",
    "ArialB": "/usr/share/fonts/TTF/Arialbd.TTF",
    "Arial": "/usr/share/fonts/TTF/Arial.TTF",
    "TimesI": "/usr/share/fonts/TTF/Timesi.TTF",
    "TimesB": "/usr/share/fonts/TTF/Timesbd.TTF",
    "NotoSansB": "/usr/share/fonts/TTF/NotoSans-Bold.ttf",
}
_cache = {}
def fit(text, fontkey, target_w):
    path = FONTS[fontkey]
    if path not in _cache:
        _cache[path] = ImageFont.truetype(path, 200)
    f = _cache[path]
    d = ImageDraw.Draw(Image.new("L", (10, 10)))
    bb = d.textbbox((0, 0), text, font=f)
    w200 = bb[2] - bb[0]
    h200 = bb[3] - bb[1]
    size = 200.0 * target_w / w200
    return {"font": fontkey, "size_pt": round(size, 1), "h_at_size": round(h200 * size / 200, 1)}

ELEMS = [
    # (label, text, candidates, target_w_slide_pt, measured_h_slide_pt)
    ("title", "Normalization", ["VerdanaB", "ArialB", "TimesB", "NotoSansB"], 229.9, 27.2),
    ("quote", "The behavior of machine learning algorithms  changes when the input distribution changes.", ["TimesI"], 813.5, 20.9),
    ("f1l1", "layer weights changes", ["VerdanaB", "ArialB", "NotoSansB"], 156.1, 14.6),
    ("f1l2", "during training steps", ["VerdanaB", "ArialB", "NotoSansB"], 147.7, 14.6),
    ("f2l1", "Outputs of Activation functions", ["VerdanaB", "ArialB", "NotoSansB"], 209.1, 13.6),
    ("f2l2", "of each layer change", ["VerdanaB", "ArialB", "NotoSansB"], 138.4, 13.6),
    ("f3l1", "Inputs to the next layer,", ["VerdanaB", "ArialB", "NotoSansB"], 155.0, 13.6),
    ("f3l2", "(With different Input distribution)", ["VerdanaB", "ArialB", "NotoSansB"], 217.5, 13.6),
    ("conclusion", "Conclusion:", ["VerdanaB", "ArialB", "NotoSansB"], 93.6, 12.5),
    ("stmt1", "Input distribution of each layer changes with each step .", ["VerdanaB", "ArialB", "NotoSansB"], 491.0, 17.8),
    ("idea", "The basic idea behind Normalization is to:", ["VerdanaB", "ArialB", "NotoSansB"], 366.2, 13.6),
    ("stmt2", "Limit covariate shift by normalizing the activations of each layer", ["VerdanaB", "ArialB", "NotoSansB"], 567.0, 14.6),
    ("lc_norm", "Normalization:", ["VerdanaB", "ArialB", "NotoSansB"], 129.0, 13.6),
    ("lc_transform", "Transforming the inputs to be", ["Verdana", "Arial", "NotoSans"], 246.5, 17.8),
    ("lc_zero", "Zero mean and unit variance.", ["VerdanaB", "ArialB", "NotoSansB"], 251.7, 12.5),
    ("sumhead", "Normalization allows each layer to:", ["VerdanaB", "ArialB", "NotoSansB"], 306.9, 16.8),
    ("b1", "learn on a more stable distribution of inputs,", ["VerdanaB", "ArialB", "NotoSansB"], None, 14.6),
    ("b2", "Accelerate the training of the network (don't stick with very small learning rates).", ["VerdanaB", "ArialB", "NotoSansB"], None, 16.8),
]
# b1/b2 targets: measure from bboxes above
if b1:
    ELEMS[-2] = ("b1", ELEMS[-2][1], ELEMS[-2][2], round((b1[2] - b1[0] + 1) / SV * (SH / SH), 1), 14.6)
    # width in slide pt: (fx1-fx0+1)/0.96123... wait mapping: slide_w = frame_w/0.96123
    ELEMS[-2] = ("b1", ELEMS[-2][1], ELEMS[-2][2], round((b1[2] - b1[0] + 1) / 0.96123, 1), 14.6)
if b2:
    ELEMS[-1] = ("b2", ELEMS[-1][1], ELEMS[-1][2], round((b2[2] - b2[0] + 1) / 0.96123, 1), 16.8)

# NotoSans regular for transform fallback
FONTS["NotoSans"] = "/usr/share/fonts/TTF/NotoSans-Regular.ttf"

res = {}
for label, text, cands, tw, th in ELEMS:
    res[label] = {"text": text, "target_w": tw, "target_h": th,
                  "fits": [fit(text, c, tw) for c in cands]}
    print(label, json.dumps(res[label]["fits"]))
print(json.dumps({k: out[k] for k in ["b1_frame", "b1_slide", "b2_frame", "b2_slide", "b1_tail_colprof", "cursor_frame"]}, indent=1))
