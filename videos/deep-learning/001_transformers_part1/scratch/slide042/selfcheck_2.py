#!/usr/bin/env python3
"""Closed-loop self-check, attempt 2 (render_2.png) — resume after attempt 1's
judge never landed. Same masks as selfcheck_1.py. Two differences, both
evidence-based (scratch/slide042/forensics_resume.py, 2026-10-12):
  * blue bands separated by <=3 rows are MERGED — the original's L5 'g' descender
    forms its own 448-451 band (orig L6) that attempt-1's want treated as absent;
  * L5 want bottom is therefore 451 (merged), right stays 849.
All other wants unchanged from selfcheck_1.py. Extra fix-verification probes for
the two attempt-2 build fixes (L2 separator 2 ' , '; L5 final ' dimension.'
un-bolded) printed at the end."""
import numpy as np
from PIL import Image

VID = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1"
ORIG = f"{VID}/unique_slides/slide_042.jpg"
REND = f"{VID}/recreated_pptx/qa/slide042/render_2.png"

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
S = rend.shape[0] / 540.0
W = rend.shape[1]

fails = []
def check(name, got, want, tol=5.0):
    d = max(abs(a - w) for a, w in zip(got, want)) if isinstance(got, (list, tuple)) else abs(got - want)
    status = "OK " if d <= tol else "FAIL"
    print(f"  [{status}] {name}: got {got} want {want} (maxdiff {d:.1f}, tol {tol})")
    if d > tol:
        fails.append(name)

def merged_bands(mask, y0f, y1f, scale, minpx=3, merge_gap=3, x0f=None, x1f=None):
    a0, a1 = int(y0f * scale), int(y1f * scale)
    m = mask[a0:a1]
    if x0f is not None:
        m = m[:, int(x0f * scale):int(x1f * scale)]
    rows = np.where(m.sum(axis=1) > minpx)[0] + a0
    out, s, p = [], rows[0], rows[0]
    for i in rows[1:]:
        if i <= p + merge_gap:
            p = i
        else:
            out.append((s, p)); s = p = i
    out.append((s, p))
    return [(a / scale, b / scale) for a, b in out]

def band_bbox(mask, band, scale, x0f=None, x1f=None):
    a, b = int(band[0] * scale), int(band[1] * scale) + 1
    m = mask[a:b]
    off = 0
    if x0f is not None:
        off = int(x0f * scale)
        m = m[:, off:int(x1f * scale)]
    xs = np.where(m.sum(axis=0) > 0)[0]
    return ((xs.min() + off) / scale, (xs.max() + off) / scale)

print("== title (want ink x299-663 y81-103 frame px) ==")
tb = merged_bands(Mr["red"], 55, 130, S, merge_gap=2, x0f=60, x1f=900)
tbx = band_bbox(Mr["red"], tb[0], S, 60, 900) if tb else None
if tbx:
    check("title bbox (x0,x1,y0,y1)", [tbx[0], tbx[1], tb[0][0], tb[0][1]], [299, 663, 81, 103], tol=5)
else:
    fails.append("title missing")

print("== subtitle (want L1 x108-832 ytop~151-152; L2 x359-581 ytop~174) ==")
sb = merged_bands(Mr["red"], 135, 193, S, merge_gap=2, x0f=60, x1f=880)
if len(sb) >= 2:
    s1x = band_bbox(Mr["red"], sb[0], S, 60, 880); s2x = band_bbox(Mr["red"], sb[1], S, 60, 880)
    check("sub L1 (x0,x1,y0)", [s1x[0], s1x[1], sb[0][0]], [108, 832, 151.5], tol=5)
    check("sub L2 (x0,x1,y0)", [s2x[0], s2x[1], sb[1][0]], [359, 581, 174], tol=5)
else:
    fails.append("subtitle bands missing")

print("== content box borders (want x 71..880, ytop 196, ybot 483) ==")
red = Mr["red"]
tops = [y for y in range(int(180 * S), int(220 * S)) if red[y, int(100*S):int(850*S)].sum() > 500]
bots = [y for y in range(int(470 * S), int(500 * S)) if red[y, int(100*S):int(850*S)].sum() > 500]
if tops: check("box top border row", tops[0] / S, 196, tol=5)
else: fails.append("box top border missing")
if bots: check("box bottom border row", bots[-1] / S, 483, tol=5)
else: fails.append("box bottom border missing")
mid = slice(int(300 * S), int(310 * S))
lc = [x for x in range(int(60 * S), int(90 * S)) if red[mid, x].sum() >= 8]
rc = [x for x in range(int(860 * S), int(900 * S)) if red[mid, x].sum() >= 8]
if lc: check("box left border col", lc[0] / S, 71, tol=5)
else: fails.append("box left border missing")
if rc: check("box right border col", rc[-1] / S, 880, tol=5)
else: fails.append("box right border missing")

