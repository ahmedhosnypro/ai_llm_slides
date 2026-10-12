#!/usr/bin/env python3
"""Resume forensics for slide 042 attempt-1 self-check FAILs.

Same masks as selfcheck_1.py, applied to BOTH the original frame (960x540,
1px=1pt) and render_1.png (2001x1125). Goals:
  1. Reproduce the selfcheck 'want' values from the original (threshold parity).
  2. L5: word-level x-projection -> which words are wider in the render (bold?).
  3. L5/L2 bottom overhangs: which x-columns hold ink below the want bottom
     (descender/comma-tail artifact vs whole-band shift).
  4. L2: group-by-group positions (W / red sup / green sub) render vs original.
"""
import numpy as np
from PIL import Image

VID = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1"
ORIG = f"{VID}/unique_slides/slide_042.jpg"
REND = f"{VID}/recreated_pptx/qa/slide042/render_1.png"

def masks(im):
    r, g, b = im[:, :, 0].astype(int), im[:, :, 1].astype(int), im[:, :, 2].astype(int)
    return {
        "red": (r - g > 60) & (r - b > 60) & (r > 110),
        "blue": (b - r > 50) & (b - g > 30),
        "green": (g - r > 40) & (g - b > 40) & (g > 90),
    }

orig = np.asarray(Image.open(ORIG).convert("RGB"))
rend = np.asarray(Image.open(REND).convert("RGB"))
Mo, Mr = masks(orig), masks(rend)
S = rend.shape[0] / 540.0  # render px per frame px

def bands(mask, y0f, y1f, scale, minpx=3):
    rows = np.where(mask[int(y0f * scale):int(y1f * scale)].sum(axis=1) > minpx)[0] + int(y0f * scale)
    out, s, p = [], rows[0], rows[0]
    for i in rows[1:]:
        if i == p + 1:
            p = i
        else:
            out.append((s, p)); s = p = i
    out.append((s, p))
    return [(a / scale, b / scale) for a, b in out]

def band_bbox(mask, band, scale):
    a, b = int(band[0] * scale), int(band[1] * scale) + 1
    m = mask[a:b]
    xs = np.where(m.sum(axis=0) > 0)[0]
    return (xs.min() / scale, xs.max() / scale)

def words(mask, band, scale, gap_pt=3.0):
    """Word runs inside a band: columns with ink, split on gaps > gap_pt frame px."""
    a, b = int(band[0] * scale), int(band[1] * scale) + 1
    colink = mask[a:b].sum(axis=0) > 0
    gap = int(round(gap_pt * scale))
    runs, s = [], None
    zero = 0
    for x in range(len(colink)):
        if colink[x]:
            if s is None:
                s = x
            zero = 0
        elif s is not None:
            zero += 1
            if zero > gap:
                runs.append((s / scale, (x - zero) / scale))
                s = None
                zero = 0
    if s is not None:
        runs.append((s / scale, (len(colink) - 1) / scale))
    return runs

print("=== 1. reproduce wants from ORIGINAL (same masks) ===")
ob = bands(Mo["blue"], 210, 470, 1.0)
print(" orig blue bands (top,bot):", [(round(a, 1), round(b, 1)) for a, b in ob])
for i, (a, b) in enumerate(ob[:6]):
    l, r = band_bbox(Mo["blue"], (a, b), 1.0)
    print(f"  orig L{i+1}: top {a:.1f} bot {b:.1f} left {l:.1f} right {r:.1f}")

print()
print("=== 2. L5 word-level comparison (frame px) ===")
# render blue bands
rb = bands(Mr["blue"], 210, 470, S)
print(" render blue bands:", [(round(a, 1), round(b, 1)) for a, b in rb])
# L5 = last band; L4 = second-to-last (wrapped box)
band_o_l5 = ob[-1]
band_r_l5 = rb[-1]
wo = words(Mo["blue"], band_o_l5, 1.0)
wr = words(Mr["blue"], band_r_l5, S)
print(f" orig L5 words ({len(wo)}):", [(round(a, 1), round(b, 1), round(b - a, 1)) for a, b in wo])
print(f" rend L5 words ({len(wr)}):", [(round(a, 1), round(b, 1), round(b - a, 1)) for a, b in wr])

print()
print("=== 3. bottom-overhang forensics ===")
def below_ink(mask, band, scale, ybot_want):
    """columns with ink below ybot_want inside the band (frame px)."""
    y0 = int((ybot_want + 0.5) * scale)
    y1 = int((band[1] + 1) * scale)
    m = mask[y0:y1]
    xs = np.where(m.sum(axis=0) > 0)[0]
    if not len(xs):
        return None
    # cluster columns
    runs, s, p = [], xs[0], xs[0]
    for x in xs[1:]:
        if x <= p + int(2 * scale):
            p = x
        else:
            runs.append((s / scale, p / scale)); s = p = x
    runs.append((s / scale, p / scale))
    return runs

print(" L2 orig band", [round(v, 1) for v in ob[1]], "ink below y=303.5:",
      below_ink(Mo["blue"], ob[1], 1.0, 303))
print(" L2 rend band", [round(v, 1) for v in rb[1]], "ink below y=303.5:",
      below_ink(Mr["blue"], rb[1], S, 303))
print(" L5 orig band", [round(v, 1) for v in band_o_l5], "ink below y=446.5:",
      below_ink(Mo["blue"], band_o_l5, 1.0, 446))
print(" L5 rend band", [round(v, 1) for v in band_r_l5], "ink below y=446.5:",
      below_ink(Mr["blue"], band_r_l5, S, 446))

print()
print("=== 4. L2 group positions (W runs are wide blue; red sups; green subs) ===")
for name, M, sc in [("orig", Mo, 1.0), ("rend", Mr, S)]:
    b2 = bands(M["blue"], 280, 312, sc)
    if not b2:
        print(f" {name}: no L2 band"); continue
    b2 = b2[0]
    w = words(M["blue"], b2, sc, gap_pt=2.5)
    # wide runs = W glyphs (bold W ~ 20-24pt wide); small runs = letters/commas
    wide = [(round(a, 1), round(b, 1)) for a, b in w if b - a > 14]
    reds = []
    a, b = int((b2[0] - 6) * sc), int((b2[1] + 12) * sc)
    m = M["red"][a:b]
    xs = np.where(m.sum(axis=0) > 0)[0]
    if len(xs):
        runs, s, p = [], xs[0], xs[0]
        for x in xs[1:]:
            if x <= p + int(2.5 * sc):
                p = x
            else:
                runs.append((s / sc, p / sc)); s = p = x
        runs.append((s / sc, p / sc))
        reds = [(round(u, 1), round(v, 1)) for u, v in runs]
    grn = []
    a, b = int(282 * sc), int(316 * sc)
    m = M["green"][a:b]
    xs = np.where(m.sum(axis=0) > 0)[0]
    if len(xs):
        runs, s, p = [], xs[0], xs[0]
        for x in xs[1:]:
            if x <= p + int(2.5 * sc):
                p = x
            else:
                runs.append((s / sc, p / sc)); s = p = x
        runs.append((s / sc, p / sc))
        grn = [(round(u, 1), round(v, 1)) for u, v in runs]
    print(f" {name} L2: W-runs {wide}")
    print(f" {name} L2: red-sups {reds}")
    print(f" {name} L2: green-subs {grn}")
