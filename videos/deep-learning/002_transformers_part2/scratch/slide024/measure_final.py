#!/usr/bin/env python3
"""Definitive measurements: font size fit (fontTools), bold via ink density,
italic via slant, underline extents, red spans, border colors, subtitle metrics."""
import numpy as np
from PIL import Image
from fontTools.ttLib import TTFont

V = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2"
img = np.asarray(Image.open(f"{V}/unique_slides/slide_024.jpg").convert("RGB")).astype(int)

sx = (899 - 58) / (919.0 - 42.0); a = 58 - sx * 42.0
sy = (516 - 43) / (540.0 - 45.0); b = 43 - sy * 45.0
def Sx(fx): return (fx - a) / sx
def Sy(fy): return (fy - b) / sy
def Fx(sx_): return a + sx * sx_

fonts = {
    "reg": TTFont("/usr/share/fonts/TTF/Arial.TTF"),
    "bold": TTFont("/usr/share/fonts/TTF/Arialbd.TTF"),
    "ita": TTFont("/usr/share/fonts/TTF/Ariali.TTF"),
    "boldita": TTFont("/usr/share/fonts/TTF/Arialbi.TTF"),
}
UPM = fonts["reg"]["head"].unitsPerEm
def adv(font, ch):
    hmtx = font["hmtx"]; cmap = font.getBestCmap()
    gid = cmap[ord(ch)]
    return hmtx[gid][0]

def span_units(font, s):
    """total advance + lsb of first + rsb of last"""
    hmtx = font["hmtx"]; cmap = font.getBestCmap()
    gids = [cmap[ord(c)] for c in s]
    total = sum(hmtx[g][0] for g in gids)
    lsb0 = hmtx[gids[0]][1]
    # rsb of last = advance - (lsb + xMax of glyph bbox)
    glyf = font["glyf"]
    gl = glyf[gids[-1]]
    xMax = gl.xMax if gl.numberOfContours else hmtx[gids[-1]][0] // 2
    rsb = hmtx[gids[-1]][0] - (hmtx[gids[-1]][1] + xMax)
    # ink width approx = total - lsb0 - rsb
    return total, lsb0, rsb

LINES = [
    (363, 386, "L1", "[1] \u03b4 value should be same for Long sequence and short sequence"),
    (386, 408, "L2", "(same positions will be encoded with same values irrespective of the length of the sequence)"),
    (408, 431, "L3", "[2] Range of position encoded values should NOT depend on sequence length"),
    (430, 452, "L4", "(predefined fixed range  e.g. from 0 to 1 , form -1 to 1 , ...)"),
    (452, 474, "L5", "[3] Position Encoding  should be a  VECTOR (not scalar) and of same dimension as Word Embedding"),
    (474, 496, "L6", "(in order to easily  combine Position Encoding and Word Encoding vectors)"),
]
print("== per-line ink span + font-size fit (regular-metric fit) ==")
for y0, y1, tag, s in LINES:
    reg = img[y0:y1, 78:884]
    r, g, bl = reg[..., 0], reg[..., 1], reg[..., 2]
    ink = ((bl > 100) & (bl > r + 30)) | ((r > 110) & (r > bl + 40) & (g < r - 30))
    cols = np.where(ink.any(axis=0))[0]
    fx0, fx1 = cols[0] + 78, cols[-1] + 78
    s0, s1 = Sx(fx0), Sx(fx1)
    total, lsb0, rsb = span_units(fonts["ita"], s)
    em_fit = (s1 - s0) / ((total - lsb0 - rsb) / UPM)
    print(f"{tag}: ink slide {s0:.1f}..{s1:.1f} (w {s1-s0:.1f})  units {total}  em_fit(reg-metrics) {em_fit:.2f}")

print("\n== per-word ink density (bold test) — main lines ==")
def word_runs(y0, y1, gap=4):
    reg = img[y0:y1, 78:884]
    r, g, bl = reg[..., 0], reg[..., 1], reg[..., 2]
    ink = ((bl > 100) & (bl > r + 30)) | ((r > 110) & (r > bl + 40) & (g < r - 30))
    d = np.diff(np.concatenate(([0], ink.any(axis=0).astype(int), [0])))
    starts = np.where(d == 1)[0]; ends = np.where(d == -1)[0]
    runs = []
    for s_, e_ in zip(starts, ends):
        if runs and s_ - runs[-1][1] <= gap: runs[-1][1] = e_
        else: runs.append([s_, e_])
    out = []
    for ws, we in runs:
        sub = ink[:, ws:we + 1]
        cov = sub.sum() / max(1, sub.shape[0] * sub.shape[1])
        rr = reg[:, ws:we + 1]
        redm = (rr[..., 0] > 110) & (rr[..., 0] > rr[..., 2] + 40) & (rr[..., 1] < rr[..., 0] - 30)
        col = "R" if redm.sum() > sub.sum() * 0.5 else "B"
        out.append((Sx(ws + 78), Sx(we + 78), cov, col, int(sub.sum())))
    return out

for y0, y1, tag, s in (LINES[0], LINES[2], LINES[4]):
    print(f"{tag}:")
    for x0, x1, cov, col, npx in word_runs(y0, y1):
        print(f"   {col} {x0:6.1f}..{x1:6.1f} w {x1-x0:5.1f}  coverage {cov:.2f}  px {npx}")

