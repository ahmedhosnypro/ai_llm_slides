#!/usr/bin/env python3
"""Closed-loop self-check attempt 1: render (2001x1125 @150dpi) vs original frame targets.
Targets in frame px (1px=1pt) scaled by 2000/960. Tolerance ~4px @150dpi (= ~2 frame px)."""
import numpy as np
from PIL import Image
from collections import Counter
import sys

REN = np.asarray(Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/qa/slide019/render_1.png").convert("RGB")).astype(int)
H, W, _ = REN.shape
S = W / 960.0
print(f"render {W}x{H}, scale {S:.4f}")
r, g, b = REN[..., 0], REN[..., 1], REN[..., 2]
lum = (r * 299 + g * 587 + b * 114) // 1000
fails = []

def target(v): return v * S

def check(name, got, want, tol=4.0):
    d = max(abs(g - w) for g, w in zip(got, want)) if got and want else 999
    ok = d <= tol
    print(f" {'OK ' if ok else 'FAIL'} {name}: got {tuple(round(x,1) for x in got)} want {tuple(round(x*S,1) for x in want)} (frame {want}) maxd {d:.1f}")
    if not ok: fails.append(name)

def runs(m, base):
    out, s = [], None
    for i, v in enumerate(m):
        if v and s is None: s = i
        elif not v and s is not None: out.append((base + s, base + i - 1)); s = None
    if s is not None: out.append((base + s, base + len(m) - 1))
    return out

def modal(px, n=3):
    if len(px) == 0: return []
    c = Counter((int(p[0]) // 16 * 16, int(p[1]) // 16 * 16, int(p[2]) // 16 * 16) for p in np.atleast_2d(px))
    return [(f"#{v[0]:02X}{v[1]:02X}{v[2]:02X}", k) for v, k in c.most_common(n)]

def ink_bbox(mask, x0, y0, x1, y1):
    sub = mask[int(y0 * S):int(y1 * S), int(x0 * S):int(x1 * S)]
    ys, xs = np.nonzero(sub)
    if len(xs) == 0: return None
    return (x0 + xs.min() / S, y0 + ys.min() / S, x0 + xs.max() / S, y0 + ys.max() / S, len(xs))

# --- 1. title
red = (r > 120) & (g < 80) & (b < 80)
tb = ink_bbox(red, 100, 60, 900, 92)
print(" title bbox(frame):", tb)
check("title.x0", [tb[0]], [221]); check("title.x1", [tb[2]], [654])
check("title.y0", [tb[1]], [69]); check("title.y1", [tb[3]], [91])

# --- 2. boxes: border strokes at row 250 (frame)
def border_runs(yf, x0f, x1f, thr=215):
    y = int(yf * S)
    return [(a / S, bb / S) for a, bb in runs(lum[y, int(x0f * S):int(x1f * S)] < thr, int(x0f * S))]
print(" input row250 runs:", border_runs(250, 55, 175))
print(" pre row250 runs:", border_runs(250, 185, 300))
print(" extr row250 runs:", border_runs(250, 305, 420))
print(" sel row250 runs:", border_runs(250, 420, 535))
print(" pred row250 runs:", border_runs(250, 645, 745))
# vertical extents via col scans
def border_cols(xf, y0f, y1f, thr=215):
    x = int(xf * S)
    return [(a / S, bb / S) for a, bb in runs(lum[int(y0f * S):int(y1f * S), x] < thr, int(y0f * S))]
print(" input col120 runs:", border_cols(120, 190, 290))
print(" pre col240 runs:", border_cols(240, 190, 290))
print(" classif col580 runs:", border_cols(580, 190, 290))
print(" pred col695 runs:", border_cols(695, 195, 285))
# fills
for nm, (xf, yf) in {"input": (120, 215), "pre": (240, 258), "extr": (360, 260), "sel": (470, 260),
                     "classif": (580, 215), "pred": (695, 220), "verr": (765, 250)}.items():
    x, y = int(xf * S), int(yf * S)
    print(f" fill {nm} @{xf},{yf}:", REN[y, x], " modal", modal(REN[y - 3:y + 3, x - 3:x + 3].reshape(-1, 3), 2))

# --- 3. verr pink extent
pink = (r > 230) & (g > 140) & (g < 215) & (b > 140) & (b < 220) & (r > g + 30)
vb = ink_bbox(pink, 730, 160, 820, 320)
print(" verr pink bbox(frame):", vb)
if vb: check("verr.x0", [vb[0]], [752], 5); check("verr.x1", [vb[2]], [789], 5); check("verr.y0", [vb[1]], [171], 5); check("verr.y1", [vb[3]], [298], 5)

# --- 4. ellipse
dark = lum < 175
eb = ink_bbox(dark, 340, 95, 505, 172)
print(" ellipse dark bbox(frame):", eb)
if eb: check("ellipse.x0", [eb[0]], [342], 5); check("ellipse.x1", [eb[2]], [500], 5); check("ellipse.y0", [eb[1]], [99], 5); check("ellipse.y1", [eb[3]], [159], 5)

# --- 5. arrows at y235
cred = (r > 140) & (g < 80) & (b < 80)
for nm, (x0f, x1f) in {"a1 in->pre": (160, 196), "a2 pre->extr": (280, 320), "a3 extr->sel": (405, 430),
                        "a4 sel->class": (515, 534), "a5 class->pred": (630, 658), "a6 pred->verr": (738, 753),
                        "a7 verr<-samples": (788, 812)}.items():
    y0, y1 = int(228 * S), int(242 * S)
    m = cred[y0:y1, int(x0f * S):int(x1f * S)]
    ys, xs = np.nonzero(m)
    if len(xs):
        print(f" {nm}: x {x0f + xs.min()/S:.1f}..{x0f + xs.max()/S:.1f} y {228 + ys.min()/S:.1f}..{228 + ys.max()/S:.1f} n={len(xs)}")
    else:
        print(f" {nm}: NO INK"); fails.append(nm)

# --- 6. container dashes rows 196/273 + fill + right edge
for yf in (196, 197, 273):
    y = int(yf * S)
    m = cred[y, int(195 * S):int(640 * S)]
    n = int(m.sum())
    rr = runs(m, int(195 * S))
    print(f" container row {yf}: red n={n} extent {(rr[0][0]/S, rr[-1][1]/S) if rr else None} runs {len(rr)}")
print(" container fill @(300,212):", REN[int(212 * S), int(300 * S)], " @(310,250):", REN[int(250 * S), int(310 * S)])
print(" container right-of-classif row235 runs (x630..660):", border_runs(235, 630, 660, 225))

# --- 7. annot box + text
tint = (g > r) & (g >= b) & (lum < 250) & (lum > 200)
ab = ink_bbox(tint, 190, 325, 830, 412)
print(" annot tint bbox(frame):", ab)
if ab: check("annot.x0", [ab[0]], [262], 6); check("annot.x1", [ab[2]], [741], 6); check("annot.y0", [ab[1]], [340], 6); check("annot.y1", [ab[3]], [377], 6)
agrn = (g < 180) & (lum < 190)
l1 = ink_bbox(agrn, 290, 338, 710, 358)
l2 = ink_bbox(agrn, 290, 358, 710, 382)
print(" annot line1(frame):", l1, " line2:", l2)

# --- 8. fans presence
blu = (b > 70) & (b > r + 35) & (b > g + 35)
for nm, (x0f, y0f, x1f, y1f) in {"blue-solid-zone": (110, 130, 200, 210), "blue-dashed-zone": (700, 140, 855, 212),
                                  "green-under-pre": (208, 258, 290, 300), "green-under-classif": (540, 265, 640, 324),
                                  "green-origin-dot": (758, 292, 783, 315)}.items():
    n = int(blu[int(y0f * S):int(y1f * S), int(x0f * S):int(x1f * S)].sum()) if "blue" in nm else 0
    if "blue" in nm:
        print(f" {nm}: blue px {n} bbox", (ink_bbox(blu, x0f, y0f, x1f, y1f)))
    else:
        mm = (g > r + 15) & (g > b + 15) & (lum < 200)
        print(f" {nm}: green px", int(mm[int(y0f * S):int(y1f * S), int(x0f * S):int(x1f * S)].sum()))

# --- 9. pencil
dk = lum < 150
pb = ink_bbox(dk, 235, 198, 292, 240)
print(" pencil ink bbox(frame):", pb)
if pb: check("pencil.x0", [pb[0]], [243], 5); check("pencil.x1", [pb[2]], [283], 5); check("pencil.y0", [pb[1]], [203], 5); check("pencil.y1", [pb[3]], [236], 5)

# --- 10. blue fan extents vs original
bs = ink_bbox(blu, 100, 120, 380, 216)
bd = ink_bbox(blu, 460, 120, 860, 216)
print(" blue solid bbox(frame):", bs, " (orig x115..372 y130..211)")
print(" blue dashed bbox(frame):", bd, " (orig x467..850 y129..211)")

print()
print("FAILS:", fails if fails else "none")
sys.exit(1 if fails else 0)
