#!/usr/bin/env python3
"""slide 029 — closed-loop pre-judge self-check, attempt 1 v2 (unit-consistent).

All measurements computed in RENDER px and compared against WANT*SCALE.
Scale = 2001/960 = 2.0844 render-px per frame-px; tolerance 4 frame px.
"""
import numpy as np
from PIL import Image

REN = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/qa/slide029/render_1.png"
ORIG = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_029.jpg"
S = 2001 / 960.0
TOL = 4.0

ren = np.asarray(Image.open(REN).convert("RGB")).astype(int)
org = np.asarray(Image.open(ORIG).convert("RGB")).astype(int)
rl = (ren[:, :, 0] * 299 + ren[:, :, 1] * 587 + ren[:, :, 2] * 114) // 1000
print(f"render {ren.shape[1]}x{ren.shape[0]}, scale {S:.4f}")
fails = []

def report(name, got_frame, want_frame, tol=TOL):
    ok = abs(got_frame - want_frame) <= tol
    print(f"{'ok ' if ok else 'FAIL'} {name}: got {got_frame:.1f} want {want_frame} (frame px)")
    if not ok:
        fails.append(name)
    return ok

# ---- title ----
sub = rl[120:300, 250:1750]
ys, xs = np.where(sub < 180)
tx0, ty0, tx1, ty1 = 250 + xs.min(), 120 + ys.min(), 250 + xs.max(), 120 + ys.max()
report("title x0", tx0 / S, 178)
report("title x1", tx1 / S, 755)
report("title cap-top", ty0 / S, 85)
report("title ink-bottom(desc)", ty1 / S, 127, tol=5)

# ---- content frame strokes ----
rr, rg, rb = ren[:, :, 0], ren[:, :, 1], ren[:, :, 2]
redish = (rr > 110) & (rg < 120) & (rb < 120)
rowsum = redish[:, 250:1700].sum(axis=1)
rows = [y for y in range(300, 1100) if rowsum[y] > 1000]
colsum = redish[450:990, :].sum(axis=0)
cols = [x for x in range(100, 1900) if colsum[x] > 400]
report("frame top stroke", np.mean(rows[:3]) / S, 203)
report("frame bottom stroke", np.mean(rows[-3:]) / S, 480.5)
report("frame left stroke", np.mean(cols[:2]) / S, 72.5)
report("frame right stroke", np.mean(cols[-2:]) / S, 894.5)

# ---- bullet lines: cap-top / text-left / advance (render px throughout) ----
BANDS = {  # windows sized to catch ONLY the line's own cap band (neighbors excluded)
    "L1a": ((228, 249), (100, 560)),
    "L2a": ((251, 270), (100, 560)),
    "L2b": ((272, 292), (100, 560)),
    "L1b": ((330, 350), (100, 560)),
    "L2c": ((353, 373), (100, 560)),
}
WANT = {
    "L1a": (233, 151, 145),
    "L2a": (255, 153, 329),
    "L2b": (277, 153, 198),
    "L1b": (335, 151, 349),
    "L2c": (358, 153, 361),
}
for k, ((y0, y1), (x0, x1)) in BANDS.items():
    sub = rl[int(y0 * S):int(y1 * S), int(x0 * S):int(x1 * S)]
    ys, xs = np.where(sub < 170)
    if not len(ys):
        print(f"FAIL {k}: no ink"); fails.append(k); continue
    captop_r = int(y0 * S) + ys.min()          # render px
    # text zone: ring sits left of x=148 frame; use ink at frame-x >= 148
    xs_r = int(x0 * S) + xs
    tmask = xs_r >= 148 * S
    left_r = xs_r[tmask].min()
    right_r = xs_r[tmask].max()
    wc, wl, wa = WANT[k]
    report(f"{k} cap-top", captop_r / S, wc)
    report(f"{k} text-left", left_r / S, wl)
    report(f"{k} advance", (right_r - left_r + 1) / S, wa, tol=6)

# ---- rings ----
for name, cx, cy in [("L1a", 133.5, 240.5), ("L1b", 132, 342.5),
                     ("L2a", 143, 260), ("L2b", 142.5, 281), ("L2c", 142.5, 362)]:
    win = rl[int((cy - 8) * S):int((cy + 8) * S), int((cx - 10) * S):int((cx + 10) * S)]
    ink = (win < 235).sum()
    ok = ink > 15
    print(f"{'ok ' if ok else 'FAIL'} ring {name}: ink px {ink}")
    if not ok:
        fails.append(f"ring {name}")

# ---- image regions vs original ----
for name, (x0, y0, x1, y1) in [("meme", (636, 209, 868, 332)), ("cards", (616, 332, 892, 474)),
                               ("closeup", (188, 389, 472, 479))]:
    R = ren[int(y0 * S):int(y1 * S), int(x0 * S):int(x1 * S)]
    O = org[y0:y1, x0:x1]
    Ri = np.asarray(Image.fromarray(R.astype(np.uint8)).resize((x1 - x0, y1 - y0))).astype(int)
    diff = np.abs(Ri - O).mean()
    ok = diff < 30
    print(f"{'ok ' if ok else 'FAIL'} {name} region mean-abs-diff vs original: {diff:.1f}")
    if not ok:
        fails.append(name)

# ---- cursor absence ----
win = ren[int(377 * S):int(387 * S), int(773 * S):int(785 * S)]
whites = ((win[:, :, 0] > 200) & (win[:, :, 1] > 200) & (win[:, :, 2] > 200)).sum()
ok = whites < 12
print(f"{'ok ' if ok else 'FAIL'} cursor absence: bright-white px = {whites}")
if not ok:
    fails.append("cursor")

# ---- bottom rows: panel gray, no black bar ----
bot = ren[int(530 * S):int(538 * S), int(200 * S):int(800 * S)]
mean_lum = ((bot[:, :, 0] * 299 + bot[:, :, 1] * 587 + bot[:, :, 2] * 114) // 1000).mean()
ok = mean_lum > 200
print(f"{'ok ' if ok else 'FAIL'} bottom band panel-gray (no black bar): mean lum {mean_lum:.0f}")
if not ok:
    fails.append("bottom bar present")

print()
if fails:
    print("SELF-CHECK: FAIL ->", fails)
    raise SystemExit(1)
print("SELF-CHECK: ALL PASS")
