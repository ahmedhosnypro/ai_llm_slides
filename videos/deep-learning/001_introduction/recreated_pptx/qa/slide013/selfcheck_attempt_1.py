#!/usr/bin/env python3
"""Closed-loop self-check for slide 013 attempt 1 (001_introduction).

Compares the 150dpi render (2001x1125) against PIL measurements of the original
frame unique_slides/slide_013.jpg (960x540, 1px=1pt). Scale: render_px = frame_px
* 150/72 (= *2.08333). Tolerance ~4 frame px = ~8.3 render px (closed-loop standard).
"""
import sys
import numpy as np
from PIL import Image

RENDER = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/qa/slide013/render_1.png"
S = 150 / 72.0  # render px per frame px
TOL = 4 * S     # ~8.3 render px

im = np.asarray(Image.open(RENDER).convert("RGB")).astype(int)
H, W = im.shape[:2]
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]
fails = []

def fr(v):  # frame px -> render px
    return v * S

def band_extents(mask, y0, y1, x0, x1):
    sub = mask[int(y0):int(y1), int(x0):int(x1)]
    ys, xs = np.where(sub)
    if len(ys) == 0:
        return None
    return (x0 + xs.min(), x0 + xs.max(), y0 + ys.min(), y0 + ys.max())

# ---- 1. banner: red fill bbox ~= x96..363, y79..135 (frame) ----
red = (r > 110) & (g < 70) & (b < 70)
bb = band_extents(red, fr(60), fr(160), fr(66), fr(500))
if bb is None:
    fails.append("banner: no red fill found")
else:
    for name, got, want in [("x0", bb[0], fr(96)), ("x1", bb[1], fr(363)),
                            ("y0", bb[2], fr(79)), ("y1", bb[3], fr(135))]:
        if abs(got - want) > TOL:
            fails.append(f"banner {name}: {got:.0f} vs {want:.0f} (tol {TOL:.1f})")
    # banner fill color modal
    core = im[int(fr(95)):int(fr(120)), int(fr(120)):int(fr(340))].reshape(-1, 3)
    core = core[(core[:, 0] > 110) & (core[:, 1] < 70)]
    med = np.median(core, axis=0)
    if abs(med[0] - 159) > 25 or med[1] > 40 or med[2] > 40:
        fails.append(f"banner fill color {med} vs (159,0,0)")

# ---- 2. title ink: white inside banner, cap band ~= y97..117, x132..326 ----
wt = (r > 190) & (g > 190) & (b > 190)
tb = band_extents(wt, fr(85), fr(130), fr(100), fr(360))
if tb is None:
    fails.append("title: no white ink in banner")
else:
    if abs(tb[0] - fr(132)) > 1.5 * TOL: fails.append(f"title left {tb[0]:.0f} vs {fr(132):.0f}")
    if abs(tb[1] - fr(326)) > 1.5 * TOL: fails.append(f"title right {tb[1]:.0f} vs {fr(326):.0f}")
    if abs(tb[2] - fr(97)) > 1.5 * TOL: fails.append(f"title cap top {tb[2]:.0f} vs {fr(97):.0f}")
    if abs(tb[3] - fr(117)) > 1.5 * TOL: fails.append(f"title baseline {tb[3]:.0f} vs {fr(117):.0f}")

# ---- 3. blue box borders: stroke centers x95, x804.5, y157, y499 (frame) ----
blue = (b > r + 40) & (b > g + 40) & (b > 120)
# top border rows (sample x 300..700 frame)
top_rows = np.where(blue[:, int(fr(300)):int(fr(700))].sum(axis=1) > int(fr(300)))[0]
top_rows = top_rows[(top_rows > fr(140)) & (top_rows < fr(175))]
bot_rows = np.where(blue[:, int(fr(300)):int(fr(700))].sum(axis=1) > int(fr(300)))[0]
bot_rows = bot_rows[(bot_rows > fr(480)) & (bot_rows < fr(515))]
if len(top_rows) == 0: fails.append("box: top border missing")
else:
    tc = (top_rows.min() + top_rows.max()) / 2
    if abs(tc - fr(157)) > TOL: fails.append(f"box top center {tc:.0f} vs {fr(157):.0f}")
if len(bot_rows) == 0: fails.append("box: bottom border missing")
else:
    bc = (bot_rows.min() + bot_rows.max()) / 2
    if abs(bc - fr(499)) > TOL: fails.append(f"box bottom center {bc:.0f} vs {fr(499):.0f}")
left_cols = np.where(blue[int(fr(200)):int(fr(450)), :].sum(axis=0) > int(fr(200)))[0]
left_cols = left_cols[left_cols < fr(120)]
right_cols = np.where(blue[int(fr(200)):int(fr(450)), :].sum(axis=0) > int(fr(200)))[0]
right_cols = right_cols[right_cols > fr(780)]
if len(left_cols) == 0: fails.append("box: left border missing")
else:
    lc = (left_cols.min() + left_cols.max()) / 2
    if abs(lc - fr(95)) > TOL: fails.append(f"box left center {lc:.0f} vs {fr(95):.0f}")
if len(right_cols) == 0: fails.append("box: right border missing")
else:
    rc = (right_cols.min() + right_cols.max()) / 2
    if abs(rc - fr(804.5)) > TOL: fails.append(f"box right center {rc:.0f} vs {fr(804.5):.0f}")

# box interior white
ic = im[int(fr(300)), int(fr(400))]
if not (ic[0] > 235 and ic[1] > 235 and ic[2] > 235):
    fails.append(f"box interior not white: {tuple(ic)}")

