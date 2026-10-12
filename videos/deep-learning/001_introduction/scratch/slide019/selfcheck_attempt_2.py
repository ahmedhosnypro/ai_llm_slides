#!/usr/bin/env python3
"""Focused re-verify attempt 2: annot text, title, chain text bands/pitch, container
dashes, verr (clean row), pencil (clean window), blue dashed start."""
import numpy as np
from PIL import Image
import sys
from collections import Counter

REN = np.asarray(Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/qa/slide019/render_2.png").convert("RGB")).astype(int)
W = REN.shape[1]; S = W / 960.0
r, g, b = REN[..., 0], REN[..., 1], REN[..., 2]
lum = (r * 299 + g * 587 + b * 114) // 1000
fails = []

def runs(m, base):
    out, s = [], None
    for i, v in enumerate(m):
        if v and s is None: s = i
        elif not v and s is not None: out.append((base + s, base + i - 1)); s = None
    if s is not None: out.append((base + s, base + len(m) - 1))
    return out

def check(name, got, want, tol=4.0):
    d = max(abs(x - w) for x, w in zip(got, want))
    ok = d <= tol
    print(f" {'OK ' if ok else 'FAIL'} {name}: got {tuple(round(x,1) for x in got)} want {tuple(w*S and w or w for w in want)}[frame] maxd {d:.1f}")
    if not ok: fails.append(name)

def ink_bbox(mask, x0, y0, x1, y1):
    sub = mask[int(y0 * S):int(y1 * S), int(x0 * S):int(x1 * S)]
    ys, xs = np.nonzero(sub)
    if len(xs) == 0: return None
    return (x0 + xs.min() / S, y0 + ys.min() / S, x0 + xs.max() / S, y0 + ys.max() / S, len(xs))

print("== TITLE ==")
red = (r > 120) & (g < 80) & (b < 80)
tb = ink_bbox(red, 100, 60, 900, 92)
print(" title ink(frame):", tb, "| orig x221..654 y69..91 center 437.5")
check("title.x0", [tb[0]], [221]); check("title.x1", [tb[2]], [654]); check("title.y0", [tb[1]], [69]); check("title.y1", [tb[3]], [91])

print("== ANNOT TEXT (dark-green ink, lum<190, g<r+15 window) ==")
agrn = (g < 185) & (lum < 195)
l1 = ink_bbox(agrn, 290, 338, 710, 359)
l2 = ink_bbox(agrn, 290, 359, 710, 384)
print(" line1(frame):", l1, "| orig x305..697 y343..356")
print(" line2(frame):", l2, "| orig x302..699 y361..374")
check("annot.l1.x0", [l1[0]], [305], 6); check("annot.l1.x1", [l1[2]], [697], 6)
check("annot.l1.y0", [l1[1]], [343], 4); check("annot.l1.y1", [l1[3]], [356], 4)
check("annot.l2.x0", [l2[0]], [302], 6); check("annot.l2.x1", [l2[2]], [699], 6)
check("annot.l2.y0", [l2[1]], [361], 4); check("annot.l2.y1", [l2[3]], [374], 4)

print("== CHAIN TEXT BANDS per box (lum<140, inside box, excluding borders/pencil) ==")
def bands(x0f, y0f, x1f, y1f, label, thr=140):
    x0, y0, x1, y1 = int(x0f * S), int(y0f * S), int(x1f * S), int(y1f * S)
    m = lum[y0:y1, x0:x1] < thr
    rows = np.nonzero(m.any(axis=1))[0] + y0
    if not len(rows): print(f" {label}: none"); return
    br, s = [], rows[0]
    for a, bb in zip(rows, rows[1:]):
        if bb - a > 2: br.append((s, a)); s = bb
    br.append((s, rows[-1]))
    cols = np.nonzero(m.any(axis=0))[0] + x0
    print(f" {label}: bands(frame) {[(round(a/S,1), round(bb/S,1)) for a,bb in br]} cols(frame) {round(cols.min()/S,1)}..{round(cols.max()/S,1)}")
    return br, (cols.min()/S, cols.max()/S)

# input: text zone y214..258 x84..158 (orig lines 222..235 / 238..250, cols 84..153)
bands(84, 214, 158, 260, "input")
bands(812, 214, 880, 260, "samples")
bands(200, 234, 278, 254, "pre-line2")     # orig line2 239..248 cols 210..276
bands(322, 214, 402, 258, "extr")          # orig lines 222..231/238..246
bands(432, 214, 508, 258, "sel")           # orig 223..231/237..246
bands(660, 214, 736, 258, "pred")          # orig 222..232/238..247
bands(540, 226, 624, 244, "classif-white")

print("== VERR pink at clean row y200 (no arrows) ==")
pink = (r > 230) & (g > 140) & (g < 215) & (b > 140) & (b < 220) & (r > g + 30)
print(" row200 pink runs(frame):", [(round(a/S,1), round(bb/S,1)) for a, bb in runs(pink[int(200*S), int(730*S):int(830*S)], 0)])
vr = runs(pink[int(200*S), int(730*S):int(830*S)], 0)
if vr: check("verr.x0@200", [vr[0][0]/S], [752], 5); check("verr.x1@200", [vr[-1][1]/S], [789], 5)
print(" verr text ink(frame):", ink_bbox((r > 140) & (g < 95) & (b < 95) & (lum < 150), 760, 175, 800, 300), "| orig x774..786 y183..286")

print("== PENCIL clean window (y198..219, above text) ==")
dk = lum < 150
pb = ink_bbox(dk, 235, 198, 292, 219)
print(" pencil bar bbox(frame):", pb, "| orig bar x243..280 y205..207")

print("== CONTAINER dashes rows profile (x195..530, outside classif) ==")
cred = (r > 140) & (g < 80) & (b < 80)
for yf in range(194, 200):
    y = int(yf * S)
    m = cred[y, int(195 * S):int(531 * S)]
    n = int(m.sum()); rr = runs(m, int(195 * S))
    print(f" row {yf}: n={n} extent {(round(rr[0][0]/S,1), round(rr[-1][1]/S,1)) if rr else None} runs {len(rr)}")
for yf in range(271, 277):
    y = int(yf * S)
    m = cred[y, int(195 * S):int(531 * S)]
    n = int(m.sum()); rr = runs(m, int(195 * S))
    print(f" row {yf}: n={n} extent {(round(rr[0][0]/S,1), round(rr[-1][1]/S,1)) if rr else None} runs {len(rr)}")
# left/right dash columns
for xf in (193, 194, 195, 628, 629, 630, 631):
    x = int(xf * S)
    m = cred[int(200 * S):int(270 * S), x]
    print(f" col {xf}: red n={int(m.sum())}")

print("== BLUE dashed start (over ellipse now?) ==")
blu = (b > 70) & (b > r + 35) & (b > g + 35)
print(" dashed zone bbox(frame):", ink_bbox(blu, 460, 120, 860, 216), "| orig x467..850 y129..211")

print()
print("FAILS:", fails if fails else "none")
sys.exit(0)
