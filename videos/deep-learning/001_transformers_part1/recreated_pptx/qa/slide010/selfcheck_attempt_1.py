#!/usr/bin/env python3
"""Self-check attempt 1 (v2) — render ink vs FRAME ink in matched windows.

For each named region: measure the ink bbox in BOTH the render (150dpi) and the
original frame (960x540), scale the frame bbox to render space, compare (tol 8
render px = ~4 frame px). Also: fills, containment strips, bar edges, underline.
"""
from PIL import Image
import numpy as np

R = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/qa/slide010/render_1.png"
F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_010.jpg"
r = np.asarray(Image.open(R).convert("RGB")).astype(int)
f = np.asarray(Image.open(F).convert("RGB")).astype(int)
SC = r.shape[0] / 540.0
fails, notes = [], []

def ink_bbox(a, x0, y0, x1, y1, thr=560, scaled=True):
    k = SC if scaled else 1.0
    win = a[int(y0*k):int(np.ceil(y1*k)), int(x0*k):int(np.ceil(x1*k))]
    m = win.sum(axis=2) < thr
    if not m.any():
        return None
    ys, xs = np.where(m)
    return (x0 + xs.min()/k, y0 + ys.min()/k, x0 + (xs.max()+1)/k, y0 + (ys.max()+1)/k)

def cmp_ink(name, x0, y0, x1, y1, tol=4.0):
    fr = ink_bbox(f, x0, y0, x1, y1, scaled=False)
    rr = ink_bbox(r, x0, y0, x1, y1)
    if fr is None and rr is None:
        notes.append(f"{name}: no ink in either (consistent)")
        return
    if fr is None or rr is None:
        fails.append(f"{name}: ink mismatch (frame={'ink' if fr else 'none'}, render={'ink' if rr else 'none'})")
        return
    d = max(abs(rr[i]-fr[i]) for i in range(4))
    if d > tol:
        fails.append(f"{name}: render ({rr[0]:.0f},{rr[1]:.0f})-({rr[2]:.0f},{rr[3]:.0f}) vs frame ({fr[0]:.0f},{fr[1]:.0f})-({fr[2]:.0f},{fr[3]:.0f}) worst {d:.1f}px")
    else:
        notes.append(f"{name}: ok (worst {d:.1f}px)")

for name, win in {
    "title L1": (230, 52, 706, 84), "subtitle": (285, 84, 655, 108),
    "Decoder caption": (676, 84, 790, 110), "Encoder caption": (210, 503, 315, 528),
    "o1": (543, 120, 568, 140), "o2": (677, 120, 702, 140), "o3": (811, 120, 836, 140),
    "softmax1": (486, 162, 546, 188), "softmax2": (620, 162, 686, 188), "softmax3": (758, 162, 820, 188),
    "s1": (612, 270, 632, 283.5), "s2": (747, 270, 767, 283.5), "s3": (883, 270, 900, 283.5),
    "h1": (199, 312, 219, 334), "h2": (333, 312, 355, 334),
    "emb1": (50, 364, 148, 388), "emb2": (184, 364, 282, 388), "emb3": (317, 364, 418, 388),
    "x1": (141, 481, 162, 499), "x2": (275, 481, 297, 499), "x3": (409, 481, 432, 499),
    "Attention left cap": (238, 197, 340, 222), "Attention right cap": (720, 340, 808, 364),
    "attention node text": (248, 255, 326, 275),
    "green callout text": (74, 152, 344, 182), "pink callout text": (570, 378, 828, 406),
    "gray header": (530, 438, 670, 460), "gray bullet1": (546, 462, 672, 488),
    "gray bullet2": (546, 487, 805, 518),
    "plus glyph": (198, 388, 224, 414),
}.items():
    cmp_ink(name, *win)

# ---- fills ----------------------------------------------------------------------
def mode_at(x, y, target, tol, label):
    c = r[int(y*SC), int(x*SC)]
    d = abs(c[0]-target[0]) + abs(c[1]-target[1]) + abs(c[2]-target[2])
    (notes if d <= tol*3 else fails).append(
        (f"{label} @({x},{y}): ok" if d <= tol*3 else
         f"{label} @({x},{y}): render #{c[0]:02x}{c[1]:02x}{c[2]:02x} vs #{target[0]:02x}{target[1]:02x}{target[2]:02x}"))