# ---- 4. header ink: x128..527, y167..184 (frame) ----
hdr = (r > 140) & (g < 100) & (b < 100) & (r > b + 60)
hb = band_extents(hdr, fr(158), fr(196), fr(90), fr(700))
if hb is None:
    fails.append("header: no red ink found")
else:
    if abs(hb[0] - fr(128)) > 1.5 * TOL: fails.append(f"header left {hb[0]:.0f} vs {fr(128):.0f}")
    if abs(hb[1] - fr(527)) > 1.5 * TOL: fails.append(f"header right {hb[1]:.0f} vs {fr(527):.0f}")
    if abs(hb[2] - fr(167)) > 1.5 * TOL: fails.append(f"header top {hb[2]:.0f} vs {fr(167):.0f}")
    if abs(hb[3] - fr(184)) > 1.5 * TOL: fails.append(f"header bottom {hb[3]:.0f} vs {fr(184):.0f}")

# ---- 5. bullets: 6 black bands, baselines 226/269.5/313/357/401/445 ----
blk = (r < 90) & (g < 90) & (b < 90)
inbox = blk[int(fr(195)):int(fr(460)), int(fr(140)):int(fr(460))]
rows = inbox.sum(axis=1)
bands = []
inb = False
for i, v in enumerate(rows):
    if v > 3 and not inb:
        s = i; inb = True
    elif v <= 3 and inb:
        if i - s > 8:  # ignore dot-only rows are same band; bands are >=9 rows
            bands.append((s, i - 1))
        inb = False
if inb:
    bands.append((s, len(rows) - 1))
# merge bands separated by < 6 render px (descender gaps)
merged = []
for bnd in bands:
    if merged and bnd[0] - merged[-1][1] < 6:
        merged[-1] = (merged[-1][0], bnd[1])
    else:
        merged.append(bnd)
if len(merged) != 6:
    fails.append(f"bullets: found {len(merged)} text bands, expected 6: {merged}")
else:
    want_base = [226, 269.5, 313, 357, 401, 445]
    for k, (s0, s1) in enumerate(merged):
        base_render = s0 + fr(195) + (s1 - s0)  # bottom row of band
        # baseline = bottom ink row (+ antialiasing); compare to want_base (frame)
        got = (s1 + fr(195)) / S
        if abs(got - want_base[k]) > TOL:
            fails.append(f"bullet {k+1} baseline {got:.1f} vs {want_base[k]} (frame px)")
    # text left edge: first ink col of band 3 (no dot ambiguity: dot at 146, text 166)
    sub3 = blk[int(fr(293)):int(fr(318)), int(fr(140)):int(fr(460))]
    ys3, xs3 = np.where(sub3)
    left_dot = (fr(140) + xs3.min()) / S
    if abs(left_dot - 146) > TOL:
        fails.append(f"bullet dot left {left_dot:.1f} vs 146 (frame px)")
    # b2 double-space width: ink 166..370 incl dot -> text right edge ~370
    sub2 = blk[int(fr(250)):int(fr(278)), int(fr(140)):int(fr(460))]
    ys2, xs2 = np.where(sub2)
    right2 = (fr(140) + xs2.max()) / S
    if abs(right2 - 370) > 1.5 * TOL:
        fails.append(f"bullet2 right ink {right2:.1f} vs 370 (double-space width)")
    # b4 right edge 404
    sub4 = blk[int(fr(337)):int(fr(365)), int(fr(140)):int(fr(500))]
    ys4, xs4 = np.where(sub4)
    right4 = (fr(140) + xs4.max()) / S
    if abs(right4 - 404) > 1.5 * TOL:
        fails.append(f"bullet4 right ink {right4:.1f} vs 404")

# line pitch (explicit lineSpacing law): measured band starts pitch ~= 43.8 frame px
if len(merged) == 6:
    starts = [m[0] + fr(195) for m in merged]
    pitches = [starts[i + 1] - starts[i] for i in range(5)]
    want_pitch = 43.8 * S
    for i, p in enumerate(pitches):
        if abs(p - want_pitch) > 1.5 * TOL:
            fails.append(f"pitch {i}->{i+1}: {p/S:.1f} frame px vs 43.8")

# ---- 6. containment: no content ink outside box/banner/chrome/blackbar ----
# panel area between box bottom (fr 501) and blackbar top (fr 518), x fr 100..800:
strip = blk[int(fr(502)):int(fr(516)), int(fr(100)):int(fr(800))]
if strip.sum() > 20:
    fails.append(f"containment: ink in gap between box bottom and blackbar ({strip.sum()} px)")
# right of box border, left of panel border (x fr 810..915, y fr 160..490):
rightgap = blk[int(fr(160)):int(fr(490)), int(fr(812)):int(fr(914))]
if rightgap.sum() > 20:
    fails.append(f"containment: ink right of box ({rightgap.sum()} px)")

# ---- 7. blackbar present: black rows fr 519..537 spanning x 40..920 ----
bar = blk[int(fr(522)):int(fr(534)), int(fr(60)):int(fr(900))]
if bar.shape[0] == 0 or bar.mean() < 0.9:
    fails.append(f"blackbar missing/incomplete (dark fraction {bar.mean():.2f})")

print(f"render {W}x{H}; scale {S:.4f} render-px per frame-px; tol {TOL:.1f}")
if fails:
    print("SELF-CHECK: FAIL")
    for f in fails:
        print("  -", f)
    sys.exit(1)
print("SELF-CHECK: PASS (banner, title, box borders+interior, header, 6 bullets +"
      " baselines/pitch/dot/double-space, containment, blackbar)")