print("== body lines (blue; want tops 234/286/346/398/428+desc->451, left 82) ==")
rb = merged_bands(Mr["blue"], 210, 470, S)
print(f"  found {len(rb)} blue bands: {[(round(a,1), round(b,1)) for a, b in rb]}")
want = [(234, 251, 82, 400), (286, 303, 82, 610), (346, 367, 82, 827), (398, 419, 82, 770), (428, 451, 82, 849)]
for i, (b0, b1) in enumerate(rb[:6]):
    l, r = band_bbox(Mr["blue"], (b0, b1), S)
    got = [b0, b1, l, r]
    if i < len(want):
        check(f"L{i+1} (top,bot,left,right)", got, list(want[i]), tol=6)
    else:
        print(f"  extra band {i+1}: {got}")

print("== green subscripts line 2 (want bbox x 464..599) ==")
g2 = Mr["green"][int(282 * S):int(316 * S), int(60 * S):int(700 * S)]
ys, xs = np.where(g2)
if len(ys):
    check("green line2 bbox (x0,x1)", [(xs.min() + int(60*S)) / S, (xs.max() + int(60*S)) / S], [464, 599], tol=6)
else:
    fails.append("green subscripts missing")

print("== red math runs ==")
inside = np.zeros(rend.shape[:2], bool); inside[int(200 * S):int(480 * S), int(78 * S):int(872 * S)] = True
redin = Mr["red"] & inside
for y0, y1, want_x, lbl in [
    (230, 255, (386, 393), "L1 red r"),
    (280, 310, (458, 589), "L2 red sups span"),
    (340, 370, (186, 821), "L3 red X..Yr"),
    (425, 450, (710, 723), "L4 red X"),
]:
    m = redin[int(y0 * S):int(y1 * S)]
    ys, xs = np.where(m)
    if len(ys):
        check(f"{lbl} (x0,x1)", [xs.min() / S, xs.max() / S], list(want_x), tol=7)
    else:
        fails.append(f"{lbl} missing")

print("== color cores ==")
def core_color(y0, y1, x0, x1, mask):
    m = mask[int(y0 * S):int(y1 * S), int(x0 * S):int(x1 * S)]
    return np.median(rend[int(y0 * S):int(y1 * S), int(x0 * S):int(x1 * S)][m], axis=0)
print("  title core:", core_color(60, 120, 250, 700, Mr["red"]), "(want ~C00000)")
print("  body core:", core_color(230, 255, 80, 420, Mr["blue"]), "(want ~0000CC)")

print()
print("== attempt-2 fix verification (probes, informational) ==")
def col_clusters(mask, y0, y1, scale, x0, x1, gap=2.2):
    m = mask[int(y0*scale):int(y1*scale), int(x0*scale):int(x1*scale)]
    cols = np.where(m.sum(axis=0) > 0)[0]
    if not len(cols): return []
    runs, s, p = [], cols[0], cols[0]
    for x in cols[1:]:
        if x <= p + gap * scale: p = x
        else: runs.append((s/scale + x0, p/scale + x0)); s = p = x
    runs.append((s/scale + x0, p/scale + x0))
    return [(round(u, 1), round(v, 1)) for u, v in runs]
print("  L2 comma2 zone x539-562 (orig comma ~555, W3 ~561):")
print("   rend:", col_clusters(Mr["blue"], 288, 308, S, 539, 562))
print("  L2 period zone x590-620 (orig ~608-610):")
print("   rend:", col_clusters(Mr["blue"], 292, 306, S, 590, 620))
print("  L5 final word zone x730-865 (orig letters->~841, period ~846-850):")
print("   rend:", col_clusters(Mr["blue"], 426, 453, S, 730, 865))

print()
if fails:
    print("SELF-CHECK GEOMETRY: FAIL ->", fails)
else:
    print("SELF-CHECK GEOMETRY: ALL OK")