print("\n== paren slant test (italic?) L2 '(' and L6 '(' ==")
for y0, y1, x0, x1, tag in ((386, 408, 95, 118, "L2 paren"), (474, 496, 95, 118, "L6 paren"), (363, 386, 60, 90, "L1 bracket")):
    reg = img[y0:y1, x0:x1]
    r, g, bl = reg[..., 0], reg[..., 1], reg[..., 2]
    ink = ((bl > 100) & (bl > r + 30)) | ((r > 110) & (r > bl + 40) & (g < r - 30))
    rows = []
    for yy in range(reg.shape[0]):
        cs = np.where(ink[yy])[0]
        if len(cs): rows.append((y0 + yy, cs.mean() + x0, cs[0] + x0, cs[-1] + x0))
    if rows:
        top = rows[:3]; bot = rows[-3:]
        print(f"{tag}: top rows {[(t[0], round(t[1],1)) for t in top]}  bottom rows {[(t[0], round(t[1],1)) for t in bot]}")

print("\n== underline full scan (dedicated rows below baseline) ==")
def underline_scan(y_lo, y_hi, tag):
    reg = img[y_lo:y_hi, 78:884]
    r, g, bl = reg[..., 0], reg[..., 1], reg[..., 2]
    blue = (bl > 90) & (bl > r + 25)
    best = {}
    for yy in range(reg.shape[0]):
        d = np.diff(np.concatenate(([0], blue[yy].astype(int), [0])))
        starts = np.where(d == 1)[0]; ends = np.where(d == -1)[0]
        for s_, e_ in zip(starts, ends):
            if e_ - s_ >= 30:
                key = y_lo + yy
                best.setdefault(key, []).append((s_ + 78, e_ + 78 - 1))
    print(f"{tag}:")
    for k in sorted(best):
        runs = best[k]
        print(f"   row {k} (slide y {Sy(k):.1f}): " + ", ".join(f"fx {s_}..{e_} (slide {Sx(s_):.1f}..{Sx(e_):.1f})" for s_, e_ in runs))

underline_scan(399, 407, "L2 underline rows")
underline_scan(465, 474, "L5 underline rows")
underline_scan(379, 388, "L1 underline rows (expect none)")
underline_scan(421, 431, "L3 underline rows (expect none)")
underline_scan(443, 452, "L4 underline rows (expect none)")
underline_scan(487, 496, "L6 underline rows (expect none)")

print("\n== red spans per main line (slide coords) ==")
for y0, y1, tag, s in (LINES[0], LINES[2], LINES[4]):
    reg = img[y0:y1, 78:884]
    r, g, bl = reg[..., 0], reg[..., 1], reg[..., 2]
    red = (r > 110) & (r > bl + 40) & (g < r - 30)
    cols = np.where(red.any(axis=0))[0]
    if len(cols):
        # contiguous red groups
        groups = []
        st = cols[0]; prev = cols[0]
        for c in cols[1:]:
            if c - prev > 8:
                groups.append((st, prev)); st = c
            prev = c
        groups.append((st, prev))
        print(f"{tag}: " + ", ".join(f"slide {Sx(g0+78):.1f}..{Sx(g1+78):.1f}" for g0, g1 in groups))

print("\n== box border colors (darkest cores) ==")
# bottom border row 502, top 348, left 74-75, right 886
for y_, x0_, x1_, tag in ((348, 200, 700, "top"), (502, 200, 700, "bottom")):
    row = img[y_, x0_:x1_]
    dark = row[row[..., 2] < 180]
    if len(dark): print(f"{tag} border mean of dark px: {dark.mean(axis=0).round(1)} n={len(dark)}")
for x_, y0_, y1_, tag in ((74, 380, 490, "left"), (886, 380, 490, "right")):
    colm = img[y0_:y1_, x_]
    dark = colm[colm[..., 2] < 180]
    if len(dark): print(f"{tag} border mean of dark px: {dark.mean(axis=0).round(1)} n={len(dark)}")
# fill census inside box, away from text: rows 352..360, 470..490 cols 100..800
reg = img[352:362, 100:800].reshape(-1, 3)
print("fill census (rows 352..361):", np.median(reg, axis=0))
reg = img[470:492, 100:800].reshape(-1, 3)
print("fill census (rows 470..491):", np.median(reg, axis=0))

print("\n== subtitle ==")
reg = img[78:112, 250:800]
r, g, bl = reg[..., 0], reg[..., 1], reg[..., 2]
blue = (bl > 100) & (bl > r + 40)
yel = (r > 225) & (g > 225) & (bl < 200)
bx = np.where(blue.any(axis=0))[0]; by = np.where(blue.any(axis=1))[0]
print(f"blue ink slide x {Sx(bx[0]+250):.1f}..{Sx(bx[-1]+250):.1f} y {Sy(by[0]+78):.1f}..{Sy(by[-1]+78):.1f}")
s = "(Rules Controlling Good Positional Encoder)"
total, lsb0, rsb = span_units(fonts["bold"], s)
print(f"bold-metrics em fit: {(Sx(bx[-1]+250)-Sx(bx[0]+250))/((total-lsb0-rsb)/UPM):.2f}")
total, lsb0, rsb = span_units(fonts["reg"], s)
print(f"reg-metrics em fit:  {(Sx(bx[-1]+250)-Sx(bx[0]+250))/((total-lsb0-rsb)/UPM):.2f}")
yx = np.where(yel.any(axis=0))[0]; yy = np.where(yel.any(axis=1))[0]
print(f"yellow strip slide x {Sx(yx[0]+250):.1f}..{Sx(yx[-1]+250):.1f} y {Sy(yy[0]+78):.1f}..{Sy(yy[-1]+78):.1f}")
ypix = img[78:112, 250:800][yel]
print("yellow census mean:", ypix.mean(axis=0).round(1), "median:", np.median(ypix, axis=0))
bpix = img[78:112, 250:800][blue]
print("blue ink census darkest mean:", bpix[bpix[:,2] < np.percentile(bpix[:,2], 30)].mean(axis=0).round(1))
