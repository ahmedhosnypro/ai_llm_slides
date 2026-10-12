#!/usr/bin/env python3
"""Definitive font-size fit per line from ink HEIGHTS (real Arial glyph bboxes),
baselines, and final box-y calibration. Then print the build constants."""
import numpy as np
from PIL import Image
from fontTools.ttLib import TTFont
from fontTools.pens.boundsPen import BoundsPen

V = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2"
img = np.asarray(Image.open(f"{V}/unique_slides/slide_024.jpg").convert("RGB")).astype(int)

def Sx(fx): return (fx - 17.628) / 0.961231
def Sy(fy): return fy / 0.955556
def Fx(sv): return 17.628 + 0.961231 * sv
PT = 1.046515  # slide pt per frame px (1/0.955556)

reg_f = TTFont("/usr/share/fonts/TTF/Arial.TTF")
bold_f = TTFont("/usr/share/fonts/TTF/Arialbd.TTF")
ita_f = TTFont("/usr/share/fonts/TTF/Ariali.TTF")
bita_f = TTFont("/usr/share/fonts/TTF/Arialbi.TTF")
UPM = reg_f["head"].unitsPerEm

def gbox(font, ch):
    gs = font.getGlyphSet()
    cp = BoundsPen(gs)
    gs[font.getBestCmap()[ord(ch)]].draw(cp)
    return cp.bounds  # (xMin,yMin,xMax,yMax) or None

for ch in "()[\u03b4g":
    b = gbox(reg_f, ch)
    print(f"Arial '{ch}': yMin {b[1]/UPM:.3f} yMax {b[2-2]/UPM:.3f} span {(b[3]-b[1])/UPM:.3f} em" if b else ch)
# fix: bounds = (xMin, yMin, xMax, yMax)
for ch in "()[\u03b4g":
    b = gbox(reg_f, ch)
    if b:
        print(f"Arial '{ch}': yMin {b[1]/UPM:+.3f}  yMax {b[3]/UPM:.3f}  span {(b[3]-b[1])/UPM:.3f}")

def ink_rows(y0, y1, x0, x1):
    reg = img[y0:y1, x0:x1]
    r, g, b = reg[..., 0], reg[..., 1], reg[..., 2]
    ink = ((b > 100) & (b > r + 30)) | ((r > 110) & (r > b + 40) & (g < r - 30))
    rows = np.where(ink.any(axis=1))[0]
    return rows[0] + y0, rows[-1] + y0

# tallest-glyph span per line (real bboxes):
# L1: '[' + ']' (bold?) span; L2: '(' ')'; L3: '[' ']'; L4: '(' ')'; L5: '[' ']'; L6: '(' ')'
print("\nheight fits (bloom -1.2pt on span):")
for tag, y0, y1, x0, x1, gch in (
    ("L1", 363, 386, 79, 640, "[]"), ("L2", 386, 408, 108, 884, "()"),
    ("L3", 408, 431, 78, 740, "[]"), ("L4", 430, 452, 104, 560, "()"),
    ("L5", 452, 474, 79, 884, "[]"), ("L6", 474, 496, 108, 700, "()")):
    fy0, fy1 = ink_rows(y0, y1, x0, x1)
    span_px = fy1 - fy0 + 1
    span_pt = span_px * PT
    b0 = gbox(reg_f, gch[0]); b1 = gbox(reg_f, gch[1])
    sp_em = max(b0[3], b1[3]) / UPM - min(b0[1], b1[1]) / UPM
    em = (span_pt - 1.2) / sp_em
    print(f"{tag}: ink fy {fy0}..{fy1} ({span_px} px = {span_pt:.2f} pt)  glyph '{gch}' span {sp_em:.3f} em  -> E = {em:.2f}")
    # baseline: bracket yMax 0.729?? use real yMax of the top glyph
    ymax_em = max(b0[3], b1[3]) / UPM
    base_slide = Sy(fy0) + 1.2 * 0.5 + ymax_em * em  # bloom half above
    print(f"      baseline (slide) ~ {base_slide:.1f}   ink top slide {Sy(fy0):.1f}")

# per-line width fits with each candidate size (bloom-corrected width)
def inkw(font, s):
    hmtx = font["hmtx"]; cmap = font.getBestCmap(); glyf = font["glyf"]
    gids = [cmap[ord(c)] for c in s]
    total = sum(hmtx[g_][0] for g_ in gids)
    lsb0 = hmtx[gids[0]][1]
    gl = glyf[gids[-1]]
    xMax = gl.xMax if gl.numberOfContours else 0
    rsb = hmtx[gids[-1]][0] - (hmtx[gids[-1]][1] + xMax)
    return (total - lsb0 - rsb) / UPM

L = {
 "L1": "[1] \u03b4 value should be same for Long sequence and short sequence",
 "L2": "(same positions will be encoded with same values irrespective of the length of the sequence)",
 "L3": "[2] Range of position encoded values should NOT depend on sequence length",
 "L4": "(predefined fixed range  e.g. from 0 to 1 , form -1 to 1 , ...)",
 "L5": "[3] Position Encoding  should be a  VECTOR (not scalar) and of same dimension as Word Embedding",
 "L6": "(in order to easily  combine Position Encoding and Word Encoding vectors)",
}
meas_w = {"L1": 546.2, "L2": 724.1, "L3": 660.6, "L4": 446.3, "L5": 831.2, "L6": 584.7}
print("\nwidth cross-check (bloom-corrected meas − 2.0):")
for k, s in L.items():
    w_ita = inkw(ita_f, s)
    w_bita = inkw(bita_f, s)
    print(f"{k}: ita-metrics em {(meas_w[k]-2.0)/w_ita:.2f}   boldita-metrics em {(meas_w[k]-2.0)/w_bita:.2f}")
