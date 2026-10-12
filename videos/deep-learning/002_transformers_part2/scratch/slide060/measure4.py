#!/usr/bin/env python3
"""Pass 4: per-line detail (bbox, row profiles, run boundaries), title bbox, cursor scan,
citation cores, underline rows, badge numeral, Arial advance font fitting."""
from PIL import Image, ImageFont
import glob
from collections import Counter

S060 = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_060.jpg"
img = Image.open(S060).convert("RGB")
W, H = img.size
px = img.load()

FX0, SX, SY = 18.63, 0.96123, 0.95556
def TX(fx): return (fx - FX0) / SX
def TY(fy): return fy / SY

def reddish(p):
    r, g, b = p
    return r > 110 and (r - g) > 45 and (r - b) > 35

def blueish(p):
    r, g, b = p
    return b > 100 and (b - r) > 35 and (b - g) > 25

fonts = {}
for pat, key in (("**/Arialbd.TTF", "b"), ("**/Arial.TTF", "r"), ("**/Ariali.TTF", "i"), ("**/Arialbi.TTF", "bi")):
    c = glob.glob("/usr/share/fonts/" + pat, recursive=True)
    if c:
        fonts[key] = c[0]
print("fonts:", fonts)

def em_for(text, target_pt, key, size=300):
    f = ImageFont.truetype(fonts[key], size)
    return target_pt / (f.getlength(text) / size)

# ---- title bbox
xs, ys = [], []
for y in range(55, 112):
    for x in range(60, 900):
        if reddish(px[x, y]):
            xs.append(x); ys.append(y)
print(f"TITLE bbox frame x {min(xs)}..{max(xs)} y {min(ys)}..{max(ys)} -> "
      f"slide x {TX(min(xs)):.1f}..{TX(max(xs)+1):.1f} (w {TX(max(xs)+1)-TX(min(xs)):.1f}) "
      f"y {TY(min(ys)):.1f}..{TY(max(ys)+1):.1f}")
title_w = TX(max(xs) + 1) - TX(min(xs))
print("title em (Arial Bold):", round(em_for("What is Next  (as of 2020)", title_w, "b"), 2))
# row profile
prof = {y: sum(1 for x in range(60, 900) if reddish(px[x, y])) for y in range(min(ys), max(ys) + 1)}
print("title rows:", {y: n for y, n in prof.items() if n > 0})

# ---- bands (from measure3) with row profiles and run boundaries
bands = [
    ("E1", 146, 163), ("C1", 169, 184), ("E2", 210, 227), ("C2", 233, 249),
    ("E3", 275, 309), ("E4", 334, 370), ("E5", 396, 413), ("E6", 439, 455),
]
for name, y0, y1 in bands:
    print(f"== {name} fy {y0}..{y1}")
    rows = []
    for y in range(y0, y1 + 1):
        b = sum(1 for x in range(83, 877) if blueish(px[x, y]))
        r = sum(1 for x in range(83, 877) if reddish(px[x, y]))
        rows.append((y, b, r))
    print("  rows:", [(y, b, r) for y, b, r in rows])
    # column classes
    bcols, rcols = set(), set()
    for x in range(83, 877):
        nb = sum(1 for y in range(y0, y1 + 1) if blueish(px[x, y]))
        nr = sum(1 for y in range(y0, y1 + 1) if reddish(px[x, y]))
        if nb >= 2: bcols.add(x)
        if nr >= 2: rcols.add(x)
    if rcols:
        print(f"  blue cols {min(bcols)}..{max(bcols)}  red cols {min(rcols)}..{max(rcols)}  "
              f"(blue-only right edge {max(c for c in bcols if c < min(rcols)) if any(c < min(rcols) for c in bcols) else None})")
    else:
        print(f"  blue cols {min(bcols)}..{max(bcols)} (no red)")
    # saturated cores
    cc = Counter()
    for y in range(y0, y1 + 1):
        for x in range(83, 877):
            p = px[x, y]
            if blueish(p) and (p[2] - p[0]) > 100:
                cc[p] += 1
    print("  saturated blue cores:", cc.most_common(5))
    rr = Counter()
    for y in range(y0, y1 + 1):
        for x in range(83, 877):
            p = px[x, y]
            if reddish(p) and p[0] < 210 and (p[0] - p[2]) > 80:
                rr[p] += 1
    print("  dark red cores:", rr.most_common(5))

# ---- cursor artifact scan: black or white-with-dark-border blobs in box interior
print("== dark px (sum<260) in box interior x 84..876 y 120..480 ==")
darks = [(x, y) for y in range(120, 480) for x in range(84, 877) if sum(px[x, y]) < 260]
print(len(darks), darks[:30])
if darks:
    print("bbox:", min(p[0] for p in darks), min(p[1] for p in darks), max(p[0] for p in darks), max(p[1] for p in darks))

# ---- fit sizes for all lines
print("== font fits (ink widths in slide pt) ==")
def line_w(fx0, fx1): return TX(fx1 + 1) - TX(fx0)

fits = [
    ("E1 full bold", "GPT-1 and GPT-2 (Generative Pre-trained Transformers)", 89, 593, "b"),
    ("E2 full bold", "BERT (Bidirectional Encoder Representations from Transformers)", 90, 686, "b"),
    ("E3 full bold", "RoBERTa (Robustly Optimized BERT Approach)", 89, 524, "b"),
    ("E4 full boldit", "Transformer-XL: Attentive Language ModelsBeyond a Fixed-Length Context", 91, 781, "bi"),
    ("E5 full bold", "T5 (Text-to-Text Transfer Transformer)", 89, 432, "b"),
    ("E6 full bold", "GPT-3  (175 Billion Parameter, Beta Release June 2020)", 89, 592, "b"),
    ("C1 ital", "Radford et al., OpenAI. June 2018 and February 2019.", 128, 532, "i"),
    ("C2 ital", "Devlin et al., Google AI Language. May 2019.", 128, 464, "i"),
    ("C3 ital", "Liu et al., Facebook AI. June 2019.", 128, 401, "i"),
    ("C4 ital", "Zhang Dai et al. Carnegie Mellon University and Google Brain", 128, 655, "i"),
]
for label, text, fx0, fx1, key in fits:
    w = line_w(fx0, fx1)
    print(f"{label:16s} ink {fx0}..{fx1} slide w {w:6.1f} -> em {em_for(text, w, key):5.2f}")