mode_at(600, 150, (253, 255, 133), 20, "dec container")
mode_at(200, 400, (248, 213, 173), 20, "enc container")
mode_at(550, 205, (232, 255, 110), 24, "green bar")
mode_at(550, 264, (250, 236, 105), 24, "hidden bar")
mode_at(150, 330, (242, 199, 167), 20, "pink bar")
mode_at(150, 421, (249, 213, 163), 20, "tan bar")
mode_at(150, 250, (239, 241, 253), 12, "left box fill")
mode_at(700, 315, (239, 241, 253), 12, "right box fill")
mode_at(287, 265, (214, 216, 228), 16, "node fill")
mode_at(200, 155, (221, 255, 232), 16, "green callout fill")
mode_at(566, 376, (248, 220, 221), 14, "pink callout fill")
mode_at(600, 445, (234, 230, 221), 12, "gray box fill")
mode_at(100, 300, (255, 255, 255), 8, "white card left zone")
mode_at(880, 400, (255, 255, 255), 8, "white card right zone")

# ---- containment: content must not cross the card's inset edges (x43 / x917) -----
for label, xs, xe in [("left strip", 43, 46), ("right strip", 903, 916)]:
    strip = r[int(120*SC):int(496*SC), int(xs*SC):int(xe*SC)]
    m = strip.sum(axis=2) < 560
    if m.sum() > 20:
        fails.append(f"containment {label}: {int(m.sum())} dark px in x{xs}..{xe} (should be empty card)")

# ---- decoder bar edges: column scan at x=530 (between dividers) -------------------
def col_edges(a, x, y0, y1):
    col = a[int(y0*SC):int(y1*SC), int(x*SC)]
    dk = np.where(col.sum(axis=1) < 620)[0]
    if not len(dk):
        return None
    return (y0 + dk.min()/SC, y0 + (dk.max()+1)/SC)

for label, x, y0, y1, tgt in [("green bar edges", 530, 188, 226, (196, 217)),
                              ("hidden bar edges", 530, 246, 282, (254, 275))]:
    got = col_edges(r, x, y0, y1)
    if got is None:
        fails.append(f"{label}: no edge ink at x={x}")
    else:
        d = max(abs(got[0]-tgt[0]), abs(got[1]-tgt[1]))
        (notes if d <= 4 else fails).append(
            f"{label}: ok render {got[0]:.1f}..{got[1]:.1f} vs {tgt}" if d <= 4
            else f"{label}: render {got[0]:.1f}..{got[1]:.1f} vs {tgt} worst {d:.1f}px")

# ---- underline: long horizontal run at y105..108 x545..635 must NOT exist ---------
band = r[int(104.5*SC):int(108.5*SC), int(545*SC):int(640*SC)].sum(axis=2) < 560
runs, cur = [], 0
for v in band.any(axis=0):
    cur = cur + 1 if v else 0
    runs.append(cur)
if max(runs or [0]) > 50:
    fails.append(f"underline spills under 'challenge': run {max(runs)} render-px")
else:
    notes.append("underline: no spill under 'challenge'")

# ---- attention node / olive heads / dashed fan ink presence -----------------------
for label, x0, y0, x1, y1 in [
    ("dash ink in right box", 505, 296, 845, 336),
    ("dash ink left box right side", 395, 240, 468, 300),
    ("pink connector", 488, 342, 556, 390),
    ("green connector", 400, 176, 428, 242),
]:
    got = ink_bbox(r, x0, y0, x1, y1, thr=640)
    if got is None:
        fails.append(f"{label}: NO ink")
    else:
        notes.append(f"{label}: ink ({got[0]:.0f},{got[1]:.0f})-({got[2]:.0f},{got[3]:.0f})")

print("== SELF-CHECK ATTEMPT 1 (v2) ==")
for n in notes: print("  ok:", n)
if fails:
    print(f"\nFAILURES ({len(fails)}):")
    for x in fails: print("  FAIL:", x)
else:
    print("\nALL CHECKS PASS")
