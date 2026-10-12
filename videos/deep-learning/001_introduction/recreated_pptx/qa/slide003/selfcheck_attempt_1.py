#!/usr/bin/env python3
"""Closed-loop self-check attempt 1 for slide_003: compare the 150dpi render against
the PIL-measured ground-truth bands of the original frame (scale render->frame: *0.48;
1 frame px = 1pt; tolerance ~4 frame px = ~8 render px)."""
import numpy as np
from PIL import Image

REN = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/qa/slide003/render_1.png"
im = np.asarray(Image.open(REN).convert("RGB")).astype(int)
H, W = im.shape[:2]
S = H / 540.0  # render px per frame px (~2.0833)
print(f"render {W}x{H}, scale {S:.4f} render-px per frame-px")
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]
fails = []

red = (r > 120) & (g < 110) & (b < 110)
black = (r < 60) & (g < 60) & (b < 60)

# ---- chrome panel/border sanity (already house_chrome_check PASS; record numbers) ----
gray = (abs(r - 233) < 16) & (abs(g - 233) < 16) & (abs(b - 231) < 18)
cols = np.where(gray[int(100 * S):int(500 * S)].sum(axis=0) > int(300 * S))[0]
print(f"panel gray cols {cols.min()}..{cols.max()} (render) = {cols.min()/S:.1f}..{cols.max()/S:.1f} frame px")

# ---- title lines: red text inside panel, excluding border strokes ----
text_red = red.copy()
text_red[:int(120 * S), :] = False
text_red[:, :int(70 * S)] = False
text_red[:, int(890 * S):] = False
text_red[int(500 * S):, :] = False
# exclude vertical border strokes (long vertical red runs)
red_cols = np.where(red[:, :].sum(axis=0) > 400 * S * 0.5)[0]
for c in red_cols:
    text_red[:, max(0, c - 3): c + 4] = False

trows = np.where(text_red.sum(axis=1) > 4)[0]
bands = []
if len(trows):
    s = p = trows[0]
    for i in trows[1:]:
        if i <= p + int(12 * S):
            p = i
        else:
            bands.append((s, p))
            s = p = i
    bands.append((s, p))
print(f"\ntitle bands (render rows): {bands}")
EXPECT = [
    ("L1 '[1] Revision of'", dict(rows=(164, 222), cap=(164, 209), cols=(269, 701))),
    ("L2 'Machine Learning'", dict(rows=(270, 328), cap=(270, 315), cols=(218, 747))),
]
for bi, band in enumerate(bands[:2]):
    y0, y1 = band
    bxs = np.where(text_red[y0:y1 + 1].sum(axis=0) > 0)[0]
    f = lambda v: v / S  # render -> frame
    name, exp = EXPECT[bi]
    ry0, ry1 = f(y0), f(y1)
    rx0, rx1 = f(bxs.min()), f(bxs.max())
    print(f"{name}: frame rows {ry0:.1f}..{ry1:.1f} (exp {exp['rows']}), "
          f"cols {rx0:.1f}..{rx1:.1f} (exp {exp['cols']}), "
          f"cx {(rx0+rx1)/2:.1f} (exp {(exp['cols'][0]+exp['cols'][1])/2:.1f})")
    d_top = abs(ry0 - exp["rows"][0])
    d_bot = abs(ry1 - exp["rows"][1])
    d_left = abs(rx0 - exp["cols"][0])
    d_right = abs(rx1 - exp["cols"][1])
    d_cx = abs((rx0 + rx1) / 2 - (exp["cols"][0] + exp["cols"][1]) / 2)
    for label, d in [("top", d_top), ("bottom", d_bot), ("left", d_left), ("right", d_right), ("center-x", d_cx)]:
        status = "OK" if d <= 4 else "FAIL"
        if d > 4:
            fails.append(f"{name} {label}: {d:.1f} frame px off (>4)")
        print(f"   {label}: delta {d:.1f} px  [{status}]")
    # title ink color modal (thick-core only)
    ink = im[y0:y1 + 1][text_red[y0:y1 + 1]]
    vals, counts = np.unique(ink.reshape(-1, 3), axis=0, return_counts=True)
    top = vals[np.argsort(-counts)[:2]]
    print(f"   modal: {'/'.join('#%02X%02X%02X' % (t[0], t[1], t[2]) for t in top)}  (exp ~BA0000)")

# ---- black bar ----
black_rows = np.where(black.sum(axis=1) > 300 * S)[0]
if len(black_rows):
    bar_y0, bar_y1 = black_rows.min(), black_rows.max()
    bx = np.where(black[bar_y0 + int(2 * S)])[0]
    print(f"\nbar: rows {bar_y0/S:.1f}..{bar_y1/S:.1f} frame (orig 519..539; drawn 519..537.5 + chrome stroke below), "
          f"cols {bx.min()/S:.1f}..{bx.max()/S:.1f} (orig 38..921)")
    if abs(bar_y0 / S - 519) > 4:
        fails.append(f"bar top {bar_y0/S:.1f} vs 519")
    if abs(bx.min() / S - 38) > 4 or abs(bx.max() / S - 921) > 4:
        fails.append("bar x extent off")
else:
    fails.append("black bar missing")

# ---- badge numeral ink present (dark strokes inside badge disc) ----
bx0, by0 = int(893 * S), int(71 * S)
d = int(18 * S)
disc = im[by0 - d:by0 + d, bx0 - d:bx0 + d]
dark = (disc[:, :, 0] < 120) & (disc[:, :, 1] < 120) & (disc[:, :, 2] < 120)
print(f"\nbadge numeral dark px: {int(dark.sum())} (expect > 50 for '3')")

# ---- wrap/containment: no title-family ink outside bands or frame ----
stray = text_red.copy()
for y0, y1 in bands:
    stray[max(0, y0 - 5):y1 + 6, :] = False
n_stray = int(stray.sum())
print(f"stray red ink outside title bands (in panel interior): {n_stray}")
if n_stray > 30:
    fails.append("stray red ink outside title bands")

print("\n" + ("SELFCHECK RESULT: PASS" if not fails else "SELFCHECK RESULT: FAIL"))
for f_ in fails:
    print("  -", f_)
